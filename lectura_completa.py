"""Genera las páginas de lectura online de obras de dominio público.

Cada obra vive en textos/<slug>.txt (un bloque por línea: H| título, P| párrafo,
V| verso citado, S| acotación entre paréntesis, N| nota del traductor; las llamadas a nota se marcan como [[n]]) y
textos/<slug>.json (metadatos y división en capítulos).

Uso, después de migrate.py:  python lectura_completa.py
Escribe public/leer/<slug>/ y añade las URL al sitemap.
"""
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import quote_plus

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
    image = f'{BASE}/leer/{meta["slug"]}/social.jpg'
    social = (f'<meta property="og:type" content="book"><meta property="og:site_name" content="La Biblioteca Filosófica">'
              f'<meta property="og:image" content="{image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
              f'<meta property="og:image:alt" content="Portada de {escape(meta["title"])}, de {escape(meta["author"])}">'
              f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{image}">')
    return document.replace("</head>", social + BOOK_ASSETS, 1)


COVER_COLORS = {"verde": "#143a2c", "burdeos": "#4a1820", "azul": "#16233b", "ocre": "#4f3615", "negro": "#161015"}


ART = Path("textos/ilustraciones")


def art_image(art, x, y, width, height, inline):
    """Pintura recortada a la ventana de la portada, centrada en el punto de interés (focus 0–1)."""
    import base64
    from PIL import Image
    source = ART / art["file"]
    with Image.open(source) as image:
        natural_w, natural_h = image.size
    scale = max(width / natural_w, height / natural_h)
    shown_w, shown_h = natural_w * scale, natural_h * scale
    fx, fy = art.get("focus", [0.5, 0.5])
    left = min(max(fx * shown_w - width / 2, 0), shown_w - width)
    top = min(max(fy * shown_h - height / 2, 0), shown_h - height)
    href = ("data:image/jpeg;base64," + base64.b64encode(source.read_bytes()).decode()) if inline else art["url"]
    return (f'<image href="{href}" x="{x - left:.1f}" y="{y - top:.1f}" width="{shown_w:.1f}" height="{shown_h:.1f}" '
            f'clip-path="url(#ventana-{art["clip"]})" preserveAspectRatio="none"/>')


def cover_svg(meta, inline=False):
    """Portada común de la colección: cambia el color, el número, los textos y, si la hay, la pintura."""
    cover = meta.get("cover", {})
    if cover.get("art"):
        return cover_art_svg(meta, inline)
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
            f'<text x="300" y="790" fill="{ink}" opacity=".85" font-family="Fraunces, Georgia, serif" font-style="italic" font-size="19" text-anchor="middle">{escape(version(meta))}</text>'
            f'<text x="300" y="836" fill="{gold}" font-family="Inter, sans-serif" font-size="12" letter-spacing="4" text-anchor="middle">LECTURA COMPLETA · Nº {number}</text>'
            '</svg>')


