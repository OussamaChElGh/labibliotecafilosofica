"""Tercera tanda: clásicos escritos en inglés, en traducciones españolas de dominio público (mismo formato que clasicos.py).

python textos/fichas/clasicos3.py  →  ficha, descripción, portada y resúmenes de capítulo en textos/<slug>.json.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clasicos  # noqa: E402

NUMBER_START = 44
SHAKESPEARE = "/libros-pdf-gratis/autores/william-shakespeare/"

BOOKS = {
    "otelo-shakespeare": {
        "color": "negro", "genero": "Tragedia", "unidad": "actos", "autor": SHAKESPEARE,
        "tema": "los celos, la manipulación y la confianza traicionada",
        "resumen": [
            "Otelo, un general moro al servicio de Venecia, se casa en secreto con Desdémona, hija del senador Brabancio. Yago, su alférez, lo odia porque ha nombrado teniente a Casio en lugar de a él, y decide destruirlo. Cuando la guerra contra los turcos lleva a todos a Chipre, Yago empieza a tejer su trampa con la ayuda del ingenuo Rodrigo, que pretende a Desdémona.",
            "Yago consigue que Casio pierda su puesto en una pelea de borrachos y luego insinúa a Otelo que Desdémona lo engaña con él. La prueba es un pañuelo, regalo de Otelo, que Emilia, mujer de Yago, encuentra y entrega a su marido. Ciego de celos, Otelo ahoga a Desdémona en su lecho. Emilia descubre la verdad y Yago la mata; Otelo, al comprender su error, se quita la vida.",
        ],
        "personajes": [("Otelo", "General moro de Venecia, valiente y noble, pero incapaz de resistir los celos."),
                       ("Desdémona", "Esposa de Otelo, fiel e inocente, víctima de la intriga."),
                       ("Yago", "Alférez de Otelo, resentido y manipulador; uno de los grandes villanos del teatro."),
                       ("Casio", "Teniente de Otelo, a quien Yago convierte en supuesto amante de Desdémona."),
                       ("Emilia", "Mujer de Yago y dama de Desdémona, que acaba denunciando a su marido."),
                       ("Rodrigo", "Caballero veneciano enamorado de Desdémona, instrumento de Yago."),
                       ("Brabancio", "Senador, padre de Desdémona, que se opone a su boda.")],
        "ideas": ["Los celos como una pasión que destruye la razón.",
                  "La manipulación: Yago gana sin mentir del todo, sembrando sospechas.",
                  "El prejuicio contra el extranjero y el diferente.",
                  "La confianza y la apariencia: el honrado parece culpable y el culpable, honrado."],
        "faq": [("¿De qué trata Otelo?", "De un general moro al que su alférez Yago convence, con mentiras y un pañuelo, de que su esposa Desdémona le es infiel. Otelo la mata y después se suicida al conocer la verdad."),
                ("¿Por qué Yago odia a Otelo?", "Porque Otelo nombró teniente a Casio en lugar de a él. Yago también da a entender que sospecha que Otelo ha estado con su mujer, aunque sus motivos nunca quedan del todo claros."),
                ("¿Qué importancia tiene el pañuelo?", "Es el primer regalo de Otelo a Desdémona. Yago lo hace llegar a Casio y lo usa como falsa prueba de la infidelidad."),
                ("¿Cuándo se escribió Otelo?", "Hacia 1603-1604. Se publicó en 1622. Esta traducción en prosa es la de Marcelino Menéndez y Pelayo (1881).")],
    },
    "hamlet-shakespeare": {
        "color": "azul", "genero": "Tragedia", "unidad": "actos", "autor": SHAKESPEARE,
        "tema": "la venganza, la duda y la corrupción del poder",
        "resumen": [
            "En el castillo de Elsingor, el fantasma del rey de Dinamarca se aparece a su hijo, el príncipe Hamlet, y le revela que fue asesinado por su hermano Claudio, que ahora reina y se ha casado con la reina Gertrudis. Hamlet jura vengarlo y finge estar loco para ocultar sus planes, mientras el consejero Polonio cree que su locura nace del amor por su hija Ofelia.",
            "Para confirmar la culpa del rey, Hamlet hace representar una obra que imita el crimen, y Claudio se delata. Hamlet mata por error a Polonio, es enviado a Inglaterra y escapa de la muerte que le preparaban. Ofelia enloquece y se ahoga. Su hermano Laertes, aliado con Claudio, reta a Hamlet a un duelo con una espada envenenada. Mueren la reina, Laertes, Claudio y el propio Hamlet, y Fortimbrás de Noruega se queda con el trono.",
        ],
        "personajes": [("Hamlet", "Príncipe de Dinamarca, inteligente y melancólico, que duda antes de vengar a su padre."),
                       ("Claudio", "Tío de Hamlet, que mató a su hermano para quedarse con la corona y la reina."),
                       ("Gertrudis", "Reina de Dinamarca y madre de Hamlet, casada con Claudio."),
                       ("La sombra", "El fantasma del rey asesinado, que pide venganza."),
                       ("Polonio", "Consejero del rey, charlatán y entrometido."),
                       ("Ofelia", "Hija de Polonio, amada por Hamlet, que enloquece tras la muerte de su padre."),
                       ("Laertes", "Hermano de Ofelia, que busca vengar a su padre y a su hermana."),
                       ("Horacio", "Amigo fiel de Hamlet y testigo de toda la historia.")],
        "ideas": ["La duda ante la acción: pensar demasiado puede paralizar.",
                  "La venganza como un deber que lo arrastra todo a la muerte.",
                  "La corrupción del poder: algo está podrido en Dinamarca.",
                  "La apariencia y la verdad: la locura fingida, el teatro dentro del teatro."],
        "faq": [("¿De qué trata Hamlet?", "Del príncipe de Dinamarca, que descubre por el fantasma de su padre que su tío Claudio lo asesinó para quedarse con el trono y con la reina, y busca vengarse."),
                ("¿Por qué Hamlet tarda en vengarse?", "Porque duda: quiere estar seguro de la culpa de Claudio y reflexiona sobre la muerte, la moral y el sentido de la acción. Esa duda es el centro de la obra."),
                ("¿Dónde está el famoso «ser o no ser»?", "En el acto III, cuando Hamlet medita a solas sobre la vida, la muerte y el suicidio."),
                ("¿Quién tradujo esta versión?", "Leandro Fernández de Moratín, que la publicó en 1798 con el seudónimo de Inarco Celenio. Fue la primera traducción española hecha directamente del inglés.")],
    },
    "el-extrano-caso-del-dr-jekyll-stevenson": {
        "color": "burdeos", "genero": "Novela corta", "tema": "la doble naturaleza humana, el bien y el mal",
        "resumen": [
            "En Londres, el abogado Utterson oye hablar de un tal Edward Hyde, un hombre repugnante que ha pisoteado a una niña y que parece tener alguna relación misteriosa con su amigo, el respetado doctor Henry Jekyll. El testamento de Jekyll deja todos sus bienes a Hyde, y Utterson teme que sea víctima de un chantaje. Poco después, Hyde mata a golpes a sir Danvers Carew y desaparece.",
            "Jekyll se encierra en su laboratorio y su criado avisa a Utterson de que la voz que sale de allí no es la de su amo. Al forzar la puerta encuentran muerto a Hyde, con las ropas de Jekyll. Dos cartas lo explican todo: Jekyll había creado una pócima para separar su lado malvado, que tomaba la forma de Hyde, pero acabó transformándose sin querer y sin poder volver atrás.",
        ],
        "personajes": [("Doctor Henry Jekyll", "Médico respetado que intenta separar el bien del mal en su propia naturaleza."),
                       ("Edward Hyde", "La encarnación del lado malvado de Jekyll, violento y sin escrúpulos."),
                       ("Gabriel John Utterson", "Abogado y amigo de Jekyll, que investiga el misterio."),
                       ("Doctor Lanyon", "Antiguo amigo de Jekyll, que presencia una transformación y muere de la impresión."),
                       ("Poole", "Mayordomo fiel de Jekyll."),
                       ("Richard Enfield", "Pariente de Utterson, que cuenta el primer encuentro con Hyde.")],
        "ideas": ["Todo ser humano tiene una doble naturaleza: el bien y el mal conviven en él.",
                  "La represión de los deseos en la sociedad victoriana.",
                  "Los peligros de la ciencia sin límites morales.",
                  "La identidad: perder el control de uno mismo."],
        "faq": [("¿De qué trata El extraño caso del Dr. Jekyll y Mr. Hyde?", "De un médico que inventa una pócima para separar su lado malvado, que se convierte en Mr. Hyde. Con el tiempo pierde el control de la transformación y Hyde termina dominándolo."),
                ("¿Quién es Mr. Hyde?", "Es el propio doctor Jekyll transformado: la parte malvada de su personalidad, liberada de toda conciencia moral."),
                ("¿Cómo termina?", "Jekyll se queda sin los ingredientes de la pócima y no puede volver a su forma. Cuando Utterson entra en el laboratorio encuentra muerto a Hyde y la confesión escrita de Jekyll."),
                ("¿Cuándo se publicó?", "En 1886. Esta traducción española es de 1891.")],
    },
    "la-isla-del-tesoro-stevenson": {
        "color": "verde", "genero": "Novela de aventuras", "tema": "piratas, tesoros y el paso a la edad adulta",
        "resumen": [
            "Jim Hawkins ayuda a su madre en la posada del Almirante Benbow, en la costa de Inglaterra. Allí se aloja un viejo pirata, Billy Bones, que muere tras recibir la «mancha negra» y deja un cofre con el mapa de una isla donde el capitán Flint enterró su tesoro. El doctor Livesey y el caballero Trelawney fletan la goleta Hispaniola, con el capitán Smollett, y llevan a Jim como grumete.",
            "El cocinero del barco, John Silver el Largo, un pirata cojo y encantador, ha reclutado a gran parte de la tripulación para quedarse con el tesoro. Jim lo descubre escondido en un barril de manzanas. En la isla estalla la lucha entre los dos bandos. Jim conoce al náufrago Ben Gunn, que ya había desenterrado el tesoro, recupera el barco y ayuda a vencer a los piratas. Silver escapa con una parte del oro.",
        ],
        "personajes": [("Jim Hawkins", "Joven narrador, valiente e impulsivo, que vive la aventura de su vida."),
                       ("John Silver el Largo", "Cocinero cojo con un loro al hombro, líder secreto de los piratas."),
                       ("El doctor Livesey", "Médico sensato y justo, uno de los jefes de la expedición."),
                       ("El caballero Trelawney", "Rico y entusiasta, financia el viaje pero habla demasiado."),
                       ("El capitán Smollett", "Capitán de la Hispaniola, severo y desconfiado con razón."),
                       ("Ben Gunn", "Pirata abandonado en la isla durante tres años."),
                       ("Billy Bones", "Viejo pirata que guarda el mapa del tesoro.")],
        "ideas": ["La aventura como aprendizaje y paso a la edad adulta.",
                  "La ambigüedad moral: Silver es un villano y a la vez un personaje que atrae.",
                  "La codicia que mueve a piratas y caballeros.",
                  "La lealtad y la traición en el grupo."],
        "faq": [("¿De qué trata La isla del tesoro?", "De Jim Hawkins, un muchacho que encuentra el mapa del tesoro del pirata Flint y viaja a la isla en una expedición, donde tiene que enfrentarse a los piratas de John Silver."),
                ("¿Quién es John Silver el Largo?", "El cocinero de la Hispaniola, un pirata cojo y astuto que organiza el motín para quedarse con el tesoro."),
                ("¿Cómo termina La isla del tesoro?", "Los protagonistas vuelven a Inglaterra con el tesoro, que Ben Gunn había desenterrado, y Silver escapa en un puerto con una parte del dinero."),
                ("¿Cuándo se publicó?", "En 1883, después de aparecer por entregas. Esta traducción de Manuel Caballero es de 1901.")],
    },
    "el-sabueso-de-los-baskerville-conan-doyle": {
        "color": "ocre", "genero": "Novela policiaca", "tema": "un crimen, una leyenda y la razón contra la superstición",
        "resumen": [
            "El doctor Mortimer visita a Sherlock Holmes y al doctor Watson para contarles la muerte de sir Charles Baskerville, hallado sin vida en su finca de Devonshire con huellas de un perro gigantesco cerca del cuerpo. Una vieja leyenda dice que un sabueso infernal persigue a la familia desde que el malvado Hugo Baskerville raptó a una muchacha. Ahora llega de América el heredero, sir Henry.",
            "Holmes envía a Watson con sir Henry a la mansión, en medio de un páramo lleno de ciénagas y con un preso fugado por los alrededores. Mientras Watson investiga, Holmes vigila en secreto. Al final descubren que el naturalista Stapleton, pariente oculto de los Baskerville, usa un enorme perro cubierto de fósforo para matar a los herederos y quedarse con la fortuna. Stapleton huye y desaparece en la ciénaga.",
        ],
        "personajes": [("Sherlock Holmes", "El célebre detective, que resuelve el caso con lógica y observación."),
                       ("El doctor Watson", "Amigo de Holmes y narrador, protagonista de buena parte de la investigación."),
                       ("Sir Henry Baskerville", "Heredero de la finca, amenazado por la leyenda."),
                       ("Stapleton", "Naturalista aparentemente inofensivo, que esconde el verdadero plan."),
                       ("Beryl", "Presentada como hermana de Stapleton, en realidad es su esposa."),
                       ("El doctor Mortimer", "Médico de la familia, que acude a Holmes."),
                       ("Barrymore", "Mayordomo de la mansión, que guarda un secreto familiar.")],
        "ideas": ["La razón y la ciencia frente a la superstición.",
                  "El paisaje del páramo como fuente de miedo.",
                  "La herencia y la codicia como móvil del crimen.",
                  "La deducción: observar los detalles que otros pasan por alto."],
        "faq": [("¿De qué trata El sabueso de los Baskerville?", "De la investigación de Sherlock Holmes sobre la muerte de sir Charles Baskerville, que parece obra de un perro sobrenatural de una leyenda familiar."),
                ("¿Quién es el culpable?", "El naturalista Stapleton, un Baskerville oculto, que usa un perro enorme untado de fósforo para matar a los herederos y quedarse con la herencia."),
                ("¿Dónde transcurre?", "Sobre todo en el páramo de Dartmoor, en Devonshire, al suroeste de Inglaterra."),
                ("¿Cuándo se publicó?", "Por entregas entre 1901 y 1902. Esta traducción de Arturo Costa Álvarez es de 1909.")],
    },
}


if __name__ == "__main__":
    clasicos.BOOKS = BOOKS
    clasicos.NUMBER_START = NUMBER_START
    clasicos.main()
    for slug, data in BOOKS.items():
        config = clasicos.TEXTS / f"{slug}.json"
        if config.exists() and data.get("autor"):
            meta = json.loads(config.read_text(encoding="utf-8"))
            meta["author_route"] = data["autor"]
            config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
