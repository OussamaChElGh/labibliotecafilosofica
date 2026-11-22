"""Descarga una obra de es.wikisource.org y la convierte al formato de textos/.

Uso:  python wikisource.py "Critón" criton-platon --autor Platón --ficha /criton-platon/
Escribe textos/<slug>.txt (H| título, P| párrafo, V| verso, N| nota) y un
textos/<slug>.json con los metadatos, los interlocutores y una división en
capítulos provisional (partes de unas 2.500 palabras cortadas en un cambio de
interlocutor), que luego se revisa a mano: títulos y resúmenes de cada parte.
"""
import argparse
import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from lxml import html

API = "https://es.wikisource.org/w/api.php"
UA = "WikisourceTextReader/1.0 (educational static site builder)"
TEXTS = Path(__file__).resolve().parent / "textos"
PART_WORDS = 2500
_last = [0.0]


def api(**params):
    params.update(format="json", formatversion="2")
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(8):
        wait = 1.1 - (time.time() - _last[0])  # Una petición por segundo, como pide Wikimedia.
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            time.sleep(int(error.headers.get("retry-after") or 5) + attempt * 2)
        except OSError:
            time.sleep(5 + attempt * 3)
    raise RuntimeError(f"Wikisource no responde: {url}")


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def clean(text):
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)  # palabra partida a final de línea
    return re.sub(r"\s+", " ", text).strip()


def speaker_name(text):
    name = clean(text).rstrip(".").strip()
    return " ".join(w if w.lower() in ("de", "del") else w.capitalize() for w in name.lower().split())


def inline(node, refs):
    """Texto de un párrafo con las llamadas a nota convertidas en [[n]]."""
    for sup in node.xpath('.//sup[contains(@class,"reference")]'):
        match = re.search(r"cite_note-(\d+)", sup.xpath("string(.//a/@href)") or "")
        sup.drop_tree() if not match else None
        if match:
            refs.append(int(match.group(1)))
            marker = html.fromstring(f"<span>[[{match.group(1)}]]</span>")
            marker.tail = sup.tail
            sup.getparent().replace(sup, marker)
    for junk in node.xpath('.//span[contains(@class,"pagenum")]|.//style|.//sup[contains(@class,"noprint")]'):
        junk.drop_tree()
    return clean(node.text_content())


def convert(page):
    data = api(action="parse", page=page, prop="text|revid", redirects=1)
    if "error" in data:
        raise SystemExit(f'{page}: {data["error"]["info"]}')
    tree = html.fromstring(data["parse"]["text"])
    roots = tree.xpath('//div[contains(@class,"prp-pages-output")]') or [tree]
    blocks, speakers, refs, pending = [], {}, [], None
    for root in roots:
        for junk in root.xpath('.//*[@id="headertemplate"]|.//*[contains(@class,"ws-noexport")]|.//*[contains(@class,"interwiki-extra")]'
                               '|.//*[contains(@class,"noprint")]|.//style|.//link'):
            junk.drop_tree()
        for node in root.iter("p", "h2", "h3", "h4", "div", "poem"):
            css = node.get("class") or ""
            if node.tag in ("h2", "h3", "h4") or "ws-h2" in css or "ws-h3" in css:
                text = clean(node.text_content())
                if text and not node.xpath('ancestor::h2|ancestor::h3|ancestor::h4'):
                    blocks.append("H|" + text)
            elif "dialogo" in css:
                pending = speaker_name(node.text_content())
            elif "personajes" in css:
                blocks.append("S|Interlocutores: " + clean(node.text_content()))
            elif node.tag == "p" and not node.xpath('ancestor::*[contains(@class,"references")]'):
                text = inline(node, refs)
                if not text:
                    continue
                if pending:
                    speakers[len(blocks)] = pending
                    pending = None
                blocks.append("P|" + text)
    notes = []
    for item in tree.xpath('//ol[contains(@class,"references")]/li'):
        text = clean(item.xpath('string(.//span[contains(@class,"reference-text")])'))
        notes.append("N|" + text)
    # Renumera las llamadas para que coincidan con el orden de las notas.
    order = {old: new for new, old in enumerate(sorted(set(refs)), start=1)}
    blocks = [re.sub(r"\[\[(\d+)\]\]", lambda m: f"[[{order.get(int(m.group(1)), m.group(1))}]]", b) for b in blocks]
    return blocks + notes, speakers, data["parse"].get("revid")


NAME = r"[A-ZÁÉÍÓÚÑ][a-záéíóúñü]+(?: (?:de |del |el |la )?[A-ZÁÉÍÓÚÑ][a-záéíóúñü]+){0,2}"
NOT_NAMES = {"Sí", "No", "Pues", "Bien", "Claro", "Cierto", "Verdad", "Exacto", "Perfecto", "Conforme", "Nada", "Nunca",
             "Jamás", "Todo", "Tal", "Eso", "Esto", "Así", "Bueno", "Ninguno", "Imposible", "Necesariamente"}
CAPS = r"[A-ZÁÉÍÓÚÑ]{2,}(?: [A-ZÁÉÍÓÚÑ]{2,}){0,2}"
INLINE_SPEAKER = re.compile(rf"({NAME}|{CAPS})(?:\.\s*[-–—]\s*|:\s+)(.+)")


