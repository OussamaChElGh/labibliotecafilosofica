"""Descarga una obra de teatro de es.wikisource.org (un acto por subpágina) al formato de textos/.

Uso:  python teatro.py "Macbeth (Menéndez y Pelayo tr.)" macbeth-shakespeare --titulo Macbeth \
          --autor "William Shakespeare" --ficha /macbeth-libros-pdf-gratis/ --traductor "Marcelino Menéndez y Pelayo" \
          --edicion "Dramas de Guillermo Shakespeare, Barcelona, 1881"

Si la obra entera está en una sola página, la corta por los encabezados «ACTO I.», «ACTO II.»…
Pensado para las traducciones en prosa de Menéndez y Pelayo, donde el nombre del personaje va
centrado y en mayúsculas sobre su intervención. Cada acto es un capítulo; las escenas y las
acotaciones van como S| y cada intervención como P| con su personaje en «speakers».
"""
import argparse
import html as htmllib
import json
import re
import urllib.parse

from wikisource import TEXTS, api, subpages, chapter_slug

ORDINAL = {"PRIMERA": "primera", "SEGUNDA": "segunda", "TERCERA": "tercera", "CUARTA": "cuarta", "QUINTA": "quinta",
           "SEXTA": "sexta", "SÉPTIMA": "séptima", "OCTAVA": "octava", "NOVENA": "novena", "DÉCIMA": "décima"}


def lines_of(page):
    """El acto como una lista de (centrado, texto) en orden de lectura."""
    data = api(action="parse", page=page, prop="text|revid", redirects=1)
    text = data["parse"]["text"]
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S)
    # Letra capital: la imagen lleva la letra en alt.
    text = re.sub(r'<span class="dropinitial"[^>]*>.*?alt="([^"]*)".*?</span></span>', r"\1", text, flags=re.S)
    text = re.sub(r'<span[^>]*class="pagenum"[^>]*></span>', "", text)
    text = re.sub(r'<sup[^>]*class="reference".*?</sup>', "", text, flags=re.S)
    text = re.sub(r'<(div|p)[^>]*(?:text-align:\s*center|align="center")[^>]*>(.*?)</\1>',
                  lambda m: "\n@@" + re.sub(r"<[^>]+>|\n", " ", m.group(2)) + "\n", text, flags=re.S)
    text = re.sub(r"<br\s*/?>|</?(?:p|div|dd|dl|h\d|li|ul|table|tr|td)[^>]*>", "\n", text)
    text = htmllib.unescape(re.sub(r"<[^>]+>", "", text))
    out = []
    for line in text.split("\n"):
        centered = line.startswith("@@")
        line = re.sub(r"\s+", " ", line.lstrip("@")).strip()
        if line:
            out.append((centered, line))
    return out, data["parse"].get("revid")


def is_speaker(text):
    letters = re.sub(r"[^A-Za-zÁÉÍÓÚÑáéíóúñ]", "", text)
    return letters and letters.isupper() and len(text) < 40 and not text.startswith("ESCENA")


def speaker_name(text):
    name = text.strip(" .")
    name = re.sub(r"\b(\w+)\b", lambda m: m.group(1) if m.group(1).lower() in ("de", "del", "y") else m.group(1).capitalize(),
                  name.lower())
    return name.replace(" Y ", " y ")


def caps_to_names(text):
    """«Tres BRUJAS, LADY MACBETH y ROSS» → «Tres Brujas, Lady Macbeth y Ross»."""
    return re.sub(r"\b[A-ZÁÉÍÓÚÑ]{2,}\b", lambda m: m.group(0).capitalize(), text)


def acts_in_page(page):
    """Obra entera en una sola página («El mercader de Venecia»): un grupo de líneas por cada «ACTO I.», «ACTO II.»…"""
    raw, revision = lines_of(page)
    acts = []
    for centered, text in raw:
        head = re.match(r"ACTO\s+([IVX]+)\.?\s*(.*)", text)
        if centered and head:
            acts.append(("Acto " + head.group(1), []))
            rest = re.sub(r"^_+\s*", "", head.group(2))
            if not rest.startswith("ESCENA"):  # «ACTO III. ____» sin «ESCENA PRIMERA»
                acts[-1][1].append((False, "ESCENA PRIMERA."))
            if rest:
                acts[-1][1].append((True, rest))
        elif acts:
            acts[-1][1].append((centered, text))
    return acts, revision


