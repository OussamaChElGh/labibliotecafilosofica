"""Genera las páginas de lectura online de obras de dominio público.

Cada obra vive en textos/<slug>.txt (un bloque por línea: H| título, P| párrafo,
N| nota del traductor; las llamadas a nota se marcan como [[n]]) y
textos/<slug>.json (metadatos y división en capítulos).

Uso, después de migrate.py:  python lectura_completa.py
Escribe public/leer/<slug>/ y añade las URL al sitemap.
"""
import json
import re
from pathlib import Path

from migrate import BASE, breadcrumb_schema, breadcrumbs, escape, shell

PROJECT = Path(__file__).resolve().parent
TEXTS = PROJECT / "textos"
OUTPUT = PROJECT / "public"
WORDS_PER_MINUTE = 220
TOOLBAR = ('<div class="reader-toolbar" hidden><a href="/biblioteca/">← Biblioteca</a><div role="group" aria-label="Aspecto de lectura">'
           '<button data-paper="noir" aria-pressed="true">Oscuro</button><button data-paper="cream" aria-pressed="false">Papel</button>'
           '<button data-paper="sepia" aria-pressed="false">Sepia</button><button data-text-size="-2" aria-label="Reducir texto">A−</button>'
           '<button data-text-size="2" aria-label="Ampliar texto">A+</button><button data-text-font aria-pressed="false">Sans</button>'
           '<button data-share-page>Compartir</button></div><span data-reader-status role="status"></span></div>')


BOOK_ASSETS = ('<link rel="stylesheet" href="/lector-libro.css"><script>document.documentElement.classList.add("book-js")</script>'
               '<script defer src="/lector-libro.js"></script></head>')


