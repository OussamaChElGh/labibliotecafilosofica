"""Sexta tanda: Bécquer y Machado (mismo formato que clasicos.py).

python textos/fichas/clasicos6.py  →  ficha, descripción, portada y resúmenes de capítulo en textos/<slug>.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clasicos  # noqa: E402

NUMBER_START = 58

BOOKS = {
    "leyendas-gustavo-adolfo-becquer": {
        "color": "negro", "genero": "Leyendas", "unidad": "leyendas", "tema": "lo sobrenatural, el amor imposible y la Edad Media",
        "resumen": [
            "Las Leyendas son relatos breves en prosa poética que Bécquer publicó en periódicos entre 1858 y 1864. Casi todas se sitúan en una Edad Media legendaria, en Soria, Toledo o el Moncayo, y mezclan la tradición popular con lo fantástico: almas en pena, apariciones, maldiciones y mujeres que no son lo que parecen.",
            "En El monte de las ánimas, Alonso muere al buscar una cinta en el monte la noche de difuntos. En Los ojos verdes, Fernando se arroja a un lago tras una mujer de agua. En El rayo de luna, Manrique persigue a una dama que resulta ser un reflejo. En Maese Pérez el organista, el alma de un músico vuelve a tocar en Nochebuena. La belleza ideal y el deseo de lo inalcanzable llevan casi siempre a la locura o a la muerte.",
        ],
        "personajes": [("Alonso y Beatriz", "Protagonistas de El monte de las ánimas."),
                       ("Fernando de Argensola", "Joven cazador seducido por la mujer del lago en Los ojos verdes."),
                       ("Manrique", "Soñador que persigue un rayo de luna creyéndolo una mujer."),
                       ("Maese Pérez", "Organista ciego cuyo espíritu vuelve a tocar en Nochebuena."),
                       ("Constanza", "La corza blanca, joven que se transforma en animal.")],
        "ideas": ["Lo sobrenatural irrumpe en la vida cotidiana.",
                  "La búsqueda de un ideal inalcanzable que lleva a la perdición.",
                  "El amor y la mujer como misterio, a menudo peligroso.",
                  "La tradición popular y la Edad Media vistas por el Romanticismo."],
        "faq": [("¿Cuáles son las leyendas de Bécquer más conocidas?", "El monte de las ánimas, Los ojos verdes, El rayo de luna, Maese Pérez el organista y El miserere son las más leídas en clase."),
                ("¿De qué trata El monte de las ánimas?", "Beatriz pide a su primo Alonso que vaya al monte en la noche de difuntos a recuperar una banda que ha perdido. Alonso no vuelve, y a la mañana siguiente Beatriz encuentra la banda ensangrentada en su habitación y muere de terror."),
                ("¿A qué movimiento pertenecen?", "Al Romanticismo tardío español. Bécquer es, junto con Rosalía de Castro, el gran puente hacia la poesía moderna."),
                ("¿Cuándo se publicaron?", "Por separado en la prensa entre 1858 y 1864. Se reunieron en las Obras de 1871, publicadas tras la muerte del autor.")],
    },
    "campos-de-castilla-antonio-machado": {
        "color": "ocre", "genero": "Poesía", "unidad": "poemas", "tema": "el paisaje de Castilla, España y la memoria de Leonor",
        "resumen": [
            "Campos de Castilla es el gran libro de Antonio Machado. Nace de sus años como profesor en Soria, donde el paisaje castellano, sus encinas, sus álamos y el río Duero se convierten en símbolo de una España pobre, dura y decadente. Poemas como A orillas del Duero, Por tierras de España o Campos de Soria unen la descripción de la tierra con la reflexión sobre el país.",
            "La muerte de su joven esposa, Leonor, en 1912, tiñe de dolor los poemas escritos después en Baeza: A un olmo seco, Caminos, Allá en las tierras altas o A José María Palacio recuerdan Soria desde la distancia. El libro se cierra con los Proverbios y cantares, breves reflexiones filosóficas entre las que está el famoso «Caminante, no hay camino, se hace camino al andar».",
        ],
        "personajes": [],
        "ideas": ["El paisaje castellano como reflejo del alma y de la historia de España.",
                  "La crítica a la España atrasada, en la línea de la Generación del 98.",
                  "El tiempo, la memoria y la muerte.",
                  "El amor y el duelo por Leonor."],
        "faq": [("¿De dónde es «Caminante, no hay camino»?", "Del poema XXIX de Proverbios y cantares, dentro de Campos de Castilla."),
                ("¿Qué significa A un olmo seco?", "Machado ve brotar hojas verdes en un olmo viejo y podrido junto al Duero y lo convierte en símbolo de su esperanza de que Leonor, gravemente enferma, se recupere."),
                ("¿Quién era Leonor?", "Leonor Izquierdo, la joven con la que Machado se casó en Soria en 1909. Murió de tuberculosis en 1912, con dieciocho años."),
                ("¿Cuándo se publicó?", "La primera edición es de 1912. La de 1917, recogida en Poesías completas, añade los poemas escritos en Baeza.")],
    },
}


if __name__ == "__main__":
    clasicos.BOOKS = BOOKS
    clasicos.NUMBER_START = NUMBER_START
    clasicos.main()
