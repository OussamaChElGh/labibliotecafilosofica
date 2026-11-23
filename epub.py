"""Convierte un libro en ePub (por ejemplo, descargado de Elejandría o de Gutenberg) al formato de textos/.

Uso:  python epub.py libro.epub <slug> --titulo "…" --autor "…" [--ficha /ruta/] [--traductor …] [--edicion …]
          [--fuente https://… ] [--licencia "Dominio público"] [--saltar "Créditos|Sobre este libro"]

Lee el orden de lectura del ePub (spine). Cada título <h1>/<h2> abre un capítulo; si un archivo no tiene títulos,
el archivo entero es un capítulo. <h3>-<h6> quedan como títulos internos. Los poemas (<br> dentro de un párrafo,
clases «verse», «poem», «verso») van como V|. Las páginas de portada, créditos, índice y licencia de la edición se saltan.
"""
import argparse
import json
import posixpath
import re
import zipfile
from pathlib import Path

from lxml import etree, html

from wikisource import TEXTS, chapter_slug, clean

SKIP_TITLES = re.compile(r"(?i)^(cubierta|portada|cover|t[ií]tulo|cr[eé]ditos|[ií]ndice|tabla de contenidos?|contents|"
                         r"sobre (este|el) libro|licencia|colof[oó]n|notas? de la edici[oó]n digital|acerca de|elejandr[ií]a)")


def spine(z):
    container = etree.fromstring(z.read("META-INF/container.xml"))
    opf_path = container.xpath("//*[local-name()='rootfile']/@full-path")[0]
    opf = etree.fromstring(z.read(opf_path))
    base = posixpath.dirname(opf_path)
    items = {i.get("id"): i.get("href") for i in opf.xpath("//*[local-name()='item']")}
    order = [items[r.get("idref")] for r in opf.xpath("//*[local-name()='itemref']") if r.get("idref") in items]
    return [posixpath.normpath(posixpath.join(base, h.split("#")[0])) for h in order]


