"""Build the public static site from a WordPress WXR export and uploads ZIP."""
import argparse
import datetime
from collections import Counter, defaultdict
import csv
import html
import json
from pathlib import Path, PurePosixPath
import re
import shutil
from urllib.parse import quote, unquote, urlsplit
from zipfile import ZipFile

from lxml import etree
from lxml import html as dom
from folio_home import render_home, render_showcase
from new_content import DESCARTES_ROUTE, DIFFICULT_BOOK_ROUTE, FIRST_BOOK_ROUTE, PLATO_ROUTE, READING_NOTES_ROUTE, descartes_guide, difficult_book_guide, first_book_guide, plato_guide, reading_notes_guide


BASE = "https://labibliotecafilosofica.com"
MEDIA = "/wp-content/uploads/"
HOSTS = {"labibliotecafilosofica.com", "www.labibliotecafilosofica.com"}
SAFE_MEDIA = set(".jpg .jpeg .png .webp .avif .gif .ico .pdf .mp3 .mp4 .ogg .wav .webm .epub .woff .woff2 .svg".split())
ALLOWED = set("""a abbr address article aside audio b blockquote br caption cite code col colgroup
dd del details div dl dt em figcaption figure h1 h2 h3 h4 h5 h6 hr i img kbd li mark ol p
picture pre q s section small source span strong sub summary sup table tbody td th thead
time tr u ul var video""".split())
DYNAMIC = re.compile(r"<!--\s*wp:([\w/-]+)\s*(\{(?:(?!-->).)*?\})?\s*/-->", re.S)


def escape(value):
    return html.escape(str(value or ""), quote=True)


def path_of(url):
    parsed = urlsplit(url)
    if parsed.netloc and parsed.hostname not in HOSTS:
        return None
    return parsed.path


def public_route(url):
    path = unquote(path_of(url) or "/")
    if any(part in {".", ".."} for part in path.split("/")) or "\\" in path:
        raise ValueError(f"Invalid route: {url}")
    return quote("/" + path.strip("/") + "/" if path.strip("/") else "/", safe="/-._~")


def shell(title, route, body, description="", noindex=False, schema=None, canonical=None):
    # Keep migrated first-party URLs canonical and secure in both rendered HTML
    # and structured data. External source URLs are intentionally left intact
    # for the editorial/legal review phase.
    body = body.replace("http://labibliotecafilosofica.com", BASE)
    home_assets = ('<link rel="stylesheet" href="/folio.css"><link rel="stylesheet" href="/folio-system.css"><link rel="stylesheet" href="/folio-reference.css"><link rel="stylesheet" href="/folio-reader.css">'
                   + ('<link rel="preload" href="/fonts/libre-caslon-display.ttf" as="font" type="font/ttf" crossorigin><script type="module" src="/folio.js"></script>' if route == '/' else ''))
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    address = BASE + (canonical or route)
    structured_json = json.dumps(schema, ensure_ascii=False).replace("http://labibliotecafilosofica.com", BASE).replace("<", chr(92) + "u003c") if schema else ""
    structured = (f'<script type="application/ld+json">{structured_json}</script>'
                  if schema else "")
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description)}">
<link rel="canonical" href="{address}">{robots}
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{address}">{structured}
<link rel="stylesheet" href="/variables.css"><link rel="stylesheet" href="/biblioteca.css"><link rel="stylesheet" href="/fable.css"><link rel="stylesheet" href="/editorial.css"><script defer src="/biblioteca.js"></script>{home_assets}</head>
<body class="folio-site {'folio-home' if route == '/' else 'folio-interior'}"><a class="skip" href="#contenido">Saltar al contenido</a>
<header class="masthead"><div class="bar"><a class="brand" href="/"><img class="original-logo" src="/wp-content/uploads/2023/07/logo-comprs.png" alt="La Biblioteca Filosófica" width="60" height="60"><span>La Biblioteca<br>Filosófica</span></a>
<button class="mobile-menu-toggle" type="button" aria-controls="primary-navigation" aria-expanded="false" hidden>Menú <span aria-hidden="true">☰</span></button><nav class="main-nav" id="primary-navigation" aria-label="Navegación principal">{navigation()}<a class="mobile-library-link" href="/mi-biblioteca/">Mi biblioteca ↗</a></nav>
<div class="header-tools"><a class="personal-link" href="/mi-biblioteca/">Mi biblioteca</a><a class="header-search" href="/biblioteca/#buscar">{SEARCH_ICON}<span>Buscar</span></a></div></div></header>
<main id="contenido">{body}</main>
<footer class="editorial-footer"><div class="footer-explore wrap"><div><p>Una lectura lleva a otra.</p><a class="footer-invitation" href="/libros-pdf-gratis/">Sigue explorando<span aria-hidden="true">↗</span></a></div><nav aria-label="Explorar la biblioteca"><a href="/libros-pdf-gratis/">Libros PDF</a><a href="/historia/">Historia de las ideas</a><a href="/libros-pdf-gratis/autores/">Autores</a><a href="/mi-biblioteca/">Mis libros guardados</a></nav></div><div class="footer-wordmark wrap" aria-hidden="true">La Biblioteca<br><em>Filosófica.</em></div><div class="bar"><a class="brand" href="/">La Biblioteca Filosófica</a><nav aria-label="Información del sitio">
<a href="/acerca-de-labibliotecafilosofica/">Acerca de</a><a href="/politica-de-privacidad/">Privacidad</a><a href="/aviso-legal/">Aviso legal</a></nav></div></footer>
</body></html>"""


SEARCH_ICON = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/></svg>'
FEATURES = (
    ("/que-es-filosofia/", "01 · Punto de partida", "¿Qué es la filosofía?",
     "Una primera lectura para orientarte entre preguntas, ramas y formas de pensar.", "2023/07/books-library-bookcase-2599241.jpg"),
    ("/los-filosofos-presocraticos/", "02 · Historia", "Los presocráticos",
     "Conoce a quienes buscaron las primeras explicaciones filosóficas del mundo.", "2023/07/filosofos-presocraticos.jpg"),
    ("/la-republica-platon/", "03 · Obra clásica", "La República, de Platón",
     "Entra en el diálogo sobre la justicia, la educación y la ciudad ideal.", "2023/07/platon-retrato.jpg"),
)


def navigation():
    groups = (
        ('Libros', '/libros-pdf-gratis/', [('Por autor', '/libros-pdf-gratis/autores/'), ('Por género', '/libros-pdf-gratis/generos-literarios/'), ('Filosofía', '/libros-pdf-gratis/filosofia-pdf/'), ('Por idioma', '/libros-pdf-gratis/idiomas/')]),
        ('Historia', '/historia/', [('Antigüedad', '/historia-filosofia-en-la-antiguedad/'), ('Edad Media', '/la-filosofia-medieval/'), ('Modernidad', '/historia-filosofia-renacimiento-y-filosofia-moderna/')]),
        ('Autores', '/libros-pdf-gratis/autores/', [('Platón', '/libros-pdf-gratis/autores/platon/'), ('Albert Camus', '/libros-pdf-gratis/autores/albert-camus/')]),
        ('Artículos', '/articulos/', [('Literatura', '/articulos/literatura/'), ('Psicología', '/articulos/psicologia/'), ('Arte', '/articulos/arte-articulos/')]),
        ('Rutas', '/rutas/introduccion-a-la-filosofia/', [('Introducción a la filosofía', '/rutas/introduccion-a-la-filosofia/'), ('Mi biblioteca', '/mi-biblioteca/')]),
        ('Colecciones', '/colecciones/', [('Filosofía', '/libros-pdf-gratis/'), ('Historia de las ideas', '/historia/'), ('Autores', '/libros-pdf-gratis/autores/')]),
    )
    return ''.join('<details class="nav-disclosure"><summary>' + title + ' <span aria-hidden="true">⌄</span></summary><div class="nav-panel"><p class="eyebrow">Explora la biblioteca</p><a class="nav-overview" href="' + route + '">Todo en ' + title.lower() + ' ↗</a>' + ''.join('<a href="' + path + '">' + label + ' <span aria-hidden="true">↗</span></a>' for label, path in links) + '</div></details>' for title, route, links in groups)


def home_intro():
    return render_home()


def legacy_home_intro():
    return '<section class="opening"><div class="wrap opening-grid"><div class="opening-copy"><span class="kicker">Un lugar para leer y pensar</span><h1>Las grandes ideas<br>empiezan con<br><em>una página.</em></h1><p>Explora obras, descubre pensadores y encuentra tu próxima pregunta.</p><form class="search" action="/biblioteca/" role="search"><input type="hidden" name="scope" value="pdf"><label class="sr" for="query">Título, autor o tema</label><input id="query" name="q" type="search" placeholder="¿Qué te gustaría leer?"><button type="submit">Buscar <span aria-hidden="true">↗</span></button></form><div class="topics"><span>Empieza por</span><a href="/libros-pdf-gratis/autores/platon/">Platón</a><a href="/libros-pdf-gratis/autores/albert-camus/">Camus</a><a href="/estoicismo/">Estoicismo</a></div></div><a class="featured-book" href="/la-republica-platon/"><span class="edition-label">Una conversación que sigue abierta</span><img src="/wp-content/uploads/2020/08/La-Republica-Platon-e1598835013508.jpg" alt="Portada de La República, de Platón"><div><span>Platón</span><h2>La República</h2><p>La justicia. La educación. La ciudad ideal.</p><span class="round-arrow" aria-hidden="true">↗</span></div></a></div></section>\r\n<nav class="library-paths wrap" aria-label="Explorar por interés"><a href="/libros-pdf-gratis/"><span>Leer</span><strong>La biblioteca</strong><b>↗</b></a><a href="/historia/"><span>Comprender</span><strong>Historia de las ideas</strong><b>↗</b></a><a href="/libros-pdf-gratis/autores/"><span>Conocer</span><strong>Sus protagonistas</strong><b>↗</b></a></nav>\r\n'


def discovery_band():
    return '<section class="history"><div class="wrap history-grid"><div><span class="kicker">Historia de la filosofía</span><h2>Cada idea tiene<br>una historia.</h2><p>Recorre las épocas y descubre cómo una pregunta conduce a la siguiente.</p><a class="pill" href="/historia/">Recorrer la historia ↗</a></div><ol><li><a href="/historia-filosofia-en-la-antiguedad/"><small>Los orígenes</small><span>Antigüedad</span><b>↗</b></a></li><li><a href="/la-filosofia-medieval/"><small>Fe y razón</small><span>Edad Media</span><b>↗</b></a></li><li><a href="/historia-filosofia-renacimiento-y-filosofia-moderna/"><small>Una nueva mirada</small><span>Modernidad</span><b>↗</b></a></li></ol></div></section>'


def route_promo():
    return '<section class="route-promo"><div><p class="eyebrow">Nueva forma de leer</p><h2>Una ruta, cinco paradas, una biblioteca que te acompaña.</h2><p>Empieza por una pregunta y sigue un recorrido editorial guardado en tu navegador.</p></div><div class="route-promo-actions"><a class="button" href="/rutas/introduccion-a-la-filosofia/">Empezar la ruta ↗</a><a class="text-link" href="/mi-biblioteca/">Ver mi biblioteca</a></div></section>'


def question_band():
    return '<section class="question-band wrap"><div><p class="eyebrow">Preguntas para empezar</p><h2>Una biblioteca también puede empezar con una duda.</h2></div><div class="question-links"><a href="/que-es-filosofia/"><span>01</span><strong>¿Qué es la filosofía?</strong><b>↗</b></a><a href="/los-filosofos-presocraticos/"><span>02</span><strong>¿Quiénes fueron los presocráticos?</strong><b>↗</b></a><a href="/sartre-existencialismo-y-libertad-la-filosofia-existencialista/"><span>03</span><strong>¿Por dónde empezar con Sartre?</strong><b>↗</b></a></div></section>'


def intro_readings():
    features = "".join(
        f'<li><a href="{route}"><div class="feature-photo"><img src="{MEDIA}{photo}" alt="{escape(title)}" loading="lazy"></div><div><p class="eyebrow">{label}</p><h3>{title}</h3><p>{summary}</p><span class="text-action">Abrir lectura ↗</span></div></a></li>'
        for route, label, title, summary, photo in FEATURES
    )
    return f"""<section class="shelf discovery"><div class="section-heading"><div><p class="eyebrow">Selección de la biblioteca</p><h2>Empieza por aquí</h2></div>