def normalize(blocks, speakers):
    """Unifica las formas de marcar quién habla en las distintas transcripciones.

    Algunas páginas ponen el nombre en un párrafo aparte («Fedro»), otras al
    principio («Sócrates: …», «Teodoro. -…»). Solo cuenta como interlocutor un
    nombre que aparece así al menos tres veces, para no confundirlo con una frase.
    """
    def strip(text):
        return re.sub(r"\s*\{\d+\}|\s*\[\d+\]", "", text).strip()

    counts = {}
    for block in blocks:
        text = strip(block[2:])
        if block.startswith("P|") and len(text) < 30 and re.fullmatch(NAME + r"\.?", text):
            counts[text.rstrip(".")] = counts.get(text.rstrip("."), 0) + 1
        elif block.startswith("P|") and (m := INLINE_SPEAKER.match(text)):
            name = speaker_name(m.group(1))
            counts[name] = counts.get(name, 0) + 1
    names = {name for name, count in counts.items()
             if count >= 3 and name not in NOT_NAMES and not name.endswith("mente")}
    out, found, pending = [], {}, None
    for index, block in enumerate(blocks):
        kind, text = block[:2], block[2:]
        if kind == "P|":
            text = strip(text)
            if text.rstrip(".") in names:
                pending = text.rstrip(".")
                continue
            if (m := INLINE_SPEAKER.match(text)) and speaker_name(m.group(1)) in names:
                pending, text = speaker_name(m.group(1)), m.group(2)
            pending = pending or speakers.get(index)
            if pending:
                found[len(out)] = pending
                pending = None
        out.append(kind + text)
    return out, found


def provisional_chapters(blocks, speakers):
    """Argumento aparte y el resto en partes de unas PART_WORDS palabras."""
    chapters, start, words = [], 0, 0
    heads = [i for i, b in enumerate(blocks) if b.startswith("H|")]
    body_start = heads[1] if len(heads) > 1 and "ARGUMENTO" in blocks[heads[0]].upper() else 0
    if body_start:
        chapters.append({"slug": "argumento", "title": "Argumento", "summary": "Resumen de la obra que acompaña a la edición de 1871.",
                         "start": heads[0], "end": body_start - 1})
    start = body_start
    last = max(i for i, b in enumerate(blocks) if not b.startswith("N|"))
    for index in range(body_start, last + 1):
        if blocks[index][:2] in ("P|", "V|"):
            words += len(blocks[index].split())
        is_turn = not speakers or index + 1 in speakers or index + 1 > last
        if (words >= PART_WORDS and is_turn) or words >= PART_WORDS * 1.5 or index == last:
            number = len([c for c in chapters if c["slug"] != "argumento"]) + 1
            chapters.append({"slug": f"parte-{number}", "title": f"Parte {number}", "summary": "",
                             "start": start, "end": index})
            start, words = index + 1, 0
    # Una última parte muy corta se une a la anterior.
    if len(chapters) >= 2 and chapters[-2]["slug"].startswith("parte") and \
            sum(len(b.split()) for b in blocks[chapters[-1]["start"]:chapters[-1]["end"] + 1]) < PART_WORDS / 3:
        tail = chapters.pop()
        chapters[-1]["end"] = tail["end"]
    return chapters


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("page")
    parser.add_argument("slug")
    parser.add_argument("--titulo")
    parser.add_argument("--autor", required=True)
    parser.add_argument("--ruta-autor", default="")
    parser.add_argument("--ficha", default="")
    parser.add_argument("--traductor", default="")
    parser.add_argument("--edicion", default="")
    args = parser.parse_args()
    blocks, speakers, revision = convert(args.page)
    blocks, speakers = normalize(blocks, speakers)
    (TEXTS / f"{args.slug}.txt").write_text("\n".join(blocks), encoding="utf-8")
    config = TEXTS / f"{args.slug}.json"
    meta = json.loads(config.read_text(encoding="utf-8")) if config.exists() else {}
    meta.update({
        "slug": args.slug, "title": args.titulo or meta.get("title") or re.sub(r"\s*\(.*?\)", "", args.page),
        "author": args.autor, "author_route": args.ruta_autor or meta.get("author_route", ""),
        "book_route": args.ficha or meta.get("book_route") or f"/{args.slug}/",
        "translator": args.traductor or meta.get("translator", ""), "edition": args.edicion or meta.get("edition", ""),
        "source_url": "https://es.wikisource.org/wiki/" + urllib.parse.quote(args.page.replace(" ", "_")),
        "source_revision": revision, "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/deed.es",
        "speakers": {str(k): v for k, v in speakers.items()},
    })
    if "chapters" not in meta:
        meta["chapters"] = provisional_chapters(blocks, speakers)
    config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    words = sum(len(b.split()) for b in blocks if b[:2] in ("P|", "V|"))
    print(f'{args.slug}: {len(blocks)} bloques, {words:,} palabras, {len(meta["chapters"])} capítulos, {len(speakers)} intervenciones')


if __name__ == "__main__":
    main()
