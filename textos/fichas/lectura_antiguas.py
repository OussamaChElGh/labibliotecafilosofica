"""Da lectura online a libros de dominio público que ya tenían ficha heredada de WordPress.

python textos/fichas/lectura_antiguas.py  (después de descargar el texto con wikisource.py)

Toma los textos de la ficha (resumen, personajes, ideas, preguntas) de textos/fichas/antiguas/*.py
para que la ficha de la URL de siempre pase a ser la ficha única del libro, como las nuevas:
lectura online por capítulos, PDF y el mismo resumen. fichas_antiguas.py deja de tocar esas rutas.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEXTS = ROOT / "textos"
sys.path.insert(0, str(ROOT))
from fichas_antiguas import load_books  # noqa: E402

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII",
         "XVIII", "XIX", "XX", "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX"]
ORDINAL = ["primero", "segundo", "tercero", "cuarto", "quinto"]
NUMBER_START = 30

# slug del texto → ruta de la ficha antigua, color de portada, unidad y cómo numerar los capítulos.
BOOKS = {
    "voltaire-candido": dict(route="/voltaire-candido/", color="ocre", unidad="capítulos", numerar="romanos"),
    "voltaire-zadig": dict(route="/voltaire-zadig/", color="azul", unidad="capítulos", numerar="romanos"),
    "fundamentacion-metafisica-costumbres-kant": dict(
        route="/fundamentacion-de-la-metafisica-de-las-costumbres-immanuel-kant/", color="negro", unidad="partes",
        numerar="ordinales"),
    "voltaire-asi-va-el-mundo": dict(route="/voltaire-asi-va-el-mundo/", color="verde", unidad="partes", numerar=""),
}


def numbered(chapters, mode):
    """«I. Título» en los capítulos numerados (capitulo-N); «Capítulo primero. Título» en los tratados."""
    count = 0
    for chapter in chapters:
        if mode == "romanos" and chapter["slug"].startswith("capitulo-"):
            prefix = ROMAN[int(chapter["slug"].split("-")[1]) - 1] + ". "
        elif mode == "ordinales" and chapter["slug"] != "prologo":
            prefix = f"Capítulo {ORDINAL[count]}. "
            count += 1
        else:
            continue
        if not chapter["title"].startswith(prefix):
            yield chapter, prefix + chapter["title"]


def main():
    fichas = load_books()
    for number, (slug, conf) in enumerate(BOOKS.items(), start=NUMBER_START):
        config = TEXTS / f"{slug}.json"
        if not config.exists():
            print("sin texto:", slug)
            continue
        meta = json.loads(config.read_text(encoding="utf-8"))
        data = fichas[conf["route"]]
        blocks = (TEXTS / f"{slug}.txt").read_text(encoding="utf-8").split("\n")
        for chapter, title in list(numbered(meta["chapters"], conf["numerar"])):
            if blocks[chapter["start"]] == "H|" + chapter["title"]:
                blocks[chapter["start"]] = "H|" + title
            chapter["title"] = title
        (TEXTS / f"{slug}.txt").write_text("\n".join(blocks), encoding="utf-8")
        title, author, unit = meta["title"], meta["author"], conf["unidad"]
        meta["book_route"] = conf["route"]
        meta["author_route"] = data.get("ruta_autor", "")
        meta["description"] = (f"{title} de {author}: resumen, ideas principales y el libro completo para leer online "
                               f"gratis o descargar en PDF. {data['genero']} sobre {data['tema']}.")[:300]
        meta["intro"] = f"<p>{data['resumen'][0]}</p><p>Aquí puedes leer {title} completo, dividido en {unit}. " \
                        "Se respeta la ortografía de la edición original.</p>"
        meta.setdefault("cover", {}).update({"color": conf["color"], "number": number})
        for chapter in meta["chapters"]:
            if not chapter.get("summary"):
                first = next((b[2:] for b in blocks[chapter["start"]:chapter["end"] + 1] if b.startswith("P|")), "")
                words = first.lstrip("—-– ").split()
                chapter["summary"] = "Empieza: «" + " ".join(words[:22]) + ("…»" if len(words) > 22 else "»")
        meta["ficha"] = {"genero": data["genero"], "unidad": unit, "tema": data["tema"], "resumen": data["resumen"],
                         "personajes": data.get("personajes", []), "ideas": data["ideas"], "faq": data["faq"],
                         "año": data["año"]}
        config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(number, slug)


if __name__ == "__main__":
    main()
