"""Pasa las fichas heredadas de WordPress al formato de ficha única de libro.

python fichas_antiguas.py  (después de pulir.py)

Para cada ruta con datos en textos/fichas/antiguas/*.py reescribe el cuerpo de la ficha con
la misma estructura que las fichas nuevas: resumen, cita, personajes, ideas principales,
contexto, datos del libro y preguntas frecuentes (con su FAQPage), además de un título y un
h1 más claros. Del texto de WordPress solo se conserva lo aprovechable (la cita destacada,
la ficha técnica, el contexto, los recuadros de Amazon y los enlaces internos), que se guarda
la primera vez en textos/fichas/antiguas/extraido.json para que el script sea idempotente.
"""
import html
import importlib.util
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
DATA = ROOT / "textos" / "fichas" / "antiguas"
BASE = "https://labibliotecafilosofica.com"
MARK = "data-ficha-v2"
CACHE = DATA / "extraido.json"
START = '<div class="entry" id="texto-obra">'
# Solo se muestran las citas antiguas que son literales y del libro de la ficha; el resto
# (paráfrasis o frases de otra obra) se descarta.
CITAS_VERIFICADAS = {
    "/el-extranjero-pdf-albert-camus/", "/albert-camus-el-mito-de-sisifo-pdf/", "/albert-camus-caligula-pdf/",
    "/albert-camus-el-verano/", "/descartes-discurso-del-metodo-pdf/", "/asi-hablo-zaratustra-friedrich-nietzsche/",
    "/mas-alla-del-bien-y-del-mal-friedrich-nietzsche/", "/la-gaya-ciencia-pdf-friedrich-nietzsche/",
    "/ecce-homo-friedrich-nietzsche-pdf/", "/sobre-verdad-y-mentira-en-sentido-extramoral-friedrich-nietzsche-pdf/",
    "/the-yellow-wallpaper-pdf-charlotte-perkins-gilman/", "/the-ones-who-walk-away-from-omelas-pdf-ursula-k-le-guin/",
}


def esc(text):
    return html.escape(text, quote=True)


