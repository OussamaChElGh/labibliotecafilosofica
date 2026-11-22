"""Textos editoriales de los diálogos de Platón: ficha, resumen, personajes y preguntas.

python textos/fichas/platon.py  →  los añade a textos/<slug>.json (no toca capítulos ni texto).
"""
import json
from pathlib import Path

TEXTS = Path(__file__).resolve().parents[1]

BOOKS = {
    "criton-platon": {
        "color": "azul",
        "tema": "la obediencia a las leyes",
        "resumen": [
            "Critón visita a Sócrates en la cárcel al amanecer, pocos días antes de la ejecución. Ha sobornado al carcelero y tiene todo listo para la fuga: hay dinero, amigos dispuestos a acogerle en Tesalia y, dice, la gente pensará que sus amigos no quisieron salvarle.",
            "Sócrates no discute por miedo ni por afecto, sino por razones: lo que importa no es la opinión de la mayoría, sino vivir bien, es decir, con justicia. Nunca se debe responder a una injusticia con otra. Para mostrarlo imagina que las Leyes de Atenas le hablan: le han dado la vida, la educación y la ciudad, y él aceptó vivir bajo ellas durante setenta años. Huir sería romper ese pacto. Critón no sabe qué responder y Sócrates decide quedarse.",
        ],
        "personajes": [("Sócrates", "Condenado a muerte, espera en la cárcel el regreso del barco sagrado de Delos."),
                       ("Critón", "Amigo de toda la vida, rico y leal, que ha preparado su fuga.")],
        "ideas": ["No hay que dejarse guiar por la opinión de la mayoría, sino por la de quien sabe.",
                  "No se debe cometer injusticia nunca, ni siquiera para devolver una injusticia recibida.",
                  "Quien vive en una ciudad acepta un pacto con sus leyes; incumplirlo es injusto."],
        "faq": [("¿De qué trata el Critón de Platón?", "Del deber de obedecer las leyes. Critón propone a Sócrates escapar de la cárcel y Sócrates explica por qué no lo hará, aunque su condena sea injusta."),
                ("¿Por qué Sócrates no huye de la cárcel?", "Porque huir sería cometer una injusticia contra las leyes de Atenas, con las que se comprometió al vivir en la ciudad, y para Sócrates nunca es lícito devolver mal por mal."),
                ("¿Qué relación tiene el Critón con la Apología y el Fedón?", "Forman una secuencia: la Apología es el juicio, el Critón transcurre en la cárcel días antes de la ejecución y el Fedón narra el último día y la muerte de Sócrates.")],
    },
    "eutifron-platon": {
        "color": "ocre",
        "tema": "la piedad",
        "resumen": [
            "A las puertas del tribunal, donde acaba de ser acusado de impiedad, Sócrates se encuentra con Eutifrón, un adivino que va a denunciar a su propio padre por la muerte de un jornalero. Eutifrón está tan seguro de saber qué es lo piadoso que Sócrates le pide que se lo enseñe.",
            "Las definiciones van cayendo una tras otra: lo piadoso es lo que hago yo, lo que agrada a los dioses, lo que agrada a todos los dioses. Sócrates plantea entonces la pregunta que ha dado fama al diálogo: ¿algo es piadoso porque los dioses lo aman, o los dioses lo aman porque es piadoso? Eutifrón da vueltas en círculo y acaba marchándose con prisa, sin haber definido nada.",
        ],
        "personajes": [("Sócrates", "Acaba de ser acusado de impiedad por Meleto y va camino del juicio."),
                       ("Eutifrón", "Adivino seguro de sí mismo que denuncia a su padre por homicidio.")],
        "ideas": ["Saber poner ejemplos no es saber definir: hace falta encontrar la esencia común.",
                  "El dilema de Eutifrón: ¿lo bueno es bueno porque Dios lo quiere, o Dios lo quiere porque es bueno?",
                  "Quien cree saber sin saber es el más difícil de enseñar."],
        "faq": [("¿Qué es el dilema de Eutifrón?", "La pregunta de si algo es piadoso porque los dioses lo aman o los dioses lo aman porque es piadoso. Sigue discutiéndose hoy en ética y filosofía de la religión."),
                ("¿Cuándo transcurre el Eutifrón?", "Justo antes del juicio de Sócrates, por lo que suele leerse antes de la Apología, el Critón y el Fedón."),
                ("¿Se llega a una definición de piedad?", "No. Como en muchos diálogos tempranos de Platón, termina en aporía: todas las definiciones fallan y la pregunta queda abierta.")],
    },
    "fedon-platon": {
        "color": "negro",
        "tema": "la inmortalidad del alma",
        "resumen": [
            "Fedón cuenta a Equécrates el último día de Sócrates en la cárcel. Rodeado de sus amigos, Sócrates explica por qué el filósofo no teme a la muerte: filosofar es prepararse para morir, porque es separar el alma de los engaños del cuerpo.",
            "Simmias y Cebes, dos jóvenes tebanos, no se conforman y le exigen pruebas. Sócrates ofrece varios argumentos de la inmortalidad del alma: el de los contrarios, el de la reminiscencia, el de la afinidad del alma con las Ideas y, el último, el de la Idea de vida, que no puede admitir la muerte. Tras un mito sobre el destino de las almas, Sócrates bebe la cicuta con serenidad. El diálogo termina con sus últimas palabras: «Critón, debemos un gallo a Asclepio».",
        ],
        "personajes": [("Fedón", "Discípulo de Sócrates, narra lo que vio el día de su muerte."),
                       ("Equécrates", "Pitagórico de Fliunte que le pide el relato."),
                       ("Sócrates", "Pasa su último día conversando sobre el alma."),
                       ("Simmias y Cebes", "Jóvenes tebanos que ponen a prueba cada argumento."),
                       ("Critón", "Amigo íntimo que atiende a Sócrates hasta el final.")],
        "ideas": ["Filosofar es aprender a morir: liberar el alma de las distracciones del cuerpo.",
                  "Conocer es recordar lo que el alma vio antes de nacer (reminiscencia).",
                  "Las Ideas existen por sí mismas y son la causa de las cosas que vemos."],
        "faq": [("¿De qué trata el Fedón de Platón?", "Del último día de Sócrates y de la inmortalidad del alma. Es el diálogo que narra su muerte por la cicuta."),
                ("¿Cuáles son los argumentos de la inmortalidad del alma en el Fedón?", "El de los contrarios, el de la reminiscencia, el de la afinidad del alma con lo invisible y el de la Idea de vida, que no admite su contrario."),
                ("¿Cuáles fueron las últimas palabras de Sócrates?", "Según el Fedón, «Critón, debemos un gallo a Asclepio; págalo, no lo olvides»."),
                ("¿Quién narra el Fedón?", "Fedón de Elis, que estuvo presente, se lo cuenta a Equécrates en Fliunte.")],
    },
    "fedro-platon": {
        "color": "verde",
        "tema": "el amor, el alma y la retórica",
        "resumen": [
            "Sócrates y Fedro salen de Atenas y se tumban a la sombra de un plátano junto al río Iliso. Fedro le lee un discurso de Lisias que sostiene que es mejor complacer a quien no está enamorado. Sócrates responde primero con otro discurso en la misma línea, pero se arrepiente y pronuncia una palinodia en honor del Amor.",
            "En ella aparece la imagen más famosa del diálogo: el alma es como un carro tirado por dos caballos alados, uno noble y otro indócil, guiado por un auriga. El amor es una locura divina que hace recordar la belleza verdadera. La segunda parte cambia de tema y pregunta qué distingue la buena retórica de la mala, y termina con el mito de Theuth sobre la invención de la escritura, que según Sócrates da apariencia de saber pero debilita la memoria.",
        ],
        "personajes": [("Sócrates", "Sale por una vez de la ciudad y se deja inspirar por el lugar."),
                       ("Fedro", "Joven admirador de los discursos, entusiasta de Lisias.")],
        "ideas": ["El mito del carro alado: el alma dividida entre razón, ánimo y deseo.",
                  "El amor como locura divina que despierta el recuerdo de la belleza.",
                  "La crítica de la escritura: un texto no puede responder a quien le pregunta."],
        "faq": [("¿Qué es el mito del carro alado?", "Una imagen del Fedro en la que el alma es un auriga que conduce dos caballos, uno dócil y otro rebelde. Representa la lucha interior entre razón y deseo."),
                ("¿Qué dice el Fedro sobre la escritura?", "Que es un remedio para recordar, no para saber, y que un texto escrito no puede defenderse ni contestar preguntas como lo hace un interlocutor vivo."),
                ("¿Dónde transcurre el Fedro?", "Fuera de las murallas de Atenas, a orillas del río Iliso, algo raro en Platón, cuyos diálogos suelen ocurrir en la ciudad.")],
    },
    "gorgias-platon": {
        "color": "burdeos",
        "tema": "la retórica y la justicia",
        "resumen": [
            "Sócrates pregunta al famoso orador Gorgias qué es exactamente la retórica. La conversación pasa después a su discípulo Polo y, finalmente, a Calicles, un político ambicioso que defiende sin rodeos que lo justo por naturaleza es que el más fuerte domine al más débil y satisfaga todos sus deseos.",
            "Frente a él, Sócrates sostiene tesis que parecen absurdas: que es peor cometer injusticia que sufrirla, que el castigo justo es un bien para quien lo recibe y que la retórica que solo busca agradar es una adulación, como la cocina frente a la medicina. El diálogo termina con un mito sobre el juicio de las almas después de la muerte.",
        ],
        "personajes": [("Sócrates", "Defiende que la vida justa es la única feliz."),
                       ("Gorgias", "Célebre maestro de retórica de Leontinos."),
                       ("Polo", "Joven discípulo de Gorgias, impetuoso."),
                       ("Calicles", "Ateniense que defiende la ley del más fuerte."),
                       ("Querefonte", "Amigo de Sócrates que le acompaña.")],
        "ideas": ["Es peor cometer injusticia que sufrirla.",
                  "La retórica sin conocimiento es adulación: busca el placer, no el bien.",
                  "La ley del más fuerte frente a la ley de la justicia."],
        "faq": [("¿De qué trata el Gorgias de Platón?", "De qué es la retórica y de cuál es la mejor forma de vivir: la del poder y el placer que defiende Calicles o la de la justicia que defiende Sócrates."),
                ("¿Qué defiende Calicles en el Gorgias?", "Que por naturaleza es justo que el fuerte domine al débil y que las leyes son un invento de los débiles para frenar a los fuertes."),
                ("¿Por qué Sócrates dice que es peor cometer injusticia que sufrirla?", "Porque la injusticia daña el alma de quien la comete, que es lo más valioso que tenemos.")],
    },
    "carmides-platon": {
        "color": "verde",
        "tema": "la templanza",
        "resumen": [
            "Sócrates vuelve a Atenas tras la batalla de Potidea y entra en la palestra de Táureas. Allí conoce al joven Cármides, admirado por su belleza, y su tutor Critias le pide que le cure un dolor de cabeza. Sócrates dice conocer un remedio, pero solo funciona si el alma del paciente tiene templanza.",
            "Así empieza la búsqueda: ¿qué es la templanza o sabiduría moral (sophrosyne)? Cármides propone que es tranquilidad y luego pudor; Critias, que es hacer lo propio y finalmente conocerse a uno mismo, un saber de los saberes. Sócrates muestra las dificultades de cada definición y el diálogo termina sin respuesta. El lector sabe además que Cármides y Critias serían después miembros de los Treinta Tiranos.",
        ],
        "personajes": [("Sócrates", "Narra la conversación y dirige la búsqueda."),
                       ("Cármides", "Joven de gran belleza, tío materno de Platón."),
                       ("Critias", "Primo de Cármides, intelectual brillante y futuro tirano.")],
        "ideas": ["La salud del cuerpo depende de la del alma.",
                  "Conocerse a uno mismo es más difícil de lo que parece.",
                  "Un saber que solo se conoce a sí mismo no sirve para nada."],
        "faq": [("¿Qué es la templanza en el Cármides?", "La sophrosyne, una virtud que combina moderación, sensatez y conocimiento de uno mismo. El diálogo busca definirla sin conseguirlo del todo."),
                ("¿Quiénes eran Cármides y Critias?", "Dos parientes de Platón. Años después del diálogo formaron parte del gobierno de los Treinta Tiranos de Atenas."),
                ("¿Cómo termina el Cármides?", "En aporía: ninguna definición resiste el examen y Sócrates reconoce que no han encontrado qué es la templanza.")],
    },
    "laques-platon": {
        "color": "ocre",
        "tema": "el valor",
        "resumen": [
            "Lisímaco y Melesias quieren dar a sus hijos la mejor educación y preguntan a dos generales famosos, Nicias y Laques, si conviene que aprendan a combatir con armas. Como los generales no se ponen de acuerdo, piden a Sócrates que intervenga.",
            "Sócrates reconduce la discusión: antes de saber cómo educar en la virtud hay que saber qué es, empezando por el valor. Laques define el valor como mantenerse firme en el puesto y luego como una firmeza del alma; Nicias, como un saber sobre lo que hay que temer y lo que no. Ninguna definición sobrevive y todos acaban admitiendo que necesitan un maestro, empezando por ellos mismos.",
        ],
        "personajes": [("Sócrates", "Reconocido por su valor en la retirada de Delio."),
                       ("Laques", "General ateniense, hombre práctico."),
                       ("Nicias", "General ateniense, más reflexivo."),
                       ("Lisímaco y Melesias", "Padres preocupados por la educación de sus hijos.")],
        "ideas": ["Para enseñar una virtud primero hay que saber qué es.",
                  "El valor no es solo resistir: también requiere saber.",
                  "Reconocer la propia ignorancia es el inicio de la educación."],
        "faq": [("¿Qué es el valor según el Laques?", "El diálogo no da una respuesta definitiva. Laques lo ve como firmeza y Nicias como el conocimiento de lo temible; ambas definiciones resultan incompletas."),
                ("¿Quiénes eran Laques y Nicias?", "Dos generales atenienses reales de la guerra del Peloponeso."),
                ("¿Por qué el Laques es un buen diálogo para empezar a leer a Platón?", "Porque es corto, accesible y muestra con claridad el método socrático de preguntar y refutar.")],
    },
    "lisis-platon": {
        "color": "azul",
        "tema": "la amistad",
        "resumen": [
            "Camino del Liceo, Sócrates se encuentra con Hipotales, enamorado del joven Lisis, que le pide consejo para conquistarlo. Sócrates le muestra cómo hablarle y entra en la palestra, donde conversa con Lisis y su amigo Menéxeno.",
            "La pregunta es qué es un amigo: ¿quien ama o quien es amado? ¿Se hacen amigos los semejantes o los contrarios? ¿Lo bueno es amigo de lo bueno? Sócrates explora cada posibilidad y llega a la idea de un primer objeto amado por el que queremos todo lo demás, pero las dudas vuelven y los pedagogos interrumpen la charla. Sócrates concluye que se tienen por amigos sin haber sabido decir qué es un amigo.",
        ],
        "personajes": [("Sócrates", "Narra el encuentro y conversa con los jóvenes."),
                       ("Lisis", "Muchacho noble y reflexivo."),
                       ("Menéxeno", "Amigo de Lisis, aficionado a discutir."),
                       ("Hipotales", "Joven enamorado de Lisis.")],
        "ideas": ["La amistad plantea si se quiere lo semejante o lo contrario.",
                  "Queremos las cosas por algo que amamos en primer lugar.",
                  "La amistad nace de una carencia: de lo que es propio y nos falta."],
        "faq": [("¿De qué trata el Lisis de Platón?", "De la amistad. Sócrates pregunta a dos jóvenes qué hace que alguien sea amigo de otro."),
                ("¿Qué relación tiene el Lisis con El banquete?", "Ambos tratan del amor y del deseo de lo que falta; el Lisis plantea preguntas que El banquete retoma con más amplitud."),
                ("¿Se define la amistad en el Lisis?", "No del todo. El diálogo termina reconociendo que no han sabido decir qué es un amigo.")],
    },
    "ion-platon": {
        "color": "burdeos",
        "tema": "la poesía y la inspiración",
        "resumen": [
            "Ion, un rapsoda que recita y comenta a Homero, acaba de ganar un concurso en Epidauro. Presume de ser el mejor intérprete de Homero, pero reconoce que cuando se habla de otros poetas se aburre y no sabe qué decir.",
            "Sócrates saca la conclusión: si fuera un arte, Ion sabría hablar de todos los poetas. Lo que mueve al rapsoda y al poeta no es un saber sino una inspiración divina, como el imán que atrae una cadena de anillos de hierro: la Musa inspira al poeta, el poeta al rapsoda y el rapsoda al público. Ion prefiere ser llamado divino antes que reconocer que no sabe.",
        ],
        "personajes": [("Sócrates", "Interroga con ironía al rapsoda."),
                       ("Ion", "Rapsoda de Éfeso, orgulloso de su talento para recitar a Homero.")],
        "ideas": ["La poesía nace de la inspiración divina, no del conocimiento.",
                  "La imagen del imán: la inspiración pasa de la Musa al poeta y del poeta al público.",
                  "Hablar bien de algo no equivale a saberlo."],
        "faq": [("¿De qué trata el Ion de Platón?", "De si los poetas y los rapsodas actúan por conocimiento o por inspiración divina."),
                ("¿Qué es la metáfora del imán en el Ion?", "Sócrates compara la inspiración con un imán que transmite su fuerza a una cadena de anillos: la Musa, el poeta, el rapsoda y los oyentes."),
                ("¿Qué es un rapsoda?", "Un recitador profesional de poesía épica, sobre todo de Homero, que actuaba en fiestas y concursos.")],
    },
    "eutidemo-platon": {
        "color": "ocre",
        "tema": "la erística y la sofística",
        "resumen": [
            "Sócrates cuenta a Critón la conversación que tuvo el día anterior con dos hermanos, Eutidemo y Dionisodoro, antiguos maestros de lucha convertidos en maestros de discusión. Aseguran poder enseñar la virtud más rápido que nadie.",
            "Su método consiste en atrapar al interlocutor con juegos de palabras y trampas lógicas, sea cual sea su respuesta. Sócrates intercala con el joven Clinias un ejemplo de diálogo verdadero sobre la felicidad y el saber. El contraste es cómico y deja ver la diferencia entre la filosofía, que busca la verdad, y la erística, que solo busca ganar.",
        ],
        "personajes": [("Sócrates", "Narra la escena a Critón."),
                       ("Eutidemo y Dionisodoro", "Hermanos sofistas, maestros de la discusión."),
                       ("Clinias", "Joven al que todos quieren educar."),
                       ("Critón", "Amigo de Sócrates, preocupado por la educación de su hijo.")],
        "ideas": ["Ganar una discusión no es lo mismo que tener razón.",
                  "La felicidad depende del buen uso de las cosas, y para eso hace falta saber.",
                  "La filosofía se distingue de la sofística por su fin: la verdad."],
        "faq": [("¿Qué es la erística?", "El arte de discutir para vencer, sin importar la verdad, usando equívocos y trampas verbales. El Eutidemo la retrata con humor."),
                ("¿Es el Eutidemo un diálogo cómico?", "Sí, es uno de los más divertidos de Platón, por los absurdos razonamientos de los dos sofistas."),
                ("¿Qué enseña Sócrates a Clinias?", "Que todos queremos ser felices y que para usar bien los bienes hace falta sabiduría, por lo que hay que amar el saber.")],
    },
    "primer-alcibiades-platon": {
        "color": "burdeos",
        "tema": "el conocimiento de uno mismo",
        "resumen": [
            "Alcibíades, joven, rico, bello y ambicioso, está a punto de entrar en la política de Atenas. Sócrates, que le ha seguido en silencio durante años, por fin le habla: ¿qué va a enseñar a los atenienses sobre lo justo y lo conveniente, si nunca lo ha aprendido?",
            "Alcibíades descubre que no sabe lo que creía saber y que sus rivales de verdad, los reyes de Esparta y Persia, están mucho mejor educados. Sócrates le muestra que antes de gobernar a otros hay que ocuparse de uno mismo, y que uno mismo es el alma. El diálogo explica así el precepto délfico «conócete a ti mismo» con la imagen del ojo que solo se ve reflejado en otro ojo.",
        ],
        "personajes": [("Sócrates", "El único que ama a Alcibíades por su alma y no por su belleza."),
                       ("Alcibíades", "Joven aristócrata ateniense, sobrino de Pericles, decidido a gobernar.")],
        "ideas": ["Para gobernar a otros primero hay que conocerse y cuidarse a uno mismo.",
                  "El ser humano es su alma; el cuerpo es su instrumento.",
                  "El alma se conoce mirándose en otra alma, como el ojo en la pupila de otro."],
        "faq": [("¿De qué trata el Primer Alcibíades?", "Del cuidado de uno mismo y del «conócete a ti mismo», en una conversación entre Sócrates y el joven Alcibíades antes de entrar en política."),
                ("¿Es auténtico el Primer Alcibíades?", "Su autoría se discute desde el siglo XIX, pero en la Antigüedad se consideraba la mejor introducción a la filosofía de Platón."),
                ("¿Quién fue Alcibíades?", "Un político y general ateniense de gran talento y vida escandalosa, discípulo de Sócrates, que cambió de bando varias veces durante la guerra del Peloponeso.")],
    },
    "segundo-alcibiades-platon": {
        "color": "negro",
        "tema": "la oración",
        "resumen": [
            "Sócrates encuentra a Alcibíades camino del templo, donde va a rezar. Le pregunta si sabe qué pedir a los dioses: mucha gente ha pedido el poder, la riqueza o un hijo y ha acabado en la desgracia por haberlo conseguido.",
            "Sócrates muestra que la ignorancia de lo mejor convierte cualquier bien en un peligro, y que es preferible pedir simplemente lo bueno, como hacen los espartanos. Recomienda a Alcibíades esperar a saber cómo comportarse con los dioses y con los hombres antes de ofrecer sacrificios.",
        ],
        "personajes": [("Sócrates", "Le invita a reflexionar antes de rezar."),
                       ("Alcibíades", "Joven ambicioso que va a hacer una ofrenda a los dioses.")],
        "ideas": ["Pedir lo que deseamos puede volverse en nuestra contra.",
                  "Sin saber qué es lo mejor, los demás saberes pueden hacer daño.",
                  "La mejor oración es pedir el bien, no cosas concretas."],
        "faq": [("¿De qué trata el Segundo Alcibíades?", "De la oración: de qué conviene pedir a los dioses cuando no sabemos qué es lo mejor para nosotros."),
                ("¿Es de Platón el Segundo Alcibíades?", "La mayoría de los estudiosos lo consideran apócrifo, escrito por un discípulo de la Academia, aunque se transmitió entre las obras de Platón.")],
    },
    "clitofon-platon": {
        "color": "azul",
        "tema": "la exhortación a la justicia",
        "resumen": [
            "Sócrates se entera de que Clitofón le ha criticado ante Lisias y elogiado al sofista Trasímaco. Clitofón le explica sus razones: los discursos de Sócrates son magníficos para animar a cuidar el alma y practicar la justicia, pero nunca dicen qué es exactamente la justicia ni cómo se consigue.",
            "Es un diálogo muy breve y casi sin respuesta: Sócrates escucha y la obra termina con el reproche de Clitofón. Por eso se ha leído como una crítica al método socrático o como un fragmento incompleto.",
        ],
        "personajes": [("Sócrates", "Escucha la crítica sin replicar."),
                       ("Clitofón", "Ateniense que aparece también en La República junto a Trasímaco.")],
        "ideas": ["Exhortar a la virtud no basta: hay que enseñar qué es.",
                  "La justicia como objeto de un saber que todavía hay que encontrar."],
        "faq": [("¿Por qué es tan corto el Clitofón?", "Porque solo recoge el discurso de Clitofón, sin respuesta de Sócrates. Algunos creen que está incompleto o que es un prólogo a La República."),
                ("¿Es auténtico el Clitofón?", "Su autoría es dudosa; se transmitió entre los diálogos de Platón pero muchos estudiosos lo consideran de otro autor.")],
    },
    "filebo-platon": {
        "color": "verde",
        "tema": "el placer y el bien",
        "resumen": [
            "Filebo sostiene que el bien es el placer. Como no quiere discutir, su joven amigo Protarco toma el relevo frente a Sócrates, que defiende que la sabiduría y el conocimiento valen más que el placer para una buena vida.",
            "Sócrates introduce una clasificación de todo lo que existe en cuatro géneros: lo ilimitado, el límite, la mezcla de ambos y la causa de la mezcla. Distingue placeres verdaderos y falsos, puros y mezclados con dolor. Concluye que la vida buena no es ni solo placer ni solo pensamiento, sino una mezcla bien medida de ambos, en la que la medida y la proporción ocupan el primer lugar.",
        ],
        "personajes": [("Sócrates", "Conduce la discusión, una de sus últimas apariciones como protagonista."),
                       ("Protarco", "Joven que defiende la tesis de Filebo."),
                       ("Filebo", "Partidario del placer como bien supremo.")],
        "ideas": ["La vida buena es una mezcla de placer y conocimiento.",
                  "Hay placeres falsos, como los que dependen de opiniones falsas.",
                  "La medida y la proporción son el primer bien."],
        "faq": [("¿De qué trata el Filebo?", "De qué es el bien para el ser humano: el placer, el conocimiento o una mezcla de ambos."),
                ("¿Qué son los cuatro géneros del Filebo?", "Lo ilimitado, el límite, la mezcla de los dos y la causa de esa mezcla. Platón los usa para explicar el orden de la realidad."),
                ("¿Es un diálogo difícil?", "Sí, es de la etapa tardía de Platón y bastante técnico. Conviene leerlo después de diálogos como el Gorgias o el Fedón.")],
    },
    "sofista-platon": {
        "color": "negro",
        "tema": "el ser y el no ser",
        "resumen": [
            "Al día siguiente de la conversación del Teeteto, un extranjero de Elea, discípulo de Parménides, acepta explicar qué es un sofista. Con el joven Teeteto aplica el método de la división: va separando las artes en clases hasta cazar al sofista, que resulta escurridizo y aparece bajo muchas formas.",
            "El sofista vive de producir apariencias y falsedades, pero decir lo falso es decir lo que no es, y Parménides había prohibido pensar el no ser. El extranjero se ve obligado a cometer un «parricidio» contra su maestro: muestra que el no ser existe de algún modo, como lo diferente. Para ello analiza cinco grandes géneros: el ser, el movimiento, el reposo, lo mismo y lo otro.",
        ],
        "personajes": [("El extranjero de Elea", "Filósofo de la escuela de Parménides, guía de la conversación."),
                       ("Teeteto", "Joven matemático de gran talento."),
                       ("Teodoro", "Geómetra, maestro de Teeteto."),
                       ("Sócrates", "Presente al principio, deja hablar al extranjero.")],
        "ideas": ["El método de la división para definir conceptos.",
                  "El no ser existe como diferencia: lo que no es una cosa es otra.",
                  "Los cinco grandes géneros: ser, movimiento, reposo, identidad y diferencia."],
        "faq": [("¿De qué trata El sofista de Platón?", "De qué es un sofista y, para responderlo, de cómo es posible decir lo falso, lo que lleva a investigar el ser y el no ser."),
                ("¿Qué es el parricidio de Parménides?", "La decisión del extranjero de contradecir a Parménides afirmando que el no ser existe en cierto sentido, como lo diferente."),
                ("¿Con qué diálogos se relaciona El sofista?", "Continúa el Teeteto y precede a El político; los tres forman una serie.")],
    },
}

