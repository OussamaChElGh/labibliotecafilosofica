"""Limpieza editorial de las páginas ya generadas en public/.

Se ejecuta después de migrate.py y lectura_completa.py:  python pulir.py
Es idempotente: se puede ejecutar varias veces sin cambiar el resultado.

Quita los restos del WordPress que el exportador arrastra dentro del texto:
- el bloque de donación («Ayuda a nuestra Biblioteca… Donar»),
- el widget «¿quieres conocer más libros de…?» con fichas copiadas,
- el bloque de descarga de Elementor repetido al final de las fichas,
- párrafos vacíos y títulos sin texto debajo.

Además, en las obras con lectura completa pone la portada de la colección y,
en todo el sitio, quita «[PDF]» del texto visible (no del <title>).
"""
import json
import re
from pathlib import Path

from lxml import html as dom

OUTPUT = Path("public")
TEXTS = Path("textos")
# Mismos colores que COVER_COLORS en lectura_completa.py.
SPINES = {"verde": "#143a2c", "burdeos": "#4a1820", "azul": "#16233b", "ocre": "#4f3615", "negro": "#161015"}
START = '<div class="entry" id="texto-obra">'
END_MARKERS = ('<div class="terms">', '<section class="related">', '<a class="button secondary" href="#lectura">')
LEGACY_HEADING = re.compile(r"quieres conocer más (libros|colecciones)", re.I)
DONATION = re.compile(r"ayuda a nuestra biblioteca de filosof|ayúdanos a seguir con una donación", re.I)
HEADINGS = ("h2", "h3", "h4")


def text(node):
    return " ".join(node.text_content().split())


def is_empty(node):
    if node.tag != "p":
        return False
    if node.xpath(".//img|.//a|.//iframe|.//video"):
        return False
    return not text(node)


def drop(node):
    """Quita el nodo conservando el texto que le sigue (tail)."""
    parent = node.getparent()
    if parent is not None:
        node.drop_tree()


def truncate_legacy(root):
    """Desde el widget de «más libros» o la donación hasta el final, todo es plantilla."""
    for node in list(root):
        legacy = node.tag in HEADINGS and LEGACY_HEADING.search(text(node))
        if legacy or (node.tag in HEADINGS + ("p", "div") and DONATION.search(text(node))):
            following = list(node.itersiblings())
            for item in following:
                item.drop_tree()
            node.drop_tree()
            # El texto suelto «Donar» queda como tail del último nodo.
            last = root[-1] if len(root) else None
            if last is not None:
                last.tail = None
            else:
                root.text = None
            return True
    return False


def clean_downloads(root, header):
    """El bloque de descarga de Elementor: imagen decorativa, saltos de línea y «Descargar»."""
    for link in root.xpath('.//a[contains(concat(" ", normalize-space(@class), " "), " download-action ")]'):
        block = link
        while block.getparent() is not None and block.getparent() is not root:
            block = block.getparent()
        href = link.get("href", "")
        if href and f'href="{href}"' in header:
            for img in block.xpath('preceding-sibling::*[1][self::img][contains(@src, "left-side-figs")]'):
                img.drop_tree()
            block.drop_tree()
            continue
        for img in link.xpath('preceding-sibling::img[contains(@src, "left-side-figs")]|ancestor::p//img[contains(@src, "left-side-figs")]'):
            img.drop_tree()
        if "button" not in (link.get("class") or "").split() and text(link).lower() == "descargar":
            for br in link.xpath(".//br"):
                br.drop_tree()
            label = text(link) or "Descargar"
            for child in list(link):
                child.drop_tree()
            link.text = "Descargar PDF ↗" if label.lower() == "descargar" else label
            link.set("class", "button download-action")
            if block.tag == "p":
                for br in block.xpath("./br"):
                    br.drop_tree()
                block.text = None
                block.set("class", "download-cta")


def drop_empty(root):
    for node in list(root):
        if is_empty(node):
            node.drop_tree()


def drop_empty_headings(root):
    """Un título seguido directamente de otro del mismo nivel o superior no tiene texto."""
    removed = []
    changed = True
    while changed:
        changed = False
        nodes = list(root)
        for index, node in enumerate(nodes):
            if node.tag not in HEADINGS:
                continue
            following = nodes[index + 1] if index + 1 < len(nodes) else None
            empty = following is None or (following.tag in HEADINGS and following.tag <= node.tag)
            if empty:
                if node.get("id"):
                    removed.append(node.get("id"))
                node.drop_tree()
                changed = True
                break
    return removed


def fix_toc(document, remaining):
    match = re.search(r'<details class="toc"><summary>En esta lectura <span>\d+ secciones</span></summary><ol>(.*?)</ol></details>', document, flags=re.S)
    if not match:
        return document
    items = re.findall(r'<li><a href="#([^"]+)">.*?</a></li>', match.group(1), flags=re.S)
    kept = [li for li in re.findall(r'<li><a href="#[^"]+">.*?</a></li>', match.group(1), flags=re.S)
            if re.search(r'href="#([^"]+)"', li).group(1) in remaining]
    if len(kept) == len(items):
        return document
    toc = "" if len(kept) < 3 else (f'<details class="toc"><summary>En esta lectura <span>{len(kept)} secciones</span></summary>'
                                   f'<ol>{"".join(kept)}</ol></details>')
    return document[:match.start()] + toc + document[match.end():]


