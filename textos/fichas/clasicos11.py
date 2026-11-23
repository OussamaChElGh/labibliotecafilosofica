"""Undécima tanda: clásicos extranjeros en traducciones antiguas de Wikisource (cola-tandas.csv, «hay versión en Wikisource»).

Traducciones: El príncipe (Madrid, 1854, anónima), El contrato social (1819, anónima), Ética a Nicómaco (Pedro Simón Abril,
siglo XVI), Poética (José Goya y Muniain, 1798), La vuelta al mundo en ochenta días (1885), Antígona (Antonio González Garbín, 1889) y Prometeo encadenado (Marcelino Menéndez y Pelayo).

1. python wikisource.py … --capitulos  (El contrato social con --partes, en el orden del libro);
   teatro_verso.py para Antígona y Prometeo.  En Git Bash, anteponer MSYS_NO_PATHCONV=1.
2. python textos/fichas/clasicos11.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clasicos  # noqa: E402

NUMBER_START = 80

BOOKS = {
    "el-principe-maquiavelo": {
        "color": "burdeos", "genero": "Ensayo político", "tema": "cómo conquistar y conservar el poder",
        "edition": "Edición española de 1854",
        "resumen": [
            "El príncipe es el tratado que Nicolás Maquiavelo escribió en 1513, apartado de la política florentina, y dedicó a Lorenzo de Médici. En veintiséis capítulos breves explica cómo se adquieren y se conservan los distintos tipos de principados: hereditarios, nuevos, conquistados con armas propias o ajenas, por fortuna o por virtud, eclesiásticos. Su modelo es César Borgia, que supo usar la astucia y la fuerza.",
            "Lo que hizo célebre y escandaloso el libro es su realismo: el príncipe debe aprender a no ser bueno cuando la necesidad lo exige, es mejor ser temido que amado si no se pueden ambas cosas, y debe saber ser zorro y león. Maquiavelo separa la política de la moral y termina con una exhortación a liberar Italia de los extranjeros. Esta edición de 1854 incluye una biografía del autor y la polémica del Anti-Maquiavelo.",
        ],
        "personajes": [("César Borgia", "Duque Valentino, modelo del príncipe nuevo que conquista por fortuna y se mantiene por virtud."),
                       ("Lorenzo de Médici", "Gobernante de Florencia a quien está dedicado el libro."),
                       ("Fernando el Católico", "Rey de Aragón, citado como ejemplo de príncipe astuto.")],
        "ideas": ["La política tiene sus propias reglas, distintas de la moral.",
                  "La virtù del gobernante frente a la fortuna.",
                  "Es más seguro ser temido que amado.",
                  "La necesidad de ejércitos propios y no mercenarios."],
        "faq": [("¿Qué significa «el fin justifica los medios»?", "La frase no aparece así en El príncipe, pero resume su idea de que el gobernante debe juzgarse por los resultados: conservar el Estado."),
                ("¿Es mejor ser amado o temido?", "Maquiavelo responde que lo ideal es ambas cosas, pero si hay que elegir, es más seguro ser temido, siempre que no se llegue a ser odiado."),
                ("¿A quién está dedicado?", "A Lorenzo di Piero de Médici, duque de Urbino."),
                ("¿Cuándo se escribió?", "En 1513. Se publicó en 1532, cinco años después de la muerte de Maquiavelo.")],
    },
    "el-contrato-social-rousseau": {
        "color": "azul", "genero": "Ensayo político", "tema": "la soberanía del pueblo y la voluntad general",
        "resumen": [
            "El contrato social, publicado en 1762, empieza con una de las frases más famosas de la filosofía política: «El hombre ha nacido libre, y en todas partes está encadenado». Jean-Jacques Rousseau busca una forma de asociación que proteja a cada persona y en la que, al unirse a todos, cada uno siga obedeciéndose a sí mismo y permanezca tan libre como antes.",
            "La respuesta es el pacto social: cada individuo entrega sus derechos a la comunidad entera, que se convierte en soberana y se guía por la voluntad general, orientada al bien común. Rousseau distingue el soberano (el pueblo) del gobierno (quien ejecuta las leyes), analiza la democracia, la aristocracia y la monarquía, y termina con la religión civil. Sus ideas influyeron en la Revolución francesa.",
        ],
        "personajes": [],
        "ideas": ["La legitimidad del poder nace de un pacto entre todos, no de la fuerza.",
                  "La voluntad general frente a la voluntad de todos.",
                  "La soberanía es del pueblo, inalienable e indivisible.",
                  "La libertad como obediencia a la ley que uno mismo se ha dado."],
        "faq": [("¿Qué es la voluntad general?", "La voluntad del pueblo como cuerpo, que busca el bien común. No es la suma de los intereses particulares, que Rousseau llama voluntad de todos."),
                ("¿Qué dice la primera frase?", "«El hombre ha nacido libre, y en todas partes está encadenado.»"),
                ("¿Cuántas partes tiene?", "Cuatro libros: el pacto social, la soberanía y la ley, el gobierno y las instituciones."),
                ("¿Cuándo se publicó?", "En 1762, el mismo año que el Emilio. Esta traducción al español es de 1819.")],
    },
    "etica-a-nicomaco-aristoteles": {
        "color": "ocre", "genero": "Filosofía", "unidad": "libros", "tema": "la felicidad, la virtud y la amistad",
        "resumen": [
            "La Ética a Nicómaco es la principal obra moral de Aristóteles, llamada así por su hijo Nicómaco, que la habría editado. Parte de una pregunta: ¿cuál es el bien supremo que todos buscamos? La respuesta es la felicidad (eudaimonía), entendida no como placer sino como una vida activa conforme a la virtud, propia de un ser racional.",
            "Aristóteles define la virtud como un término medio entre dos extremos, el exceso y el defecto: el valor está entre la cobardía y la temeridad, la generosidad entre la tacañería y el derroche. Estudia la justicia, la prudencia, el dominio de uno mismo, el placer y dedica dos libros enteros a la amistad, antes de concluir que la vida más feliz es la contemplativa. Esta es la traducción de Pedro Simón Abril, del siglo XVI.",
        ],
        "personajes": [],
        "ideas": ["La felicidad como fin último de la vida humana.",
                  "La virtud como hábito y como término medio.",
                  "La prudencia (frónesis) como sabiduría práctica.",
                  "La amistad como bien necesario para vivir."],
        "faq": [("¿Qué es la eudaimonía?", "La felicidad o plenitud: vivir y obrar bien según la razón y la virtud, a lo largo de toda una vida."),
                ("¿Qué es el término medio?", "La virtud está entre dos vicios, uno por exceso y otro por defecto. Por ejemplo, el valor entre la cobardía y la temeridad."),
                ("¿Por qué se llama Ética a Nicómaco?", "Por Nicómaco, hijo de Aristóteles, a quien se atribuye la edición de las lecciones de su padre."),
                ("¿Cuántos libros tiene?", "Diez. Los libros VIII y IX están dedicados a la amistad.")],
    },
    "poetica-aristoteles": {
        "color": "negro", "genero": "Filosofía", "tema": "la tragedia, la imitación y el arte de componer",
        "resumen": [
            "La Poética es el primer tratado de teoría literaria de Occidente. Aristóteles define las artes como formas de imitación (mímesis) y distingue la tragedia, la comedia y la epopeya por los medios, los objetos y el modo en que imitan. El ser humano, dice, aprende imitando y disfruta contemplando imitaciones.",
            "La parte central analiza la tragedia: la imitación de una acción seria y completa que, mediante la compasión y el temor, produce la catarsis de esas pasiones. Estudia sus partes (la fábula, los caracteres, el pensamiento, el lenguaje), la peripecia y la anagnórisis, y la figura del héroe trágico que cae por un error. Esta traducción de José Goya y Muniain, de 1798, está dedicada a Jovellanos.",
        ],
        "personajes": [],
        "ideas": ["El arte como imitación (mímesis).",
                  "La catarsis: la purificación de la compasión y el temor.",
                  "La fábula o trama como alma de la tragedia.",
                  "La unidad de acción y la verosimilitud."],
        "faq": [("¿Qué es la catarsis?", "La purificación o descarga de las pasiones de compasión y temor que produce en el espectador la tragedia."),
                ("¿Qué partes tiene la tragedia según Aristóteles?", "Seis: fábula, caracteres, elocución, pensamiento, espectáculo y canto. La más importante es la fábula."),
                ("¿Hay una segunda parte sobre la comedia?", "Se cree que existió un segundo libro sobre la comedia, que se perdió."),
                ("¿Quién hizo esta traducción?", "José Goya y Muniain, que la publicó en Madrid en 1798.")],
    },
    "la-vuelta-al-mundo-en-ochenta-dias-julio-verne": {
        "color": "azul", "genero": "Novela", "tema": "la aventura, la puntualidad y el viaje alrededor del mundo",
        "resumen": [
            "En el Reform Club de Londres, el metódico Phileas Fogg apuesta veinte mil libras a que es capaz de dar la vuelta al mundo en ochenta días. Esa misma noche parte con su nuevo criado francés, Picaporte (Passepartout), en un viaje en tren y en barco por Suez, Bombay, Calcuta, Hong Kong, Yokohama, San Francisco y Nueva York.",
            "Por el camino rescatan en la India a una joven viuda, Aouda, a punto de ser quemada en la pira de su marido, y los persigue el inspector Fix, convencido de que Fogg es el ladrón de un banco. Cuando creen haber perdido la apuesta por cinco minutos, descubren que, al viajar hacia el este, han ganado un día. Fogg gana la apuesta y se casa con Aouda.",
        ],
        "personajes": [("Phileas Fogg", "Caballero inglés, frío y puntual, que hace la apuesta."),
                       ("Picaporte (Passepartout)", "Criado francés de Fogg, ingenioso y leal."),
                       ("Aouda", "Joven india salvada de la muerte, que acaba casándose con Fogg."),
                       ("El inspector Fix", "Detective que persigue a Fogg creyéndolo un ladrón.")],
        "ideas": ["La aventura del viaje y la confianza en el progreso técnico.",
                  "La puntualidad y el cálculo frente a los imprevistos.",
                  "El contraste entre culturas.",
                  "La lealtad y el valor por encima del dinero."],
        "faq": [("¿Cómo gana Fogg la apuesta?", "Al dar la vuelta al mundo hacia el este gana un día sin darse cuenta. Llega al club justo a tiempo."),
                ("¿Por qué lo persigue el inspector Fix?", "Porque cree que Fogg es el hombre que ha robado cincuenta y cinco mil libras del Banco de Inglaterra."),
                ("¿Hay un viaje en globo?", "No en la novela. El globo aparece en las películas, pero Fogg viaja en tren, barco, elefante y trineo."),
                ("¿Cuándo se publicó?", "En 1872 por entregas, y en libro en 1873.")],
    },
    "antigona-sofocles": {
        "color": "burdeos", "genero": "Tragedia", "unidad": "partes: el estudio del traductor y la tragedia", "tema": "la ley de los dioses frente a la ley del Estado", "edition": "La Antígona de Sófocles, la Apología de Sócrates y Las poetisas de Lesbos, 1889",
        "resumen": [
            "Tras la guerra entre los hijos de Edipo, Eteocles y Polinices mueren uno a manos del otro. Creonte, nuevo rey de Tebas, ordena enterrar con honores a Eteocles y dejar el cuerpo de Polinices sin sepultura, para que lo devoren las aves, por haber atacado la ciudad. Antígona, hermana de ambos, decide desobedecer: las leyes no escritas de los dioses mandan enterrar a los muertos.",
            "Su hermana Ismena no se atreve a ayudarla. Antígona cubre el cadáver, es descubierta y condenada a ser enterrada viva en una cueva. El adivino Tiresias advierte a Creonte de su error, pero cuando el rey rectifica ya es tarde: Antígona se ha ahorcado, su prometido Hemón, hijo de Creonte, se quita la vida junto a ella, y la reina Eurídice también se suicida.",
        ],
        "personajes": [("Antígona", "Hija de Edipo, que entierra a su hermano contra la orden del rey."),
                       ("Creonte", "Rey de Tebas, firme en defender la ley de la ciudad."),
                       ("Ismena", "Hermana de Antígona, prudente y temerosa."),
                       ("Hemón", "Hijo de Creonte y prometido de Antígona."),
                       ("Tiresias", "Adivino ciego que anuncia la desgracia."),
                       ("El coro de ancianos tebanos", "Comenta y juzga la acción.")],
        "ideas": ["La ley divina y la conciencia frente a la ley del Estado.",
                  "La obstinación del poder y sus consecuencias.",
                  "El deber familiar y religioso.",
                  "El destino trágico de la familia de Edipo."],
        "faq": [("¿Por qué Antígona entierra a su hermano?", "Porque considera que las leyes de los dioses, que obligan a enterrar a los muertos, están por encima de las órdenes de un rey."),
                ("¿Cómo termina Antígona?", "Antígona se ahorca en la cueva donde la han encerrado; Hemón y Eurídice se suicidan, y Creonte queda solo y destrozado."),
                ("¿Quién escribió Antígona?", "Sófocles, hacia el año 442 a. C. Forma con Edipo rey y Edipo en Colono el ciclo tebano."),
                ("¿Quién hizo esta traducción?", "Antonio González Garbín, catedrático de griego en Granada, publicada en 1889.")],
    },
    "prometeo-encadenado-esquilo": {
        "color": "ocre", "genero": "Tragedia", "unidad": "partes", "tema": "la rebeldía, el castigo y la libertad", "edition": "Odas, epístolas y tragedias",
        "resumen": [
            "Por orden de Zeus, Hefesto, acompañado del Poder y la Fuerza, encadena al titán Prometeo a una roca del Cáucaso. Su crimen ha sido robar el fuego a los dioses y dárselo a los hombres, a los que además enseñó las artes, los números y la escritura. Solo e inmóvil, Prometeo recibe la visita de las Oceánides, del dios Océano y de la desdichada Ío, perseguida por un tábano.",
            "Prometeo conoce un secreto que amenaza el poder de Zeus y se niega a revelarlo, pese a las amenazas de Hermes. La obra termina con un terremoto que lo precipita al abismo sin que haya cedido. Esquilo convierte a Prometeo en el gran símbolo de la rebeldía frente al poder y del amor a la humanidad. La traducción es de Marcelino Menéndez y Pelayo.",
        ],
        "personajes": [("Prometeo", "Titán que dio el fuego a los hombres y es castigado por Zeus."),
                       ("Hefesto", "Dios herrero que lo encadena contra su voluntad."),
                       ("Las Oceánides", "Coro de hijas de Océano que compadecen a Prometeo."),
                       ("Ío", "Joven convertida en vaca y perseguida por la ira de Hera."),
                       ("Hermes", "Mensajero de Zeus que exige el secreto de Prometeo.")],
        "ideas": ["La rebeldía frente a un poder tiránico.",
                  "El progreso humano como regalo de Prometeo: el fuego y las artes.",
                  "El sufrimiento del que ayuda a los demás.",
                  "El conocimiento del futuro como arma."],
        "faq": [("¿Por qué castigan a Prometeo?", "Por robar el fuego a los dioses y dárselo a los hombres, desobedeciendo a Zeus."),
                ("¿Qué secreto conoce Prometeo?", "Que un hijo de Zeus con cierta diosa (Tetis) podría destronarlo. Se niega a decirlo."),
                ("¿Quién escribió Prometeo encadenado?", "Se atribuye a Esquilo, el más antiguo de los grandes trágicos griegos (siglo V a. C.)."),
                ("¿Quién hizo esta traducción?", "Marcelino Menéndez y Pelayo, en 1879; la incluyó en Odas, epístolas y tragedias.")],
    },
}


if __name__ == "__main__":
    clasicos.BOOKS = BOOKS
    clasicos.NUMBER_START = NUMBER_START
    clasicos.main()
