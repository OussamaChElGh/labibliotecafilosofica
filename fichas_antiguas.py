"""Pasa las fichas heredadas de WordPress al formato de ficha única de libro.

python fichas_antiguas.py  (después de pulir.py)

Para cada ruta con datos en textos/fichas/antiguas/*.py añade a la página que ya existe
resumen, personajes, ideas principales, preguntas frecuentes (con su FAQPage) y un
título y un h1 más claros. Se conserva todo el contenido anterior bajo «Sobre la obra»,
así que la URL no pierde nada de lo que ya posiciona. Es idempotente.
"""
import html
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
DATA = ROOT / "textos" / "fichas" / "antiguas"
BASE = "https://labibliotecafilosofica.com"
MARK = "data-ficha-v2"


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


def crumbs_html(items):
    lis = "".join(f'<li><a href="{href}">{esc(name)}</a></li>' for name, href in items[:-1])
    return (f'<nav class="crumbs" aria-label="Ruta de navegación"><ol>{lis}'
            f'<li aria-current="page">{esc(items[-1][0])}</li></ol></nav>')


def upgrade(route, data, document):
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
            [("ideas", "Ideas principales"), ("sobre-la-obra", "Sobre la obra"), ("preguntas", "Preguntas")]
    toc = " · ".join(f'<a href="#{i}">{t}</a>' for i, t in links)
    resumen = "".join(f"<p>{esc(p)}</p>" for p in data["resumen"])
    people = ("<h2 id=\"personajes\">Personajes</h2><dl class=\"guide-characters\">" +
              "".join(f"<dt>{esc(n)}</dt><dd>{esc(d)}</dd>" for n, d in data["personajes"]) + "</dl>") if has_people else ""
    ideas = "".join(f"<li>{esc(i)}</li>" for i in data["ideas"])
    top = (f'<!--ficha-v2--><nav class="toc-inline" aria-label="En esta ficha">{toc}</nav>'
           f'<h2 id="resumen">Resumen de {esc(title)}</h2>{resumen}{people}'
           f'<h2 id="ideas">Ideas principales</h2><ul>{ideas}</ul>'
           f'<h2 id="sobre-la-obra">Sobre la obra</h2><!--/ficha-v2-->')
    document = document.replace('<div class="entry" id="texto-obra">', '<div class="entry" id="texto-obra">' + top, 1)
    faq = "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in data["faq"])
    author_link = f'<a href="{data["ruta_autor"]}">Más libros de {esc(author)}</a> · ' if data.get("ruta_autor") else ""
    bottom = (f'<!--ficha-v2--><h2 id="preguntas">Preguntas frecuentes sobre {esc(title)}</h2>{faq}'
              f'<p class="guide-link">{author_link}<a href="/resumenes/">Más resúmenes</a> · <a href="/leer/">Libros para leer online gratis</a></p><!--/ficha-v2-->')
    end = document.find('</div><div class="terms">')
    if end < 0:
        end = document.find("</div></article>")
    document = document[:end] + bottom + document[end:]

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
    for route, data in books.items():
        target = PUBLIC / route.strip("/") / "index.html"
        if not target.exists():
            print("no existe:", route)
            continue
        target.write_text(upgrade(route, data, target.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"{len(books)} fichas actualizadas al formato nuevo")


if __name__ == "__main__":
    main()