def cover_art_svg(meta, inline=False):
    """Variante con pintura de dominio público en una ventana dentro del marco."""
    cover = meta["cover"]
    bg = COVER_COLORS.get(cover.get("color", "verde"), cover.get("color", "#143a2c"))
    ink, gold = "#f7f4ee", "#c8a96a"
    slug = escape(meta["slug"])
    art = {**cover["art"], "clip": slug}
    win = (64, 132, 472, 400)  # x, y, ancho, alto
    words, lines = meta["title"].split(), []
    for word in words:
        if lines and len(lines[-1]) + 1 + len(word) <= 16:
            lines[-1] += " " + word
        else:
            lines.append(word)
    longest = max(len(line) for line in lines)
    size = min(70, int(470 / (longest * 0.48)))
    top = 688 - (len(lines) - 1) * size * 0.5
    title = "".join(f'<text x="300" y="{top + i * size * 1.05:.0f}" font-size="{size}">{escape(line)}</text>' for i, line in enumerate(lines))
    number = f'{int(cover.get("number", 1)):02d}'
    x, y, w, h = win
    return (f'<svg class="book-cover-art" viewBox="0 0 600 900" role="img" aria-label="Portada de {escape(meta["title"])}, de {escape(meta["author"])}" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><clipPath id="ventana-{slug}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2"/></clipPath>'
            f'<linearGradient id="fundido-{slug}" x1="0" y1="0" x2="0" y2="1"><stop offset=".62" stop-color="{bg}" stop-opacity="0"/><stop offset="1" stop-color="{bg}" stop-opacity=".85"/></linearGradient>'
            f'<radialGradient id="luz-{slug}" cx="50%" cy="30%" r="80%"><stop offset="0" stop-color="#fff" stop-opacity=".08"/><stop offset="1" stop-color="#000" stop-opacity=".35"/></radialGradient></defs>'
            f'<rect width="600" height="900" fill="{bg}"/><rect width="600" height="900" fill="url(#luz-{slug})"/>'
            f'{art_image(art, x, y, w, h, inline)}'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#fundido-{slug})"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{gold}" stroke-width="1.2"/>'
            f'<rect x="28" y="28" width="544" height="844" fill="none" stroke="{gold}" stroke-width="1.6"/>'
            f'<rect x="38" y="38" width="524" height="824" fill="none" stroke="{gold}" stroke-width=".7" opacity=".7"/>'
            f'<text x="300" y="90" fill="{ink}" opacity=".82" font-family="Inter, sans-serif" font-size="13" letter-spacing="4.5" text-anchor="middle">LA BIBLIOTECA FILOSÓFICA</text>'
            f'<line x1="270" y1="108" x2="330" y2="108" stroke="{gold}" stroke-width="1"/>'
            f'<text x="300" y="{top - size - 18:.0f}" fill="{gold}" font-family="Inter, sans-serif" font-size="19" letter-spacing="7" text-anchor="middle">{escape(meta["author"].upper())}</text>'
            f'<g fill="{ink}" font-family="\'Caslon Display\', Fraunces, Georgia, serif" text-anchor="middle">{title}</g>'
            f'<line x1="282" y1="{top + (len(lines) - 1) * size * 1.05 + 34:.0f}" x2="318" y2="{top + (len(lines) - 1) * size * 1.05 + 34:.0f}" stroke="{gold}" stroke-width="1"/>'
            f'<text x="300" y="790" fill="{ink}" opacity=".85" font-family="Fraunces, Georgia, serif" font-style="italic" font-size="19" text-anchor="middle">{escape(version(meta))}</text>'
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


def version(meta, edition=False):
    """«Traducción de …» o, para obras escritas en español, la edición."""
    text = f'Traducción de {meta["translator"]}' if meta.get("translator") else "Texto original en español"
    if edition and meta.get("edition"):
        text += f' ({meta["edition"]})'
    return text


def translator_schema(meta):
    return {"translator": {"@type": "Person", "name": meta["translator"]}} if meta.get("translator") else {}


def credit(meta):
    return (f'<p class="rights-note">Texto de dominio público. {escape(version(meta, edition=True))}. Transcripción de <a href="{escape(meta["source_url"])}">Wikisource</a>, '
            f'publicada bajo licencia <a href="{escape(meta["license_url"])}">{escape(meta["license"])}</a>. '
            f'División en capítulos, títulos y resúmenes: La Biblioteca Filosófica.{art_credit(meta)}</p>')


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
            kind = line[:2]
            if index in skip or kind not in ("P|", "V|", "S|"):
                continue
            text = re.sub(r"(\w)- ([a-záéíóúüñ])", r"\1\2", line[2:].replace("»>", "»"))  # guiones de fin de línea del OCR
            words += len(text.split())
            used += [int(n) for n in re.findall(r"\[\[(\d+)\]\]", text)]
            speaker = f'<strong>{escape(speakers[index])}.</strong> ' if index in speakers else ""
            css = {"V|": "verse", "S|": "stage-note"}.get(kind) or ("continued" if text[:1].islower() else "")
            attr = f' class="{css}"' if css else ""
            paragraphs.append(f"<p{attr}>{speaker}{with_note_links(text)}</p>")
        note_list = ""
        if used:
            items = "".join(f'<li id="nota-{n}" value="{n}">{escape(notes.get(n, ""))} <a href="#llamada-{n}" aria-label="Volver al texto">↩</a></li>'
                            for n in sorted(set(used)))
            note_list = f'<section class="reading-notes"><h2>Notas del traductor</h2><ol>{items}</ol></section>'
        rendered.append((chapter, "".join(paragraphs), note_list, words))

    total_words = sum(item[3] for item in rendered)
    crumbs_index = [("Inicio", "/"), ("Libros PDF Gratis", "/libros-pdf-gratis/"),
                    (meta["title"], meta["book_route"]), ("Leer online", base_route)]
    # Con ficha única, la ficha hace de índice: /leer/<slug>/ redirige a ella (vercel.json).
    single = bool(meta.get("ficha"))
    index_link = f'{meta["book_route"]}#leer' if single else base_route
    if single:
        routes.remove(base_route)

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
                  f'<figcaption><a href="{base_route}portada.jpg" download>Descargar portada</a></figcaption></figure>{meta["intro"]}'
                  f'<div class="continue-reading" data-continue-book="{escape(slug)}" hidden></div>'
                  f'<p class="actions"><a class="button" href="{start_reading}">Empezar a leer ↗</a>'
                  f'<a class="button secondary" href="{base_route}{slug}.pdf" download>Descargar PDF gratis ↓</a></p>'
                  f'<h2 id="capitulos">Capítulos</h2><ol class="chapter-list">{chapter_links}</ol>{credit(meta)}'
                  + (f'<p class="guide-link">Guía de lectura: <a href="{guide_route(meta)}">resumen de {escape(meta["title"])} por capítulos, personajes e ideas principales</a>.</p>' if meta.get("guide") else "") +
                  f'<p>¿Quieres orientarte antes de leer? Consulta la <a href="{meta["book_route"]}">ficha de {escape(meta["title"])}</a> '
                  f'y la guía <a href="/por-donde-empezar-a-leer-a-platon/">por dónde empezar a leer a Platón</a>.</p></div></article>')
    index_schema = {"@context": "https://schema.org", "@graph": [breadcrumb_schema(crumbs_index), {
        "@type": "Book", "name": meta["title"], "url": BASE + base_route, "inLanguage": "es",
        "isAccessibleForFree": True, "author": {"@type": "Person", "name": meta["author"]},
        **translator_schema(meta),
        "license": meta["license_url"],
        "hasPart": [{"@type": "Chapter", "name": c["title"], "position": i, "url": f'{BASE}{base_route}{c["slug"]}/'}
                    for i, c in enumerate(chapters, start=1)]}]}
    meta["_start_reading"] = start_reading
    covers = Path("build/portadas")
    covers.mkdir(parents=True, exist_ok=True)
    (covers / f"{slug}.svg").write_text(cover_svg(meta), encoding="utf-8")  # la lee portadas.mjs
    if single:
        stale = OUTPUT / base_route.strip("/") / "index.html"
        stale.unlink(missing_ok=True)
    else:
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
        pager += f'<a class="button secondary" href="{index_link}">Índice</a>'
        if following:
            pager += f'<a class="button" href="{base_route}{following["slug"]}/" rel="next">{escape(following["title"])} →</a>'
        pager += "</nav>"
        crumbs = crumbs_index[:-1] + ([] if single else [("Leer online", base_route)]) + [(chapter["title"], route)]
        body = (f'{TOOLBAR}<article class="reading reader-v2 reader-article" id="lectura">{breadcrumbs(crumbs)}'
                f'<a class="back-link" href="{index_link}">← {"Ficha" if single else "Índice"} de {escape(meta["title"])}</a>'
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
    write_print_edition(meta, rendered)
    publish_art(meta)
    if meta.get("guide"):
        routes.append(write_guide(meta, rendered, total_words, blocks))
    return routes


# Guía de la obra: resumen por capítulos, personajes, ideas, frases y preguntas.
# Se genera si el JSON trae la clave "guide". Ruta: /leer/<slug>/resumen/
def guide_route(meta):
    return f'/leer/{meta["slug"]}/resumen/'


def check_quotes(meta, blocks):
    """Cada frase de la guía tiene que estar literalmente en el capítulo que cita."""
    chapters = {c["slug"]: c for c in meta["chapters"]}
    for quote in meta["guide"].get("quotes", []):
        chapter = chapters[quote["chapter"]]
        text = " ".join(blocks[chapter["start"]:chapter["end"] + 1])
        if quote["text"] not in re.sub(r"\[\[\d+\]\]", "", text):
            raise SystemExit(f'Frase no encontrada en {meta["slug"]}/{quote["chapter"]}: {quote["text"][:60]}…')


def write_ficha(meta):
    """Ficha única del libro: PDF, lectura online, resumen, personajes, ideas y preguntas en una sola URL."""
    ficha, slug, route = meta["ficha"], meta["slug"], meta["book_route"]
    title, author = meta["title"], meta["author"]
    base = f"/leer/{slug}/"
    stats = meta["_stats"]
    crumbs = [("Inicio", "/"), ("Libros PDF Gratis", "/libros-pdf-gratis/")]
    if meta.get("author_route"):
        crumbs.append((author, meta["author_route"]))
    crumbs.append((title, route))
    resumen = "".join(f"<p>{escape(p)}</p>" for p in ficha["resumen"])
    people = "".join(f"<dt>{escape(n)}</dt><dd>{escape(d)}</dd>" for n, d in ficha["personajes"])
    people_toc = '<a href="#personajes">Personajes</a> · ' if people else ""
    people_html = f'<h2 id="personajes">Personajes</h2><dl class="guide-characters">{people}</dl>' if people else ""
    ideas = "".join(f"<li>{escape(i)}</li>" for i in ficha["ideas"])
    chapters = "".join(f'<li><a href="{base}{c["slug"]}/"><strong>{escape(c["title"])}</strong></a><p>{escape(c["summary"])}</p></li>'
                       for c in meta["chapters"])
    faq = "".join(f"<h3>{escape(q)}</h3><p>{escape(a)}</p>" for q, a in ficha["faq"])
    author_link = (f'<a href="{meta["author_route"]}">Más libros de {escape(author)}</a> · ' if meta.get("author_route") else "")
    body = (f'{TOOLBAR}<article class="reading reader-v2 reader-book guide book-ficha" id="lectura">{breadcrumbs(crumbs)}'
            f'<div class="book-detail"><figure class="featured"><img src="{base}portada-ficha.jpg" alt="Portada de {escape(title)}, de {escape(author)}" width="400" height="600"></figure>'
            f'<div><p class="eyebrow">Ficha de libro · {escape(author)}</p><h1>{escape(title)}, de {escape(author)}</h1>'
            f'<p class="book-context">{escape(ficha.get("genero", "Diálogo"))} sobre {escape(ficha["tema"])}. {stats["chapters"]} {ficha.get("unidad", "partes")} · {duration(stats["minutes"])} de lectura.</p>'
            f'<p class="access-badge"><span aria-hidden="true">●</span> Dominio público: lectura online y PDF gratis</p>'
            f'<div class="actions"><a class="button" href="{meta["_start_reading"]}">Leer online gratis ↗</a>'
            f'<a class="button secondary" href="{base}{slug}.pdf" download>Descargar PDF ↓</a></div>'
            f'<div class="save-controls"><button class="button save-book" type="button" data-save-route="{route}" aria-pressed="false" hidden>Guardar libro</button>'
            f'<a class="text-link" href="#resumen">{"Resumen y personajes" if people else "Resumen e ideas"} ↓</a></div>'
            f'<p class="save-message" role="status" aria-live="polite"></p></div></div>'
            f'<div class="entry" id="texto-obra"><div class="continue-reading" data-continue-book="{escape(slug)}" hidden></div>'
            f'<nav class="toc-inline" aria-label="En esta ficha"><a href="#resumen">Resumen</a> · {people_toc}'
            f'<a href="#ideas">Ideas principales</a> · <a href="#leer">Leer completo</a> · <a href="#preguntas">Preguntas</a></nav>'
            f'<h2 id="resumen">Resumen de {escape(title)}</h2>{resumen}'
            f'{people_html}'
            f'<h2 id="ideas">Ideas principales</h2><ul>{ideas}</ul>'
            f'<h2 id="leer">Leer {escape(title)} completo</h2>'
            f'<p>El texto íntegro, gratis y sin registro, en {stats["chapters"]} {ficha.get("unidad", "partes")}. También puedes '
            f'<a href="{base}{slug}.pdf" download>descargar {escape(title)} en PDF</a>.</p><ol class="chapter-list">{chapters}</ol>'
            f'<h2 id="preguntas">Preguntas frecuentes</h2>{faq}'
            f'<p class="guide-link">{author_link}<a href="/leer/">Más obras para leer online</a> · <a href="/resumenes/">Resúmenes</a></p>'
            f'{credit(meta)}</div></article>')
    schema = {"@context": "https://schema.org", "@graph": [breadcrumb_schema(crumbs), {
        "@type": "Book", "name": title, "url": BASE + route, "inLanguage": "es", "isAccessibleForFree": True,
        "author": {"@type": "Person", "name": author}, **translator_schema(meta),
        "image": f"{BASE}{base}portada-ficha.jpg", "license": meta["license_url"], "description": meta["description"],
        "workExample": {"@type": "Book", "bookFormat": "https://schema.org/EBook", "url": f'{BASE}{meta["_start_reading"]}'}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                            for q, a in ficha["faq"]]}]}
    document = shell(f"{title} de {author}: resumen, {'personajes' if people else 'ideas'} y PDF gratis · La Biblioteca Filosófica",
                     route, body, meta["description"], schema=schema)
    write(route, with_book_assets(document, meta))
    return route


