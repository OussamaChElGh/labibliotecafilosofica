"""Limpia La Celestina (Wikisource, ed. de 1913) tras descargarla con wikisource.py --capitulos.

python textos/fichas/celestina.py  →  quita los apéndices, titula los actos como «Acto I…», separa el
argumento y la lista de interlocutores (S|) y pasa «CALISTO.- texto» a una intervención con su personaje.
"""
import json
import re
from pathlib import Path

TEXTS = Path(__file__).resolve().parents[1]
SLUG = "la-celestina-fernando-de-rojas"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII",
         "XVIII", "XIX", "XX", "XXI"]
FUERA = ("Concluye el autor", "Alonso de Proaza corrector de la impresión")


def name(caps):
    return " ".join(w.capitalize() for w in caps.lower().split())


def main():
    config, source = TEXTS / f"{SLUG}.json", TEXTS / f"{SLUG}.txt"
    meta = json.loads(config.read_text(encoding="utf-8"))
    if meta.get("speakers"):
        print(SLUG, "ya estaba limpia")
        return
    blocks = source.read_text(encoding="utf-8").split("\n")
    out, chapters, speakers, act = [], [], {}, 0
    for chapter in meta["chapters"]:
        if chapter["title"] in FUERA:
            continue
        part = blocks[chapter["start"]:chapter["end"] + 1]
        if re.search(r"a[uv]?cto", chapter["title"], re.I) or chapter["title"].startswith("Acto "):
            title = f"Acto {ROMAN[act]}"
            act += 1
            chapter.update(slug=f"acto-{act}", title=title)
            part[0] = "H|" + title
        start = len(out)
        out.append(part[0])
        for block in part[1:]:
            text = block[2:]
            said = re.match(r"([A-ZÁÉÍÓÚÑ]{3,}(?: [A-ZÁÉÍÓÚÑ]{2,})?)\.\s*[-—–]+\s*(.*)", text)
            if block.startswith("P|") and said:
                speakers[str(len(out))] = name(said.group(1))
                out.append("P|" + said.group(2))
            elif block.startswith("P|") and (text.startswith("ARGUMENTO") or
                                             re.fullmatch(r"[A-ZÁÉÍÓÚÑ ,.]+", text)):
                out.append("S|" + text if text.startswith("ARGUMENTO") else "S|" + name(text.rstrip(".")).replace(" ,", ","))
            elif block.startswith("P|") and out[-1].startswith("S|ARGUMENTO") and ":" not in out[-1]:
                out.append("S|" + text)  # el argumento del acto primero va en su propio párrafo
            else:
                out.append(block)
        chapter.update(start=start, end=len(out) - 1)
        chapters.append(chapter)
    meta.update(chapters=chapters, speakers=speakers)
    source.write_text("\n".join(out), encoding="utf-8")
    config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(SLUG, len(chapters), "partes,", len(speakers), "intervenciones")


if __name__ == "__main__":
    main()
