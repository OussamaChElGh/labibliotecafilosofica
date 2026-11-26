"""Build the public static site from a WordPress WXR export and uploads ZIP."""
import argparse
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
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    address = BASE + (canonical or route)
    structured = (f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace("<", chr(92) + "u003c")}</script>'
                  if schema else "")
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description)}">
<link rel="canonical" href="{address}">{robots}
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:url" content="{address}">{structured}
<link rel="stylesheet" href="/variables.css"><link rel="stylesheet" href="/biblioteca.css"><link rel="stylesheet" href="/fable.css"><script defer src="/biblioteca.js"></script><script>window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};</script><script defer src="/_vercel/insights/script.js"></script></head>
<body><a class="skip" href="#contenido">Saltar al contenido</a>
<header class="masthead"><div class="bar"><a class="brand" href="/"><span class="brand-mark" aria-hidden="true">Φ</span><span>La Biblioteca<br>Filosófica</span></a>
<nav class="main-nav" aria-label="Navegación principal">{navigation()}</nav>
<a class="header-search" href="/biblioteca/#buscar">{SEARCH_ICON}<span>Buscar</span></a></div></header>
<main id="contenido">{body}</main>
<footer><div class="bar"><a class="brand" href="/">La Biblioteca Filosófica</a><nav aria-label="Información del sitio">
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
    )
    return ''.join('<details class="nav-disclosure"><summary>' + title + ' <span aria-hidden="true">⌄</span></summary><div class="nav-panel"><p class="eyebrow">Explora la biblioteca</p><a class="nav-overview" href="' + route + '">Todo en ' + title.lower() + ' ↗</a>' + ''.join('<a href="' + path + '">' + label + ' <span aria-hidden="true">↗</span></a>' for label, path in links) + '</div></details>' for title, route, links in groups)


def home_intro():
    return f"""<section class="hero"><div class="band-inner">
<div class="hero-copy"><p class="eyebrow">Biblioteca digital · Filosofía y humanidades</p>
<h1>Un libro.<br>Mil maneras<br>de <em>pensar.</em></h1>
<p>Clásicos que siguen preguntando. Ideas que cambian la mirada. Encuentra tu lugar en la filosofía.</p>
<div class="actions"><a class="button" href="/libros-pdf-gratis/">Explorar libros <span aria-hidden="true">↗</span></a><a class="hero-link" href="/que-es-filosofia/">¿Por dónde empezar? →</a></div></div>
<div class="hero-art editorial-orbit"><span class="orbit-circle" aria-hidden="true"></span><span class="orbit-star" aria-hidden="true">✳</span>
<a class="orbit-book orbit-one" href="/la-republica-platon/"><img src="/wp-content/uploads/2020/08/La-Republica-Platon-e1598835013508.jpg" alt="Leer La República, de Platón" width="220" height="320" fetchpriority="high"></a>
<a class="orbit-book orbit-two" href="/asi-hablo-zaratustra-friedrich-nietzsche/"><img src="/wp-content/uploads/2020/09/Asi-hablo-Zaratustra-Friedrich-Nietzsche.jpg" alt="Leer Así habló Zaratustra, de Nietzsche" width="180" height="270"></a>
<a class="orbit-book orbit-three" href="/el-banquete-platon-pdf/"><img src="/wp-content/uploads/2020/08/El-banquete-Platon.jpg" alt="Leer El Banquete, de Platón" width="150" height="220"></a>
<span class="orbit-caption">Grandes ideas.<br>Siempre abiertas.</span></div>
</div><div class="hero-bottom"><span>Una biblioteca para mentes curiosas</span><a href="#explorar">Encuentra tu camino ↓</a></div></section>
<section class="pathways shelf" id="explorar"><p class="eyebrow">Cuatro puertas. Infinitas preguntas.</p><div class="pathway-grid">
<a href="/libros-pdf-gratis/"><span class="path-icon" aria-hidden="true">▥</span><span><strong>Quiero leer</strong><small>Obras, géneros y colecciones</small></span><b aria-hidden="true">↗</b></a>
<a href="/historia/"><span class="path-icon" aria-hidden="true">◷</span><span><strong>Quiero entender</strong><small>Una historia de las ideas</small></span><b aria-hidden="true">↗</b></a>
<a href="/libros-pdf-gratis/autores/"><span class="path-icon" aria-hidden="true">Φ</span><span><strong>Busco un autor</strong><small>Voces que siguen conversando</small></span><b aria-hidden="true">↗</b></a>
<a href="/articulos/"><span class="path-icon" aria-hidden="true">✳</span><span><strong>Quiero descubrir</strong><small>Cultura, guías y nuevas miradas</small></span><b aria-hidden="true">↗</b></a>
</div></section>"""


def discovery_band():
    return """<section class="feature-band"><div class="band-inner">
<div class="feature-copy"><p class="eyebrow">Rutas de lectura</p><h2>Viaja por la historia de las ideas</h2>
<p>De las preguntas de los presocráticos al pensamiento moderno. Elige una época y sigue leyendo a tu ritmo.</p>
<a class="button" href="/historia/">Explorar la historia ↗</a></div>
<div class="reading-preview"><p class="eyebrow">Historia de la filosofía</p>
<a href="/historia-filosofia-en-la-antiguedad/"><span>01</span> Antigüedad <b aria-hidden="true">↗</b></a>
<a href="/la-filosofia-medieval/"><span>02</span> Edad Media <b aria-hidden="true">↗</b></a>
<a href="/historia-filosofia-renacimiento-y-filosofia-moderna/"><span>03</span> Renacimiento y modernidad <b aria-hidden="true">↗</b></a>
</div></div></section>"""


