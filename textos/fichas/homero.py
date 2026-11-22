"""Limpia la Odisea y la Ilíada de Segalá tras descargarlas con wikisource.py --capitulos.

python textos/fichas/homero.py  →  quita los índices finales y los números de verso, y titula cada canto con su epígrafe.
"""
import json
import re
from pathlib import Path

TEXTS = Path(__file__).resolve().parents[1]
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII",
         "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV"]
EPIGRAFES = {
    "la-odisea-homero": [
        "Concilio de los dioses. Exhortación de Atenea a Telémaco", "Telémaco reúne al pueblo en el ágora. Partida de Telémaco",
        "Lo de Pilos", "Lo de Lacedemonia", "La balsa de Ulises", "Llegada de Ulises al país de los feacios",
        "Entrada de Ulises en el palacio de Alcínoo", "Presentación de Ulises a los feacios", "Relatos a Alcínoo. Cicloplea",
        "Lo relativo a Eolo, a los lestrigones y a Circe", "Evocación de los muertos", "Las sirenas, Escila, Caribdis, las vacas del Sol",
        "Partida de Ulises del país de los feacios y su llegada a Ítaca", "Conversación de Ulises con Eumeo",
        "Llegada de Telémaco a la cabaña de Eumeo", "Telémaco reconoce a Ulises", "Telémaco vuelve a la ciudad",
        "Pugilato de Ulises e Iro", "Coloquio de Ulises y Penélope. El baño", "Lo que precedió a la matanza de los pretendientes",
        "El certamen del arco", "Matanza de los pretendientes", "Penélope reconoce a Ulises", "Las libaciones"],
    "la-iliada-homero": [
        "Peste. Cólera", "Sueño. Beocia o catálogo de las naves",
        "Juramentos. Desde la muralla. Combate singular de Alejandro y Menelao",
        "Violación de los juramentos. Agamenón revista las tropas", "Principalía de Diomedes", "Coloquio de Héctor y Andrómaca",
        "Combate singular de Héctor y Áyax", "Batalla interrumpida", "Embajada a Aquiles. Súplicas", "Dolonía",
        "Principalía de Agamenón", "Combate en la muralla", "Batalla junto a las naves", "Engaño de Júpiter",
        "Nueva ofensiva desde las naves", "Patroclea", "Principalía de Menelao", "Fabricación de las armas",
        "Renunciación de la cólera", "Combate de los dioses", "Batalla junto al río", "Muerte de Héctor",
        "Juegos en honor de Patroclo", "Rescate de Héctor"],
}


def main():
    for slug, epigrafes in EPIGRAFES.items():
        config, source = TEXTS / f"{slug}.json", TEXTS / f"{slug}.txt"
        if not config.exists():
            continue
        meta = json.loads(config.read_text(encoding="utf-8"))
        blocks = source.read_text(encoding="utf-8").split("\n")
        notes = [b for b in blocks if b.startswith("N|")]
        out, chapters = [], []
        for chapter in meta["chapters"]:
            if chapter["title"].upper().startswith(("ÍNDICE", "INDICE")):
                continue
            part = blocks[chapter["start"]:chapter["end"] + 1]
            match = re.fullmatch(r"Canto ([IVXL]+)(?:\..*)?", chapter["title"])
            if match:
                title = f"Canto {match.group(1)}. {epigrafes[ROMAN.index(match.group(1))]}"
                part[0] = "H|" + title
                chapter["title"] = title
            part = [re.sub(r"^P\|\d+ ", "P|", b) for b in part]
            chapter.update(start=len(out), end=len(out) + len(part) - 1)
            out += part
            chapters.append(chapter)
        meta["chapters"] = chapters
        source.write_text("\n".join(out + notes), encoding="utf-8")
        config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(slug, len(chapters), "cantos y prólogo")


if __name__ == "__main__":
    main()
