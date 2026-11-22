"""Fichas de Friedrich Nietzsche en el formato nuevo (fichas_antiguas.py)."""

AUTOR = "Friedrich Nietzsche"
RUTA = "/libros-pdf-gratis/autores/nietzsche/"


def book(**data):
    data.setdefault("autor", AUTOR)
    data.setdefault("ruta_autor", RUTA)
    return data


BOOKS = {
    "/asi-hablo-zaratustra-friedrich-nietzsche/": book(
        titulo="Así habló Zaratustra", genero="Obra filosófica y poética", año="1883-1885", tema="el superhombre, la muerte de Dios y el eterno retorno",
        descripcion="Así habló Zaratustra de Nietzsche: resumen de sus cuatro partes, ideas principales (superhombre, eterno retorno, voluntad de poder) y preguntas frecuentes.",
        resumen=[
            "Tras diez años de soledad en la montaña, Zaratustra baja a los hombres para anunciarles que Dios ha muerto y que el ser humano es algo que debe ser superado: una cuerda tendida entre el animal y el superhombre. En la plaza del mercado nadie le entiende, y decide hablar solo a unos pocos discípulos.",
            "A lo largo de cuatro partes escritas como un libro sagrado, con parábolas, discursos y cantos, Zaratustra enseña la transvaloración de los valores, la voluntad de poder y su pensamiento más abismal, el eterno retorno de lo mismo: querer la propia vida hasta desear que se repita infinitamente. La cuarta parte reúne a los hombres superiores en su cueva, a la espera de un nuevo comienzo.",
        ],
        personajes=[("Zaratustra", "Profeta y maestro solitario, portavoz de Nietzsche."),
                    ("El último hombre", "Figura del ser humano conformista que solo busca comodidad."),
                    ("El enano", "Espíritu de la pesadez que se burla de Zaratustra."),
                    ("Los hombres superiores", "Visitantes de la cueva en la cuarta parte: un rey, un papa jubilado, un mago…"),
                    ("El águila y la serpiente", "Animales de Zaratustra, símbolos del orgullo y la sabiduría.")],
        ideas=["La muerte de Dios y el vacío de valores que deja.",
               "El superhombre como sentido de la tierra.",
               "La voluntad de poder como impulso de toda vida.",
               "El eterno retorno: vivir de modo que se quiera repetir eternamente cada instante.",
               "Las tres transformaciones del espíritu: camello, león y niño."],
        faq=[("¿De qué trata Así habló Zaratustra?", "De los discursos de Zaratustra, un sabio que baja de la montaña para anunciar la muerte de Dios, el superhombre y el eterno retorno."),
             ("¿Qué es el superhombre de Nietzsche?", "El ser humano que supera los valores tradicionales y crea los suyos propios, afirmando la vida terrena sin necesidad de un más allá."),
             ("¿Qué son las tres transformaciones?", "El primer discurso de Zaratustra: el espíritu se convierte en camello, que carga con los deberes; en león, que dice no; y en niño, que crea con un sí inocente."),
             ("¿Por qué Zaratustra?", "Nietzsche eligió al profeta persa Zoroastro, creador de la moral del bien y del mal, para que fuera él quien la superara.")]),
    "/mas-alla-del-bien-y-del-mal-friedrich-nietzsche/": book(
        titulo="Más allá del bien y del mal", genero="Ensayo filosófico", año="1886", tema="la crítica de la filosofía y la moral",
        resumen=[
            "Subtitulado Preludio de una filosofía del futuro, el libro ataca los prejuicios de los filósofos: su fe en la oposición de los valores, en la verdad absoluta, en el sujeto y en la libertad de la voluntad. Detrás de toda filosofía, dice Nietzsche, se esconde una confesión personal y una voluntad de poder.",
            "En nueve partes de aforismos y ensayos breves trata de los espíritus libres, la religión, la moral, los pueblos de Europa y la nobleza. Distingue por primera vez entre la moral de señores y la moral de esclavos, y propone unos filósofos del futuro capaces de crear valores nuevos.",
        ],
        ideas=["Toda filosofía es la expresión de una voluntad de poder.",
               "Moral de señores frente a moral de esclavos.",
               "El perspectivismo: no hay hechos, solo interpretaciones.",
               "Los espíritus libres y los filósofos del futuro."],
        faq=[("¿De qué trata Más allá del bien y del mal?", "Es una crítica de los prejuicios de la filosofía y de la moral cristiana, y una propuesta de nuevos filósofos que creen valores más allá de la oposición entre bien y mal."),
             ("¿Qué relación tiene con La genealogía de la moral?", "La genealogía, de 1887, se escribió para desarrollar y aclarar las ideas morales de Más allá del bien y del mal.")]),
    "/la-genealogia-de-la-moral-pdf-friedrich-nietzsche/": book(
        titulo="La genealogía de la moral", genero="Ensayo filosófico", año="1887", tema="el origen de nuestros valores morales",
        resumen=[
            "En tres tratados, Nietzsche investiga de dónde vienen nuestros valores. El primero contrapone la oposición noble de bueno y malo, nacida de la afirmación de sí, a la oposición de bueno y malvado, creada por el resentimiento de los débiles en una rebelión de los esclavos en la moral.",
            "El segundo explica la culpa y la mala conciencia como deudas y como instintos de crueldad vueltos hacia dentro. El tercero analiza el ideal ascético de sacerdotes, filósofos y científicos, que prefiere querer la nada a no querer nada. Es la obra más sistemática de Nietzsche.",
        ],
        ideas=["La moral de esclavos nace del resentimiento.",
               "La culpa procede de la relación entre acreedor y deudor.",
               "La mala conciencia son los instintos vueltos contra uno mismo.",
               "El ideal ascético: el ser humano prefiere querer la nada a no querer."],
        faq=[("¿Qué es el resentimiento según Nietzsche?", "El sentimiento de los débiles que, incapaces de actuar, se vengan imaginariamente llamando malvados a los fuertes y buenos a sí mismos."),
             ("¿Cuántos tratados tiene La genealogía de la moral?", "Tres: sobre bueno y malo, sobre la culpa y la mala conciencia, y sobre el ideal ascético.")]),
    "/la-gaya-ciencia-pdf-friedrich-nietzsche/": book(
        titulo="La gaya ciencia", genero="Aforismos", año="1882 y 1887", tema="la muerte de Dios y la alegría del conocimiento",
        resumen=[
            "La gaya ciencia, o el alegre saber, es un libro de aforismos escrito en una época de recuperación y entusiasmo. Nietzsche quiere unir el conocimiento con la alegría, como los trovadores provenzales unían el canto y la vida.",
            "En el aforismo 125 un loco busca a Dios en la plaza con una linterna y anuncia que lo hemos matado nosotros. En el 341 aparece por primera vez el eterno retorno, y el libro cuarto termina con el comienzo de Zaratustra. La edición de 1887 añadió un prólogo, un quinto libro y los poemas de las Canciones del príncipe Vogelfrei.",
        ],
        ideas=["Dios ha muerto: el anuncio del loco en la plaza.",
               "El eterno retorno como prueba para la vida.",
               "Amor fati: amar el propio destino.",
               "El conocimiento como alegría y experimento."],
        faq=[("¿Dónde aparece «Dios ha muerto»?", "En el aforismo 125 de La gaya ciencia, el del hombre loco que busca a Dios en la plaza con una linterna."),
             ("¿Qué significa «gaya ciencia»?", "El alegre saber: la expresión provenzal para el arte de los trovadores, que Nietzsche usa para un conocimiento unido a la alegría de vivir.")]),
    "/humano-demasiado-humano-friedrich-nietzsche/": book(
        titulo="Humano, demasiado humano", genero="Aforismos", año="1878", tema="la crítica de la metafísica y la religión",
        resumen=[
            "Subtitulado Un libro para espíritus libres y dedicado a Voltaire, marca la ruptura de Nietzsche con Wagner y con Schopenhauer. Abandona el tono romántico de El nacimiento de la tragedia y adopta un estilo de aforismos breves, fríos y científicos.",
            "En nueve capítulos examina el origen de los sentimientos morales, la religión, el arte, la cultura, el trato social, la mujer, el Estado y la soledad, y muestra que lo que creemos elevado tiene orígenes humanos, demasiado humanos.",
        ],
        ideas=["Los valores elevados tienen un origen humano.",
               "El espíritu libre se emancipa de la tradición.",
               "La filosofía histórica frente a la metafísica.",
               "Ruptura con Wagner y con el romanticismo."],
        faq=[("¿Por qué Humano, demasiado humano está dedicado a Voltaire?", "Porque se publicó en el centenario de su muerte y Nietzsche quiso homenajear al espíritu ilustrado y libre."),
             ("¿Qué incluye El viajero y su sombra?", "Es la segunda parte de Humano, demasiado humano, junto con Opiniones y sentencias varias.")]),
    "/el-viajero-y-su-sombra-friedrich-nietzsche-pdf/": book(
        titulo="El viajero y su sombra", genero="Aforismos", año="1880", tema="las cosas cercanas y la vida cotidiana",
        resumen=[
            "Publicado en 1880 y después integrado como segunda parte del segundo volumen de Humano, demasiado humano, el libro se abre y se cierra con un diálogo entre un viajero y su sombra.",
            "Entre ambos, cientos de aforismos tratan de las cosas cercanas que la filosofía suele despreciar, la comida, el clima, el trato con los demás, la salud, y también de la moral, el arte y la libertad. Nietzsche lo escribió en un periodo de grave enfermedad.",
        ],
        ideas=["La importancia de las cosas cercanas y cotidianas.",
               "Crítica de la libertad de la voluntad.",
               "El viajero como figura del espíritu libre."],
        faq=[("¿Qué es El viajero y su sombra?", "Un libro de aforismos de 1880 que Nietzsche integró después en Humano, demasiado humano."),
             ("¿Por qué ese título?", "Porque el libro empieza y acaba con un diálogo entre un viajero, el espíritu libre, y su sombra.")]),
    "/el-nacimiento-de-la-tragedia-en-el-espiritu-de-la-musica-pdf-friedrich-nietzsche/": book(
        titulo="El nacimiento de la tragedia", genero="Ensayo", año="1872", tema="lo apolíneo y lo dionisíaco",
        resumen=[
            "El primer libro de Nietzsche explica el origen de la tragedia griega como unión de dos impulsos: lo apolíneo, la forma, la medida y el sueño de las imágenes, y lo dionisíaco, la embriaguez, la música y la fusión con la naturaleza. De su lucha y reconciliación nació el arte de Esquilo y Sófocles.",
            "La tragedia murió con Eurípides y con Sócrates, que impusieron el optimismo racional sobre la sabiduría trágica. Nietzsche esperaba su renacimiento en la música de Wagner. En el prólogo de 1886, Ensayo de autocrítica, se distanció de esa esperanza.",
        ],
        ideas=["Lo apolíneo y lo dionisíaco como fuerzas del arte.",
               "La tragedia griega como afirmación de la vida frente al dolor.",
               "Sócrates como inicio de la decadencia racionalista.",
               "La existencia solo se justifica como fenómeno estético."],
        faq=[("¿Qué es lo apolíneo y lo dionisíaco?", "Dos impulsos del arte griego: Apolo representa la forma, la medida y la individualidad; Dioniso, la embriaguez, la música y la disolución del individuo."),
             ("¿Por qué Nietzsche culpa a Sócrates?", "Porque con su confianza en la razón y la dialéctica acabó con el espíritu trágico, que aceptaba el sufrimiento sin explicarlo.")]),
    "/como-se-filosofa-a-martillazos-friedrich-nietzsche-pdf/": book(
        titulo="Crepúsculo de los ídolos", genero="Ensayo filosófico", año="1889", tema="la demolición de los ídolos de la filosofía",
        resumen=[
            "Crepúsculo de los ídolos, o cómo se filosofa con el martillo, es un resumen rápido y feroz del pensamiento de Nietzsche, escrito en pocos días de 1888. El martillo sirve para auscultar a los ídolos, los grandes valores, y comprobar que suenan a hueco.",
            "Nietzsche ataca el problema de Sócrates, la razón en la filosofía, la moral como contranaturaleza, los cuatro grandes errores y los alemanes. En el capítulo más célebre cuenta en seis pasos cómo el mundo verdadero acabó convirtiéndose en una fábula.",
        ],
        ideas=["Filosofar con el martillo: poner a prueba los ídolos.",
               "La moral como contranaturaleza.",
               "Cómo el mundo verdadero acabó convirtiéndose en una fábula.",
               "Los cuatro grandes errores de la moral y la religión."],
        faq=[("¿Cómo se filosofa a martillazos es lo mismo que Crepúsculo de los ídolos?", "Sí. El título completo es Crepúsculo de los ídolos, o cómo se filosofa con el martillo."),
             ("¿Qué significa filosofar con el martillo?", "Golpear los ídolos, los valores tradicionales, como un médico que ausculta, para descubrir que están huecos.")]),
    "/el-anticristo-pdf-friedrich-nietzsche/": book(
        titulo="El Anticristo", genero="Ensayo", año="1888 (publicado en 1895)", tema="la crítica del cristianismo",
        resumen=[
            "Subtitulado Maldición sobre el cristianismo, es el ataque más directo de Nietzsche contra la religión cristiana, a la que acusa de ser una moral de la compasión que niega la vida, los instintos y este mundo.",
            "Nietzsche distingue entre la figura de Jesús, que vivió una práctica de paz interior, y el cristianismo de Pablo y de la Iglesia, que lo convirtió en una doctrina de culpa, castigo y más allá. Escrito en 1888, poco antes de su colapso mental, no se publicó hasta 1895.",
        ],
        ideas=["El cristianismo como religión de la compasión que niega la vida.",
               "Diferencia entre Jesús y el cristianismo de Pablo.",
               "La transvaloración de todos los valores.",
               "Elogio de la ciencia y del espíritu libre frente a la fe."],
        faq=[("¿De qué trata El Anticristo de Nietzsche?", "Es una crítica radical del cristianismo, al que Nietzsche acusa de haber convertido la debilidad y el resentimiento en virtudes."),
             ("¿Criticaba Nietzsche a Jesús?", "No tanto: distingue a Jesús, al que considera un tipo psicológico de paz interior, del cristianismo construido por Pablo y la Iglesia.")]),
    "/ecce-homo-friedrich-nietzsche-pdf/": book(
        titulo="Ecce homo", genero="Autobiografía", año="1888 (publicado en 1908)", tema="cómo se llega a ser lo que se es",
        resumen=[
            "Ecce homo, subtitulado Cómo se llega a ser lo que se es, es la autobiografía intelectual de Nietzsche, escrita en el otoño de 1888, semanas antes de su colapso en Turín. Sus capítulos tienen títulos provocadores: Por qué soy tan sabio, Por qué soy tan inteligente, Por qué escribo tan buenos libros, Por qué soy un destino.",
            "Repasa su vida, su salud, su alimentación y sus lugares, y comenta cada uno de sus libros. Con ironía y exaltación, se presenta como el que dividirá la historia en dos. Su hermana retrasó la publicación hasta 1908.",
        ],
        ideas=["Llegar a ser lo que se es: el autoconocimiento como tarea.",
               "Amor fati: no querer que nada sea distinto.",
               "La importancia de las cosas pequeñas: clima, comida, descanso.",
               "Nietzsche como destino de la historia de los valores."],
        faq=[("¿Qué significa Ecce homo?", "He aquí el hombre: las palabras de Pilato al presentar a Jesús, que Nietzsche aplica a sí mismo."),
             ("¿Cuándo escribió Nietzsche Ecce homo?", "En 1888, poco antes de su colapso mental de enero de 1889. Se publicó en 1908.")]),
    "/sobre-verdad-y-mentira-en-sentido-extramoral-friedrich-nietzsche-pdf/": book(
        titulo="Sobre verdad y mentira en sentido extramoral", genero="Ensayo", año="1873 (publicado en 1896)", tema="el origen del lenguaje y de la verdad",
        resumen=[
            "Este breve ensayo empieza con una fábula: en un rincón del universo, unos animales inteligentes inventaron el conocimiento, y aquel fue el minuto más soberbio y mentiroso de la historia universal; poco después el astro se enfrió y murieron.",
            "Nietzsche sostiene que el intelecto es un instrumento para sobrevivir y disimular, y que las palabras son metáforas de impresiones que olvidamos que eran metáforas. Las verdades son ilusiones que hemos olvidado que lo son, monedas que han perdido su imagen.",
        ],
        ideas=["El intelecto nace para la supervivencia y el disimulo.",
               "El lenguaje es un tejido de metáforas olvidadas.",
               "La verdad como ilusión que hemos olvidado que es ilusión.",
               "El ser humano intuitivo frente al ser humano racional."],
        faq=[("¿Qué es la verdad para Nietzsche en este ensayo?", "Un ejército móvil de metáforas y metonimias que, tras un largo uso, nos parecen firmes y obligatorias: ilusiones de las que hemos olvidado que lo son."),
             ("¿Cuándo se escribió?", "En 1873. Quedó inédito y se publicó tras la muerte de Nietzsche.")]),
    "/voluntad-de-poder-pdf-friedrich-nietzsche/": book(
        titulo="La voluntad de poder", genero="Fragmentos póstumos", año="1901 y 1906", tema="la transvaloración de todos los valores",
        resumen=[
            "Nietzsche planeó durante años una obra principal con el título La voluntad de poder, pero la abandonó. Tras su muerte, su hermana Elisabeth Förster-Nietzsche y Peter Gast ordenaron sus notas de los años ochenta en un libro con ese nombre, en ediciones de 1901 y 1906.",
            "Los fragmentos tratan del nihilismo europeo, la crítica de los valores supremos, los principios de una nueva valoración y la disciplina y el eterno retorno. Los especialistas, desde la edición crítica de Colli y Montinari, consideran que la compilación no refleja un libro de Nietzsche y debe leerse con cautela.",
        ],
        ideas=["El nihilismo como desvalorización de los valores supremos.",
               "La voluntad de poder como esencia de la vida.",
               "La necesidad de una transvaloración de los valores.",
               "Una obra póstuma compilada por otros."],
        faq=[("¿Escribió Nietzsche La voluntad de poder?", "No como libro: es una selección de sus notas póstumas ordenada por su hermana y Peter Gast tras su muerte."),
             ("¿Qué es la voluntad de poder?", "El impulso fundamental de todo lo vivo a crecer, expandirse e imponer formas, que Nietzsche propone como clave para interpretar el mundo.")]),
}