<a class="text-action" href="/biblioteca/">Ver el catálogo <span aria-hidden="true">↗</span></a></div>
<ul class="feature-grid">{features}</ul></section>"""


def catalog(posts):
    categories = sorted({(slug, name) for post in posts for domain, slug, name in post["terms"]
                         if domain == "category" and slug and name}, key=lambda pair: pair[1].casefold())
    options = "".join(f'<option value="{escape(slug)}">{escape(name)}</option>' for slug, name in categories)
    entries = []
    for post in posts:
        labels = [(slug, name) for domain, slug, name in post["terms"] if domain == "category"]
        label = labels[0][1] if labels else ("Página" if post["kind"] == "page" else "Lectura")
        slugs = " ".join(slug for slug, _ in labels if slug)
        summary = " ".join(name for _, _, name in post["terms"])
        entries.append(f'<li data-category="{escape(slugs)}" data-pdf="{str(BOOK_ROOT in post["branches"]).lower()}" data-search="{escape(post["title"] + " " + summary)}">'
                       f'<a href="{post["route"]}"><span class="eyebrow">{escape(label)}</span>'
                       f'<h2>{escape(post["title"])}</h2><span class="text-action">Abrir <span aria-hidden="true">↗</span></span></a></li>')
    return f"""<section class="shelf catalog" data-catalog>