def convert_act(page, raw=None):
    revision = None
    if raw is None:
        raw, revision = lines_of(page)
    first = next((i for i, (_, text) in enumerate(raw) if text.upper().startswith("ESCENA")), 0)
    blocks, speakers, pending = [], {}, None
    header = False
    for centered, text in raw[first:]:
        text = re.sub(r"\{\{\w+\||\}\}", "", text).strip()
        if not text:
            continue
        scene = re.match(r"ESCENA\s+([A-ZÁÉÍÓÚÑ]+|[IVXL]+)\.?\s*(.*)", text)
        if scene:
            number = scene.group(1)
            blocks.append("S|Escena " + ORDINAL.get(number, number) + ".")
            place, pending, header = scene.group(2), None, True
            last = re.fullmatch(r"(.*\.)\s+([^.]+)\.", place)
            if last and is_speaker(last.group(2)):  # «…PÓRCIA y NERISSA. EL PRÍNCIPE.»: el último es quien habla
                place, pending, header = last.group(1), speaker_name(last.group(2)), False
            if place:
                blocks.append("S|" + caps_to_names(place))
        elif text.startswith("↑") or not re.search(r"\w", text):
            continue  # notas al pie sin llamada y restos de puntuación
        elif centered and re.fullmatch(r"([^()]+?)\.?\s*(\(.*\))", text) and is_speaker(text.split("(")[0]):
            name, note = re.fullmatch(r"([^()]+?)\.?\s*(\(.*\))", text).groups()
            pending, header = speaker_name(name) + " " + note.replace(".)", ")"), False
        elif (centered or header) and is_speaker(text):
            pending, header = speaker_name(text), False
        elif text.startswith("(") and text.endswith(")") or centered or (header and not pending) or \
                (not pending and blocks and blocks[-1].startswith("S|") and len(text) < 90 and re.search(r"\b[A-ZÁÉÍÓÚÑ]{3,}\b", text)):
            blocks.append("S|" + caps_to_names(text))
        elif blocks and not pending and blocks[-1].startswith("P|") and not re.search(r"[.!?»:;)—]$", blocks[-1]) \
                and text[:1].islower():
            blocks[-1] += " " + text  # párrafo partido por un salto de página
        else:
            if pending:
                speakers[len(blocks)] = pending
                pending = None
            # Versalitas de la primera palabra: «CUándo», «YA eres» → «Cuándo», «Ya eres».
            text = re.sub(r"^([¿¡«]?[A-ZÁÉÍÓÚÑ])([A-ZÁÉÍÓÚÑ]+)(?=[a-záéíóúñ]|\s+[a-záéíóúñ])",
                          lambda m: m.group(1) + m.group(2).lower(), text)
            blocks.append("P|" + text)
    # Limpieza: escena repetida, espacio antes de puntuación y «De»/«Del» de los nombres en versalitas.
    clean, moved = [], {}
    for i, block in enumerate(blocks):
        if block.startswith("S|") and clean and clean[-1] == block:
            continue
        block = re.sub(r"\s+([.,;:])", r"\1", block)
        if block.startswith("S|"):
            block = re.sub(r"\b(De|Del)\b(?= [A-ZÁÉÍÓÚÑ])", lambda m: m.group(1).lower(), block)
        if i in speakers:
            moved[len(clean)] = speakers[i]
        clean.append(block)
    return clean, moved, revision


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("page")
    parser.add_argument("slug")
    parser.add_argument("--titulo", required=True)
    parser.add_argument("--autor", required=True)
    parser.add_argument("--ficha", required=True)
    parser.add_argument("--traductor", default="")
    parser.add_argument("--edicion", default="")
    args = parser.parse_args()
    _, parts, revision = subpages(args.page)
    if parts:
        acts = [(sub.split("/", 1)[1], None, sub) for sub, _ in parts]
    else:  # sin subpáginas: todos los actos en la misma página
        found, revision = acts_in_page(args.page)
        acts = [(name, raw, args.page) for name, raw in found]
    body, speakers, chapters = [], {}, []
    for name, raw, sub in acts:
        if name.lower() == "personajes":
            continue
        blocks, own, _ = convert_act(sub, raw)
        offset = len(body) + 1
        chapters.append({"slug": chapter_slug(name) or f"parte-{len(chapters) + 1}", "title": name.replace("Acto", "Acto"),
                         "summary": "", "start": len(body), "end": len(body) + len(blocks)})
        speakers.update({k + offset: v for k, v in own.items()})
        body += ["H|" + name] + blocks
    (TEXTS / f"{args.slug}.txt").write_text("\n".join(body), encoding="utf-8")
    config = TEXTS / f"{args.slug}.json"
    meta = json.loads(config.read_text(encoding="utf-8")) if config.exists() else {}
    meta.update({
        "slug": args.slug, "title": args.titulo, "author": args.autor, "author_route": meta.get("author_route", ""),
        "book_route": args.ficha, "translator": args.traductor, "edition": args.edicion,
        "source_url": "https://es.wikisource.org/wiki/" + urllib.parse.quote(args.page.replace(" ", "_")),
        "source_revision": revision, "license": "CC BY-SA 4.0",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/deed.es",
        "speakers": {str(k): v for k, v in speakers.items()}, "chapters": chapters,
    })
    config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    words = sum(len(b.split()) for b in body if b[:2] == "P|")
    print(f"{args.slug}: {len(body)} bloques, {words:,} palabras, {len(chapters)} actos, {len(speakers)} intervenciones")


if __name__ == "__main__":
    main()