def load_books():
    books = {}
    for path in sorted(DATA.glob("*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        books.update(module.BOOKS)
    return books


def clean(fragment):
    """Texto plano sin etiquetas, emojis ni espacios sobrantes."""
    text = html.unescape(re.sub(r"<[^>]+>", " ", fragment))
    text = "".join(ch for ch in text if unicodedata.category(ch) not in ("So", "Cn", "Mn") or ch in "\u0301\u0303")
    text = unicodedata.normalize("NFC", text).replace("\u200d", "")
    text = re.sub(r"\s+([.,;:!?)»])", r"\1", re.sub(r"\s+", " ", text))
    return re.sub(r"([(«¿¡])\s+", r"\1", text).strip(" :–-|")


def body_bounds(document):
    start = document.index(START) + len(START)
    end = document.find('</div><div class="terms">', start)
    if end < 0:
        end = document.find("</div></article>", start)
    return start, end


def extract(route, document):
    """Lo aprovechable del cuerpo de WordPress: cita, ficha técnica, contexto, Amazon y enlaces."""
    document = re.sub(r"<!--ficha-v2-->.*?<!--/ficha-v2-->", "", document, flags=re.S)
    start, end = body_bounds(document)
    body = document[start:end]
    out = {"paper_box": "", "affiliate": [], "cita": "", "datos": [], "contexto": [], "enlaces": []}
    box = re.search(r'<aside class="paper-box".*?</aside>', body, re.S)
    if box:
        out["paper_box"] = box.group(0)
    out["affiliate"] = re.findall(r'<aside class="affiliate".*?</aside>', body, re.S)
    body = re.sub(r"<aside.*?</aside>", "", body, flags=re.S)
    heads = list(re.finditer(r"<h([2-4])[^>]*>(.*?)</h\1>", body, re.S))

    def after(match):
        """HTML entre un encabezado y el siguiente."""
        nxt = [h.start() for h in heads if h.start() > match.end()]
        return body[match.end():nxt[0] if nxt else len(body)]

    quote = re.search(r"<blockquote[^>]*>(.*?)</blockquote>", body, re.S)
    if quote:
        out["cita"] = clean(quote.group(1))
    for head in heads:
        name = clean(head.group(2)).lower()
        if not out["cita"] and "cita destacada" in name:
            first = re.search(r"<p[^>]*>(.*?)</p>", after(head), re.S)
            out["cita"] = clean(first.group(1)) if first else ""
        elif not out["cita"] and name[:1] in "\"«“" and name[-1:] in "\"»”" and len(name) < 200:
            out["cita"] = clean(head.group(2))
        elif "ficha técnica" in name or "ficha tecnica" in name:
            for item in re.findall(r"<li[^>]*>(.*?)</li>", after(head), re.S):
                key, sep, value = clean(item).partition(":")
                if sep and value.strip():
                    out["datos"].append([key.strip(), value.strip()])
        elif name.startswith("contexto"):
            section = re.split(r"<hr|<div", after(head))[0]
            out["contexto"] = [clean(p) for p in re.findall(r"<p[^>]*>(.*?)</p>", section, re.S) if len(clean(p)) > 40]
    out["cita"] = re.sub(r"^cita destacada:?\s*", "", out["cita"], flags=re.I).strip("\"“”«» ")
    if len(out["cita"]) > 320:
        out["cita"] = ""
    seen = {route}
    for ul in re.findall(r'<ul class="cards">(.*?)</ul>', body, re.S):
        for href, text in re.findall(r'<a href="(/[^"#]*)">(.*?)</a>', ul, re.S):
            if href not in seen:
                seen.add(href)
                out["enlaces"].append([href, re.sub(r"\s+-\s+", ", de ", clean(text), count=1)])
    return out


def fact_rows(data, extra):
    """Datos del libro: lo de la ficha técnica antigua sin repetir autor ni formato."""
    rows = [("Autor", data["autor"]), ("Género", data["genero"]), ("Publicación", data["año"])]
    skip = ("autor", "formato", "título", "titulo", "género", "genero", "año", "fecha")
    for key, value in extra:
        low = key.lower()
        if low.startswith(skip) and not low.startswith(("título original", "titulo original")):
            continue
        if low.startswith(("extensión", "extension")):
            value = re.sub(r"^PDF\s*\|?\s*", "", value, flags=re.I)
        if low == "idioma" and value.lower() == "español":
            key = "Idioma de esta edición"
        if value and len(rows) < 9:
            rows.append((key[:1].upper() + key[1:], value))
    return rows


def crumbs_html(items):
    lis = "".join(f'<li><a href="{href}">{esc(name)}</a></li>' for name, href in items[:-1])
    return (f'<nav class="crumbs" aria-label="Ruta de navegación"><ol>{lis}'
            f'<li aria-current="page">{esc(items[-1][0])}</li></ol></nav>')


def upgrade(route, data, document, kept):
    title, author = data["titulo"], data["autor"]
    name = f"{title}, de {author}"
    # Recupera el documento original si ya se actualizó: el bloque nuevo va entre marcas.
    document = re.sub(r"<!--ficha-v2-->.*?<!--/ficha-v2-->", "", document, flags=re.S)
    old_title = re.search(r"<title>(.*?) · La Biblioteca Filosófica</title>", document)
    pdf = " [PDF]" if old_title and "PDF" in old_title.group(1).upper() else ""
    seo_title = f"{title} de {author}{pdf}: resumen, personajes y análisis" if data.get("personajes") else \
        f"{title} de {author}{pdf}: resumen, ideas y análisis"
    document = re.sub(r"<title>.*?</title>", f"<title>{esc(seo_title)} · La Biblioteca Filosófica</title>", document, count=1)
    document = re.sub(r'<meta property="og:title" content="[^"]*">',
                      f'<meta property="og:title" content="{esc(seo_title)}">', document, count=1)
    if data.get("descripcion"):
        for attr in ('name="description"', 'property="og:description"'):
            document = re.sub(rf'<meta {attr} content="[^"]*">', f'<meta {attr} content="{esc(data["descripcion"])}">', document, count=1)

    # Migas con el autor correcto y h1 «Título, de Autor».
    crumbs = [("Inicio", "/"), ("Libros PDF Gratis", "/libros-pdf-gratis/")]
    if data.get("ruta_autor"):
        crumbs += [("Autores", "/libros-pdf-gratis/autores/"), (author, data["ruta_autor"])]
    crumbs.append((title, route))
    document = re.sub(r'<nav class="crumbs".*?</nav>', crumbs_html(crumbs), document, count=1, flags=re.S)
    if data.get("ruta_autor"):
        document = re.sub(r'<a class="back-link" href="[^"]*">[^<]*</a>',
                          f'<a class="back-link" href="{data["ruta_autor"]}">← Más libros de {esc(author)}</a>', document, count=1)
    context = f'{data["genero"]} · {data["año"]}. Sobre {data["tema"]}.'
    document = re.sub(r'<p class="eyebrow">(?:Ficha de libro|La Biblioteca · Lecturas e ideas)[^<]*</p><h1>.*?</h1>',
                      f'<p class="eyebrow">Ficha de libro · {esc(author)}</p><h1>{esc(name)}</h1>'
                      f'<!--ficha-v2--><p class="book-context">{esc(context)}</p><!--/ficha-v2-->', document, count=1, flags=re.S)
    document = re.sub(r'<a class="button" href="#texto-obra">Leer sobre la obra ↓</a>',
                      '<a class="button" href="#resumen">Leer el resumen ↓</a>', document, count=1)
    document = re.sub(r'<a class="text-link" href="#texto-obra">Leer el análisis ↓</a>',
                      '<a class="text-link" href="#preguntas">Preguntas frecuentes ↓</a>', document, count=1)
    document = re.sub(r'<details class="toc">.*?</details>', "", document, count=1, flags=re.S)

    has_people = bool(data.get("personajes"))
    links = [("resumen", "Resumen")] + ([("personajes", "Personajes")] if has_people else []) + \
            [("ideas", "Ideas principales")] + ([("contexto", "Contexto")] if kept["contexto"] else []) + \
            [("datos", "Datos del libro"), ("preguntas", "Preguntas")]
    toc = " · ".join(f'<a href="#{i}">{t}</a>' for i, t in links)
    parts = [f'<nav class="toc-inline" aria-label="En esta ficha">{toc}</nav>',
             f'<h2 id="resumen">Resumen de {esc(title)}</h2>' + "".join(f"<p>{esc(p)}</p>" for p in data["resumen"])]
    if kept["cita"] and route in CITAS_VERIFICADAS:
        parts.append(f'<blockquote class="editorial-quote"><p>«{esc(kept["cita"])}»</p>'
                     f'<p class="quote-source">{esc(author)}, <cite>{esc(title)}</cite></p></blockquote>')
    current = re.search(r'<aside class="paper-box".*?</aside>', document, re.S)
    box = current.group(0) if current else kept["paper_box"]
    parts.append(re.sub(r'(<p class="paper-box-title">¿Prefieres leer «)[^»]*(» en papel\?</p>)', rf"\g<1>{esc(name)}\g<2>", box))
    if has_people:
        parts.append('<h2 id="personajes">Personajes</h2><dl class="guide-characters">' +
                     "".join(f"<dt>{esc(n)}</dt><dd>{esc(d)}</dd>" for n, d in data["personajes"]) + "</dl>")
    parts.append('<h2 id="ideas">Ideas principales</h2><ul>' + "".join(f"<li>{esc(i)}</li>" for i in data["ideas"]) + "</ul>")
    if kept["contexto"]:
        parts.append(f'<h2 id="contexto">Contexto de {esc(title)}</h2>' + "".join(f"<p>{esc(p)}</p>" for p in kept["contexto"]))
    parts.append('<h2 id="datos">Datos del libro</h2><dl class="guide-characters book-facts">' +
                 "".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k, v in fact_rows(data, kept["datos"])) +
                 f"<dt>Tema</dt><dd>{esc(data['tema'][:1].upper() + data['tema'][1:])}</dd></dl>")
    parts.extend(kept["affiliate"][:1])
    parts.append(f'<h2 id="preguntas">Preguntas frecuentes sobre {esc(title)}</h2>' +
                 "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in data["faq"]))
    if kept["enlaces"]:
        parts.append('<h2 id="relacionados">Más lecturas relacionadas</h2><ul class="cards">' +
                     "".join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in kept["enlaces"][:8]) + "</ul>")
    author_link = f'<a href="{data["ruta_autor"]}">Más libros de {esc(author)}</a> · ' if data.get("ruta_autor") else ""
    parts.append(f'<p class="guide-link">{author_link}<a href="/resumenes/">Más resúmenes</a> · '
                 '<a href="/leer/">Libros para leer online gratis</a></p>')
    start, end = body_bounds(document)
    document = document[:start] + "<!--ficha-v2-->" + "".join(parts) + "<!--/ficha-v2-->" + document[end:]

    # Datos estructurados: migas, Book con descripción y FAQPage.
    def schema(match):
        graph = json.loads(match.group(1))
        items = [entry for entry in graph.get("@graph", []) if entry.get("@type") not in ("BreadcrumbList", "FAQPage")]
        for entry in items:
            if entry.get("@type") == "Book":
                entry.update({"name": title, "author": {"@type": "Person", "name": author}, "genre": data["genero"],
                              "abstract": data["resumen"][0]})
        items.insert(0, {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": n, "item": BASE + h} for i, (n, h) in enumerate(crumbs, start=1)]})
        items.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in data["faq"]]})
        return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": items}, ensure_ascii=False) + "</script>"
    document = re.sub(r'<script type="application/ld\+json">(.*?)</script>', schema, document, count=1, flags=re.S)
    if "/lector-libro.css" not in document:
        document = document.replace("</head>", '<link rel="stylesheet" href="/lector-libro.css"></head>', 1)
    if MARK not in document:
        document = re.sub(r'<article class="reading reader-v2 (reader-book|reader-article)"',
                          rf'<article {MARK} class="reading reader-v2 \1 guide book-ficha"', document, count=1)
    return document


def main():
    books = load_books()
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    for route, data in books.items():
        target = PUBLIC / route.strip("/") / "index.html"
        if not target.exists():
            print("no existe:", route)
            continue
        document = target.read_text(encoding="utf-8")
        if route not in cache:
            cache[route] = extract(route, document)
        target.write_text(upgrade(route, data, document, cache[route]), encoding="utf-8")
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(books)} fichas actualizadas al formato nuevo")


if __name__ == "__main__":
    main()