def write_guide(meta, rendered, total_words, blocks):
    guide = meta["guide"]
    check_quotes(meta, blocks)
    slug, base_route, route = meta["slug"], f'/leer/{meta["slug"]}/', guide_route(meta)
    title, author = meta["title"], meta["author"]
    query = quote_plus(f"{title} {author}")
    crumbs = [("Inicio", "/"), ("Resúmenes", "/resumenes/"), (title, meta["book_route"]), ("Resumen", route)]
    sections = [("de-que-trata", f"De qué trata {title}"), ("resumen", "Resumen por capítulos"),
                ("personajes", "Personajes"), ("ideas", "Ideas principales"), ("frases", "Frases destacadas"),
                ("preguntas", "Preguntas frecuentes")]
    toc = "".join(f'<li><a href="#{anchor}">{escape(label)}</a></li>' for anchor, label in sections)
    chapters = "".join(
        f'<h3 id="cap-{c["slug"]}">{number}. {escape(c["title"])}</h3>'
        f'<p>{escape(guide.get("chapters", {}).get(c["slug"], c["summary"]))}</p>'
        f'<p class="guide-read"><a href="{base_route}{c["slug"]}/">Leer «{escape(c["title"])}» completo · {minutes(words)} min ↗</a></p>'
        for number, (c, _, _, words) in enumerate(rendered, start=1))
    characters = "".join(f'<dt>{escape(item["name"])}</dt><dd>{escape(item["text"])}</dd>' for item in guide["characters"])
    ideas = "".join(f'<h3>{escape(item["title"])}</h3><p>{escape(item["text"])}</p>' for item in guide["ideas"])
    titles = {c["slug"]: c["title"] for c in meta["chapters"]}
    quotes = "".join(
        f'<blockquote><p>«{"…" if q["text"][:1].islower() else ""}{escape(q["text"])}»</p><p class="quote-source">{escape(q.get("by", author))} · <cite><a href="{base_route}{q["chapter"]}/">{escape(titles[q["chapter"]])}</a></cite></p></blockquote>'
        for q in guide["quotes"])
    faq = "".join(f'<h3>{escape(item["q"])}</h3><p>{escape(item["a"])}</p>' for item in guide["faq"])
    speakers = {q.get("by", author) for q in guide["quotes"]}
    pages_file = TEXTS / "frases" / "paginas.json"
    quote_pages = [p for p in json.loads(pages_file.read_text(encoding="utf-8"))
                   if p.get("author") == author or p.get("by") in speakers] if pages_file.exists() else []
    if quote_pages:
        quotes += '<p class="guide-link">Más citas: ' + " · ".join(
            f'<a href="/frases/{p["slug"]}/">{escape(p["title"])}</a>' for p in quote_pages) + '.</p>'
    body = (f'{TOOLBAR}<article class="reading reader-v2 reader-article guide" id="lectura">{breadcrumbs(crumbs)}'
            f'<a class="back-link" href="{meta["book_route"]}">← Ficha del libro</a>'
            f'<header class="folio-article-head"><p class="eyebrow">Guía de lectura · {escape(author)}</p>'
            f'<h1>{escape(title)}: resumen, personajes y análisis</h1>'
            f'<div class="reading-meta"><span>{len(rendered)} capítulos · {minutes(total_words)} min para leer la obra completa</span>'
            f'<a href="#resumen">Ir al resumen ↓</a></div></header>'
            f'<div class="entry" id="texto-obra">'
            f'<aside class="quick-answer"><p class="eyebrow">Resumen breve</p><p>{escape(guide["short"])}</p>'
            f'<div class="quick-links"><a href="{base_route}">Leer {escape(title)} completo gratis ↗</a>'
            f'<a href="{base_route}{slug}.pdf" download>Descargar el PDF ↓</a>'
            f'<a href="https://www.amazon.es/s?k={query}&amp;i=stripbooks&amp;tag=labibliote044-21" rel="sponsored nofollow" data-query="{query}">Ver edición en papel ↗</a></div></aside>'
            f'<details class="toc" open><summary>En esta guía</summary><ol>{toc}</ol></details>'
            f'<h2 id="de-que-trata">De qué trata {escape(title)}</h2>{guide["intro"]}'
            f'<h2 id="resumen">Resumen por capítulos</h2>{chapters}'
            f'<h2 id="personajes">Personajes</h2><dl class="guide-characters">{characters}</dl>'
            f'<h2 id="ideas">Ideas principales</h2>{ideas}'
            f'<h2 id="frases">Frases destacadas</h2><p>Citas de la traducción de {escape(meta["translator"])}, con la ortografía de la edición original.</p>{quotes}'
            f'<h2 id="preguntas">Preguntas frecuentes</h2>{faq}'
            f'<p class="actions"><a class="button" href="{base_route}">Leer la obra completa ↗</a>'
            f'<a class="button secondary" href="{base_route}{slug}.pdf" download>Descargar PDF gratis ↓</a></p>'
            f'<p class="reading-credit">Guía escrita por La Biblioteca Filosófica. Las citas proceden de la traducción de {escape(meta["translator"])} '
            f'({escape(meta["edition"])}), transcrita en <a href="{escape(meta["source_url"])}">Wikisource</a> '
            f'(<a href="{escape(meta["license_url"])}">{escape(meta["license"])}</a>).</p></div></article>')
    schema = {"@context": "https://schema.org", "@graph": [breadcrumb_schema(crumbs), {
        "@type": "Article", "headline": f"{title}: resumen, personajes y análisis", "url": BASE + route, "inLanguage": "es",
        "author": {"@type": "Organization", "name": "La Biblioteca Filosófica", "url": BASE + "/"},
        "image": f'{BASE}/leer/{slug}/social.jpg',
        "about": {"@type": "Book", "name": title, "author": {"@type": "Person", "name": author}, "url": BASE + base_route}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": item["q"],
                                              "acceptedAnswer": {"@type": "Answer", "text": item["a"]}} for item in guide["faq"]]}]}
    page = shell(guide.get("seo_title", f"{title} de {author}: resumen por capítulos, personajes y análisis") + " · La Biblioteca Filosófica",
                 route, body, guide["description"], schema=schema)
    image = f'{BASE}/leer/{slug}/social.jpg'
    social = (f'<meta property="og:type" content="article"><meta property="og:site_name" content="La Biblioteca Filosófica">'
              f'<meta property="og:image" content="{image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
              f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{image}">'
              '<link rel="stylesheet" href="/lector-libro.css"></head>')
    write(route, page.replace("</head>", social, 1))
    return route


