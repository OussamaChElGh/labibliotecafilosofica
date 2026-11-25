"""Séptima tanda: cuentos cortos en inglés de dominio público (Wikisource en inglés).

1. python wikisource.py "The Story of an Hour" cuentos-cortos-en-ingles --wiki en --titulo "Cuentos cortos en inglés" \
       --autor "Wilde, Poe, O. Henry y otros" --ficha /cuentos-cortos-en-ingles/ --partes "<las páginas de STORIES, separadas por «|»>"
   (la página principal solo sirve para la revisión; cada cuento se descarga de su página de --partes).
2. python textos/fichas/ingles.py  →  limpia el texto (títulos repetidos, créditos de la edición, avisos de licencia
   de Wikisource y pies de ilustración), pone título, autor, nivel y resumen en español a cada cuento y genera la ficha.

Los niveles (MCER) son orientativos: dependen del vocabulario, la sintaxis y el inglés de la época de cada cuento.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clasicos  # noqa: E402

SLUG = "cuentos-cortos-en-ingles"
TEXTS = Path(__file__).resolve().parents[1]
NUMBER_START = 60

# (página de Wikisource, slug, título, autor, año, nivel, resumen en español)
STORIES = [
    ("The Happy Prince and Other Tales/The Happy Prince", "the-happy-prince", "The Happy Prince", "Oscar Wilde", 1888, "A2-B1",
     "La estatua de un príncipe, cubierta de oro y piedras preciosas, ve desde lo alto la miseria de su ciudad. Pide a una golondrina que se queda con él en invierno que reparta sus riquezas entre los pobres."),
    ("The Story of an Hour", "the-story-of-an-hour", "The Story of an Hour", "Kate Chopin", 1894, "B1",
     "Louise Mallard, enferma del corazón, recibe la noticia de que su marido ha muerto en un accidente de tren. Encerrada en su cuarto, descubre algo inesperado: la libertad."),
    ("The Four Million/The Gift of the Magi", "the-gift-of-the-magi", "The Gift of the Magi", "O. Henry", 1905, "B1",
     "Della y Jim, un matrimonio pobre de Nueva York, quieren hacerse un regalo de Navidad. Cada uno sacrifica lo que más valora, con un final irónico y tierno."),
    ("The Last Leaf (Henry)", "the-last-leaf", "The Last Leaf", "O. Henry", 1907, "B1",
     "Johnsy, una joven pintora con neumonía, está convencida de que morirá cuando caiga la última hoja de la hiedra que ve por la ventana. Un viejo pintor vecino decide intervenir."),
    ("The Open Window (Saki)", "the-open-window", "The Open Window", "Saki", 1914, "B1",
     "Framton Nuttel, un hombre nervioso, visita a una familia en el campo para descansar. La sobrina de la casa, de quince años, le cuenta una historia trágica sobre una ventana abierta."),
    ("Poe's Tales of Mystery and Imagination/The Tell-Tale Heart", "the-tell-tale-heart", "The Tell-Tale Heart", "Edgar Allan Poe", 1843, "B2",
     "Un narrador que insiste en que no está loco cuenta cómo mató a un anciano por culpa de su ojo de buitre, y cómo el latido de un corazón lo delató."),
    ("Poe's Tales of Mystery and Imagination/The Cask of Amontillado", "the-cask-of-amontillado", "The Cask of Amontillado", "Edgar Allan Poe", 1846, "B2",
     "Durante el carnaval, Montresor atrae a Fortunato a sus bodegas con la excusa de probar un vino amontillado. Es una venganza planeada con todo detalle."),
    ("The Lady of the Barge/The Monkey's Paw", "the-monkeys-paw", "The Monkey's Paw", "W. W. Jacobs", 1902, "B2",
     "Un sargento trae de la India una pata de mono que concede tres deseos. La familia White pide doscientas libras, y descubre el precio de cada deseo."),
    ("The Celebrated Jumping Frog of Calaveras County, and Other Sketches/The Celebrated Jumping Frog of Calaveras County",
     "the-celebrated-jumping-frog", "The Celebrated Jumping Frog of Calaveras County", "Mark Twain", 1865, "C1",
     "Simon Wheeler cuenta, sin pausa y con humor, la historia de Jim Smiley, un apostador que entrenó a una rana saltarina. Su inglés coloquial del Oeste lo hace difícil y divertido."),
    ("Century Magazine/Volume 76/Issue 4/To Build a Fire", "to-build-a-fire", "To Build a Fire", "Jack London", 1908, "B2",
     "Un hombre camina solo por el Yukón a más de cincuenta grados bajo cero, acompañado solo por un perro. Encender un fuego se convierte en una cuestión de vida o muerte."),
    ("The Collected Works of Ambrose Bierce/Volume 2/An Occurrence at Owl Creek Bridge", "an-occurrence-at-owl-creek-bridge",
     "An Occurrence at Owl Creek Bridge", "Ambrose Bierce", 1890, "C1",
     "Durante la guerra de Secesión, Peyton Farquhar va a ser ahorcado en un puente. Cuando la cuerda se rompe, empieza una huida desesperada hacia su casa."),
    ("The Yellow Wall Paper", "the-yellow-wallpaper", "The Yellow Wallpaper", "Charlotte Perkins Gilman", 1892, "C1",
     "Una mujer a la que su marido, médico, obliga a descansar escribe un diario en una habitación con un papel pintado amarillo. Poco a poco cree ver a alguien atrapado detrás."),
]

BOOK = {
    "color": "azul", "genero": "Cuentos", "unidad": "cuentos", "tema": "el amor, el miedo, la ironía y la supervivencia, en su inglés original",
    "edition": "ediciones originales en inglés, 1843-1914",
    "resumen": [
        "Doce cuentos clásicos en su inglés original, para leer online gratis y practicar el idioma. Todos son de dominio público y están completos. Van ordenados de más fácil a más difícil, con un nivel orientativo del Marco Común Europeo (de A2 a C1) y un resumen en español al principio de cada uno.",
        "Hay cuentos de Navidad y de amor (The Gift of the Magi, The Last Leaf), de humor (The Open Window, The Celebrated Jumping Frog), de terror (The Tell-Tale Heart, The Cask of Amontillado, The Monkey's Paw) y de supervivencia (To Build a Fire). Los más exigentes, An Occurrence at Owl Creek Bridge y The Yellow Wallpaper, son también dos de los relatos más estudiados de la literatura en inglés.",
    ],
    "personajes": [],
    "ideas": [
        "Leer textos auténticos y completos, no adaptados, es una de las mejores formas de mejorar el inglés.",
        "Empieza por los cuentos de nivel A2-B1 y deja para el final los de C1.",
        "No hace falta entender cada palabra: el resumen en español de cada cuento ayuda a seguir la historia.",
        "Los cuentos son de los siglos XIX y XX, así que algunas palabras y grafías son antiguas (to-day, shew).",
    ],
    "faq": [
        ("¿Qué cuento corto en inglés es más fácil para empezar?",
         "The Happy Prince de Oscar Wilde, The Story of an Hour de Kate Chopin y The Gift of the Magi de O. Henry: frases claras, vocabulario sencillo y una historia fácil de seguir."),
        ("¿Son los cuentos completos?",
         "Sí. Son los textos originales completos, sin adaptar, revisados a partir de ediciones antiguas de dominio público."),
        ("¿Se pueden descargar en PDF?",
         "Sí. Todos los cuentos son de dominio público y puedes leerlos online o descargar el PDF de la colección completa."),
        ("¿Qué nivel de inglés hace falta?",
         "Depende del cuento. Cada uno indica un nivel orientativo, de A2 (básico) a C1 (avanzado). Los de Mark Twain y Charlotte Perkins Gilman son los más difíciles."),
    ],
}

TITLE_JUNK = re.compile(r"(public domain|copyright|^by [a-z .]+$|^author of |small, maynard|^the$|press ?boston|"
                        r"^he travels fastest who travels alone|^this story is reprinted from)", re.I)  # imprenta y nota editorial (Gilman), entradilla (London)


def is_heading_junk(text, title):
    plain = re.sub(r"[^a-z]", "", text.lower())
    target = re.sub(r"[^a-z]", "", title.lower())
    return bool(plain) and (target.startswith(plain) or plain.startswith(target) or plain == target + "i")


def clean_story(blocks, title):
    out = []
    for block in blocks:
        kind, text = block[:2], block[2:].strip()
        if kind == "H|" or TITLE_JUNK.search(text) or "Public domainPublic domain" in text:
            continue
        if kind == "P|" and len(text) < 90 and is_heading_junk(text, title):
            continue
        # Pie de ilustración en mayúsculas («"WHAT'S THAT?" CRIED THE OLD WOMAN.»); los números de sección se quedan.
        if kind == "P|" and not re.search(r"[a-z]", text) and not re.fullmatch(r"[IVX]+\.?", text):
            continue
        out.append(block)
    return out


def main():
    meta = json.loads((TEXTS / f"{SLUG}.json").read_text(encoding="utf-8"))
    blocks = (TEXTS / f"{SLUG}.txt").read_text(encoding="utf-8").split("\n")
    if len(meta["chapters"]) != len(STORIES):
        raise SystemExit(f"{len(meta['chapters'])} capítulos y {len(STORIES)} cuentos: vuelve a descargar con wikisource.py")
    # Recién descargado con wikisource.py, los capítulos aún tienen los slugs de las páginas de Wikisource.
    if [c["slug"] for c in meta["chapters"]] != [s[1] for s in STORIES]:
        new_blocks, chapters = [], []
        for chapter, (page, slug, title, author, year, level, summary) in zip(meta["chapters"], STORIES):
            story = clean_story(blocks[chapter["start"]:chapter["end"] + 1], title)
            start = len(new_blocks)
            new_blocks += [f"H|{title}"] + story
            chapters.append({"slug": slug, "title": f"{title} ({author})",
                             "summary": f"Nivel {level} · {author}, {year}. {summary}", "start": start, "end": len(new_blocks) - 1})
        meta["chapters"] = chapters
        (TEXTS / f"{SLUG}.txt").write_text("\n".join(new_blocks), encoding="utf-8")
    meta.update({
        "title": "Cuentos cortos en inglés", "author": "Wilde, Poe, O. Henry y otros", "author_route": "",
        "book_route": "/cuentos-cortos-en-ingles/", "translator": "", "language": "en",
        "source_url": "https://en.wikisource.org/wiki/" + STORIES[0][0].replace(" ", "_"),
        "sources": [{"title": s[2], "author": s[3], "url": "https://en.wikisource.org/wiki/" + s[0].replace(" ", "_")} for s in STORIES],
    })
    (TEXTS / f"{SLUG}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    clasicos.BOOKS = {SLUG: BOOK}
    clasicos.NUMBER_START = NUMBER_START
    clasicos.main()
    meta = json.loads((TEXTS / f"{SLUG}.json").read_text(encoding="utf-8"))
    meta["description"] = ("Cuentos cortos en inglés para leer online gratis: 12 clásicos completos de Wilde, O. Henry, Poe, "
                           "Jack London y otros, con nivel de A2 a C1 y resumen en español. También en PDF.")
    (TEXTS / f"{SLUG}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
