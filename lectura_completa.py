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


def with_book_assets(document):
    return document.replace("</head>", BOOK_ASSETS, 1)


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
                  f'<div class="entry" id="texto-obra">{meta["intro"]}'
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
                            base_route, index_body, meta["description"], schema=index_schema)))

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
                f'<div class="book" data-book="{escape(slug)}" data-book-title="{escape(meta["title"])}" data-book-route="{base_route}" '
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
                           route, body, description[:300], schema=schema)))
    return routes


def update_sitemap(routes):
    sitemap = OUTPUT / "sitemap.xml"
    content = sitemap.read_text(encoding="utf-8")
    missing = [r for r in routes if f"<loc>{BASE}{r}</loc>" not in content]
    if missing:
        entries = "".join(f"<url><loc>{BASE}{r}</loc></url>\n" for r in missing)
        content = content.replace("</urlset>", entries + "</urlset>")
        sitemap.write_text(content, encoding="utf-8")


def main():
    routes = []
    for config in sorted(TEXTS.glob("*.json")):
        meta = json.loads(config.read_text(encoding="utf-8"))
        blocks = (TEXTS / f'{meta["slug"]}.txt').read_text(encoding="utf-8").split("\n")
        routes += build(meta, blocks)
    update_sitemap(routes)
    print(f"{len(routes)} páginas de lectura generadas")


if __name__ == "__main__":
    main()