# Páginas de frases (/frases/<slug>/) a partir de las citas comprobadas de las guías.
# textos/frases/paginas.json define cada página: por personaje («by») o por autor de la obra («author»).
QUOTES = Path("build/frases.json")


QUOTE_PAGES = []


def quote_id(meta, quote):
    return f'{meta["slug"]}-{hashlib.md5(quote["text"].encode("utf-8")).hexdigest()[:8]}'


def write_quote_pages(metas):
    config = TEXTS / "frases" / "paginas.json"
    if not config.exists():
        return []
    cards, routes = {}, []
    for page in json.loads(config.read_text(encoding="utf-8")):
        route = f'/frases/{page["slug"]}/'
        groups = []
        for meta in metas:
            if not meta.get("guide") or (page.get("author") and meta["author"] != page["author"]):
                continue
            titles = {c["slug"]: c["title"] for c in meta["chapters"]}
            chosen = [q for q in meta["guide"]["quotes"] if not page.get("by") or q.get("by") == page["by"]]
            if chosen:
                groups.append((meta, titles, chosen))
        total = sum(len(chosen) for _, _, chosen in groups)
        if not total:
            continue
        sections, first_image = "", None
        for meta, titles, chosen in groups:
            base_route = f'/leer/{meta["slug"]}/'
            sections += f'<h2 id="{meta["slug"]}">En {escape(meta["title"])}</h2>'
            for quote in chosen:
                qid = quote_id(meta, quote)
                image = f"/frases/img/{qid}.jpg"
                first_image = first_image or image
                color = COVER_COLORS.get(meta.get("cover", {}).get("color"), COVER_COLORS["verde"])
                cards[qid] = {"id": qid, "text": ("…" if quote["text"][:1].islower() else "") + quote["text"],
                              "by": quote.get("by", meta["author"]), "work": meta["title"], "color": color}
                speaker = "" if page.get("by") else f'{escape(quote.get("by", meta["author"]))}, '
                sections += (f'<div class="quote-card" id="{qid}"><blockquote><p>«{"…" if quote["text"][:1].islower() else ""}{escape(quote["text"])}»</p></blockquote>'
                             f'<p class="quote-meta">{speaker}<cite>{escape(meta["title"])}</cite> · {escape(titles[quote["chapter"]])}</p>'
                             f'<p class="quote-actions"><a href="{base_route}{quote["chapter"]}/">Leer en su contexto ↗</a>'
                             f'<a href="{image}" download>Descargar imagen ↓</a></p></div>')
            sections += (f'<p class="guide-link">Más sobre esta obra: <a href="{base_route}resumen/">resumen de {escape(meta["title"])}</a> · '
                         f'<a href="{base_route}">leer {escape(meta["title"])} completo gratis</a>.</p>')
        crumbs = [("Inicio", "/"), ("Frases", "/frases/"), (page["title"], route)]
        related = " · ".join(f'<a href="{href}">{escape(label)}</a>' for href, label in page.get("related", []))
        faq = "".join(f'<h3>{escape(item["q"])}</h3><p>{escape(item["a"])}</p>' for item in page.get("faq", []))
        body = (f'{TOOLBAR}<article class="reading reader-v2 reader-article guide quotes-page" id="lectura">{breadcrumbs(crumbs)}'
                f'<header class="folio-article-head"><p class="eyebrow">Citas comprobadas · {total} frases</p>'
                f'<h1>{escape(page["title"])}</h1>'
                f'<div class="reading-meta"><span>Con la obra y el capítulo de cada cita</span><a href="#frases">Ver las frases ↓</a></div></header>'
                f'<div class="entry" id="texto-obra">{page["intro"]}<div id="frases">{sections}</div>'
                + (f'<h2 id="preguntas">Preguntas frecuentes</h2>{faq}' if faq else "")
                + (f'<p class="guide-link">Sigue leyendo: {related}</p>' if related else "")
                + '<p class="reading-credit">Citas de la traducción de Patricio de Azcárate (Obras completas de Platón, Madrid, 1871), '
                  'transcrita en Wikisource (CC BY-SA 4.0). Se respeta la ortografía de la edición original. '
                  'Las imágenes pueden compartirse libremente citando la fuente.</p></div></article>')
        schema = {"@context": "https://schema.org", "@graph": [breadcrumb_schema(crumbs), {
            "@type": "Article", "headline": page["title"], "url": BASE + route, "inLanguage": "es",
            "author": {"@type": "Organization", "name": "La Biblioteca Filosófica", "url": BASE + "/"},
            "image": BASE + first_image}] + ([{"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
                for item in page["faq"]]}] if page.get("faq") else [])}
        document = shell(page["seo_title"] + " · La Biblioteca Filosófica", route, body, page["description"], schema=schema)
        social = (f'<meta property="og:type" content="article"><meta property="og:image" content="{BASE}{first_image}">'
                  f'<meta property="og:image:width" content="1080"><meta property="og:image:height" content="1080">'
                  f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}{first_image}">'
                  '<link rel="stylesheet" href="/lector-libro.css"></head>')
        write(route, document.replace("</head>", social, 1))
        routes.append(route)
        QUOTE_PAGES.append({"slug": page["slug"], "title": page["title"], "description": page["description"],
                            "count": total, "image": first_image})
    QUOTES.parent.mkdir(exist_ok=True)
    QUOTES.write_text(json.dumps(list(cards.values()), ensure_ascii=False, indent=1), encoding="utf-8")
    return routes


