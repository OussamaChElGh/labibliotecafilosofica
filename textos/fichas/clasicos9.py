"""Novena tanda: Las mil y una noches (tomo I) y el Diccionario filosófico de Voltaire (selección).

1. python wikisource.py "Las mil y una noches" las-mil-y-una-noches-tomo-1 --titulo "Las mil y una noches (Tomo I)" \
       --autor "Anónimo" --ficha /las-mil-y-una-noches-pdf/ --traductor "Vicente Blasco Ibáñez" --edicion "…" \
       --partes "<páginas del índice de El libro de las mil noches y una noche/Tomo I/Índice, sin repetir tras resolver redirecciones>"
   python wikisource.py "Diccionario Filosófico" voltaire-diccionario-filosofico --titulo "Diccionario filosófico (selección)" \
       --autor Voltaire --ruta-autor /libros-pdf-gratis/autores/voltaire/ --ficha /voltaire-diccionario-filosofico/ \
       --traductor "Cayetano Lanuza" --partes "<los artículos «… (DFV)» de Wikisource, en orden alfabético>"
   En Git Bash, anteponer MSYS_NO_PATHCONV=1.
2. python textos/fichas/clasicos9.py  →  ficha, descripción, portada y resúmenes de capítulo en textos/<slug>.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clasicos  # noqa: E402

NUMBER_START = 65

BOOKS = {
    "las-mil-y-una-noches-tomo-1": {
        "color": "azul", "genero": "Cuentos", "unidad": "noches", "tema": "Scheherezade, los genios y los cuentos de Oriente",
        "resumen": [
            "El rey Schahriar, traicionado por su esposa, decide casarse cada día con una joven y hacerla matar al amanecer. Scheherezade, la hija del visir, se ofrece a casarse con él y, la primera noche, empieza a contarle una historia que deja sin terminar al llegar el alba. Intrigado, el rey la deja vivir un día más para conocer el final, y así noche tras noche.",
            "Este primer tomo, en la traducción de Vicente Blasco Ibáñez de la versión francesa de J. C. Mardrus, reúne las primeras noches: la historia del mercader y el efrit, la del pescador y el efrit, la del mandadero y las tres doncellas con los tres saalukes, la de la mujer despedazada y las tres manzanas, la del visir Nureddin y la del jorobado, entre otras. Los cuentos se encajan unos dentro de otros, mezclan lo maravilloso con la vida de Bagdad y El Cairo y conservan la sensualidad y el humor del original árabe.",
        ],
        "personajes": [("Scheherezade", "Hija del visir, culta y astuta, que salva su vida contando historias."),
                       ("El rey Schahriar", "Rey que, por despecho, mata cada mañana a su nueva esposa."),
                       ("Doniazada", "Hermana pequeña de Scheherezade, que le pide cada noche un nuevo cuento."),
                       ("El efrit", "Genio poderoso y temible que aparece en varios cuentos."),
                       ("El califa Harún al-Raschid", "Califa de Bagdad que recorre la ciudad disfrazado."),
                       ("El jorobado", "Bufón cuya supuesta muerte enreda a medio Cairo.")],
        "ideas": ["El poder de la palabra: contar historias para salvar la vida.",
                  "Los relatos enmarcados, unos dentro de otros.",
                  "Lo maravilloso (genios, encantamientos, metamorfosis) junto a la vida cotidiana.",
                  "El destino, la astucia y la generosidad como motores de las historias."],
        "faq": [("¿De qué trata Las mil y una noches?", "Scheherezade se casa con el rey Schahriar, que mata a cada esposa al amanecer, y lo entretiene cada noche con un cuento que deja a medias. Así sobrevive mil y una noches."),
                ("¿Están aquí Aladino, Alí Babá y Simbad?", "No en este primer tomo. Simbad el marino aparece más adelante, y Aladino y Alí Babá los añadió Antoine Galland en su traducción francesa del siglo XVIII."),
                ("¿Quién hizo esta traducción?", "Vicente Blasco Ibáñez, que tradujo al español la versión francesa de J. C. Mardrus para la editorial Prometeo de Valencia."),
                ("¿Por qué solo está el tomo I?", "La obra completa ocupa más de mil noches y miles de páginas. Iremos añadiendo los siguientes tomos.")],
    },
    "voltaire-diccionario-filosofico": {
        "color": "ocre", "genero": "Ensayo", "unidad": "artículos", "tema": "la religión, la tolerancia y la razón",
        "resumen": [
            "El Diccionario filosófico es una colección de artículos breves ordenados alfabéticamente que Voltaire publicó en 1764 y amplió en ediciones posteriores. Bajo la apariencia de un diccionario, es un arma de la Ilustración: cada entrada le sirve para burlarse del fanatismo, de la superstición y de los abusos de la Iglesia y del poder, y para defender la tolerancia, la razón y la justicia.",
            "Esta selección reúne los artículos que hay transcritos de la traducción de Cayetano Lanuza (1825), noventa y tres entradas de las letras I a S, de «Impotencia» a «Sócrates»: Infierno, Inquisición, Intolerancia, Jesuitas, Libertad de pensar, Locura, Propiedad, Razón, Religión, Reliquias y muchas más. Voltaire escribe con ironía, ejemplos históricos y diálogos imaginarios, lo que hace del libro una lectura viva y polémica.",
        ],
        "personajes": [],
        "ideas": ["La tolerancia religiosa frente al fanatismo y la persecución.",
                  "La crítica a la Inquisición, al clero y a las supersticiones.",
                  "La ley natural y la justicia como algo común a todos los hombres.",
                  "La ironía como forma de pensar y de convencer."],
        "faq": [("¿Qué es el Diccionario filosófico de Voltaire?", "Un libro de artículos breves, ordenados de la A a la Z, en el que Voltaire critica el fanatismo religioso y defiende la razón y la tolerancia."),
                ("¿Cuándo se publicó?", "La primera edición, anónima, es de 1764, en Ginebra. Fue condenada y quemada en varios países."),
                ("¿Por qué es una selección?", "Wikisource solo tiene transcritos parte de los tomos de la traducción de 1825. Aquí están todos los artículos disponibles."),
                ("¿Qué dice Voltaire sobre la tolerancia?", "Que la intolerancia es contraria a la razón y a la humanidad, y que ningún hombre tiene derecho a perseguir a otro por sus creencias.")],
    },
}


if __name__ == "__main__":
    clasicos.BOOKS = BOOKS
    clasicos.NUMBER_START = NUMBER_START
    clasicos.main()