def intro_readings():
    features = "".join(
        f'<li><a href="{route}"><div class="feature-photo"><img src="{MEDIA}{photo}" alt="" loading="lazy"></div><div><p class="eyebrow">{label}</p><h3>{title}</h3><p>{summary}</p><span class="text-action">Abrir lectura ↗</span></div></a></li>'
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
<p class="eyebrow">Índice de lecturas</p><h1>Biblioteca</h1><p>Busca una obra, un autor o un tema entre las publicaciones del sitio.</p>
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
BOOK_TEMPLATES = {"wp-custom-template-libros", "wp-custom-template-libros-individuales",
                  "wp-custom-template-libros-individuales-2-0"}
PDF_SECTIONS = {
    BOOK_ROOT: ("Libros PDF Gratis", "Explora las obras por autor, género, tema o idioma."),
    "autores": ("Autores", "Encuentra las obras reunidas por autor."),
    "generos-literarios": ("Géneros literarios", "Elige un género para explorar sus lecturas."),
    "idiomas": ("Idiomas", "Lecturas y materiales para aprender inglés o japonés."),
    "ramasdelafilosofia": ("Ramas de la filosofía", "Recopilaciones sobre ética, lógica, metafísica y otras ramas."),
    "filosofia-pdf": ("Filosofía en PDF", "Obras filosóficas y lecturas de referencia."),
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
        photo = (f'<img src="{escape(image)}" alt="" width="140" height="175" loading="lazy" decoding="async">'
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
                    return f'<figure class="featured"><img src="{escape(src)}" alt="" decoding="async"></figure>'
            return ""

        def book_grid(entries, route):
            entries = list(entries)
            cards_html = []
            for entry in entries:
                thumb = attachments.get(entry["meta"].get("_thumbnail_id", ""))
                cover = local_media(thumb, route) if thumb else None
                picture = (f'<img src="{escape(cover)}" alt="" loading="lazy" decoding="async">'
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
                    f'<h1>{escape(heading)}</h1><p>{escape(lead)}</p>{search}</div></div>{children}{listing}</section>')

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
                if el.tag == "img" and not el.get("src") and not el.get("srcset"):
                    el.drop_tree()
            headings = []
            ids = set(root.xpath(".//*[@id]/@id"))
            for index, heading in enumerate(root.xpath(".//h2|.//h3"), start=1):
                label = " ".join(heading.text_content().split())
                if not label:
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
            description = post["meta"].get("rank_math_description") or excerpt[:155]
            seo = post["meta"].get("rank_math_title", "").replace("%sep%", "–").replace("%sitename%", "La Biblioteca Filosófica").replace("%title%", title)
            if "%" in seo:
                seo = ""
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
                body += ('<section class="shelf journal"><div class="section-heading"><div><p class="eyebrow">En el estante</p>'
                         '<h2>Encuentra tu próxima lectura</h2></div><a class="text-action" href="/libros-pdf-gratis/">Ver todos los libros ↗</a></div>'
                         + book_grid(recent, route) + '</section>' + discovery_band() + intro_readings())
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
                suggested = f'<section class="related"><h2>Sigue explorando</h2>{cards(related)}</section>' if related else ""
                if post["is_book"]:
                    book_doc = dom.fragment_fromstring(markup, create_parent="div")
                    download = book_doc.xpath('.//a[@href and contains(concat(" ",normalize-space(@class)," ")," download-action ")]/@href')
                    purchase = book_doc.xpath('.//a[@href and contains(@rel,"sponsored")]/@href')
                    usable = [value for value in download if value.startswith(MEDIA) or (
                              urlsplit(value).scheme in {"http", "https"} and path_of(value) not in {"", "/"})]
                    actions = (f'<a class="button" href="{escape(usable[0])}">Abrir enlace de descarga ↓</a>'
                               if usable else '<a class="button" href="#texto-obra">Leer sobre la obra ↓</a>')
                    if purchase:
                        actions += f'<a class="button secondary" href="{escape(purchase[0])}" rel="sponsored nofollow">Ver edición física ↗</a>'
                    header = (f'<div class="book-detail">{feature(post)}<div><p class="eyebrow">Ficha de libro</p>'
                              f'<h1>{escape(title)}</h1><div class="actions">{actions}</div></div></div>')
                    back = '<a class="back-link" href="/libros-pdf-gratis/">← Libros PDF</a>'
                else:
                    header = f'<h1>{escape(title)}</h1><div class="reading-meta">{date}</div>{feature(post)}'
                    back = '<a class="back-link" href="/biblioteca/">← Volver a la biblioteca</a>'
                crumbs = post_crumbs(post)
                body = f'<article class="reading" id="lectura">{breadcrumbs(crumbs)}{back}{header}{toc}<div class="entry" id="texto-obra">{markup}</div>{term_links(post)}{suggested}<a class="button secondary" href="#lectura">Volver arriba ↑</a></article>'
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
                    work = {"@type": "Book", "name": title, "url": BASE + route}
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

        write("/biblioteca/", shell("Biblioteca · La Biblioteca Filosófica", "/biblioteca/",
              catalog(posts)))
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
            (routes - {"/libros-gratis-en-online/"}) | {"/biblioteca/"} |
            {category_route(slug) for slug in categories if category_posts[slug]}))
        + "</urlset>\n", encoding="utf-8")
    (output / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n" if args.production
        else "User-agent: *\nDisallow: /\n", encoding="utf-8")
    config = {"$schema": "https://openapi.vercel.sh/vercel.json", "framework": None,
              "outputDirectory": "public", "trailingSlash": True,
              "redirects": [{"source": "/sitemap_index.xml", "destination": "/sitemap.xml", "permanent": True}]
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