def hub_page(route, crumb, eyebrow, title, seo_title, description, intro, items, extra=""):
    """Índice de una sección del menú (/leer/, /resumenes/, /frases/): crece solo al añadir obras."""
    crumbs = [("Inicio", "/"), (crumb, route)]
    cards = "".join(
        f'<li><a href="{href}">' + (f'<img src="{image}" alt="" width="{w}" height="{h}" loading="lazy">' if image else "")
        + f'<span><span class="hub-kicker">{escape(kicker)}</span><strong>{escape(name)}</strong><span class="hub-text">{escape(text)}</span>'
          f'<span class="hub-cta">{cta} ↗</span></span></a></li>'
        for href, image, w, h, kicker, name, text, cta in items)
    body = (f'{TOOLBAR}<article class="reading reader-v2 reader-article guide hub-page" id="lectura">{breadcrumbs(crumbs)}'
            f'<header class="folio-article-head"><p class="eyebrow">{eyebrow}</p><h1>{escape(title)}</h1></header>'
            f'<div class="entry" id="texto-obra">{intro}<ul class="hub-list">{cards}</ul>{extra}</div></article>')
    schema = {"@context": "https://schema.org", "@graph": [breadcrumb_schema(crumbs), {
        "@type": "CollectionPage", "name": title, "url": BASE + route, "inLanguage": "es", "description": description,
        "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": BASE + item[0], "name": item[5]} for i, item in enumerate(items)]}}]}
    document = shell(seo_title + " · La Biblioteca Filosófica", route, body, description, schema=schema)
    write(route, document.replace("</head>", '<link rel="stylesheet" href="/lector-libro.css"></head>', 1))
    return route


