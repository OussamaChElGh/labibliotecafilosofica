"""Descarga una obra de teatro en prosa de es.wikisource.org cuyo diálogo va como «<b>PERSONAJE:</b> texto».

Uso:  python teatro_prosa.py "Luces de bohemia" luces-de-bohemia-valle-inclan --titulo "Luces de bohemia" \
          --autor "Ramón María del Valle-Inclán" --edicion "Madrid, 1924"

Una subpágina por capítulo (escena o acto). Las acotaciones (en cursiva) van como S| y cada intervención
como P| con su personaje en «speakers». Se salta la subpágina de personajes (Dramatis personae).
"""
import argparse
import html as htmllib
import json
import re
import urllib.parse

from wikisource import TEXTS, api, subpages, chapter_slug

SPEAKER = re.compile(r"^\s*<b>([^<]{2,60}?)[:.]?\s*</b>\s*[:.]?\s*(.*)$", re.S)


def plain(fragment):
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", "", fragment))).strip()


def caps_to_names(text):
    return re.sub(r"\b[A-ZÁÉÍÓÚÑ]{2,}\b", lambda m: m.group(0).capitalize(), text)


def speaker_name(text):
    words = text.strip(" .:").lower().split()
    return " ".join(w if w in ("de", "del", "la", "el", "y") and i else w.capitalize() for i, w in enumerate(words))


def convert_part(page):
    data = api(action="parse", page=page, prop="text|revid", redirects=1)
    text = re.sub(r"<style.*?</style>", "", data["parse"]["text"], flags=re.S)
    text = re.sub(r'<sup[^>]*class="reference".*?</sup>', "", text, flags=re.S)
    start = text.find('<div class="prose">')
    text = text[start:] if start >= 0 else text
    blocks, speakers = [], {}
    for line in re.split(r"<br\s*/?>|</?p>|</?div[^>]*>", text):
        clean = plain(line)
        if not clean or not re.search(r"\w", clean):
            continue
        said = SPEAKER.match(line)
        if said and plain(said.group(1)).replace(" ", "").isupper():
            speakers[len(blocks)] = speaker_name(plain(said.group(1)))
            blocks.append("P|" + plain(said.group(2)))
        elif line.strip().startswith("<i>") or re.fullmatch(r"\(.*\)", clean):
            blocks.append("S|" + caps_to_names(clean))
        elif blocks and blocks[-1].startswith("P|") and "<i>" not in line and not re.search(r"\b[A-ZÁÉÍÓÚÑ]{4,}\b", clean):
            blocks[-1] += " " + clean  # continuación de la intervención anterior
        else:
            blocks.append("S|" + caps_to_names(clean))
    return blocks, speakers, data["parse"].get("revid")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("page")
    parser.add_argument("slug")
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--autor", required=True)
    parser.add_argument("--ficha", default="")
    parser.add_argument("--edicion", default="")
    args = parser.parse_args()
    _, parts, revision = subpages(args.page)
    body, speakers, chapters = [], {}, []
    for sub, label in parts:
        name = sub.split("/", 1)[1]
        if name.lower() in ("personajes", "dramatis personae"):
            continue
        blocks, own, _ = convert_part(sub)
        offset = len(body) + 1
        chapters.append({"slug": chapter_slug(name), "title": name, "summary": "",
                         "start": len(body), "end": len(body) + len(blocks)})
        speakers.update({k + offset: v for k, v in own.items()})
        body += ["H|" + name] + blocks
    (TEXTS / f"{args.slug}.txt").write_text("\n".join(body), encoding="utf-8")
    config = TEXTS / f"{args.slug}.json"
    meta = json.loads(config.read_text(encoding="utf-8")) if config.exists() else {}
    meta.update({
        "slug": args.slug, "title": args.titulo, "author": args.autor, "author_route": meta.get("author_route", ""),
        "book_route": args.ficha or f"/{args.slug}/", "translator": "", "edition": args.edicion,
        "source_url": "https://es.wikisource.org/wiki/" + urllib.parse.quote(args.page.replace(" ", "_")),
        "source_revision": revision, "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/deed.es",
        "speakers": {str(k): v for k, v in speakers.items()}, "chapters": chapters,
    })
    config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    words = sum(len(b.split()) for b in body if b[:2] == "P|")
    print(f"{args.slug}: {len(body)} bloques, {words:,} palabras, {len(chapters)} partes, {len(speakers)} intervenciones")


if __name__ == "__main__":
    main()