def with_book_assets(document, meta):
    # Imagen para redes y vista previa de enlaces (la genera portadas.mjs).
    image = f'{BASE}/leer/{meta["slug"]}/social.png'
    social = (f'<meta property="og:type" content="book"><meta property="og:site_name" content="La Biblioteca Filosófica">'
              f'<meta property="og:image" content="{image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
              f'<meta property="og:image:alt" content="Portada de {escape(meta["title"])}, de {escape(meta["author"])}">'
              f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{image}">')
    return document.replace("</head>", social + BOOK_ASSETS, 1)


COVER_COLORS = {"verde": "#143a2c", "burdeos": "#4a1820", "azul": "#16233b", "ocre": "#4f3615", "negro": "#161015"}


def cover_svg(meta):
    """Portada común de la colección: cambia el color, el número y los textos."""
    cover = meta.get("cover", {})
    bg = COVER_COLORS.get(cover.get("color", "verde"), cover.get("color", "#143a2c"))
    ink, gold = "#f7f4ee", "#c8a96a"
    words, lines = meta["title"].split(), []
    for word in words:
        if lines and len(lines[-1]) + 1 + len(word) <= 12:
            lines[-1] += " " + word
        else:
            lines.append(word)
    longest = max(len(line) for line in lines)
    size = min(92, int(470 / (longest * 0.48)))
    top = 470 - (len(lines) - 1) * size * 0.55
    title = "".join(f'<text x="300" y="{top + i * size * 1.05:.0f}" font-size="{size}">{escape(line)}</text>' for i, line in enumerate(lines))
    rays = "".join(f'<line x1="300" y1="618" x2="300" y2="600" transform="rotate({angle} 300 650)"/>' for angle in range(0, 360, 15))
    number = f'{int(cover.get("number", 1)):02d}'
    return (f'<svg class="book-cover-art" viewBox="0 0 600 900" role="img" aria-label="Portada de {escape(meta["title"])}, de {escape(meta["author"])}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="600" height="900" fill="{bg}"/>'
            f'<rect width="600" height="900" fill="url(#cover-grain-{escape(meta["slug"])})" opacity=".5"/>'
            f'<defs><radialGradient id="cover-grain-{escape(meta["slug"])}" cx="50%" cy="38%" r="75%"><stop offset="0" stop-color="#fff" stop-opacity=".10"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient></defs>'
            f'<rect x="28" y="28" width="544" height="844" fill="none" stroke="{gold}" stroke-width="1.6"/>'
            f'<rect x="38" y="38" width="524" height="824" fill="none" stroke="{gold}" stroke-width=".7" opacity=".7"/>'
            f'<text x="300" y="104" fill="{ink}" opacity=".82" font-family="Inter, sans-serif" font-size="13" letter-spacing="4.5" text-anchor="middle">LA BIBLIOTECA FILOSÓFICA</text>'
            f'<line x1="270" y1="128" x2="330" y2="128" stroke="{gold}" stroke-width="1"/>'
            f'<text x="300" y="{top - size - 28:.0f}" fill="{gold}" font-family="Inter, sans-serif" font-size="20" letter-spacing="7" text-anchor="middle">{escape(meta["author"].upper())}</text>'
            f'<g fill="{ink}" font-family="\'Caslon Display\', Fraunces, Georgia, serif" text-anchor="middle">{title}</g>'
            f'<g stroke="{gold}" stroke-width="1.4" fill="none"><circle cx="300" cy="650" r="54"/><circle cx="300" cy="650" r="20"/>{rays}</g>'
            f'<text x="300" y="790" fill="{ink}" opacity=".85" font-family="Fraunces, Georgia, serif" font-style="italic" font-size="19" text-anchor="middle">Traducción de {escape(meta["translator"])}</text>'
            f'<text x="300" y="836" fill="{gold}" font-family="Inter, sans-serif" font-size="12" letter-spacing="4" text-anchor="middle">LECTURA COMPLETA · Nº {number}</text>'
            '</svg>')


def minutes(words):
    return max(1, round(words / WORDS_PER_MINUTE))


def with_note_links(text):
    return re.sub(r"\[\[(\d+)\]\]", lambda m: f'<sup><a href="#nota-{m[1]}" id="llamada-{m[1]}">{m[1]}</a></sup>', escape(text))


def write(route, document):
    target = OUTPUT / route.strip("/") / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(document, encoding="utf-8")


def credit(meta):
    return (f'<p class="rights-note">Texto de dominio público. Traducción de {escape(meta["translator"])} '
            f'({escape(meta["edition"])}). Transcripción de <a href="{escape(meta["source_url"])}">Wikisource</a>, '
            f'publicada bajo licencia <a href="{escape(meta["license_url"])}">{escape(meta["license"])}</a>. '
            'División en capítulos, títulos y resúmenes: La Biblioteca Filosófica.</p>')


def build(meta, blocks):
    slug = meta["slug"]
    base_route = f"/leer/{slug}/"
    full_title = f'{meta["title"]}, de {meta["author"]}'
    notes = {}
    for line in blocks:
        if line.startswith("N|"):
            notes[len(notes) + 1] = line[2:]
    skip = set(meta.get("skip", []))
    speakers = {int(k): v for k, v in meta.get("speakers", {}).items()}
    chapters = meta["chapters"]
    routes = [base_route]

    rendered = []
    for chapter in chapters:
        paragraphs, used, words = [], [], 0
        for index in range(chapter["start"], chapter["end"] + 1):
            line = blocks[index]
            if index in skip or not line.startswith("P|"):
                continue
            text = re.sub(r"(\w)- ([a-záéíóúüñ])", r"\1\2", line[2:].replace("»>", "»"))  # guiones de fin de línea del OCR
            words += len(text.split())
            used += [int(n) for n in re.findall(r"\[\[(\d+)\]\]", text)]
            speaker = f'<strong>{escape(speakers[index])}.</strong> ' if index in speakers else ""
            paragraphs.append(f"<p>{speaker}{with_note_links(text)}</p>")
        note_list = ""
        if used:
            items = "".join(f'<li id="nota-{n}" value="{n}">{escape(notes.get(n, ""))} <a href="#llamada-{n}" aria-label="Volver al texto">↩</a></li>'
                            for n in sorted(set(used)))
            note_list = f'<section class="reading-notes"><h2>Notas del traductor</h2><ol>{items}</ol></section>'
        rendered.append((chapter, "".join(paragraphs), note_list, words))

    total_words = sum(item[3] for item in rendered)
    crumbs_index = [("Inicio", "/"), ("Libros PDF Gratis", "/libros-pdf-gratis/"),
                    (meta["title"], meta["book_route"]), ("Leer online", base_route)]

    # Página índice de la obra.
    chapter_links = "".join(
        f'<li><a href="{base_route}{chapter["slug"]}/"><strong>{escape(chapter["title"])}</strong></a>'
        f'<p>{escape(chapter["summary"])} <small>{minutes(words)} min</small></p></li>'
        for number, (chapter, _, _, words) in enumerate(rendered, start=1))
    first = f'{base_route}{chapters[0]["slug"]}/'
    start_reading = f'{base_route}{chapters[1]["slug"]}/' if len(chapters) > 1 and chapters[0]["slug"] == "argumento" else first
    index_body = (f'{TOOLBAR}<article class="reading reader-v2 reader-article" id="lectura">{breadcrumbs(crumbs_index)}'
                  f'<a class="back-link" href="{meta["book_route"]}">← Ficha del libro</a>'
                  f'<header class="folio-article-head"><p class="eyebrow">Lectura completa · {escape(meta["author"])}</p>'
                  f'<h1>{escape(meta["title"])}: leer online completo</h1>'
                  f'<div class="reading-meta"><span>{len(chapters)} capítulos · {total_words:,} palabras · {minutes(total_words)} min de lectura</span>'
                  f'<a href="{start_reading}">Empezar a leer ↓</a></div></header>'
                  f'<div class="entry" id="texto-obra"><figure class="book-cover">{cover_svg(meta)}'
                  f'<figcaption><a href="{base_route}portada.png" download>Descargar portada</a></figcaption></figure>{meta["intro"]}'
                  f'<div class="continue-reading" data-continue-book="{escape(slug)}" hidden></div>'
                  f'<p><a class="button" href="{start_reading}">Empezar a leer ↗</a></p>'
                  f'<h2 id="capitulos">Capítulos</h2><ol class="chapter-list">{chapter_links}</ol>{credit(meta)}'
                  f'<p>¿Quieres orientarte antes de leer? Consulta la <a href="{meta["book_route"]}">ficha de {escape(meta["title"])}</a> '
                  f'y la guía <a href="/por-donde-empezar-a-leer-a-platon/">por dónde empezar a leer a Platón</a>.</p></div></article>')
    index_schema = {"@context": "https://schema.org", "@graph": [breadcrumb_schema(crumbs_index), {
        "@type": "Book", "name": meta["title"], "url": BASE + base_route, "inLanguage": "es",
        "isAccessibleForFree": True, "author": {"@type": "Person", "name": meta["author"]},
        "translator": {"@type": "Person", "name": meta["translator"]},
        "license": meta["license_url"],
        "hasPart": [{"@type": "Chapter", "name": c["title"], "position": i, "url": f'{BASE}{base_route}{c["slug"]}/'}
                    for i, c in enumerate(chapters, start=1)]}]}
    write(base_route, with_book_assets(shell(f'{meta["title"]} de {meta["author"]}: leer online completo y gratis · La Biblioteca Filosófica',
                            base_route, index_body, meta["description"], schema=index_schema), meta))

    # Una página por capítulo.
    done_words = 0
    for number, (chapter, paragraphs, note_list, words) in enumerate(rendered, start=1):
        progress_start, progress_span = done_words / total_words, words / total_words
        done_words += words
        route = f'{base_route}{chapter["slug"]}/'
        routes.append(route)
        previous = rendered[number - 2][0] if number > 1 else None
        following = rendered[number][0] if number < len(rendered) else None
        pager = '<nav class="actions chapter-pager" aria-label="Capítulos">'
        if previous:
            pager += f'<a class="button secondary" href="{base_route}{previous["slug"]}/" rel="prev">← {escape(previous["title"])}</a>'
        pager += f'<a class="button secondary" href="{base_route}">Índice</a>'
        if following:
            pager += f'<a class="button" href="{base_route}{following["slug"]}/" rel="next">{escape(following["title"])} →</a>'
        pager += "</nav>"
        crumbs = crumbs_index[:-1] + [("Leer online", base_route), (chapter["title"], route)]
        body = (f'{TOOLBAR}<article class="reading reader-v2 reader-article" id="lectura">{breadcrumbs(crumbs)}'
                f'<a class="back-link" href="{base_route}">← Índice de {escape(meta["title"])}</a>'
                f'<header class="folio-article-head"><p class="eyebrow">{escape(full_title)} · Capítulo {number} de {len(rendered)}</p>'
                f'<h1>{escape(chapter["title"])}</h1>'
                f'<div class="reading-meta"><span>{minutes(words)} min de lectura</span><a href="#texto-obra">Empezar a leer ↓</a></div></header>'
                f'<div class="entry" id="texto-obra">'
                f'<div class="book" data-book="{escape(slug)}" data-book-title="{escape(meta["title"])}" data-book-route="{escape(meta["book_route"])}" '
                f'data-chapter="{number}" data-chapters="{len(rendered)}" data-chapter-title="{escape(chapter["title"])}" '
                f'data-progress-start="{progress_start:.4f}" data-progress-span="{progress_span:.4f}" '
                f'data-prev="{base_route + previous["slug"] + "/" if previous else ""}" data-next="{base_route + following["slug"] + "/" if following else ""}">'
                f'<div class="book-viewport"><div class="book-flow"><p class="book-summary"><em>{escape(chapter["summary"])}</em></p>{paragraphs}{note_list}</div></div></div>'
                f'{pager}{credit(meta)}</div></article>')
        schema = {"@context": "https://schema.org", "@graph": [breadcrumb_schema(crumbs), {
            "@type": "Chapter", "name": chapter["title"], "position": number, "url": BASE + route,
            "isPartOf": {"@type": "Book", "name": meta["title"], "url": BASE + base_route,
                         "author": {"@type": "Person", "name": meta["author"]}}}]}
        description = f'{chapter["title"]} de {full_title}: texto completo online. {chapter["summary"]}'
        write(route, with_book_assets(shell(f'{chapter["title"]} · {full_title} (texto completo) · La Biblioteca Filosófica',
                           route, body, description[:300], schema=schema), meta))
    meta["_stats"] = {"chapters": len(rendered), "minutes": minutes(total_words)}
    return routes


def duration(total):
    hours, rest = divmod(total, 60)
    return f"{hours} h {rest:02d} min" if hours else f"{rest} min"


def update_home(metas):
    """Estante «Leer online gratis» en la portada, entre el buscador y la selección."""
    home = OUTPUT / "index.html"
    document = home.read_text(encoding="utf-8")
    cards = "".join(
        f'<li><a href="/leer/{escape(m["slug"])}/"><img src="/leer/{escape(m["slug"])}/portada-ficha.jpg" '
        f'alt="Portada de {escape(m["title"])}, de {escape(m["author"])}" width="400" height="600" loading="lazy">'
        f'<span class="online-shelf-author">{escape(m["author"])}</span><strong>{escape(m["title"])}</strong>'
        f'<span class="online-shelf-meta">{m["_stats"]["chapters"]} capítulos · {duration(m["_stats"]["minutes"])}</span>'
        f'<span class="online-shelf-cta">Leer ahora ↗</span></a></li>' for m in metas)
    section = ('<!--lectura-completa--><section class="online-shelf" id="leer-online"><div class="online-shelf-intro">'
               '<p class="eyebrow">Lectura completa · gratis y sin registro</p><h2>Lee las obras completas aquí, página a página.</h2>'
               '<p>Textos de dominio público en traducciones clásicas, con modo libro, notas y un marcapáginas que recuerda dónde lo dejaste.</p></div>'
               f'<ul class="online-shelf-list">{cards}</ul></section><!--/lectura-completa-->')
    if "<!--lectura-completa-->" in document:
        document = re.sub(r"<!--lectura-completa-->.*?<!--/lectura-completa-->", lambda _: section, document, flags=re.S)
    else:
        document = document.replace('<section class="edition-section"', section + '<section class="edition-section"', 1)
    if 'href="/lector-libro.css"' not in document:
        document = document.replace("</head>", '<link rel="stylesheet" href="/lector-libro.css"></head>', 1)
    home.write_text(document, encoding="utf-8")


def update_sitemap(routes):
    sitemap = OUTPUT / "sitemap.xml"
    content = sitemap.read_text(encoding="utf-8")
    missing = [r for r in routes if f"<loc>{BASE}{r}</loc>" not in content]
    if missing:
        entries = "".join(f"<url><loc>{BASE}{r}</loc></url>\n" for r in missing)
        content = content.replace("</urlset>", entries + "</urlset>")
        sitemap.write_text(content, encoding="utf-8")


def main():
    routes, metas = [], []
    for config in sorted(TEXTS.glob("*.json")):
        meta = json.loads(config.read_text(encoding="utf-8"))
        blocks = (TEXTS / f'{meta["slug"]}.txt').read_text(encoding="utf-8").split("\n")
        routes += build(meta, blocks)
        metas.append(meta)
    update_sitemap(routes)
    update_home(sorted(metas, key=lambda m: m.get("cover", {}).get("number", 99)))
    print(f"{len(routes)} páginas de lectura generadas")


if __name__ == "__main__":
    main()