def write_hubs(metas):
    reading = [(m["book_route"] if m.get("ficha") else f'/leer/{m["slug"]}/', f'/leer/{m["slug"]}/portada-ficha.jpg', 400, 600, m["author"], m["title"],
                f'{m["_stats"]["chapters"]} capítulos · {duration(m["_stats"]["minutes"])} de lectura', "Leer gratis") for m in metas]
    guides = [(f'/leer/{m["slug"]}/resumen/', f'/leer/{m["slug"]}/portada-ficha.jpg', 400, 600, m["author"], m["title"],
               m["guide"]["short"], "Ver resumen y personajes") if m.get("guide") else
              (f'{m["book_route"]}#resumen', f'/leer/{m["slug"]}/portada-ficha.jpg', 400, 600, m["author"], m["title"],
               m["ficha"]["resumen"][0], "Ver resumen y personajes")
              for m in metas if m.get("guide") or m.get("ficha")]
    routes = [
        hub_page("/leer/", "Leer gratis", f"Lectura completa · {len(reading)} obras", "Libros de filosofía y literatura clásica para leer online gratis",
                 "Leer libros de filosofía y clásicos online gratis y completos",
                 "Obras completas de filosofía y literatura clásica para leer online gratis y sin registro: textos de dominio público divididos en capítulos, con notas y marcapáginas.",
                 "<p>Obras completas de dominio público para leer aquí mismo, sin descargar nada ni registrarte. Cada libro está dividido en capítulos, "
                 "conserva las notas de la edición y recuerda en tu navegador dónde lo dejaste. También puedes descargar cada obra en PDF.</p>",
                 reading, '<p class="guide-link">¿Prefieres empezar por lo esencial? <a href="/resumenes/">Resúmenes y guías de lectura</a> · '
                          '<a href="/frases/">Frases célebres con su fuente</a>.</p>'),
    ]
    if guides:
        routes.append(hub_page("/resumenes/", "Resúmenes", f"Guías de lectura · {len(guides)} obras", "Resúmenes de libros de filosofía",
                               "Resúmenes de libros de filosofía por capítulos",
                               "Resúmenes de obras de filosofía por capítulos, con sus personajes, las ideas principales y citas comprobadas en el texto original. Gratis y con enlace a la obra completa.",
                               "<p>Guías para entender cada obra antes, durante o después de leerla: de qué trata, un resumen capítulo a capítulo, "
                               "sus personajes, las ideas principales y citas comprobadas en el texto. Desde cada capítulo puedes saltar a la lectura completa.</p>",
                               guides, '<p class="guide-link">Sigue con: <a href="/leer/">todas las obras para leer online</a> · <a href="/frases/">frases célebres</a>.</p>'))
    if QUOTE_PAGES:
        items = [(f'/frases/{p["slug"]}/', p["image"], 1080, 1080, f'{p["count"]} frases', p["title"], p["description"], "Ver las frases") for p in QUOTE_PAGES]
        routes.append(hub_page("/frases/", "Frases", "Citas comprobadas · con su fuente", "Frases célebres de filósofos",
                               "Frases célebres de filósofos con su fuente",
                               "Frases célebres de filósofos citadas de sus obras, con el libro y el capítulo de cada cita y una imagen para compartir.",
                               "<p>Cada frase está copiada de la obra original, con el libro y el capítulo donde aparece, para que puedas leerla en su contexto. "
                               "Todas tienen una imagen lista para compartir.</p>",
                               items, '<p class="guide-link">Sigue con: <a href="/resumenes/">resúmenes de las obras</a> · <a href="/leer/">leer las obras completas gratis</a>.</p>'))
    return routes