def polish(document):
    start = document.find(START)
    if start < 0:
        return document
    body_start = start + len(START)
    ends = [document.find(marker, body_start) for marker in END_MARKERS]
    ends = [e for e in ends if e >= 0]
    if not ends:
        return document
    close = document.rfind("</div>", body_start, min(ends))
    markup = document[body_start:close]
    # Shortcodes [caption] que el exportador dejó como texto.
    markup = re.sub(r"\[caption[^\]]*\]\s*(<img[^>]*>)\s*(.*?)\s*\[/caption\]",
                    lambda m: f'<figure class="wp-caption">{m[1]}<figcaption>{m[2].strip()}</figcaption></figure>' if m[2].strip() else f"<figure>{m[1]}</figure>",
                    markup, flags=re.S)
    markup = re.sub(r"\[/?caption[^\]]*\]", "", markup)
    root = dom.fragment_fromstring(markup, create_parent="div")
    truncate_legacy(root)
    clean_downloads(root, document[:start])
    # Imagen decorativa de Elementor que acompañaba a los botones de descarga.
    for img in root.xpath('.//img[contains(@src, "/elementor/thumbs/left-side-figs")]'):
        holder = img.getparent()
        if holder is not root and holder.tag in ("figure", "p") and len(holder) == 1 and not text(holder):
            holder.drop_tree()
        else:
            img.drop_tree()
    drop_empty(root)
    drop_empty_headings(root)
    lead = root.text or ""
    cleaned = lead + "".join(dom.tostring(node, encoding="unicode") for node in root)
    remaining = set(root.xpath(".//@id"))
    document = document[:body_start] + cleaned + document[close:]
    return fix_toc(document, remaining)


def strip_pdf_label(document):
    """«[PDF]» se queda en el título de Google (<title>), pero no en el texto visible."""
    head_end = document.find("</head>")
    if head_end < 0:
        return document
    body = re.sub(r"\s*\[PDF\]", "", document[head_end:])
    body = re.sub(r"<h1>(.*?)</h1>", lambda m: "<h1>" + " ".join(m[1].split()) + "</h1>", body, flags=re.S)
    return document[:head_end] + body


STOP = {"pdf", "libros", "libro", "gratis", "de", "la", "el", "los", "las", "y", "en", "del", "a", "o", "un", "una",
        "para", "que", "por", "con", "online", "epub", "filosofia", "sobre", "al", "es", "lo", "se", "mas", "leer"}
# Etiquetas y secciones que comparten casi todas las páginas: no dicen nada del tema.
GENERIC = re.compile(r"^/(tag/libros-pdf[^/]*|libros-pdf-gratis|articulos|historia|biografias|libros-gratis-en-online)/$")
RELATED = re.compile(r'<section class="related"><h2>Sigue explorando</h2><ul class="cards">.*?</ul></section>', re.S)


def route_of(page):
    parts = page.parent.relative_to(OUTPUT).parts
    return "/" + "/".join(parts) + "/" if parts else "/"


def tokens(route):
    return {t for t in re.split(r"[-/]", route.lower()) if len(t) > 2 and t not in STOP and not t.isdigit()}


def related_index(pages):
    """Páginas candidatas a «Sigue explorando», con sus etiquetas y palabras clave."""
    entries = {}
    for page, document in pages.items():
        if not RELATED.search(document):
            continue
        route = route_of(page)
        h1 = re.search(r"<h1>(.*?)</h1>", document, re.S)
        terms = re.search(r'<div class="terms">(.*?)</div>', document, re.S)
        entries[route] = {
            "title": " ".join(re.sub(r"<[^>]+>", "", h1[1]).split()) if h1 else route,
            "book": "reader-book" in document,
            "terms": {t for t in re.findall(r'href="([^"]+)"', terms[1]) if not GENERIC.search(t)} if terms else set(),
            "tokens": tokens(route),
            "length": len(document),
        }
    # Las lecturas completas también son candidatas, ligadas a su ficha.
    for config in sorted(TEXTS.glob("*.json")):
        meta = json.loads(config.read_text(encoding="utf-8"))
        ficha = entries.get(meta["book_route"])
        if ficha:
            entries[f'/leer/{meta["slug"]}/'] = {
                "title": f'Leer online gratis: {meta["title"]}, de {meta["author"]}', "book": True, "online": True,
                "terms": set(ficha["terms"]), "tokens": tokens(meta["book_route"]) | tokens(meta["slug"]),
                "ficha": meta["book_route"], "length": ficha["length"]}
    # Autores: una ficha enlazada desde la página de un autor comparte ese autor.
    for page, document in pages.items():
        route = route_of(page)
        if re.fullmatch(r"/libros-pdf-gratis/autores/[^/]+/", route):
            for link in set(re.findall(r'href="(/[^"#]+/)"', document)):
                if link in entries:
                    entries[link]["terms"].add(route)
    frequency = {}
    for entry in entries.values():
        for key in entry["terms"] | {"t:" + t for t in entry["tokens"]}:
            frequency[key] = frequency.get(key, 0) + 1
    return entries, frequency