def blocks_of(markup):
    if isinstance(markup, bytes):
        enc = re.search(rb'encoding=["\']([\w-]+)', markup[:200])
        markup = markup.decode(enc.group(1).decode() if enc else "utf-8", errors="replace")
        markup = re.sub(r"^<\?xml[^>]*\?>", "", markup.lstrip("﻿"))
    # Letra capital como imagen (ediciones de Gutenberg): se queda la letra del alt.
    # «⁂» marca que la letra es una palabra entera («A la mitad…»), sin él es el principio de una palabra («E»+«L día»).
    markup = re.sub(r'<img[^>]*alt="(\w)(\s?)"[^>]*/?>', lambda m: f"<span>{m.group(1)}{'⁂' if m.group(2) else ''}</span>", markup)
    doc = html.fromstring(markup)
    for junk in doc.xpath("//script|//style|//nav|//*[@epub:type='pagebreak']",
                          namespaces={"epub": "http://www.idpf.org/2007/ops"}):
        junk.drop_tree()
    for sup in doc.xpath("//sup|//a[contains(@class,'noteref')]"):
        sup.drop_tree()
    out = []
    body = doc.find(".//body")
    for node in (body if body is not None else doc).iter("h1", "h2", "h3", "h4", "h5", "h6", "p", "div", "blockquote", "li"):
        if node.xpath("ancestor::p|ancestor::li|ancestor::h1|ancestor::h2|ancestor::h3"):
            continue
        tag, css = node.tag, (node.get("class") or "").lower()
        if tag == "div" and node.xpath(".//p|.//div|.//h1|.//h2|.//h3"):
            continue  # contenedor: se leen sus párrafos
        if tag in ("h1", "h2"):
            text = clean(node.text_content())
            if text:
                out.append(("H", text))
        elif tag in ("h3", "h4", "h5", "h6"):
            text = clean(node.text_content())
            if text:
                out.append(("T", text))
        else:
            raw = etree.tostring(node, encoding="unicode", method="html")
            verse = any(k in css for k in ("verse", "verso", "poem", "poema", "estrofa")) or raw.count("<br") >= 2
            if verse:
                for line in re.split(r"<br\s*/?>", raw):
                    text = clean(html.fromstring(f"<p>{line}</p>").text_content()) if line.strip() else ""
                    if text:
                        out.append(("V", text))
            else:
                text = clean(node.text_content())
                if text:
                    cap = out[-1][1] if out and out[-1][0] == "P" else ""
                    if re.fullmatch(r"\w⁂", cap):  # «A» + «la mitad del viaje…»
                        out.pop()
                        text = cap[0] + " " + text
                    elif re.fullmatch(r"\w", cap):  # «E» + «L día…» → «El día…»
                        out.pop()
                        text = cap + (text[0].lower() + text[1:] if text[1:2] in (" ", ",") else text)
                    elif text.startswith("⁂"):
                        text = text[1:]
                    if not re.fullmatch(r"\w⁂", text):  # la letra capital sola espera al párrafo siguiente
                        text = text.replace("⁂", " ").strip()
                    out.append(("P", text))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("epub")
    parser.add_argument("slug")
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--autor", required=True)
    parser.add_argument("--ficha", default="")
    parser.add_argument("--ruta-autor", default="")
    parser.add_argument("--traductor", default="")
    parser.add_argument("--edicion", default="")
    parser.add_argument("--fuente", default="", help="URL de donde sale el texto")
    parser.add_argument("--licencia", default="Dominio público")
    parser.add_argument("--saltar", default="", help="títulos de secciones que no son de la obra, separados por «|»")
    args = parser.parse_args()
    extra = [s.lower() for s in args.saltar.split("|") if s]

    z = zipfile.ZipFile(args.epub)
    body, chapters, inner = [], [], False
    title_norm = args.titulo.lower().strip()
    for name in spine(z):
        try:
            parts = blocks_of(z.read(name))
        except (KeyError, etree.ParserError):
            continue
        if not parts:
            continue
        heads = [t for k, t in parts if k == "H"]
        first = heads[0] if heads else ""
        if SKIP_TITLES.match(first) or (first.lower() in extra) or (not heads and len(parts) < 4 and
                                                                     any(SKIP_TITLES.match(t) for _, t in parts)):
            continue
        if not heads:  # archivo sin título: un capítulo propio
            parts = [("H", f"Parte {len(chapters) + 1}")] + parts
        for kind, text in parts:
            if kind == "H":
                if text.lower().strip() == title_norm and not chapters:
                    continue  # título de la obra repetido al principio
                if chapters and chapters[-1]["start"] == len(body) - 1:  # dos títulos seguidos: «Capítulo I» + «El jardín»
                    chapters[-1]["title"] += ". " + text
                    body[-1] = "H|" + chapters[-1]["title"]
                    continue
                if chapters:
                    chapters[-1]["end"] = len(body) - 1
                chapters.append({"slug": "", "title": text, "summary": "", "start": len(body), "end": len(body)})
                body.append("H|" + text)
            elif kind == "T":
                inner = True
                body.append("H|" + text)
            else:
                if not chapters:
                    chapters.append({"slug": "", "title": "Inicio", "summary": "", "start": len(body), "end": len(body)})
                    body.append("H|Inicio")
                body.append(f"{kind}|{text}")
    if chapters:
        chapters[-1]["end"] = len(body) - 1
    used = set()
    for n, c in enumerate(chapters, start=1):
        slug = (chapter_slug(c["title"]) or f"parte-{n}")[:60].strip("-")
        while slug in used:
            slug += "-2"
        used.add(slug)
        c["slug"] = slug
    (TEXTS / f"{args.slug}.txt").write_text("\n".join(body), encoding="utf-8")
    config = TEXTS / f"{args.slug}.json"
    meta = json.loads(config.read_text(encoding="utf-8")) if config.exists() else {}
    meta.update({"slug": args.slug, "title": args.titulo, "author": args.autor,
                 "author_route": args.ruta_autor or meta.get("author_route", ""),
                 "book_route": args.ficha or meta.get("book_route") or f"/{args.slug}/",
                 "translator": args.traductor, "edition": args.edicion, "source_url": args.fuente,
                 "license": args.licencia, "license_url": "", "speakers": {}, "chapters": chapters})
    if inner:
        meta["inner_titles"] = True
    config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    words = sum(len(b.split()) for b in body if b[:2] in ("P|", "V|"))
    print(f"{args.slug}: {len(body)} bloques, {words:,} palabras, {len(chapters)} capítulos")


if __name__ == "__main__":
    main()
