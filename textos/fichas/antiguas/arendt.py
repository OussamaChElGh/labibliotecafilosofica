"""Fichas de Hannah Arendt en el formato nuevo (fichas_antiguas.py)."""

AUTOR = "Hannah Arendt"
RUTA = "/libros-pdf-gratis/autores/hannah-arendt/"


def book(**data):
    data.setdefault("autor", AUTOR)
    data.setdefault("ruta_autor", RUTA)
    return data


BOOKS = {
    "/hannah-arendt-los-origenes-del-totalitarismo/": book(
        titulo="Los orígenes del totalitarismo", genero="Ensayo político", año="1951", tema="el nazismo, el estalinismo y las raíces del totalitarismo",
        resumen=[
            "Arendt quiere comprender cómo fue posible algo sin precedentes: el totalitarismo, una forma de dominación que no se limita a oprimir, sino que pretende transformar la naturaleza humana. El libro se divide en tres partes. La primera estudia el antisemitismo moderno y la situación de los judíos en Europa; la segunda, el imperialismo, el racismo y la crisis del Estado nacional, que dejó a millones de apátridas sin el derecho a tener derechos.",
            "La tercera analiza el nazismo y el estalinismo: la sociedad de masas formada por individuos aislados, los movimientos totalitarios, la propaganda, la policía secreta y la combinación de ideología y terror. Los campos de concentración son el laboratorio donde se intenta demostrar que todo es posible y hacer a los seres humanos superfluos.",
        ],
        ideas=["El totalitarismo es una forma de gobierno nueva, distinta de la tiranía.",
               "Ideología y terror son la esencia del dominio total.",
               "La sociedad de masas y el aislamiento preparan el terreno del totalitarismo.",
               "Los apátridas revelan que los derechos humanos dependen de pertenecer a una comunidad política: el derecho a tener derechos."],
        faq=[("¿De qué trata Los orígenes del totalitarismo?", "Del antisemitismo, el imperialismo y el totalitarismo: las corrientes del siglo XIX y XX que cristalizaron en el nazismo y el estalinismo."),
             ("¿Qué es el «derecho a tener derechos»?", "La idea de Arendt de que los derechos humanos solo están garantizados para quien pertenece a una comunidad política; los apátridas los perdieron todos."),
             ("¿Qué diferencia hay entre totalitarismo y tiranía según Arendt?", "La tiranía busca obediencia; el totalitarismo quiere dominar por completo a las personas, destruir su espontaneidad y lo hace mediante la ideología y el terror.")]),
    "/hannah-arendt-la-condicion-humana/": book(
        titulo="La condición humana", genero="Ensayo filosófico", año="1958", tema="la labor, el trabajo y la acción",
        resumen=[
            "Arendt se propone pensar qué hacemos cuando estamos activos. Distingue tres actividades de la vita activa: la labor, que responde a las necesidades biológicas y se consume sin dejar rastro; el trabajo, con el que el homo faber fabrica un mundo de objetos duraderos; y la acción, que se da entre las personas sin mediación de cosas y depende de la pluralidad.",
            "La acción, junto con el discurso, es lo que revela quién es cada uno y permite empezar algo nuevo: Arendt lo llama natalidad. La modernidad ha invertido la jerarquía y ha convertido la sociedad en una comunidad de trabajadores y consumidores donde se pierde el espacio público. Contra la imprevisibilidad y la irreversibilidad de la acción, propone dos remedios: la promesa y el perdón.",
        ],
        ideas=["Tres actividades humanas: labor, trabajo y acción.",
               "La pluralidad es la condición de la política.",
               "La natalidad: cada nacimiento trae la posibilidad de un nuevo comienzo.",
               "El ascenso de lo social y la pérdida del espacio público.",
               "El perdón y la promesa como remedios a la fragilidad de la acción."],
        faq=[("¿Qué diferencia hay entre labor, trabajo y acción?", "La labor mantiene la vida biológica; el trabajo fabrica objetos duraderos que forman un mundo; la acción es la actividad política entre personas, en la que cada uno muestra quién es."),
             ("¿Qué es la natalidad para Arendt?", "La capacidad de empezar algo nuevo que trae cada ser humano al nacer, base de la acción y de la libertad."),
             ("¿Cuándo se publicó La condición humana?", "En 1958, en inglés, con el título The Human Condition.")]),
    "/hannah-arendt-eichmann-en-jerusalen/": book(
        titulo="Eichmann en Jerusalén", genero="Ensayo y crónica", año="1963", tema="la banalidad del mal",
        resumen=[
            "En 1961 Arendt viajó a Jerusalén como corresponsal de la revista The New Yorker para asistir al juicio contra Adolf Eichmann, el funcionario nazi que había organizado la deportación de millones de judíos a los campos de exterminio. Sus crónicas se reunieron en este libro, subtitulado Un informe sobre la banalidad del mal.",
            "Arendt esperaba encontrar un monstruo y vio a un burócrata mediocre, obsesionado con su carrera y que hablaba con clichés, incapaz de pensar desde el punto de vista de los demás. De ahí nace la idea de la banalidad del mal: los peores crímenes pueden cometerlos personas normales que no piensan. Su crítica del papel de algunos consejos judíos provocó una enorme polémica.",
        ],
        personajes=[("Adolf Eichmann", "Teniente coronel de las SS encargado de organizar las deportaciones."),
                    ("Gideon Hausner", "Fiscal general de Israel en el juicio."),
                    ("Los jueces del tribunal", "Tres magistrados que dirigieron el proceso en Jerusalén.")],
        ideas=["La banalidad del mal: el mal extremo puede nacer de la incapacidad de pensar.",
               "La responsabilidad personal no desaparece dentro de una burocracia.",
               "Los límites y la legitimidad del juicio de Jerusalén.",
               "El juicio moral exige pensar por uno mismo."],
        faq=[("¿Qué es la banalidad del mal?", "La tesis de Arendt de que Eichmann no actuó por odio o maldad diabólica, sino por una ausencia de pensamiento propia de un burócrata obediente y ambicioso."),
             ("¿Por qué fue polémico Eichmann en Jerusalén?", "Por la idea de la banalidad del mal y por sus críticas a la colaboración de algunos consejos judíos con los nazis."),
             ("¿Cuándo se celebró el juicio de Eichmann?", "En 1961, en Jerusalén. Eichmann fue condenado a muerte y ejecutado en 1962.")]),
    "/hannah-arendt-sobre-la-revolucion/": book(
        titulo="Sobre la revolución", genero="Ensayo político", año="1963", tema="la libertad y la fundación de la república",
        resumen=[
            "Arendt compara las dos grandes revoluciones del siglo XVIII. La estadounidense logró su objetivo, fundar un espacio de libertad política mediante una constitución, mientras que la francesa fue arrastrada por la cuestión social: la urgencia de la miseria de las masas hizo que la libertad quedara sacrificada a la necesidad y al terror.",
            "Distingue entre liberación, librarse de la opresión, y libertad, participar en los asuntos públicos. Al final recuerda el tesoro perdido de la tradición revolucionaria: los consejos, las asambleas y las comunas que surgieron espontáneamente en todas las revoluciones como formas de participación directa.",
        ],
        ideas=["La revolución tiene como fin la fundación de la libertad.",
               "La diferencia entre liberación y libertad.",
               "La cuestión social desvió la Revolución francesa hacia el terror.",
               "El sistema de consejos como tesoro perdido de la tradición revolucionaria."],
        faq=[("¿Qué revoluciones compara Arendt?", "La Revolución estadounidense y la Revolución francesa, que considera, respectivamente, un éxito y un fracaso en la fundación de la libertad."),
             ("¿Qué es la cuestión social?", "El problema de la pobreza masiva, que según Arendt hizo que la Revolución francesa abandonara la libertad para atender a la necesidad.")]),
    "/hannah-arendt-sobre-la-violencia/": book(
        titulo="Sobre la violencia", genero="Ensayo político", año="1970", tema="la diferencia entre poder y violencia",
        resumen=[
            "Escrito en el contexto de las protestas estudiantiles de 1968, la guerra de Vietnam y la amenaza nuclear, este ensayo examina la glorificación de la violencia en la Nueva Izquierda y en autores como Sorel, Sartre o Fanon.",
            "Arendt distingue conceptos que suelen confundirse: poder, potencia, fuerza, autoridad y violencia. El poder surge cuando las personas actúan juntas y no necesita justificación, mientras que la violencia es instrumental y siempre necesita una. Por eso poder y violencia son opuestos: donde uno domina por completo, el otro está ausente. La violencia puede destruir el poder, pero nunca crearlo.",
        ],
        ideas=["Poder y violencia son opuestos, no grados de lo mismo.",
               "El poder nace de la acción conjunta de muchos.",
               "La violencia es instrumental y puede destruir el poder, pero no crearlo.",
               "Crítica de la glorificación de la violencia revolucionaria."],
        faq=[("¿Qué diferencia hay entre poder y violencia según Arendt?", "El poder es la capacidad de actuar juntos y descansa en el apoyo de muchos; la violencia es un instrumento que puede imponerse sin ese apoyo, y aparece cuando el poder se pierde."),
             ("¿En qué contexto se escribió Sobre la violencia?", "En el de los movimientos estudiantiles de 1968, la guerra de Vietnam y los debates de la Nueva Izquierda sobre la violencia.")]),
    "/hannah-arendt-que-es-la-politica/": book(
        titulo="¿Qué es la política?", genero="Ensayo filosófico", año="1993 (póstumo)", tema="el sentido de la política",
        resumen=[
            "Este libro reúne los fragmentos de una introducción a la política que Arendt preparó entre 1956 y 1959 y que no llegó a terminar. Los editó Ursula Ludz a partir de los manuscritos de su legado.",
            "Arendt parte de una idea sencilla: la política se basa en el hecho de la pluralidad humana, en que no existe el hombre, sino los hombres. Analiza los prejuicios contra la política, que tras los totalitarismos y la bomba atómica parece una amenaza, y responde que el sentido de la política es la libertad.",
        ],
        ideas=["La política nace de la pluralidad: trata del estar juntos de los diversos.",
               "El sentido de la política es la libertad.",
               "Los prejuicios contra la política tras el totalitarismo.",
               "La política se da en el espacio entre las personas."],
        faq=[("¿Qué es la política según Arendt?", "La actividad que trata de la convivencia entre personas diferentes y cuyo sentido es la libertad."),
             ("¿Es un libro terminado?", "No. Son fragmentos escritos entre 1956 y 1959 y publicados póstumamente en 1993.")]),
    "/hannah-arendt-hombres-en-tiempos-de-oscuridad/": book(
        titulo="Hombres en tiempos de oscuridad", genero="Ensayos biográficos", año="1968", tema="personas que dieron luz en épocas sombrías",
        resumen=[
            "Arendt reúne retratos de hombres y mujeres que vivieron en las épocas oscuras del siglo XX o antes, y que aun así iluminaron su tiempo con su vida o su obra: Lessing, Rosa Luxemburgo, el papa Juan XXIII, Karl Jaspers, Isak Dinesen, Hermann Broch, Walter Benjamin, Bertolt Brecht, Waldemar Gurian y Randall Jarrell.",
            "El título procede de un poema de Brecht. Arendt sostiene que incluso en los tiempos más oscuros tenemos derecho a esperar cierta iluminación, que no viene tanto de teorías como de la luz incierta que algunas personas encienden con sus vidas y sus obras.",
        ],
        ideas=["En tiempos oscuros la luz llega de personas concretas.",
               "La amistad y el diálogo como base de la humanidad.",
               "El valor del juicio independiente frente a la presión de la época."],
        faq=[("¿Quiénes aparecen en Hombres en tiempos de oscuridad?", "Lessing, Rosa Luxemburgo, Juan XXIII, Karl Jaspers, Isak Dinesen, Hermann Broch, Walter Benjamin, Bertolt Brecht, Waldemar Gurian y Randall Jarrell."),
             ("¿De dónde viene el título?", "Del poema A los que vendrán después, de Bertolt Brecht.")]),
    "/hannah-arendt-la-vida-del-espiritu/": book(
        titulo="La vida del espíritu", genero="Ensayo filosófico", año="1978 (póstumo)", tema="pensar, querer y juzgar",
        resumen=[
            "Tras La condición humana, dedicada a la vida activa, Arendt quiso estudiar la vida contemplativa en tres partes: el pensamiento, la voluntad y el juicio. La pregunta nació del juicio a Eichmann: ¿puede la actividad de pensar evitar que hagamos el mal?",
            "Arendt murió en 1975 cuando acababa de empezar la tercera parte. El libro se publicó con las dos primeras, editadas por Mary McCarthy, y con un apéndice sobre el juicio basado en sus lecciones sobre la filosofía política de Kant. El pensamiento aparece como un diálogo silencioso con uno mismo que nos retira del mundo y nos permite juzgar.",
        ],
        ideas=["Pensar es un diálogo silencioso de uno consigo mismo.",
               "La incapacidad de pensar está relacionada con el mal.",
               "La voluntad como facultad de empezar algo nuevo.",
               "El juicio como capacidad política de pensar en el lugar de los demás."],
        faq=[("¿Qué partes tiene La vida del espíritu?", "Pensar y Querer, completas, y Juzgar, que quedó sin escribir; se completa con sus lecciones sobre Kant."),
             ("¿Qué relación tiene con Eichmann en Jerusalén?", "La banalidad del mal llevó a Arendt a preguntarse si el pensamiento puede impedir el mal, pregunta de la que nace este libro.")]),
    "/hannah-arendt-ensayos-de-comprension/": book(
        titulo="Ensayos de comprensión 1930-1954", genero="Ensayos", año="1994 (recopilación)", tema="comprender el siglo XX",
        resumen=[
            "Este volumen, editado por Jerome Kohn, reúne artículos, conferencias, reseñas y entrevistas de Arendt escritos entre 1930 y 1954, los años en que se formó su pensamiento, desde su exilio en Francia hasta la publicación de Los orígenes del totalitarismo.",
            "Incluye textos como Comprensión y política, en el que explica que comprender no es justificar, sino reconciliarse con un mundo en el que han sucedido cosas terribles, y la célebre entrevista con Günter Gaus de 1964, ¿Qué queda? Queda la lengua materna.",
        ],
        ideas=["Comprender es una tarea interminable, no un perdón.",
               "El totalitarismo rompe las categorías tradicionales del pensamiento.",
               "La relación de Arendt con la filosofía alemana y el exilio."],
        faq=[("¿Qué contiene Ensayos de comprensión?", "Artículos, conferencias y entrevistas de Arendt entre 1930 y 1954, entre ellos Comprensión y política y la entrevista con Günter Gaus."),
             ("¿Qué significa comprender para Arendt?", "Una actividad sin fin con la que intentamos reconciliarnos con la realidad, sin justificar lo que ha sucedido.")]),
    "/hannah-arendt-de-la-historia-a-la-accion/": book(
        titulo="De la historia a la acción", genero="Ensayos", año="1995 (recopilación)", tema="la evolución del pensamiento de Arendt",
        resumen=[
            "Esta antología en castellano reúne textos de Arendt que muestran cómo evolucionó su pensamiento, desde la preocupación por los problemas históricos y políticos del siglo XX hasta su interés final por los fundamentos filosóficos de la actividad humana: pensar, actuar y juzgar.",
            "Por su variedad es una buena puerta de entrada para formarse una primera imagen global de la autora, en la que aparecen sus grandes temas: la comprensión del totalitarismo, la acción política, la responsabilidad y la relación entre pensamiento y moral.",
        ],
        ideas=["La historia y la acción como ejes de su pensamiento.",
               "La relación entre pensamiento, juicio y moral.",
               "Una introducción de conjunto a la obra de Arendt."],
        faq=[("¿Qué es De la historia a la acción?", "Una antología de textos de Hannah Arendt publicada en castellano que recorre la evolución de su pensamiento político y filosófico."),
             ("¿Es un buen libro para empezar a leer a Arendt?", "Sí: al reunir textos breves de distintas etapas, ofrece una visión de conjunto antes de abordar obras largas como La condición humana.")]),
    "/hannah-arendt-la-tradicion-oculta/": book(
        titulo="La tradición oculta", genero="Ensayos", año="1948 (en alemán)", tema="la cuestión judía en la modernidad",
        resumen=[
            "Arendt reúne siete ensayos de los años treinta y cuarenta: Sobre el imperialismo, Culpa organizada, La tradición oculta, Los judíos en el mundo de ayer, Franz Kafka, La Ilustración y la cuestión judía y El sionismo, una retrospectiva. Casi todos proceden de Sechs Essays, su primer libro publicado en la Alemania de posguerra.",
            "En La tradición oculta describe la figura del judío como paria consciente, que se niega a asimilarse a cualquier precio y conserva una mirada crítica sobre la sociedad, en escritores como Heine, Bernard Lazare, Kafka o en la figura de Charlot.",
        ],
        ideas=["El paria consciente frente al advenedizo que se asimila.",
               "La historia judía como clave para comprender la modernidad.",
               "La culpa organizada y la responsabilidad tras el nazismo."],
        faq=[("¿Qué es la tradición oculta según Arendt?", "La línea de escritores y artistas judíos, como Heine, Lazare o Kafka, que eligieron ser parias conscientes en lugar de asimilarse."),
             ("¿Qué ensayos incluye?", "Sobre el imperialismo, Culpa organizada, La tradición oculta, Los judíos en el mundo de ayer, Franz Kafka, La Ilustración y la cuestión judía y El sionismo.")]),
    "/hannah-arendt-karl-marx-y-la-tradicion-del-pensamiento-politico-occidental-pdf/": book(
        titulo="Karl Marx y la tradición del pensamiento político occidental", genero="Ensayo", año="1953 (conferencias)", tema="Marx y la ruptura con la tradición",
        resumen=[
            "Tras Los orígenes del totalitarismo, Arendt quiso estudiar los elementos del marxismo que el estalinismo había utilizado. Estas conferencias y manuscritos de 1953 muestran a Marx no como el origen del totalitarismo, sino como el último pensador de la gran tradición que empieza con Platón y Aristóteles.",
            "Arendt analiza tres tesis de Marx que rompen esa tradición: el trabajo crea al hombre, la violencia es la partera de la historia y los filósofos deben transformar el mundo en lugar de interpretarlo. Estas reflexiones prepararon La condición humana.",
        ],
        ideas=["Marx como final de la tradición filosófica occidental.",
               "La glorificación del trabajo en la modernidad.",
               "La relación entre violencia e historia.",
               "El germen de la distinción entre labor, trabajo y acción."],
        faq=[("¿Culpaba Arendt a Marx del totalitarismo?", "No directamente: veía en él al último gran pensador de la tradición, cuyas ideas el totalitarismo deformó y utilizó."),
             ("¿Qué relación tiene con La condición humana?", "Estas reflexiones sobre el trabajo en Marx dieron lugar a la distinción entre labor, trabajo y acción de La condición humana.")]),
    "/hannah-arendt-la-libertad-de-ser-libres-pdf/": book(
        titulo="La libertad de ser libres", genero="Ensayo", año="Escrito hacia 1967", tema="la libertad política y la revolución",
        resumen=[
            "En este ensayo breve, inédito hasta 2018, Arendt vuelve a los temas de Sobre la revolución. Distingue entre la liberación, librarse del miedo, la opresión y la miseria, y la libertad política, que consiste en participar en los asuntos públicos.",
            "La libertad de ser libres significa no solo no ser oprimido, sino tener la posibilidad de actuar y hablar con otros en un espacio público. Arendt recuerda que la pobreza hace imposible esa libertad, y que las revoluciones fracasan cuando confunden liberación y libertad.",
        ],
        ideas=["Liberación y libertad no son lo mismo.",
               "La libertad política consiste en participar en lo público.",
               "La pobreza como obstáculo para la libertad.",
               "Las revoluciones como fundación de la libertad."],
        faq=[("¿De qué trata La libertad de ser libres?", "De la diferencia entre liberarse de la opresión y ser libre para participar en la vida pública, a partir de las revoluciones modernas."),
             ("¿Cuándo se publicó?", "Escrito a finales de los años sesenta, se publicó por primera vez en 2018.")]),
}