PRINT = Path("build/impresion")


def publish_art(meta):
    art = meta.get("cover", {}).get("art")
    if art:
        target = OUTPUT / art["url"].lstrip("/")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ART / art["file"]).read_bytes())


def art_credit(meta):
    art = meta.get("cover", {}).get("art")
    return f' Portada: {escape(art["credit"])}' if art and art.get("credit") else ""


def write_print_edition(meta, rendered):
    """HTML para imprimir el PDF de la colección (lo convierte portadas.mjs)."""
    slug = meta["slug"]
    site = f"{BASE}/leer/{slug}/"
    ficha = BASE + meta["book_route"]
    contents = "".join(f'<li><a href="#cap-{n}">{escape(chapter["title"])}</a></li>' for n, (chapter, *_rest) in enumerate(rendered, start=1))
    chapters = "".join(
        f'<section class="chapter" id="cap-{n}"><p class="chapter-number">{n:02d}</p><h2>{escape(chapter["title"])}</h2>'
        f'<p class="summary">{escape(chapter["summary"])}</p>{paragraphs}{notes.replace("Notas del traductor", "Notas")}</section>'
        for n, (chapter, paragraphs, notes, _) in enumerate(rendered, start=1))
    first_paragraph = re.search(r"<p>.*?</p>", meta["intro"], re.S)
    document = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{escape(meta["title"])} · {escape(meta["author"])}</title>