NUMBER_START = 3


def main():
    for number, (slug, data) in enumerate(BOOKS.items(), start=NUMBER_START):
        config = TEXTS / f"{slug}.json"
        meta = json.loads(config.read_text(encoding="utf-8"))
        title, author = meta["title"], meta["author"]
        if not meta.get("book_route") or meta["book_route"] in ("I", "II", "III", "IV", "VI"):
            meta["book_route"] = f"/{slug}/"
        meta["description"] = (f"{title} de {author}: resumen, personajes e ideas principales, y el texto completo para leer online "
                               f"gratis o descargar en PDF. Diálogo sobre {data['tema']}.")[:300]
        meta["intro"] = "".join(f"<p>{p}</p>" for p in data["resumen"][:1]) + (
            f"<p>Aquí puedes leer {title} completo, dividido en partes, con las notas de la traducción "
            f"de {meta['translator']}. Se respeta la ortografía de la edición original.</p>")
        meta.setdefault("cover", {}).update({"color": data["color"], "number": number})
        blocks = (TEXTS / f"{slug}.txt").read_text(encoding="utf-8").split("\n")
        for chapter in meta["chapters"]:
            if not chapter.get("summary"):
                first = next((b[2:] for b in blocks[chapter["start"]:chapter["end"] + 1] if b.startswith("P|")), "")
                words = first.lstrip("—-– ").split()
                chapter["summary"] = "Empieza: «" + " ".join(words[:22]) + ("…»" if len(words) > 22 else "»")
        meta["ficha"] = {"tema": data["tema"], "resumen": data["resumen"], "personajes": data["personajes"],
                         "ideas": data["ideas"], "faq": data["faq"]}
        config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(number, slug)


if __name__ == "__main__":
    main()