def suggestions(route, entries, frequency, size=3):
    import math
    me = entries[route]
    total = len(entries)
    weight = lambda key: math.log(total / frequency.get(key, total)) if frequency.get(key) else 0
    mine = me["terms"] | {"t:" + t for t in me["tokens"]}
    scored = []
    for other, entry in entries.items():
        if other == route or entry.get("ficha") == route or me.get("ficha") == other:
            continue
        shared = mine & (entry["terms"] | {"t:" + t for t in entry["tokens"]})
        score = sum(weight(key) * (2 if "/autores/" in key else 1) for key in shared)
        if score <= 0.5:
            continue
        if entry["book"] == me["book"]:
            score += 0.5
        if entry.get("online"):
            score += 1.5
        scored.append((round(score, 3), entry["length"], other))
    # A igual parecido, primero las páginas con más contenido.
    scored.sort(key=lambda item: (-item[0], -item[1], item[2]))
    picks = [other for _, _, other in scored]
    # Si hay una lectura completa del mismo autor, ocupa siempre el primer hueco.
    online = [other for score, _, other in scored if entries[other].get("online") and score >= 2.5]
    if online:
        picks = online[:1] + [other for other in picks if other != online[0]]
    return picks[:size]


def render_related(document, picks, entries):
    if len(picks) < 2:
        return document
    items = "".join(f'<li><a href="{other}">{entries[other]["title"]}</a></li>' for other in picks)
    return RELATED.sub(lambda _: f'<section class="related"><h2>Sigue explorando</h2><ul class="cards">{items}</ul></section>', document, count=1)


def collection_covers():
    """Obras con lectura completa: su portada de la colección sustituye a la imagen antigua.

    Devuelve {imagen antigua: (portada nueva, texto alternativo)} y {portada nueva: color del lomo}.
    """
    swaps, spines = {}, {}
    for config in sorted(TEXTS.glob("*.json")):
        meta = json.loads(config.read_text(encoding="utf-8"))
        ficha = OUTPUT / meta["book_route"].strip("/") / "index.html"
        if not ficha.exists():
            continue
        found = re.search(r'<div class="book-detail"><figure class="featured"><img[^>]*?src="([^"]+)"', ficha.read_text(encoding="utf-8"))
        new = f'/leer/{meta["slug"]}/portada-ficha.jpg'
        spines[new] = SPINES.get(meta.get("cover", {}).get("color", "verde"))
        if found and found[1] != new:
            swaps[found[1]] = (new, f'Portada de {meta["title"]}, de {meta["author"]}')
    return swaps, spines


def swap_covers(document, swaps):
    for old, (new, alt) in swaps.items():
        def replace(match):
            tag = re.sub(r'\s(srcset|sizes)="[^"]*"', "", match[0]).replace(f'src="{old}"', f'src="{new}"')
            tag = re.sub(r'\swidth="\d+"\s+height="\d+"', ' width="400" height="600"', tag)
            return re.sub(r'alt="[^"]*"', f'alt="{alt}"', tag)
        document = re.sub(r'<img[^>]*?src="' + re.escape(old) + r'"[^>]*>', replace, document)
    return document


def main():
    swaps, spines = collection_covers()
    books = OUTPUT / "folio-books.json"
    if books.exists() and spines:
        catalog = json.loads(books.read_text(encoding="utf-8"))
        for item in catalog:
            if item.get("source") in swaps:
                item["cover"] = item["source"] = swaps[item["source"]][0]
            if item.get("source") in spines:
                item["spineColor"] = spines[item["source"]]
        books.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    changed = 0
    originals, pages = {}, {}
    for page in sorted(OUTPUT.rglob("index.html")):
        original = page.read_text(encoding="utf-8")
        result = strip_pdf_label(swap_covers(polish(original), swaps))
        for _ in range(3):  # Quitar un bloque puede dejar otro vacío: repetir hasta que no cambie.
            again = polish(result)
            if again == result:
                break
            result = again
        originals[page], pages[page] = original, result
    # «Sigue explorando»: obras del mismo autor o tema, no las tres primeras de la categoría.
    entries, frequency = related_index(pages)
    for page, document in pages.items():
        route = route_of(page)
        if route in entries:
            pages[page] = render_related(document, suggestions(route, entries, frequency), entries)
    for page, result in pages.items():
        if result != originals[page]:
            page.write_text(result, encoding="utf-8")
            changed += 1
    print(f"{changed} páginas pulidas")


if __name__ == "__main__":
    main()