<header class="folio-page-head"><p class="eyebrow">Índice de lecturas</p><h1>Biblioteca</h1><p>Busca una obra, un autor o un tema entre las publicaciones del sitio.</p><a class="folio-head-link" href="/colecciones/">Prefiero explorar por colecciones ↗</a></header>
<form class="catalog-controls" role="search" hidden>
<label for="buscar">Buscar<span class="search-field">{SEARCH_ICON}<input id="buscar" name="q" type="search" placeholder="Ej. Platón, ética, estoicismo"></span></label>
<label for="tema">Tema<select id="tema" name="tema"><option value="">Todos los temas</option>{options}</select></label>
<button class="button secondary" type="reset">Limpiar</button></form>
<p class="catalog-status" role="status" data-status>{len(posts)} publicaciones</p>
<ul class="catalog-grid">{"".join(entries)}</ul>
<div class="catalog-more"><button class="button secondary" type="button" data-more hidden>Mostrar más <span aria-hidden="true">↓</span></button></div>
</section>"""


def cards(entries):
    return '<ul class="cards">' + "".join(
        f'<li><a href="{entry["route"]}">{escape(entry["title"])}</a></li>'
        for entry in entries
    ) + "</ul>"


BOOK_ROOT = "libros-pdf-gratis"
ROUTE_PATH = "/rutas/introduccion-a-la-filosofia/"
BOOK_TEMPLATES = {"wp-custom-template-libros", "wp-custom-template-libros-individuales",
                  "wp-custom-template-libros-individuales-2-0"}
PDF_SECTIONS = {
    BOOK_ROOT: ("Libros PDF Gratis", "Explora obras de filosofía y literatura por autor, género, tema o idioma. Cada ficha ofrece contexto de lectura y conduce a la fuente disponible."),
    "autores": ("Autores", "Encuentra las obras reunidas por autor."),
    "generos-literarios": ("Géneros literarios", "Elige un género para explorar sus lecturas."),
    "idiomas": ("Idiomas", "Lecturas y materiales para aprender inglés o japonés."),
    "ramasdelafilosofia": ("Ramas de la filosofía", "Recopilaciones sobre ética, lógica, metafísica y otras ramas."),
    "filosofia-pdf": ("Filosofía en PDF", "Descubre obras filosóficas de Platón, Camus, Arendt y otros autores, con contexto, temas principales y rutas para seguir leyendo."),
}


def breadcrumb_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": index, "name": name, "item": BASE + path}
        for index, (name, path) in enumerate(crumbs, start=1)]}


def breadcrumbs(crumbs):
    links = "".join(f'<li><a href="{path}">{escape(name)}</a></li>' for name, path in crumbs[:-1])
    return f'<nav class="crumbs" aria-label="Ruta de navegación"><ol>{links}<li aria-current="page">{escape(crumbs[-1][0])}</li></ol></nav>'


def product_cards(items):
    products = []
    for item in items:
        url = item.get("product_url") or item.get("url") or ""
        dest = urlsplit(url)
        if dest.scheme != "https" or not dest.hostname or not (
                dest.hostname.startswith("www.amazon.") or dest.hostname == "amzn.to"):
            continue
        title = item.get("title") or "Consultar edición"
        image = item.get("image_url") or ""
        media = urlsplit(image)
        photo = (f'<img src="{escape(image)}" alt="Portada de {escape(title)}" width="140" height="175" loading="lazy" decoding="async">'
                 if media.scheme == "https" and media.hostname in {"m.media-amazon.com", "images-na.ssl-images-amazon.com", "images-eu.ssl-images-amazon.com"}
                 else '<span class="product-placeholder" aria-hidden="true">Φ</span>')
        products.append(f'<li class="product-card"><div class="product-image">{photo}</div><div class="product-body">'
                        f'<p class="eyebrow">Edición en Amazon</p><p class="product-title">{escape(title)}</p>'
                        f'<a class="button secondary" href="{escape(url)}" rel="sponsored nofollow noopener">Ver en Amazon ↗</a></div></li>')
    if not products:
        return ""
    return ('<aside class="affiliate" aria-label="Ediciones en Amazon"><div class="affiliate-head">'
            '<div><p class="eyebrow">Selección de la biblioteca</p><p class="affiliate-title">Ediciones y recursos en Amazon</p></div>'
            '<span class="affiliate-label">Enlaces de afiliación</span></div>'
            '<ul class="product-grid">' + "".join(products) + '</ul></aside>')


def inert_svg(data):
    """Accept only SVG artwork that can be served without scripts or external loads."""
    try:
        svg = etree.fromstring(data, etree.XMLParser(resolve_entities=False, no_network=True))
    except etree.XMLSyntaxError:
        return None
    shapes = {"svg", "g", "title", "desc", "defs", "path", "rect", "circle", "ellipse",
              "line", "polyline", "polygon", "linearGradient", "radialGradient", "stop",
              "clipPath", "mask", "use", "symbol", "style"}
    if svg.tag != "{http://www.w3.org/2000/svg}svg":
        return None
    declarations = r"(?:\s*(?:fill|fill-rule|stroke|stroke-width|stroke-miterlimit)\s*:\s*(?:none|evenodd|#[a-fA-F0-9]{3,8}|[\d.]+(?:px)?)\s*;?)+"
    for element in svg.iter():
        if isinstance(element, etree._Comment):
            continue
        if not isinstance(element.tag, str):
            return None
        tag = etree.QName(element)
        if tag.namespace != "http://www.w3.org/2000/svg" or tag.localname not in shapes:
            return None
        if tag.localname == "style" and not re.fullmatch(
                rf"(?:\s*\.[\w-]+\s*\{{{declarations}\}})+\s*", element.text or ""):
            return None
        for name, value in element.attrib.items():
            key = etree.QName(name).localname.lower()
            if key.startswith("on") or key == "base":
                return None
            if key == "style" and not re.fullmatch(declarations, value):
                return None
            if key == "href" and not re.fullmatch(r"#[\w.-]+", value):
                return None
            if "url(" in value.lower() and not re.fullmatch(r"url\(#[\w.-]+\)", value):
                return None
    # Serializing the root excludes the source DTD and processing instructions.
    return etree.tostring(svg, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wxr", type=Path)
    parser.add_argument("uploads", type=Path)
    parser.add_argument("--crawl", type=Path, help="CSV of observed URL-to-canonical mappings")
    parser.add_argument("--production", action="store_true", help="Enable indexing")
    args = parser.parse_args()
    project = Path(__file__).resolve().parent
    corrections = json.loads((project / "correcciones.json").read_text(encoding="utf-8"))
    output = project / "public"
    output.mkdir(exist_ok=True)

    tree = etree.parse(str(args.wxr), etree.XMLParser(resolve_entities=False, no_network=True))
    channel = tree.find("channel")
    ns = tree.getroot().nsmap

    def read(node, name):
        return node.findtext(name, default="", namespaces=ns)

    def meta(item):
        return {read(row, "wp:meta_key"): read(row, "wp:meta_value")
                for row in item.findall("wp:postmeta", ns)}

    authors = {read(item, "wp:author_login"): read(item, "wp:author_display_name")
               for item in channel.findall("wp:author", ns)}
    posts, blocks, attachments = [], {}, {}
    by_id = {}
    private_media = set()
    for item in channel.findall("item"):
        kind, status, ident = (read(item, "wp:" + key) for key in ("post_type", "status", "post_id"))
        raw = read(item, "content:encoded")
        if kind == "wp_block" and status == "publish":
            blocks[ident] = raw
        if kind == "attachment":
            url = read(item, "wp:attachment_url")
            path = path_of(url)
            if path and path.startswith(MEDIA):
                if status == "private":
                    private_media.add(unquote(path))
                else:
                    attachments[ident] = url
        if kind in {"post", "page"} and status == "publish":
            url = read(item, "link")
            if not url or path_of(url) is None:
                raise ValueError(f"Missing site URL for {ident}")
            comments = [(read(c, "wp:comment_author"), read(c, "wp:comment_date")[:10],
                         read(c, "wp:comment_content"))
                        for c in item.findall("wp:comment", ns)
                        if read(c, "wp:comment_approved") == "1"
                        and read(c, "wp:comment_type") in {"", "comment"}]
            post = dict(id=ident, kind=kind, route=public_route(url),
                        title=html.unescape(read(item, "title")), raw=raw,
                        date=read(item, "wp:post_date")[:10], meta=meta(item),
                        author=authors.get(read(item, "dc:creator"), ""),
                        modified=read(item, "wp:post_modified")[:10],
                        comments=comments,
                        terms=[(term.get("domain"), term.get("nicename"), term.text or "")
                               for term in item.findall("category")])
            posts.append(post)
            by_id[ident] = post

    routes = {p["route"] for p in posts}
    if len(routes) != len(posts) or "/" not in routes:
        raise ValueError("Duplicate post URLs or missing home page")
    posts.sort(key=lambda p: (p["date"], p["id"]), reverse=True)
    terms = defaultdict(list)
    taxonomy_ids = {}
    categories = {}
    for node in channel.findall("wp:category", ns):
        slug = read(node, "wp:category_nicename")
        taxonomy_ids[read(node, "wp:term_id")] = slug
        categories[slug] = (read(node, "wp:cat_name"), read(node, "wp:category_parent"))
    for node in channel.findall("wp:tag", ns):
        taxonomy_ids[read(node, "wp:term_id")] = read(node, "wp:tag_slug")
    def lineage(slug):
        chain = []
        while slug and slug in categories and slug not in chain:
            chain.append(slug)
            slug = categories[slug][1]
        return tuple(reversed(chain))

    def category_route(slug):
        return public_route("/" + "/".join(lineage(slug)))

    def category_crumbs(slug):
        return [("Inicio", "/")] + [
            (PDF_SECTIONS.get(parent, categories[parent])[0], category_route(parent))
            for parent in lineage(slug)]

    def post_crumbs(post):
        assigned = [slug for domain, slug, _ in post["terms"] if domain == "category" and slug in categories]
        if post["is_book"]:
            assigned = [slug for slug in assigned if BOOK_ROOT in lineage(slug)] or [BOOK_ROOT]
        elif "historia" in assigned:
            assigned = ["historia"]
        primary = max(assigned, key=lambda slug: len(lineage(slug)), default=None)
        return (category_crumbs(primary) if primary else [("Inicio", "/")]) + [(post["title"], post["route"])]

    category_posts = defaultdict(list)
    for post in posts:
        assigned = {slug for domain, slug, _ in post["terms"] if domain == "category"}
        post["branches"] = {parent for slug in assigned for parent in lineage(slug)}
        post["is_book"] = post["meta"].get("_wp_page_template") in BOOK_TEMPLATES
        # Rights are explicit metadata. Existing migrated books default to a
        # lawful external-destination state until editorial evidence is added.
        post["rights"] = {
            "status": "publisher-link" if post["is_book"] else "editorial",
            "redistribution_allowed": False,
            "reviewed": False,
        }
        for slug in post["branches"]:
            category_posts[slug].append(post)
        for domain, slug, name in post["terms"]:
            if domain == "post_tag" and slug:
                route = public_route("/tag/" + slug)
                terms[(route, name)].append(post)
    archive_routes = {route for route, name in terms} | {category_route(slug) for slug in categories}
    all_routes = routes | archive_routes | {"/biblioteca/"}
    redirects = {}
    if args.crawl:
        with args.crawl.open(encoding="utf-8-sig", newline="") as source:
            for row in csv.DictReader(source):
                old, canonical = row["Url"], row["Canonical"]
                if (row["Status"] == "200" and canonical and path_of(old)
                        and path_of(canonical) and not urlsplit(old).query):
                    source_route, target = public_route(old), public_route(canonical)
                    if source_route not in all_routes and target in all_routes:
                        redirects[source_route] = target
    for old, target in corrections["redirects"].items():
        if old in all_routes or target not in all_routes:
            raise ValueError(f"Invalid redirect: {old} -> {target}")
        redirects[old] = target
    for slug in categories:
        old = public_route("/categoria/" + slug)
        if old not in all_routes:
            redirects.setdefault(old, category_route(slug))
    unresolved = defaultdict(set)
    legacy_links = defaultdict(set)
    dynamic = Counter()
    conversions = Counter()
    copies = {}

    with ZipFile(args.uploads) as archive:
        members = {entry.filename.removeprefix("uploads/"): entry
                   for entry in archive.infolist() if not entry.is_dir()}
        checked_svg = {}

        def local_media(url, route):
            path = path_of(url)
            if not path or not path.startswith(MEDIA):
                return url
            path = unquote(path)
            if (path == MEDIA + "2023/02/image-5.png"
                    and route == "/leo-messi-la-filosofia-detras-de-su-juego/"):
                path = MEDIA + "2023/02/messi-filosofia.jpg"
                conversions["imagen sustituida por la portada de su artículo"] += 1
            name = path.removeprefix(MEDIA)
            parts = PurePosixPath(name).parts
            if (not parts or name.startswith("/") or ".." in parts or "\\" in name
                    or ":" in name or path in private_media):
                return None
            suffix = PurePosixPath(name).suffix.lower()
            if suffix not in SAFE_MEDIA:
                return None
            if name not in members:
                unresolved[path].add(route)
                return None
            if suffix == ".svg":
                if name not in checked_svg:
                    checked_svg[name] = inert_svg(archive.read(members[name]))
                if not checked_svg[name]:
                    unresolved[path].add(route)
                    return None
            copies[name] = members[name]
            return quote(path, safe="/-._~")

        def expand(raw, post, trail=()):
            def block(match):
                kind = match[1]
                try:
                    attrs = json.loads(match[2] or "{}")
                except json.JSONDecodeError:
                    dynamic[kind] += 1
                    return ""
                if kind == "block":
                    ref = str(attrs.get("ref", ""))
                    if ref in blocks and ref not in trail:
                        return expand(blocks[ref], post, trail + (ref,))
                    if ref == "263" and post["route"] in {"/albert-camus-el-hombre-rebelde/", "/timeo-platon/"}:
                        # Both live pages leave this missing reference empty. The article renders its own related section.
                        conversions["referencias vacías verificadas en el original"] += 1
                        return ""
                if kind == "hostinger-affiliate-plugin/block":
                    items = (attrs.get("items") or {}).values()
                    if not items:
                        items = corrections["affiliate_lists"].get(attrs.get("keywords"), [])
                    product = product_cards(items)
                    if product:
                        conversions["módulos de Amazon convertidos"] += 1
                        return product
                if kind == "uagb/icon" and attrs.get("icon") == "book":
                    conversions["iconos de libro convertidos"] += 1
                    return '<span class="reading-icon" aria-hidden="true">▤</span>'
                if kind == "html" and not attrs:
                    conversions["bloques HTML vacíos"] += 1
                    return ""
                if kind == "olympus-google-fonts/google-fonts":
                    tag = attrs.get("blockType") or "p"
                    if tag not in {"p", "h2", "h3", "h4", "h5", "h6", "blockquote"}:
                        tag = "p"
                    conversions["bloques tipográficos convertidos"] += 1
                    return f'<{tag} class="typographic-block">{attrs.get("content", "")}</{tag}>'
                if kind in {"themeisle-blocks/posts-grid", "essential-blocks/post-grid"}:
                    query = attrs.get("queryData") or {}
                    slugs = {category.get("slug") for category in attrs.get("categories", [])
                             if isinstance(category, dict)}
                    for taxonomy in (query.get("taxonomies") or {}).values():
                        try:
                            selected = json.loads(taxonomy.get("value") or "[]")
                            slugs.update(taxonomy_ids.get(str(choice.get("value"))) for choice in selected)
                        except (ValueError, TypeError, AttributeError):
                            dynamic[kind + " (filtro pendiente)"] += 1
                    slugs.discard(None)
                    candidates = [p for p in posts if p["kind"] == "post" and p is not post
                                  and (not slugs or any(slug in slugs for _, slug, _ in p["terms"]))]
                    try:
                        size = max(1, min(24, int(query.get("per_page") or attrs.get("postsToShow") or 6)))
                        offset = max(0, int(query.get("offset") or 0))
                    except (ValueError, TypeError):
                        size, offset = 6, 0
                    if query.get("order") == "asc":
                        candidates.reverse()
                    return cards(candidates[offset:offset + size]) if candidates else ""
                if kind == "post-title":
                    return f'<h2>{escape(post["title"])}</h2>'
                if kind == "post-date":
                    return f'<time>{escape(post["date"])}</time>'
                if kind == "post-author" and post["author"]:
                    return f'<span>{escape(post["author"])}</span>'
                if kind == "post-featured-image":
                    return feature(post)
                if kind == "post-terms":
                    return term_links(post)
                dynamic[kind] += 1
                return ""
            return DYNAMIC.sub(block, raw)

        def term_links(post):
            links = []
            for domain, slug, name in post["terms"]:
                if slug and domain in {"category", "post_tag"}:
                    route = category_route(slug) if domain == "category" else public_route("/tag/" + slug)
                    links.append(f'<a href="{route}">{escape(name)}</a>')
            return '<div class="terms">' + "".join(links) + "</div>" if links else ""

        def feature(post):
            url = attachments.get(post["meta"].get("_thumbnail_id", ""))
            if url:
                src = local_media(url, post["route"])
                if src:
                    return f'<figure class="featured"><img src="{escape(src)}" alt="{escape(post["title"])}" decoding="async"></figure>'
            return ""

        def book_grid(entries, route):
            entries = list(entries)
            cards_html = []
            for entry in entries:
                thumb = attachments.get(entry["meta"].get("_thumbnail_id", ""))
                cover = local_media(thumb, route) if thumb else None
                picture = (f'<img src="{escape(cover)}" alt="Portada de {escape(entry["title"])}" loading="lazy" decoding="async">'
                           if cover else '<span class="book-monogram" aria-hidden="true">Φ</span>')
                kind = "Ficha de libro" if entry["is_book"] else "Guía o selección"
                cards_html.append(f'<li><a href="{entry["route"]}"><div class="book-cover">{picture}</div>'
                                  f'<div class="book-info"><p class="eyebrow">{kind}</p><h2>{escape(entry["title"])}</h2>'
                                  '<span class="text-action">Abrir ficha →</span></div></a></li>')
            return f'<ul class="book-grid">{"".join(cards_html)}</ul>' if cards_html else ""

        def section_intro(slug, route, title=None):
            chain = lineage(slug)
            name = categories[slug][0]
            heading, description = PDF_SECTIONS.get(slug, (name, ""))
            if title:
                heading = title
            crumbs = category_crumbs(slug)
            entries = category_posts[slug]
            pdf = BOOK_ROOT in chain
            style = "pdf" if pdf else ("history" if slug == "historia" else "editorial")
            lead = description or (f"Explora las lecturas de {heading}." if pdf else "")
            if slug == "historia":
                lead = "Recorre la historia de la filosofía desde los presocráticos hasta el pensamiento contemporáneo mediante autores, épocas, conceptos y obras fundamentales."
            elif slug == "articulos":
                lead = "Análisis, guías y biografías para comprender obras, autores e ideas de filosofía, literatura e historia de la cultura."
            child_links = []
            priority = ("autores", "generos-literarios", "filosofia-pdf", "ramasdelafilosofia", "idiomas", "colecciones")
            for child, (child_name, parent) in categories.items():
                if parent == slug:
                    label = PDF_SECTIONS.get(child, (child_name, ""))[0]
                    order = priority.index(child) if child in priority else len(priority)
                    link = (f'<li><a href="{category_route(child)}">{escape(label)}'
                            f'<span aria-label="{len(category_posts[child])} publicaciones">{len(category_posts[child])} →</span></a></li>')
                    child_links.append((order, label, link))
            children = ('<h2>Explorar por sección</h2><ul class="subsections">'
                        + "".join(link for _, _, link in sorted(child_links)) + "</ul>") if child_links else ""
            if slug == "historia":
                eras = (
                    ("/historia-filosofia-en-la-antiguedad/", "Antigüedad"),
                    ("/la-filosofia-medieval/", "Edad Media"),
                    ("/historia-filosofia-renacimiento-y-filosofia-moderna/", "Renacimiento y modernidad"),
                    ("/historia-filosofia-contemporanea-ilustracion/", "Ilustración y pensamiento contemporáneo"),
                )
                children = '<h2>Recorre las épocas</h2><ol class="timeline">' + "".join(
                    f'<li><a href="{path}"><span>0{index}</span>{escape(label)} →</a></li>'
                    for index, (path, label) in enumerate(eras, start=1) if path in routes) + "</ol>"
            if slug == "estoicismo":
                heading = "Estoicismo"
                lead = "Una escuela práctica sobre el juicio, la virtud y la forma de vivir cuando no controlamos los acontecimientos."
                children = '<h2>Empieza por estas preguntas</h2><ul class="subsections"><li><a href="/ensenanzas-estoicos-seneca-epicteto-marco-aurelio/">¿Qué enseñan los estoicos? →</a></li><li><a href="/filosofia-estoica-sabiduria-para-la-vida-diaria/">¿Cómo se aplica a la vida diaria? →</a></li></ul>'
            if slug == "platon":
                children = '<h2>Empieza por aquí</h2><ul class="subsections"><li><a href="/por-donde-empezar-a-leer-a-platon/">Guía de lectura de Platón →</a></li><li><a href="/biografia-de-platon-el-filosofo-de-las-ideas-eternas/">Biografía de Platón →</a></li></ul>'
            if slug == "existencialismo":
                heading = "Existencialismo"
                lead = "Una colección sobre libertad, responsabilidad, sentido y decisiones concretas en un mundo sin respuestas prefabricadas."
                children = '<h2>Empieza por estas preguntas</h2><ul class="subsections"><li><a href="/sartre-existencialismo-y-libertad-la-filosofia-existencialista/">¿Qué significa ser libre para Sartre? →</a></li><li><a href="/el-existencialismo-en-la-era-de-la-informacion-como-encontrar-significado-en-un-mundo-hiperconectado/">¿Cómo encontrar sentido hoy? →</a></li><li><a href="/el-extranjero-pdf-albert-camus/">¿Por dónde empezar con Camus? →</a></li></ul>'
            if slug == BOOK_ROOT:
                picks = [entry for entry in entries if entry["route"] in {
                    "/la-republica-platon/", "/descartes-meditaciones-metafisicas/", "/el-banquete-platon-pdf/"}]
                listing = ('<h2>Obras destacadas</h2>' + book_grid(picks, route)
                           + f'<details class="books-all"><summary>Ver las {len(entries)} publicaciones de esta sección</summary>'
                           + book_grid(entries, route) + "</details>")
            else:
                listing = book_grid(entries, route) if pdf else (cards(entries) if entries else "")
                listing = f'<h2>Lecturas <span class="count">{len(entries)}</span></h2>{listing}' if listing else '<p>Esta sección aún no tiene publicaciones propias.</p>'
            search = ('<form class="pdf-search" action="/biblioteca/" method="get" role="search">'
                      '<input type="hidden" name="scope" value="pdf"><label class="visually-hidden" for="pdf-query">Buscar un libro</label>'
                      '<input type="search" id="pdf-query" name="q" placeholder="Busca por título, autor o tema">'
                      f'<button class="button" type="submit">{SEARCH_ICON} Buscar libros</button></form>') if slug == BOOK_ROOT else ""
            return (f'<section class="shelf category-page {style}">{breadcrumbs(crumbs)}'
                    f'<div class="category-hero"><div><p class="eyebrow">{"Biblioteca digital" if pdf else "Revista y guías"}</p>'
                    f'<h1>{escape(heading)}</h1><p>{escape(lead)}</p>{search}</div></div><div class="category-layout"><aside class="category-navigation">{children}</aside><div class="category-listing">{listing}</div></div></section>')

        def content(post):
            route = post["route"]
            root = dom.fragment_fromstring(expand(post["raw"], post), create_parent="div")
            for el in list(root.iterdescendants()):
                if isinstance(el, etree._Comment):
                    el.getparent().remove(el)
                    continue
                if not isinstance(el.tag, str) or el.getparent() is None:
                    continue
                if el.tag in {"script", "style", "object", "embed", "svg", "template", "noscript"}:
                    el.drop_tree()
                    continue
                if el.tag == "iframe":
                    src = el.get("src", "")
                    parsed = urlsplit(src)
                    if parsed.scheme == "https" and parsed.hostname in {"www.youtube.com", "www.youtube-nocookie.com", "player.vimeo.com"}:
                        replacement = etree.Element("a", href=src)
                        replacement.text = el.get("title") or "Ver vídeo"
                        el.addprevious(replacement)
                    el.drop_tree()
                    continue
                if el.tag not in ALLOWED:
                    el.drop_tag()
                    continue
                if el.tag == "h1":
                    el.tag = "h2"
                if el.tag == "img":
                    el.set("src", el.get("data-src") or el.get("src", ""))
                    el.set("alt", el.get("alt", ""))
                    el.set("loading", "lazy")
                    el.set("decoding", "async")
                allowed_attrs = {"id", "class", "alt", "title", "href", "src", "srcset", "sizes",
                                 "width", "height", "loading", "decoding", "rel", "datetime",
                                 "colspan", "rowspan", "scope", "start", "controls", "type", "media", "aria-label", "aria-hidden"}
                for attr in list(el.attrib):
                    if attr not in allowed_attrs:
                        del el.attrib[attr]
                for attr in ("src", "href"):
                    value = el.get(attr)
                    if value is None:
                        continue
                    value = value.strip()
                    parsed = urlsplit(value)
                    if parsed.scheme not in {"", "http", "https", "mailto", "tel"}:
                        del el.attrib[attr]
                        continue
                    path = path_of(value)
                    if path and path.startswith(MEDIA):
                        replacement = local_media(value, route)
                        if replacement:
                            el.set(attr, replacement)
                        else:
                            del el.attrib[attr]
                    elif attr == "href" and path and (path.startswith("/") or parsed.hostname in HOSTS):
                        target = public_route(path)
                        if target in (all_routes | redirects.keys()) and not parsed.query:
                            fragment = parsed.fragment if parsed.fragment != "google_vignette" else ""
                            el.set(attr, redirects.get(target, target) + ("#" + fragment if fragment else ""))
                        else:
                            legacy_links[value].add(route)
                    if attr == "href" and parsed.hostname and (
                            parsed.hostname.startswith("www.amazon.") or parsed.hostname == "amzn.to"):
                        el.set("rel", "sponsored nofollow")
                    if attr == "href" and (parsed.path.lower().endswith((".pdf", ".epub"))
                                           or "descargar" in el.text_content().casefold()[:45]):
                        el.set("class", (el.get("class", "") + " download-action").strip())
                if "srcset" in el.attrib:
                    candidates = []
                    for candidate in el.attrib.pop("srcset").split(","):
                        fields = candidate.strip().split()
                        if fields and urlsplit(fields[0]).scheme in {"", "http", "https"}:
                            src = local_media(fields[0], route)
                            if src:
                                candidates.append(" ".join([src, *fields[1:]]))
                    if candidates:
                        el.set("srcset", ", ".join(candidates))
                if el.tag == "blockquote":
                    el.set("class", (el.get("class", "") + " editorial-quote").strip())
                if el.tag == "img" and not el.get("src") and not el.get("srcset"):
                    el.drop_tree()
            headings = []
            ids = set(root.xpath(".//*[@id]/@id"))
            for index, heading in enumerate(root.xpath(".//h2|.//h3"), start=1):
                label = " ".join(heading.text_content().split())
                if not label:
                    heading.drop_tree()
                    continue
                ident = heading.get("id")
                if not ident:
                    ident = f"seccion-{index}"
                    while ident in ids:
                        ident += "-a"
                    heading.set("id", ident)
                    ids.add(ident)
                headings.append((ident, label))
            markup = escape(root.text) + "".join(dom.tostring(el, encoding="unicode") for el in root)
            return markup, " ".join(root.text_content().split()), headings

        def write(route, document):
            target = output / unquote(route).lstrip("/") / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(document, encoding="utf-8")

        for post in posts:
            route, title = post["route"], post["title"]
            markup, excerpt, headings = content(post)
            if route == "/que-es-filosofia/":
                headings = [(ident, label) for ident, label in headings if not label.lower().startswith(("¿quieres saber más", "puedes saber más", "+20 libros", "ayuda a nuestra"))]
                markup = re.sub(r'<h3[^>]*>\s*Ayuda a nuestra Biblioteca de Filosofía a seguir con una donación!\s*</h3>[\s\S]{0,500}?\bDonar\b', '', markup, flags=re.I)
                markup = ('<aside class="quick-answer"><p class="eyebrow">Respuesta breve</p><p>La filosofía es la práctica de examinar las preguntas fundamentales sobre la realidad, el conocimiento, la acción y la vida buena mediante razones, conceptos y argumentos.</p><div class="quick-links"><a href="/historia/">Historia de la filosofía ↗</a><a href="/rutas/introduccion-a-la-filosofia/">Ruta para empezar ↗</a><a href="/libros-pdf-gratis/">Obras relacionadas ↗</a></div></aside>' + markup)
            elif route == "/los-filosofos-presocraticos/":
                markup = ('<aside class="quick-answer"><p class="eyebrow">Respuesta breve</p><p>Los presocráticos fueron pensadores griegos anteriores o contemporáneos de Sócrates que buscaron explicar el mundo mediante principios naturales, argumentos y observación, en lugar de recurrir únicamente al mito.</p><div class="quick-links"><a href="/historia-filosofia-en-la-antiguedad/">Antigüedad ↗</a><a href="/que-es-filosofia/">Qué es la filosofía ↗</a><a href="/rutas/introduccion-a-la-filosofia/">Ruta para empezar ↗</a></div></aside>' + markup)
            elif route == "/sartre-existencialismo-y-libertad-la-filosofia-existencialista/":
                markup = ('<aside class="quick-answer"><p class="eyebrow">Respuesta breve</p><p>En Sartre, la libertad no es una propiedad opcional: expresa la responsabilidad de elegir y dar sentido a la propia existencia en un mundo sin garantías externas.</p><div class="key-ideas"><strong>1. La existencia precede a la esencia</strong><strong>2. La libertad implica responsabilidad</strong><strong>3. La mala fe oculta nuestras elecciones</strong></div><div class="quick-links"><a href="/libros-pdf-gratis/">Obras y autores ↗</a><a href="/historia/">Historia de las ideas ↗</a><a href="/rutas/introduccion-a-la-filosofia/">Ruta para empezar ↗</a></div></aside>' + markup)
            elif route == "/la-republica-platon/":
                markup = ('<aside class="quick-answer"><p class="eyebrow">Orientación rápida</p><p><em>La República</em> es un diálogo sobre la justicia, la educación y la organización de la ciudad. Su recorrido va de la pregunta por la vida justa a la alegoría de la caverna.</p><div class="key-ideas"><strong>1. La justicia como orden del alma y la ciudad</strong><strong>2. La educación como giro de la mirada</strong><strong>3. La alegoría de la caverna y el conocimiento</strong></div><div class="quick-links"><a href="/libros-pdf-gratis/autores/platon/">Más sobre Platón ↗</a><a href="/historia-filosofia-en-la-antiguedad/">Antigüedad ↗</a><a href="/rutas/introduccion-a-la-filosofia/">Ruta para empezar ↗</a></div></aside>' + markup)
            elif route in {"/descartes-discurso-del-metodo-pdf/", "/descartes-meditaciones-metafisicas/"}:
                markup = ('<aside class="quick-answer"><p class="eyebrow">Orientación rápida</p><p>Descartes busca un punto de partida firme para el conocimiento: somete las creencias a duda, examina el pensamiento y reconstruye desde ahí la relación entre mente, mundo y verdad.</p><div class="key-ideas"><strong>1. La duda como método</strong><strong>2. El cogito como certeza inicial</strong><strong>3. La razón como herramienta de reconstrucción</strong></div><div class="quick-links"><a href="/por-donde-empezar-a-leer-a-descartes/">Por dónde empezar a leer a Descartes ↗</a><a href="/historia-filosofia-descartes-filosofia-cartesiana-duda-metodica/">Más sobre Descartes ↗</a><a href="/historia-filosofia-renacimiento-y-filosofia-moderna/">Modernidad ↗</a><a href="/rutas/introduccion-a-la-filosofia/">Ruta para empezar ↗</a></div></aside>' + markup)
            elif route == "/asi-hablo-zaratustra-friedrich-nietzsche/":
                markup = ('<aside class="quick-answer"><p class="eyebrow">Orientación rápida</p><p><em>Así habló Zaratustra</em> combina relato, discurso y aforismo para explorar la creación de valores, la superación de uno mismo y la crítica de las certezas heredadas.</p><div class="key-ideas"><strong>1. El superhombre como tarea, no como etiqueta</strong><strong>2. La crítica de la moral recibida</strong><strong>3. El eterno retorno como pregunta vital</strong></div><div class="quick-links"><a href="/libros-pdf-gratis/autores/nietzsche/">Más sobre Nietzsche ↗</a><a href="/historia/">Historia de las ideas ↗</a><a href="/rutas/introduccion-a-la-filosofia/">Ruta para empezar ↗</a></div></aside>' + markup)
            elif route == "/ensenanzas-estoicos-seneca-epicteto-marco-aurelio/":
                markup = ('<aside class="quick-answer"><p class="eyebrow">Orientación rápida</p><p>El estoicismo propone distinguir lo que depende de nosotros, cultivar el juicio y practicar una vida guiada por la virtud, no por el control de los acontecimientos externos.</p><div class="key-ideas"><strong>1. Distinguir control e incertidumbre</strong><strong>2. Convertir la virtud en práctica diaria</strong><strong>3. Leer la adversidad como ejercicio de criterio</strong></div><div class="quick-links"><a href="/estoicismo/">Colección de estoicismo ↗</a><a href="/libros-pdf-gratis/">Obras relacionadas ↗</a><a href="/rutas/introduccion-a-la-filosofia/">Ruta para empezar ↗</a></div></aside>' + markup)
            elif route == "/el-existencialismo-en-la-era-de-la-informacion-como-encontrar-significado-en-un-mundo-hiperconectado/":
                markup = ('<aside class="quick-answer"><p class="eyebrow">Orientación rápida</p><p>El existencialismo pregunta cómo construir sentido y responsabilidad cuando no existe una respuesta externa que decida por nosotros.</p><div class="key-ideas"><strong>1. Libertad situada</strong><strong>2. Responsabilidad ante la elección</strong><strong>3. Sentido como tarea compartida</strong></div><div class="quick-links"><a href="/sartre-existencialismo-y-libertad-la-filosofia-existencialista/">Sartre y la libertad ↗</a><a href="/historia/">Historia de las ideas ↗</a><a href="/rutas/introduccion-a-la-filosofia/">Ruta para empezar ↗</a></div></aside>' + markup)
            description = post["meta"].get("rank_math_description") or excerpt[:155]
            seo = post["meta"].get("rank_math_title", "").replace("%sep%", "–").replace("%sitename%", "La Biblioteca Filosófica").replace("%title%", title)
            if "%" in seo:
                seo = ""
            if route == "/que-es-filosofia/":
                seo = "Qué es la filosofía: definición, ramas, origen y ejemplos · La Biblioteca Filosófica"
                description = "Qué es la filosofía, de dónde nace, cuáles son sus ramas y por qué sigue siendo útil. Guía clara con autores, corrientes y lecturas para continuar."
            schema = None
            canonical = None
            if route == "/":
                body = home_intro()
                seo = "La Biblioteca Filosófica · Libros PDF, autores e historia"
                description = "Explora libros de filosofía, obras por autor y género, guías de lectura e historia del pensamiento en La Biblioteca Filosófica."
                reading_order = (
                    "/la-republica-platon/", "/el-banquete-platon-pdf/", "/fedon-platon-pdf/",
                    "/descartes-discurso-del-metodo-pdf/", "/descartes-meditaciones-metafisicas/",
                    "/asi-hablo-zaratustra-friedrich-nietzsche/",
                )
                by_route = {item["route"]: item for item in posts}
                recent = [by_route[path] for path in reading_order if path in by_route]
                body += render_showcase() + route_promo() + question_band() + discovery_band() + intro_readings()
                body += f'<section class="shelf home-archive"><details><summary>Más lecturas y secciones</summary><div class="entry">{markup}</div></details></section>'
            elif route in {"/libros-gratis-en-online/", "/historia/", "/colecciones/"}:
                slug = {"/libros-gratis-en-online/": BOOK_ROOT, "/historia/": "historia",
                        "/colecciones/": "colecciones"}[route]
                body = section_intro(slug, route)
                schema = {"@context": "https://schema.org", **breadcrumb_schema(category_crumbs(slug))}
                if route == "/libros-gratis-en-online/":
                    canonical = category_route(BOOK_ROOT)
                if not description:
                    description = PDF_SECTIONS.get(slug, ("", ""))[1] or f"Explora las lecturas y guías de {categories[slug][0]}."
                if excerpt:
                    body += f'<section class="reading entry">{markup}</section>'
            else:
                date = f'<time datetime="{post["date"]}">{post["date"]}</time>' if post["kind"] == "post" else ""
                toc = ""
                if len(headings) >= 3:
                    links = "".join(f'<li><a href="#{escape(ident)}">{escape(label)}</a></li>' for ident, label in headings)
                    toc = f'<details class="toc"><summary>En esta lectura <span>{len(headings)} secciones</span></summary><ol>{links}</ol></details>'
                assigned_categories = {slug for domain, slug, _ in post["terms"] if domain == "category" and slug}
                related = [item for item in posts if item is not post and item["kind"] == "post"
                           and assigned_categories.intersection(slug for domain, slug, _ in item["terms"] if domain == "category")][:3]
                if route == "/que-es-filosofia/":
                    related_routes = {"/los-filosofos-presocraticos/", "/la-republica-platon/", "/sartre-existencialismo-y-libertad-la-filosofia-existencialista/"}
                    related = [item for item in posts if item["route"] in related_routes]
                suggested = f'<section class="related"><h2>Sigue explorando</h2>{cards(related)}</section>' if related else ""
                if post["is_book"]:
                    book_doc = dom.fragment_fromstring(markup, create_parent="div")
                    download = book_doc.xpath('.//a[@href and contains(concat(" ",normalize-space(@class)," ")," download-action ")]/@href')
                    purchase = book_doc.xpath('.//a[@href and contains(@rel,"sponsored")]/@href')
                    usable = [value for value in download if value.startswith(MEDIA) or (
                              urlsplit(value).scheme in {"http", "https"} and path_of(value) not in {"", "/"})]
                    actions = ('<p class="rights-note">Acceso legal: consulta la edición o fuente enlazada. La redistribución del texto no está verificada.</p>'
                               f'<a class="button" href="{escape(usable[0])}">Consultar fuente enlazada ↗</a>'
                               if usable else '<a class="button" href="#texto-obra">Leer sobre la obra ↓</a>')
                    if purchase:
                        actions += f'<a class="button secondary" href="{escape(purchase[0])}" rel="sponsored nofollow">Ver edición física ↗</a>'
                    header = (f'<div class="book-detail">{feature(post)}<div><p class="eyebrow">Ficha de libro</p>'
                              f'<h1>{escape(title)}</h1><p class="access-badge"><span aria-hidden="true">●</span> Estado de acceso: ficha editorial y fuente enlazada</p><div class="actions">{actions}</div>'
                              f'<div class="save-controls"><button class="button save-book" type="button" data-save-route="{escape(route)}" aria-pressed="false" hidden>Guardar libro</button>'
                              '<a class="text-link" href="#texto-obra">Leer el análisis ↓</a></div>'
                              '<p class="save-message" role="status" aria-live="polite"></p>'
                              '<p class="device-note">Tu biblioteca se guarda en este navegador, sin cuenta.</p></div></div>')
                    back = '<a class="back-link" href="/libros-pdf-gratis/">← Libros PDF</a>'
                else:
                    header = (f'<header class="folio-article-head"><p class="eyebrow">La Biblioteca · Lecturas e ideas</p><h1>{escape(title)}</h1>'
                              f'<div class="reading-meta">{date}<a href="#texto-obra">Empezar a leer ↓</a></div></header>{feature(post)}')
                    back = '<a class="back-link" href="/biblioteca/">← Volver a la biblioteca</a>'
                crumbs = post_crumbs(post)
                toolbar = '<div class="reader-toolbar" hidden><a href="/biblioteca/">← Biblioteca</a><div role="group" aria-label="Aspecto de lectura"><button data-paper="noir" aria-pressed="true">Oscuro</button><button data-paper="cream" aria-pressed="false">Papel</button><button data-paper="sepia" aria-pressed="false">Sepia</button><button data-text-size="-2" aria-label="Reducir texto">A−</button><button data-text-size="2" aria-label="Ampliar texto">A+</button><button data-text-font aria-pressed="false">Sans</button><button data-share-page>Compartir</button></div><span data-reader-status role="status"></span></div>'
                body = f'{toolbar}<article class="reading reader-v2 {"reader-book" if post["is_book"] else "reader-article"}" id="lectura">{breadcrumbs(crumbs)}{back}{header}{toc}<div class="entry" id="texto-obra">{markup}</div>{term_links(post)}{suggested}<a class="button secondary" href="#lectura">Volver arriba ↑</a></article>'
                graph = [breadcrumb_schema(crumbs)]
                if post["kind"] == "post" and not post["is_book"]:
                    article = {"@type": "Article", "headline": title, "url": BASE + route,
                               "mainEntityOfPage": BASE + route, "inLanguage": "es",
                               "datePublished": post["date"], "dateModified": post["modified"] or post["date"]}
                    if post["author"]:
                        article["author"] = {"@type": "Person", "name": post["author"]}
                    thumb = attachments.get(post["meta"].get("_thumbnail_id", ""))
                    if thumb:
                        article["image"] = thumb
                    graph.append(article)
                elif post["is_book"]:
                    work = {"@type": "Book", "name": title, "url": BASE + route,
                            "inLanguage": "es", "isAccessibleForFree": False,
                            "author": {"@type": "Person", "name": post["author"] or "Autor no identificado"}}
                    thumb = attachments.get(post["meta"].get("_thumbnail_id", ""))
                    if thumb:
                        work["image"] = thumb
                    graph.append(work)
                schema = {"@context": "https://schema.org", "@graph": graph}
                if post["comments"]:
                    comments = "".join(
                        f'<li><strong>{escape(author)}</strong> · <time>{escape(day)}</time><p>{escape(text)}</p></li>'
                        for author, day, text in post["comments"])
                    body += f'<section class="reading"><h2>Comentarios</h2><ol>{comments}</ol></section>'
            write(route, shell(seo or ("La Biblioteca Filosófica" if route == "/" else f"{title} · La Biblioteca Filosófica"),
                               route, body, description, schema=schema, canonical=canonical))

        saved_cards = []
        for item in posts:
            if not item["is_book"]:
                continue
            saved_cards.append(f'<li data-saved-route="{escape(item["route"])}" hidden>'
                               f'<a href="{escape(item["route"])}">{feature(item)}<h2>{escape(item["title"])}</h2></a>'
                               f'<button class="remove-saved" type="button" data-remove-route="{escape(item["route"])}" aria-label="Quitar {escape(item["title"])} de mi biblioteca">Quitar de mi biblioteca</button></li>')
        write("/mi-biblioteca/", shell("Mi biblioteca · La Biblioteca Filosófica", "/mi-biblioteca/",
              '<section class="shelf personal-library" data-personal-library><header class="folio-page-head"><p class="eyebrow">Tu próxima lectura</p><h1>Mi biblioteca</h1>'
              '<p>Los libros que quieres tener a mano. Guardados solo en este navegador y dispositivo.</p>'
              '<p class="device-note">Si borras los datos del navegador, también se borrará esta selección.</p><a class="folio-head-link" href="/biblioteca/">Añadir una próxima lectura ↗</a></header>'
              '<section class="dashboard-route" data-dashboard-route><div><p class="eyebrow">Ruta en curso</p><h2>Una primera entrada a la filosofía</h2><p data-dashboard-progress>Comprueba tu progreso y continúa donde lo dejaste.</p></div><a class="button" href="/rutas/introduccion-a-la-filosofia/">Continuar ruta ↗</a></section>'
              '<p role="status" data-library-status>Activa JavaScript para consultar tus libros guardados.</p>'
              '<div class="library-empty" data-library-empty hidden><h2>Una estantería por llenar.</h2><p>Abre una ficha y pulsa «Guardar libro» para encontrarla aquí.</p><a class="button" href="/libros-pdf-gratis/">Explorar libros ↗</a></div>'
              '<ul class="saved-grid">' + ''.join(saved_cards) + '</ul></section>', noindex=True))
        write("/biblioteca/", shell("Biblioteca · La Biblioteca Filosófica", "/biblioteca/",
              catalog(posts)))
        collections_body = ('<section class="collections-hub shelf"><header class="folio-page-head"><p class="eyebrow">Elige tu próxima sala</p><h1>Explora por colecciones</h1><p class="collection-lead">Una biblioteca crece cuando cada lectura encuentra su contexto. Empieza por una colección y deja que las relaciones te lleven a la siguiente.</p></header><div class="collection-grid">'
                            '<a class="collection-card collection-card-featured" href="/libros-pdf-gratis/"><span>01 · Colección fundacional</span><strong>Filosofía</strong><small>Obras, autores, conceptos y rutas para pensar con más contexto.</small><b>Entrar ↗</b></a>'
                            '<a class="collection-card" href="/historia/"><span>02 · Línea temporal</span><strong>Historia de las ideas</strong><small>De la Antigüedad a la modernidad.</small><b>Explorar ↗</b></a>'
                            '<a class="collection-card" href="/libros-pdf-gratis/autores/"><span>03 · Personas</span><strong>Autores</strong><small>Una entrada por cada voz del catálogo.</small><b>Conocer ↗</b></a>'
                            '<a class="collection-card" href="/rutas/introduccion-a-la-filosofia/"><span>04 · Recorrido</span><strong>Rutas de lectura</strong><small>Itinerarios breves para no perderse al empezar.</small><b>Comenzar ↗</b></a>'
                            '</div></section>')
        collections_schema = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Colecciones", "description": "Explora las colecciones de lectura de La Biblioteca Filosófica.", "inLanguage": "es", "url": BASE + "/colecciones/"}
        write("/colecciones/", shell("Colecciones · La Biblioteca Filosófica", "/colecciones/", collections_body, "Explora las colecciones de lectura de La Biblioteca Filosófica.", schema=collections_schema))
        route_order = (
            "/la-republica-platon/",
            "/el-banquete-platon-pdf/",
            "/fedon-platon-pdf/",
            "/descartes-discurso-del-metodo-pdf/",
            "/asi-hablo-zaratustra-friedrich-nietzsche/",
        )
        by_route = {item["route"]: item for item in posts}
        route_items = [by_route[path] for path in route_order if path in by_route]
        route_steps = ''.join(
            f'<li><a class="route-step" href="{escape(item["route"])}" data-route-step="{index}"><span>{index + 1:02d}</span><strong>{escape(item["title"])}</strong><small>Ficha y contexto de lectura ↗</small></a></li>'
            for index, item in enumerate(route_items))
        route_body = (f'<section class="route-page shelf" data-reading-route="intro-filosofia"><header class="folio-page-head"><p class="eyebrow">Ruta de lectura · 5 etapas</p>'
                      '<h1>Una primera entrada a la filosofía</h1><p class="route-lead">Un recorrido breve para pasar de una pregunta general a obras, autores y conceptos que merecen una segunda lectura.</p>'
                      '<div class="route-meta"><span>45–60 min</span><span>Guardado en este navegador</span></div></header>'
                      f'<ol class="route-steps">{route_steps}</ol>'
                      '<p class="route-progress" role="status" data-route-progress>0 de 5 etapas completadas</p>'
                      '<button class="button" type="button" data-complete-route>Marcar ruta como completada</button>'
                      '<p>¿Aún no sabes qué obra escoger? <a href="/que-libro-de-filosofia-leer-primero/">Compara cuatro primeras lecturas →</a>. Si una obra se te resiste, consulta <a href="/como-leer-un-libro-dificil/">cómo leer un libro difícil</a> o aprende <a href="/como-tomar-notas-al-leer-filosofia/">a tomar notas</a>.</p></section>')
        route_schema = {"@context": "https://schema.org", "@type": "Course", "name": "Una primera entrada a la filosofía", "description": "Ruta de lectura introductoria a la filosofía.", "inLanguage": "es", "url": BASE + ROUTE_PATH}
        write(ROUTE_PATH, shell("Ruta: Introducción a la filosofía · La Biblioteca Filosófica", ROUTE_PATH, route_body, "Ruta de lectura introductoria a la filosofía con obras y autores seleccionados.", schema=route_schema))
        write(PLATO_ROUTE, shell("Por dónde empezar a leer a Platón · La Biblioteca Filosófica", PLATO_ROUTE, plato_guide(),
                                "Un orden de lectura para empezar con Platón: Eutifrón, Apología, Fedón, El banquete y La República."))
        write(FIRST_BOOK_ROUTE, shell("Qué libro de filosofía leer primero · La Biblioteca Filosófica", FIRST_BOOK_ROUTE, first_book_guide(),
                                      "Elige tu primera lectura de filosofía según tus intereses: Sócrates, Platón, Descartes o Camus."))
        write(DESCARTES_ROUTE, shell("Por dónde empezar a leer a Descartes · La Biblioteca Filosófica", DESCARTES_ROUTE, descartes_guide(),
                                     "Una ruta para leer a Descartes: Discurso del método, Meditaciones, cartas con Isabel y Las pasiones del alma."))
        write(DIFFICULT_BOOK_ROUTE, shell("Cómo leer un libro difícil sin abandonarlo · La Biblioteca Filosófica", DIFFICULT_BOOK_ROUTE, difficult_book_guide(),
                                          "Aprende a leer libros difíciles con tres pasadas: orientarte, seguir el argumento y reconstruir lo leído."))
        write(READING_NOTES_ROUTE, shell("Cómo tomar notas al leer filosofía · La Biblioteca Filosófica", READING_NOTES_ROUTE, reading_notes_guide(),
                                         "Un método sencillo para tomar notas al leer filosofía: pregunta, argumento, duda y conexiones."))
        for (route, name), entries in terms.items():
            write(route, shell(f"{name} · La Biblioteca Filosófica", route,
                               f'<section class="shelf"><h1>{escape(name)}</h1>{cards(entries)}</section>', noindex=True))
        for slug in categories:
            route = category_route(slug)
            if route not in routes:
                name = PDF_SECTIONS.get(slug, categories[slug])[0]
                description = PDF_SECTIONS.get(slug, ("", ""))[1] or f"Obras y lecturas de {name} en La Biblioteca Filosófica."
                write(route, shell(f"{name} · La Biblioteca Filosófica", route,
                                   section_intro(slug, route), description, noindex=not category_posts[slug],
                                   schema={"@context": "https://schema.org", **breadcrumb_schema(category_crumbs(slug))}))
        for url in attachments.values():
            local_media(url, "Biblioteca de medios")
        for name, member in sorted(copies.items()):
            destination = output / "wp-content" / "uploads" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            if name in checked_svg:
                destination.write_bytes(checked_svg[name])
            else:
                with archive.open(member) as source, destination.open("wb") as target:
                    shutil.copyfileobj(source, target)

    shutil.copyfile(project / "biblioteca.css", output / "biblioteca.css")
    shutil.copyfile(project / "fable.css", output / "fable.css")
    shutil.copyfile(project / "editorial.css", output / "editorial.css")
    for name in ('folio.css', 'folio-system.css', 'folio-reference.css', 'folio-reader.css', 'folio-experience.js', 'folio.js', 'folio-scene.js', 'folio-books.json'):
        shutil.copyfile(project / name, output / name)
    shutil.copytree(project / 'folio-assets', output / 'folio-assets', dirs_exist_ok=True)
    shutil.copytree(project / 'editorial-images', output / 'editorial-images', dirs_exist_ok=True)
    shutil.copytree(project / 'vendor', output / 'vendor', dirs_exist_ok=True)
    shutil.copyfile(project / "design" / "variables.css", output / "variables.css")
    shutil.copyfile(project / "design" / "lectora.svg", output / "lectora.svg")
    shutil.copytree(project / "fonts", output / "fonts", dirs_exist_ok=True)
    shutil.copyfile(project / "biblioteca.js", output / "biblioteca.js")
    shutil.copyfile(project / "vendor" / "gsap.min.js", output / "gsap.min.js")
    shutil.copyfile(project / "ads.txt", output / "ads.txt")
    (output / "404.html").write_text(shell("Página no encontrada", "/404/",
        '<section class="shelf"><h1>Página no encontrada</h1><p><a href="/biblioteca/">Volver a la biblioteca</a></p></section>', noindex=True), encoding="utf-8")
    (output / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{escape(BASE + route)}</loc></url>\n" for route in sorted(
            (routes - {"/libros-gratis-en-online/"}) | {"/biblioteca/", ROUTE_PATH, PLATO_ROUTE, FIRST_BOOK_ROUTE, DESCARTES_ROUTE, DIFFICULT_BOOK_ROUTE, READING_NOTES_ROUTE, "/colecciones/"} |
            {category_route(slug) for slug in categories if category_posts[slug]}))
        + "</urlset>\n", encoding="utf-8")
    (output / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n" if args.production
        else "User-agent: *\nDisallow: /\n", encoding="utf-8")
    catalog_records = []
    for post in posts:
        catalog_records.append({
            "schema_version": 1,
            "id": post["id"],
            "type": "work" if post["is_book"] else "editorial",
            "title": post["title"],
            "slug": post["route"].strip("/"),
            "language": "es",
            "author": post["author"] or None,
            "rights": post.get("rights", {"status": "editorial", "redistribution_allowed": False}),
            "access": {"kind": "external-or-editorial", "redistribution_allowed": False},
            "canonical_url": BASE + post["route"],
            "indexable": True,
            "updated_at": post["modified"] or post["date"],
        })
    catalog_records.append({
        "schema_version": 1, "id": "route-introduccion-filosofia", "type": "route",
        "title": "Una primera entrada a la filosofía", "slug": ROUTE_PATH.strip("/"),
        "language": "es", "rights": {"status": "editorial", "redistribution_allowed": False},
        "access": {"kind": "internal", "url": BASE + ROUTE_PATH, "redistribution_allowed": False},
        "canonical_url": BASE + ROUTE_PATH, "indexable": True, "updated_at": datetime.date.today().isoformat()
    })
    catalog_records.append({
        "schema_version": 1, "id": "collection-filosofia", "type": "collection",
        "title": "Colecciones", "slug": "colecciones", "language": "es",
        "rights": {"status": "editorial", "redistribution_allowed": False},
        "access": {"kind": "internal", "url": BASE + "/colecciones/", "redistribution_allowed": False},
        "canonical_url": BASE + "/colecciones/", "indexable": True, "updated_at": datetime.date.today().isoformat()
    })
    (output / "catalog.json").write_text(json.dumps({"schema_version": 1, "records": catalog_records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    config = {"$schema": "https://openapi.vercel.sh/vercel.json", "framework": None,
              "outputDirectory": "public", "trailingSlash": True,
              "redirects": [
                  {"source": "/sitemap_index.xml", "destination": "/sitemap.xml", "permanent": True},
                  {"source": "/libros-gratis-en-online/", "destination": "/libros-pdf-gratis/", "permanent": True},
              ]
              + [{"source": source, "destination": target, "permanent": True}
                 for source, target in sorted(redirects.items())]}
    if not args.production:
        config["headers"] = [{"source": "/(.*)", "headers": [{"key": "X-Robots-Tag", "value": "noindex"}]}]
    (project / "vercel.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    report = {"publicaciones": len(posts), "rutas_publicadas": sorted(routes), "archivos_de_medios": len(copies),
              "archivos_privados_excluidos": len(private_media),
              "comentarios_publicados": sum(len(post["comments"]) for post in posts),
              "fichas_de_libro": sum(post["is_book"] for post in posts),
              "categorias": {slug: {"ruta": category_route(slug), "publicaciones": len(category_posts[slug]),
                                    "padre": parent} for slug, (_, parent) in categories.items()},
              "recursos_por_revisar": {key: sorted(value) for key, value in sorted(unresolved.items())},
              "enlaces_internos_sin_destino_generado": {key: sorted(value) for key, value in sorted(legacy_links.items())},
              "conversiones_de_modulos": dict(conversions),
              "bloques_dinamicos_por_revisar": dict(dynamic)}
    (project / "revision-migracion.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(posts)} publicaciones, {len(archive_routes)} archivos de taxonomía, {len(copies)} medios.")
    print(f"{len(unresolved)} recursos y {len(legacy_links)} destinos internos pendientes de revisión.")


if __name__ == "__main__":
    main()