<meta name="author" content="{escape(meta["author"])}"><link rel="stylesheet" href="../../impresion.css"></head><body>
<section class="cover" style="background:{COVER_COLORS.get(meta.get("cover", {}).get("color", "verde"), "#143a2c")}">{cover_svg(meta, inline=True)}</section>
<section class="title-page"><p class="series">La Biblioteca Filosófica · Lectura completa</p><p class="author">{escape(meta["author"])}</p>
<h1>{escape(meta["title"])}</h1><p class="translator">{escape(version(meta))}</p></section>
<section class="credits"><p>{escape(meta["title"])}, de {escape(meta["author"])}. {escape(version(meta, edition=True))}.
Texto de dominio público.</p><p>Transcripción de <a href="{escape(meta["source_url"])}">Wikisource</a>, publicada bajo licencia
<a href="{escape(meta["license_url"])}">{escape(meta["license"])}</a>. Esta edición, con su división en capítulos, títulos y resúmenes,
se publica bajo la misma licencia.{art_credit(meta)}</p><p>Edición de La Biblioteca Filosófica. Léela también online, con marcapáginas, en
<a href="{site}">{site.replace("https://", "")}</a>.</p></section>
<section class="about"><h2>Sobre esta obra</h2>{first_paragraph[0] if first_paragraph else ""}
<p>Se respeta la ortografía de la edición original, por eso verás «á» como preposición o «ménos» con tilde.</p>
<h2>Índice</h2><ol class="contents">{contents}</ol></section>
{chapters}
<section class="colophon"><p class="series">La Biblioteca Filosófica</p><h2>Sigue leyendo</h2>
<p>Encontrarás el análisis de la obra, otras lecturas de {escape(meta["author"])} y más libros completos gratis en
<a href="{ficha}">labibliotecafilosofica.com</a>.</p><p><a href="{BASE}/libros-pdf-gratis/">Biblioteca de libros gratis ↗</a><br>
<a href="{BASE}/rutas/introduccion-a-la-filosofia/">Una ruta para empezar en filosofía ↗</a></p></section>
</body></html>"""
    PRINT.mkdir(parents=True, exist_ok=True)
    (PRINT / f"{slug}.html").write_text(document, encoding="utf-8")


def duration(total):
    hours, rest = divmod(total, 60)
    return f"{hours} h {rest:02d} min" if hours else f"{rest} min"


def update_home(metas):
    """Estante «Leer online gratis» en la portada, entre el buscador y la selección."""
    home = OUTPUT / "index.html"
    document = home.read_text(encoding="utf-8")
    cards = "".join(
        f'<li><a href="{escape(m["book_route"] if m.get("ficha") else "/leer/" + m["slug"] + "/")}"><img src="/leer/{escape(m["slug"])}/portada-ficha.jpg" '
        f'alt="Portada de {escape(m["title"])}, de {escape(m["author"])}" width="400" height="600" loading="lazy">'
        f'<span class="online-shelf-author">{escape(m["author"])}</span><strong>{escape(m["title"])}</strong>'
        f'<span class="online-shelf-meta">{m["_stats"]["chapters"]} capítulos · {duration(m["_stats"]["minutes"])}</span>'
        f'<span class="online-shelf-cta">Leer ahora ↗</span></a></li>' for m in metas[:8])
    section = ('<!--lectura-completa--><section class="online-shelf" id="leer-online"><div class="online-shelf-intro">'
               '<p class="eyebrow">Lectura completa · gratis y sin registro</p><h2>Lee las obras completas aquí, página a página.</h2>'
               '<p>Textos de dominio público en traducciones clásicas, con modo libro, notas y un marcapáginas que recuerda dónde lo dejaste.</p>'
               '<p class="online-shelf-links"><a href="/leer/">Todas las obras ↗</a><a href="/resumenes/">Resúmenes y guías ↗</a><a href="/frases/">Frases célebres ↗</a></p></div>'
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


def update_redirects(metas):
    """/leer/<slug>/ → ficha, para los libros con ficha única."""
    config = PROJECT / "vercel.json"
    data = json.loads(config.read_text(encoding="utf-8"))
    rules = [r for r in data["redirects"] if not re.fullmatch(r"/leer/[^/]+/", r["source"])]
    rules += [{"source": f'/leer/{m["slug"]}/', "destination": m["book_route"], "permanent": True}
              for m in metas if m.get("ficha")]
    data["redirects"] = rules
    config.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sitemap = OUTPUT / "sitemap.xml"
    content = sitemap.read_text(encoding="utf-8")
    for m in metas:
        if m.get("ficha"):
            content = content.replace(f'<url><loc>{BASE}/leer/{m["slug"]}/</loc></url>\n', "")
    sitemap.write_text(content, encoding="utf-8")


def main():
    routes, metas = [], []
    for config in sorted(TEXTS.glob("*.json")):
        meta = json.loads(config.read_text(encoding="utf-8"))
        blocks = (TEXTS / f'{meta["slug"]}.txt').read_text(encoding="utf-8").split("\n")
        routes += build(meta, blocks)
        if meta.get("ficha"):
            routes.append(write_ficha(meta))
        metas.append(meta)
    ordered = sorted(metas, key=lambda m: m.get("cover", {}).get("number", 99))
    routes += write_quote_pages(ordered)
    routes += write_hubs(ordered)
    update_sitemap(routes)
    update_redirects(metas)
    update_home(sorted(metas, key=lambda m: m.get("cover", {}).get("number", 99)))
    print(f"{len(routes)} páginas de lectura generadas")


if __name__ == "__main__":
    main()
