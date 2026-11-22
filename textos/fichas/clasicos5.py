"""Quinta tanda: lecturas escolares muy buscadas (mismo formato que clasicos.py).

python textos/fichas/clasicos5.py  →  ficha, descripción, portada y resúmenes de capítulo en textos/<slug>.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clasicos  # noqa: E402

NUMBER_START = 54

BOOKS = {
    "cuentos-de-la-selva-horacio-quiroga": {
        "color": "verde", "genero": "Cuentos", "unidad": "cuentos", "tema": "los animales y la naturaleza de la selva de Misiones",
        "resumen": [
            "Ocho cuentos para niños ambientados en la selva de Misiones, en el norte de Argentina, donde Horacio Quiroga vivió muchos años. Los protagonistas son animales que hablan: una tortuga que salva a un hombre enfermo cargándolo hasta Buenos Aires, unos flamencos que acaban con las patas rojas por querer lucir medias, un loro que pierde las plumas, unos yacarés que defienden su río de un buque de guerra.",
            "Completan el libro la historia de una gama que queda ciega por desobedecer a su madre, la de dos cachorros de coatí y dos niños, la de las rayas que defienden a un hombre en el paso del Yabebirí y la de una abeja perezosa que aprende el valor del trabajo. Son fábulas sencillas, con humor y algo de crueldad, que enseñan a respetar la naturaleza.",
        ],
        "personajes": [("La tortuga gigante", "Lleva a cuestas al cazador enfermo que la había salvado."),
                       ("Los flamencos", "Vanidosos, se ponen medias de víboras de coral para ir a un baile."),
                       ("El loro pelado", "Loro charlatán que se queda sin plumas por culpa de un tigre."),
                       ("Los yacarés", "Cocodrilos del río que luchan contra un buque de guerra."),
                       ("La gama ciega", "Cervatilla que queda ciega por comer miel de avispas."),
                       ("La abeja haragana", "Abeja perezosa que aprende, tras una noche de miedo, a trabajar.")],
        "ideas": ["La selva como un mundo con sus propias leyes.",
                  "El respeto entre los animales y el ser humano.",
                  "Fábulas con enseñanza: la vanidad, la obediencia, el trabajo y la gratitud.",
                  "El humor y la crueldad de la naturaleza contados para niños."],
        "faq": [("¿Cuántos cuentos tiene Cuentos de la selva?", "Ocho: La tortuga gigante, Las medias de los flamencos, El loro pelado, La guerra de los yacarés, La gama ciega, Historia de dos cachorros de coatí y de dos cachorros de hombre, El paso del Yabebirí y La abeja haragana."),
                ("¿Dónde transcurren los cuentos?", "En la selva de Misiones, en el norte de Argentina, junto al río Paraná."),
                ("¿Por qué las medias de los flamencos son rojas?", "Según el cuento, los flamencos fueron a un baile con medias hechas de piel de víbora de coral. Las víboras los mordieron y desde entonces tienen las patas rojas de dolor."),
                ("¿Cuándo se publicó?", "En 1918, con el título Cuentos de la selva para los niños.")],
    },
    "cuentos-de-amor-de-locura-y-de-muerte-horacio-quiroga": {
        "color": "negro", "genero": "Cuentos", "unidad": "cuentos", "tema": "el amor, la locura y la muerte en la ciudad y en la selva",
        "resumen": [
            "Dieciocho cuentos que reunió Horacio Quiroga en 1917 y que lo consagraron como maestro del cuento latinoamericano. Muchos transcurren en la selva de Misiones, donde la naturaleza es indiferente y mortal: un hombre mordido por una víbora intenta llegar río abajo en canoa (A la deriva), un perro presiente la muerte de su amo (La insolación), unos peones viven explotados en los obrajes (Los mensú).",
            "Otros son relatos de terror psicológico y amor enfermizo: una joven esposa se consume misteriosamente en la cama (El almohadón de pluma), cuatro hermanos con discapacidad cometen un crimen atroz (La gallina degollada), un hombre ve morir su amor por orgullo (La muerte de Isolda). La influencia de Poe se nota en el gusto por el horror y por los finales sorprendentes.",
        ],
        "personajes": [("Paulino", "Protagonista de A la deriva, mordido por una víbora en el río Paraná."),
                       ("Alicia y Jordán", "La pareja de El almohadón de pluma."),
                       ("Los cuatro hijos idiotas y Bertita", "Protagonistas de La gallina degollada."),
                       ("Mr. Jones y sus perros", "El colono y los perros que ven llegar la Muerte en La insolación."),
                       ("Cayé y Podeley", "Los peones explotados de Los mensú.")],
        "ideas": ["La muerte como presencia constante, a menudo absurda.",
                  "La naturaleza de Misiones, hermosa e indiferente al ser humano.",
                  "La locura y el horror psicológico, a la manera de Poe.",
                  "El amor como pasión que destruye."],
        "faq": [("¿Cuáles son los cuentos más conocidos?", "El almohadón de pluma, A la deriva, La gallina degollada, La insolación y Los mensú son los más leídos en clase."),
                ("¿De qué trata El almohadón de pluma?", "De Alicia, una recién casada que enferma y se debilita día tras día sin causa aparente. Al morir descubren en su almohadón un parásito que le chupaba la sangre."),
                ("¿De qué trata A la deriva?", "De un hombre mordido por una víbora que baja el río en canoa en busca de ayuda mientras el veneno lo mata poco a poco."),
                ("¿Cuándo se publicó?", "En 1917, en Buenos Aires.")],
    },
    "el-si-de-las-ninas-moratin": {
        "color": "azul", "genero": "Comedia", "unidad": "actos", "tema": "los matrimonios concertados y la educación de las jóvenes",
        "resumen": [
            "En una posada de Alcalá de Henares, don Diego, un hombre rico de cincuenta y nueve años, ha concertado su boda con doña Francisca, una joven de dieciséis recién salida del convento. La madre de la muchacha, doña Irene, está encantada con un partido tan ventajoso. Pero Francisca está enamorada de un joven oficial al que conoció en Guadalajara y que se hace llamar don Félix.",
            "Avisado por carta, el joven llega a Alcalá y resulta ser don Carlos, sobrino de don Diego, que obedece a su tío y se marcha. Una serenata nocturna y una carta descubren el secreto. Don Diego comprende que Francisca solo le daría un «sí» forzado por la obediencia, renuncia a la boda y bendice la unión de los dos jóvenes.",
        ],
        "personajes": [("Don Diego", "Hombre maduro, rico y sensato, que acaba renunciando a casarse con la joven."),
                       ("Doña Francisca (Paquita)", "Joven educada para obedecer, enamorada de don Carlos."),
                       ("Doña Irene", "Madre de Francisca, interesada y charlatana."),
                       ("Don Carlos (don Félix)", "Oficial, sobrino de don Diego, enamorado de Francisca."),
                       ("Rita", "Criada y confidente de Francisca."),
                       ("Calamocha", "Criado de don Carlos."),
                       ("Simón", "Criado de don Diego.")],
        "ideas": ["La crítica a los matrimonios por interés entre personas de edad muy distinta.",
                  "Una educación que enseña a las jóvenes a mentir y a ocultar lo que sienten.",
                  "La razón y el sentido común de la Ilustración.",
                  "La comedia neoclásica: unidad de lugar, tiempo y acción."],
        "faq": [("¿De qué trata El sí de las niñas?", "De la boda concertada entre don Diego, de casi sesenta años, y la joven Francisca, que ama a otro. Al final don Diego descubre que su rival es su sobrino y renuncia a casarse."),
                ("¿Qué significa el título?", "Se refiere al «sí» que las jóvenes dan en el altar por obediencia a sus madres, aunque no lo sientan."),
                ("¿Dónde y cuándo transcurre?", "En una posada de Alcalá de Henares, en apenas unas horas, entre la tarde y la mañana siguiente."),
                ("¿Cuándo se estrenó?", "En 1806, en Madrid, con un enorme éxito. Esta edición es la de París de 1830.")],
    },
    "luces-de-bohemia-valle-inclan": {
        "color": "negro", "genero": "Esperpento", "unidad": "escenas", "tema": "la última noche de un poeta ciego en un Madrid absurdo",
        "resumen": [
            "Max Estrella, poeta ciego y hambriento, pasa su última noche recorriendo Madrid con su amigo don Latino de Hispalis, un bohemio mezquino. Van de la librería de Zaratustra a la taberna de Pica Lagartos, de la Buñolería Modernista a la comisaría, donde Max es detenido por escándalo. En el calabozo conoce a un preso catalán que va a ser ejecutado sin juicio.",
            "Max visita al ministro, antiguo compañero de bohemia, que le ofrece un sueldo. Al amanecer, tras discutir sobre el esperpento como única forma de retratar la tragedia de España, muere de frío en el portal de su casa, mientras don Latino le roba la cartera con el billete de lotería premiado. La obra termina con el entierro y el suicidio de su mujer y su hija.",
        ],
        "personajes": [("Max Estrella", "Poeta ciego, orgulloso y lúcido, inspirado en Alejandro Sawa."),
                       ("Don Latino de Hispalis", "Compañero de Max, adulador, cobarde y traidor."),
                       ("Madama Collet", "Mujer francesa de Max."),
                       ("Claudinita", "Hija de Max."),
                       ("Zaratustra", "Librero avaro que engaña a Max."),
                       ("El preso catalán", "Obrero anarquista que comparte calabozo con Max y es asesinado."),
                       ("El ministro", "Antiguo amigo de bohemia de Max, ahora en el poder.")],
        "ideas": ["El esperpento: deformar la realidad para mostrar su verdad grotesca.",
                  "La crítica a la España de principios del siglo XX: corrupción, censura y miseria.",
                  "La bohemia literaria y la miseria de los escritores.",
                  "La muerte y el absurdo como destino."],
        "faq": [("¿De qué trata Luces de bohemia?", "De la última noche de Max Estrella, un poeta ciego y pobre que recorre Madrid con don Latino hasta morir al amanecer en la puerta de su casa."),
                ("¿Qué es el esperpento?", "La estética que Valle-Inclán define en la escena XII: los héroes clásicos reflejados en los espejos cóncavos del callejón del Gato, para mostrar la realidad deformada de España."),
                ("¿Cuántas escenas tiene?", "Quince. La versión definitiva, de 1924, añadió tres escenas a la primera de 1920."),
                ("¿En quién se inspira Max Estrella?", "En el escritor Alejandro Sawa, que murió ciego y en la miseria en Madrid en 1909.")],
    },
}


if __name__ == "__main__":
    clasicos.BOOKS = BOOKS
    clasicos.NUMBER_START = NUMBER_START
    clasicos.main()
