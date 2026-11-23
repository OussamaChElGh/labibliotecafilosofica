"""Duodécima tanda: los más descargados de Elejandría (elejandria-titulos.csv), desde sus ePub.

1. python epub.py <ePub> <slug> --titulo … --autor … --ficha … --fuente <URL de Elejandría>   (ver tanda-12-descargas.md)
2. python textos/fichas/fix_epub12.py   (capítulos reales y sin páginas de promoción)
3. python textos/fichas/clasicos12.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clasicos  # noqa: E402

NUMBER_START = 87

BOOKS = {
    "don-quijote-de-la-mancha-cervantes": {
        "color": "ocre", "genero": "Novela", "tema": "la locura, los ideales y la realidad",
        "resumen": [
            "Alonso Quijano, un hidalgo de un lugar de la Mancha, lee tantos libros de caballerías que pierde el juicio y decide hacerse caballero andante con el nombre de don Quijote. Con una armadura vieja, su caballo Rocinante y una dama imaginaria, Dulcinea del Toboso, sale a deshacer agravios. En su segunda salida le acompaña como escudero Sancho Panza, un labrador sencillo al que promete el gobierno de una ínsula.",
            "Don Quijote confunde molinos con gigantes, rebaños con ejércitos y ventas con castillos, y casi siempre sale malparado. En la segunda parte (1615) los protagonistas son ya famosos por el primer libro, y unos duques se divierten engañándolos; Sancho llega a gobernar la ínsula Barataria. Vencido por el Caballero de la Blanca Luna, don Quijote vuelve a casa, recobra la cordura y muere como Alonso Quijano el Bueno. Es la primera novela moderna.",
        ],
        "personajes": [("Don Quijote de la Mancha", "Alonso Quijano, hidalgo que enloquece leyendo libros de caballerías."),
                       ("Sancho Panza", "Su escudero, labrador práctico y refranero."),
                       ("Dulcinea del Toboso", "Dama idealizada por don Quijote; en realidad, la labradora Aldonza Lorenzo."),
                       ("Rocinante", "El viejo caballo de don Quijote."),
                       ("Sansón Carrasco", "Bachiller que, disfrazado de caballero, intenta devolverlo a casa."),
                       ("El cura y el barbero", "Amigos de don Quijote que queman sus libros.")],
        "ideas": ["La frontera entre la locura y la cordura, la ficción y la realidad.",
                  "La parodia de los libros de caballerías.",
                  "El idealismo de don Quijote frente al realismo de Sancho.",
                  "La novela que habla de sí misma: los personajes leen la primera parte."],
        "faq": [("¿De qué trata el Quijote?", "De un hidalgo que enloquece leyendo libros de caballerías y sale a recorrer España como caballero andante, acompañado de su escudero Sancho Panza."),
                ("¿Cómo empieza el Quijote?", "«En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero…»"),
                ("¿Qué pasa con los molinos de viento?", "Don Quijote los toma por gigantes y los ataca; una aspa lo derriba. Es la aventura más famosa del libro."),
                ("¿Cómo termina el Quijote?", "Don Quijote vuelve a casa, enferma, recupera el juicio, reniega de los libros de caballerías y muere."),
                ("¿Cuándo se publicó?", "La primera parte en 1605 y la segunda en 1615.")],
    },
    "crimen-y-castigo-dostoyevski": {
        "color": "negro", "genero": "Novela", "tema": "la culpa, la redención y los límites morales",
        "resumen": [
            "Rodión Raskólnikov, un estudiante pobre de San Petersburgo, se convence de que ciertos hombres extraordinarios tienen derecho a saltarse la moral si es por un fin superior. Para probarlo, asesina con un hacha a una vieja prestamista, y también a su hermana Lizaveta, que lo sorprende. No llega a usar el dinero que roba.",
            "Desde ese momento, la fiebre y la culpa lo consumen. El juez Porfiri Petróvich sospecha de él y juega con su conciencia; Sonia, una joven obligada a prostituirse para mantener a su familia, le ofrece el camino del arrepentimiento. Raskólnikov acaba confesando y es condenado a trabajos forzados en Siberia, donde Sonia lo acompaña y comienza su redención.",
        ],
        "personajes": [("Rodión Raskólnikov", "Estudiante pobre y orgulloso que comete un doble asesinato."),
                       ("Sonia Marmeládova", "Joven humilde y creyente que lo lleva a la confesión."),
                       ("Porfiri Petróvich", "Juez de instrucción que acorrala psicológicamente a Raskólnikov."),
                       ("Dunia", "Hermana de Raskólnikov."),
                       ("Razumijin", "Amigo fiel de Raskólnikov."),
                       ("Svidrigáilov", "Hombre cínico y depravado que persigue a Dunia.")],
        "ideas": ["La culpa como castigo más duro que la ley.",
                  "La teoría del hombre extraordinario y sus límites.",
                  "La redención a través del sufrimiento y el amor.",
                  "La pobreza de San Petersburgo."],
        "faq": [("¿De qué trata Crimen y castigo?", "De Raskólnikov, un estudiante que mata a una prestamista para demostrar una teoría, y de la culpa que lo lleva a confesar."),
                ("¿Por qué mata Raskólnikov?", "Porque cree que los hombres extraordinarios, como Napoleón, pueden cometer crímenes por un fin superior. Quiere probar que él es uno de ellos."),
                ("¿Cómo termina?", "Raskólnikov confiesa y es enviado a Siberia. Sonia lo sigue y en el epílogo empieza su regeneración."),
                ("¿Cuándo se publicó?", "En 1866, por entregas en la revista El Mensajero Ruso.")],
    },
    "noches-blancas-dostoyevski": {
        "color": "azul", "genero": "Novela corta", "unidad": "noches", "tema": "la soledad, el amor y el ensueño",
        "resumen": [
            "Un joven solitario, que se llama a sí mismo un soñador, pasea por San Petersburgo durante las noches blancas del verano, cuando casi no oscurece. Una noche encuentra llorando junto al canal a Nástenka, una muchacha a la que salva de un desconocido, y quedan en volver a verse.",
            "Durante cuatro noches, ella le cuenta su historia: espera desde hace un año a un inquilino del que se enamoró y que prometió volver. El soñador, que se ha enamorado de ella, la ayuda a escribirle. Cuando parece que ella empieza a corresponderle, el antiguo amor aparece. A la mañana siguiente, el soñador recibe una carta de Nástenka y se queda con el recuerdo de un minuto de felicidad.",
        ],
        "personajes": [("El soñador", "Narrador sin nombre, joven solitario que vive en sus fantasías."),
                       ("Nástenka", "Muchacha de diecisiete años que vive con su abuela ciega."),
                       ("El inquilino", "Joven del que Nástenka está enamorada.")],
        "ideas": ["La soledad en la gran ciudad.", "El amor idealizado y no correspondido.",
                  "El ensueño frente a la vida real.", "La felicidad de un instante."],
        "faq": [("¿Qué son las noches blancas?", "Las noches de verano en San Petersburgo en las que el sol apenas se pone y no llega a oscurecer."),
                ("¿Cómo termina Noches blancas?", "Nástenka se va con su antiguo amor. El soñador queda solo, agradecido por «un minuto entero de felicidad»."),
                ("¿Cuándo se publicó?", "En 1848. Es una de las primeras obras de Dostoyevski.")],
    },
    "memorias-del-subsuelo-dostoyevski": {
        "color": "negro", "genero": "Novela", "unidad": "partes", "tema": "la conciencia, la libertad y el resentimiento",
        "resumen": [
            "Un antiguo funcionario de San Petersburgo, encerrado en su «subsuelo», escribe unas memorias amargas. En la primera parte reflexiona contra la idea de que el ser humano actúa siempre por su propio interés racional: el hombre prefiere a veces lo absurdo y lo que le perjudica, solo para afirmar su libertad.",
            "En la segunda parte recuerda episodios de su juventud: su obsesión por un oficial que lo ignoró, una cena humillante con antiguos compañeros de escuela y su encuentro con Liza, una joven prostituta a la que primero conmueve y luego humilla. Es considerada la primera novela existencialista.",
        ],
        "personajes": [("El hombre del subsuelo", "Narrador sin nombre, solitario, hipersensible y rencoroso."),
                       ("Liza", "Joven prostituta a la que el narrador trata con crueldad."),
                       ("Zverkov", "Antiguo compañero de escuela, triunfador y vulgar.")],
        "ideas": ["La crítica al racionalismo y al utilitarismo.", "La libertad como capricho y como sufrimiento.",
                  "La conciencia excesiva que paraliza.", "El resentimiento y la humillación."],
        "faq": [("¿Por qué se considera existencialista?", "Porque pone en el centro la libertad individual, la angustia y la conciencia frente a cualquier sistema racional."),
                ("¿Qué partes tiene?", "Dos: «El subsuelo», un monólogo filosófico, y «A propósito de la nieve húmeda», el relato de su juventud."),
                ("¿Cuándo se publicó?", "En 1864.")],
    },
    "el-principito-saint-exupery": {
        "color": "azul", "genero": "Novela corta", "tema": "la amistad, el amor y lo esencial",
        "resumen": [
            "Un aviador cae con su avión en el desierto del Sahara. Allí aparece un niño de cabellos dorados que le pide que le dibuje un cordero: es el principito, que viene de un asteroide diminuto donde vive con tres volcanes y una rosa orgullosa a la que ama.",
            "El principito le cuenta su viaje por otros planetas, habitados por adultos absurdos: un rey sin súbditos, un vanidoso, un bebedor, un hombre de negocios, un farolero y un geógrafo. En la Tierra conoce a una serpiente y a un zorro que le enseña a crear lazos: «Lo esencial es invisible a los ojos». Al cumplirse un año de su llegada, decide volver con su rosa.",
        ],
        "personajes": [("El principito", "Niño que viene del asteroide B 612."),
                       ("El aviador", "Narrador, piloto perdido en el desierto."),
                       ("La rosa", "Flor vanidosa y frágil a la que el principito ama."),
                       ("El zorro", "Le enseña el valor de la amistad y de «domesticar»."),
                       ("La serpiente", "Promete ayudarle a volver a su planeta.")],
        "ideas": ["Lo esencial es invisible a los ojos.", "La crítica al mundo de los adultos.",
                  "La amistad y la responsabilidad por lo que amamos.", "La mirada de la infancia."],
        "faq": [("¿Qué significa «lo esencial es invisible a los ojos»?", "Que lo más importante, como el amor o la amistad, no se ve: se siente con el corazón. Se lo dice el zorro."),
                ("¿Qué representa la rosa?", "El amor: es única para el principito porque la ha cuidado, aunque haya miles de rosas iguales."),
                ("¿Cuándo se publicó?", "En 1943, en Nueva York. Saint-Exupéry murió en 1944.")],
    },
    "el-arte-de-la-guerra-sun-tzu": {
        "color": "burdeos", "genero": "Tratado", "tema": "la estrategia, la astucia y el liderazgo",
        "resumen": [
            "El arte de la guerra es un tratado de estrategia militar atribuido a Sun Tzu, un general chino del siglo V a. C. En trece capítulos breves explica cómo planificar una campaña, cuándo combatir y cuándo no, cómo aprovechar el terreno, el engaño y el uso de espías.",
            "Su idea central es que la mejor victoria es la que se consigue sin luchar, y que hay que conocer bien al enemigo y a uno mismo. Por su enfoque práctico se lee hoy como un libro de estrategia aplicado a la empresa, la política o el deporte.",
        ],
        "personajes": [],
        "ideas": ["Vencer sin combatir es la mayor excelencia.", "Conoce a tu enemigo y conócete a ti mismo.",
                  "Toda guerra se basa en el engaño.", "La importancia del terreno y de la información."],
        "faq": [("¿Qué dice la frase más famosa?", "«Conoce a tu enemigo y conócete a ti mismo, y en cien batallas no correrás peligro.»"),
                ("¿Cuántos capítulos tiene?", "Trece, desde la evaluación inicial hasta el uso de los espías."),
                ("¿Por qué se usa en empresas?", "Porque sus principios sobre planificación, información y liderazgo se aplican a cualquier competencia.")],
    },
    "meditaciones-marco-aurelio": {
        "color": "ocre", "genero": "Filosofía", "unidad": "libros", "tema": "el estoicismo y el dominio de uno mismo",
        "resumen": [
            "Las Meditaciones son las notas personales que el emperador romano Marco Aurelio escribió en griego, entre campañas militares, durante los últimos años de su vida. No las escribió para publicarlas: son ejercicios para recordarse a sí mismo cómo vivir según la filosofía estoica.",
            "En doce libros breves reflexiona sobre la brevedad de la vida, la muerte, el deber, la aceptación de lo que no depende de nosotros y la importancia de actuar con justicia. El primer libro es un agradecimiento a quienes le enseñaron algo. Es uno de los libros de filosofía más leídos de todos los tiempos.",
        ],
        "personajes": [],
        "ideas": ["Distinguir lo que depende de nosotros de lo que no.", "La brevedad de la vida y la aceptación de la muerte.",
                  "Vivir conforme a la razón y a la naturaleza.", "El deber hacia los demás y el bien común."],
        "faq": [("¿Qué es el estoicismo?", "Una escuela filosófica que enseña a vivir con serenidad, aceptando lo que no podemos cambiar y actuando con virtud."),
                ("¿Para quién escribió Marco Aurelio?", "Para sí mismo. El título original griego significa «A sí mismo»."),
                ("¿Cuántos libros tiene?", "Doce.")],
    },
    "de-la-brevedad-de-la-vida-seneca": {
        "color": "verde", "genero": "Filosofía", "tema": "el tiempo y cómo vivir bien",
        "resumen": [
            "De la brevedad de la vida es un diálogo que Séneca dirige a su amigo Paulino. Su tesis es sencilla: la vida no es corta, somos nosotros quienes la acortamos al malgastarla en ocupaciones vacías, ambiciones, negocios, banquetes y preocupaciones por el qué dirán.",
            "Séneca critica a los «ocupados», que viven pendientes del futuro y nunca disponen de sí mismos, y propone dedicar el tiempo a la filosofía y a conversar con los sabios del pasado. Es uno de los textos estoicos más leídos y una lección vigente sobre el uso del tiempo.",
        ],
        "personajes": [],
        "ideas": ["La vida es larga si se sabe aprovechar.", "El tiempo es el bien más valioso.",
                  "La crítica a los ocupados.", "La filosofía como forma de vivir."],
        "faq": [("¿Qué dice Séneca sobre el tiempo?", "Que no recibimos una vida breve, sino que la hacemos breve; no somos pobres de tiempo, sino derrochadores."),
                ("¿A quién está dedicado?", "A Paulino, encargado del abastecimiento de trigo de Roma."),
                ("¿Cuándo se escribió?", "Hacia el año 49 d. C.")],
    },
    "la-divina-comedia-dante": {
        "color": "negro", "genero": "Poema", "unidad": "cantos", "tema": "el viaje por el más allá y la salvación del alma",
        "resumen": [
            "Perdido en una selva oscura a mitad de su vida, Dante es rescatado por el poeta Virgilio, que lo guía por el Infierno, un embudo de nueve círculos donde los condenados sufren castigos según sus pecados, y por el Purgatorio, una montaña donde las almas se purifican.",
            "En la cima, Beatriz, la mujer que Dante amó, lo conduce por el Paraíso, a través de las esferas celestes, hasta la visión de Dios. Los cien cantos están llenos de personajes históricos de la Italia de su tiempo. Esta es la versión en prosa de Manuel Aranda y Sanjuán.",
        ],
        "personajes": [("Dante", "El poeta, protagonista del viaje."), ("Virgilio", "Poeta latino que lo guía por el Infierno y el Purgatorio."),
                       ("Beatriz", "Amada de Dante, que lo guía por el Paraíso."), ("Francesca y Paolo", "Amantes condenados en el segundo círculo."),
                       ("Ulises", "Héroe griego castigado entre los consejeros fraudulentos.")],
        "ideas": ["El viaje del alma del pecado a la salvación.", "La justicia divina: cada castigo corresponde a su culpa.",
                  "El amor como fuerza que mueve el universo.", "La política de Florencia vista desde el más allá."],
        "faq": [("¿Qué partes tiene?", "Tres cánticas: Infierno, Purgatorio y Paraíso, con cien cantos en total."),
                ("¿Cuántos círculos tiene el Infierno?", "Nueve, cada vez más profundos y con pecados más graves."),
                ("¿Qué dice la puerta del Infierno?", "«Abandonad toda esperanza los que entráis.»"),
                ("¿Quién hizo esta traducción?", "Manuel Aranda y Sanjuán, en prosa, en el siglo XIX.")],
    },
    "la-metamorfosis-kafka": {
        "color": "verde", "genero": "Novela corta", "tema": "la alienación, la familia y el absurdo",
        "resumen": [
            "Una mañana, Gregorio Samsa, un viajante de comercio que mantiene a toda su familia, despierta convertido en un monstruoso insecto. Su primera preocupación no es su cuerpo, sino haber perdido el tren para ir a trabajar.",
            "Encerrado en su cuarto, Gregorio pasa a ser una carga para sus padres y su hermana Grete, que al principio lo cuida y acaba rechazándolo. Herido por una manzana que le lanza su padre, se va apagando hasta morir. La familia, aliviada, sale de paseo y hace planes para el futuro.",
        ],
        "personajes": [("Gregorio Samsa", "Viajante convertido en insecto."), ("Grete", "Su hermana, que primero lo cuida y luego lo rechaza."),
                       ("El padre", "Hombre autoritario que vuelve a trabajar."), ("La madre", "Débil y asustada ante su hijo.")],
        "ideas": ["La alienación del trabajo.", "La familia que solo valora a quien es útil.",
                  "El absurdo de la existencia.", "La soledad y la incomunicación."],
        "faq": [("¿En qué se convierte Gregorio?", "En un insecto monstruoso, que se suele imaginar como un escarabajo o una cucaracha; Kafka no lo precisa."),
                ("¿Cómo termina?", "Gregorio muere y la familia, liberada, sale al campo y piensa en casar a Grete."),
                ("¿Cuándo se publicó?", "En 1915.")],
    },
    "asi-hablo-zaratustra-nietzsche": {
        "color": "burdeos", "genero": "Filosofía", "unidad": "discursos", "tema": "el superhombre, la muerte de Dios y el eterno retorno",
        "resumen": [
            "Zaratustra, tras diez años de soledad en la montaña, baja a enseñar a los hombres. Su primer anuncio es que Dios ha muerto y que el hombre es algo que debe ser superado: hay que crear el superhombre. Pero la multitud del mercado se ríe de él, y Zaratustra decide buscar compañeros y discípulos.",
            "A lo largo de cuatro partes, en discursos y parábolas de estilo poético, habla de las tres transformaciones del espíritu, de la voluntad de poder, de la crítica a la moral de los débiles y, sobre todo, del eterno retorno: vivir de tal modo que se quiera repetir la vida infinitas veces. Es la obra más famosa de Nietzsche.",
        ],
        "personajes": [("Zaratustra", "Profeta que anuncia el superhombre."), ("El santo del bosque", "Anciano que aún no sabe que Dios ha muerto."),
                       ("El águila y la serpiente", "Animales de Zaratustra."), ("Los hombres superiores", "Visitantes de la cuarta parte.")],
        "ideas": ["La muerte de Dios.", "El superhombre.", "La voluntad de poder.", "El eterno retorno de lo mismo."],
        "faq": [("¿Qué es el superhombre?", "El ideal de un ser humano que crea sus propios valores tras la muerte de Dios."),
                ("¿Qué es el eterno retorno?", "La idea de que todo se repetirá infinitas veces; Nietzsche la usa como prueba para afirmar la vida."),
                ("¿Cuándo se publicó?", "Entre 1883 y 1885, en cuatro partes.")],
    },
    "la-republica-platon": {
        "color": "ocre", "genero": "Filosofía", "unidad": "libros", "tema": "la justicia y la ciudad ideal",
        "resumen": [
            "La República es el gran diálogo de Platón. Empieza con una pregunta, ¿qué es la justicia?, que Sócrates discute con Céfalo, Polemarco y el sofista Trasímaco, para quien lo justo es lo que conviene al más fuerte. Para responder, Sócrates imagina una ciudad ideal y estudia la justicia a gran escala.",
            "La ciudad tiene tres clases (gobernantes, guardianes y productores), igual que el alma tiene razón, ánimo y deseo; la justicia es que cada parte cumpla su función. La gobiernan los filósofos, que conocen la idea del Bien. El libro VII contiene el mito de la caverna, y el último termina con el mito de Er sobre el destino del alma.",
        ],
        "personajes": [("Sócrates", "Dirige la conversación."), ("Glaucón y Adimanto", "Hermanos de Platón, principales interlocutores."),
                       ("Trasímaco", "Sofista que defiende que la justicia es lo que conviene al más fuerte."),
                       ("Céfalo y Polemarco", "Padre e hijo, en cuya casa transcurre el diálogo.")],
        "ideas": ["La justicia en el alma y en la ciudad.", "El gobierno de los filósofos.",
                  "El mito de la caverna y la teoría de las Ideas.", "La educación de los guardianes."],
        "faq": [("¿Qué es el mito de la caverna?", "Una alegoría del libro VII: prisioneros que solo ven sombras en la pared creen que son la realidad, hasta que uno sale y ve el sol."),
                ("¿Qué es el rey filósofo?", "La idea de que la ciudad solo será justa si la gobiernan quienes aman la sabiduría."),
                ("¿Cuántos libros tiene?", "Diez.")],
    },
    "frankenstein-mary-shelley": {
        "color": "verde", "genero": "Novela", "tema": "la ciencia, la creación y la soledad",
        "resumen": [
            "En el Ártico, el explorador Robert Walton rescata del hielo a Victor Frankenstein, que le cuenta su historia. De joven, obsesionado con los secretos de la vida, Victor reunió restos humanos y les dio vida en su laboratorio. Horrorizado por el aspecto de su criatura, la abandonó la misma noche de su nacimiento.",
            "La criatura, sola y rechazada por todos, aprende a hablar y a leer espiando a una familia, pero su fealdad le cierra todas las puertas. Pide a Victor una compañera; cuando él se niega, se venga matando a su hermano, a su amigo y a su esposa. Creador y criatura se persiguen hasta los hielos del Polo.",
        ],
        "personajes": [("Victor Frankenstein", "Joven científico que da vida a la criatura."), ("La criatura", "Ser creado por Victor, inteligente y desdichado."),
                       ("Robert Walton", "Explorador que recoge la historia en sus cartas."), ("Elizabeth", "Prometida de Victor."),
                       ("Henry Clerval", "Amigo de Victor.")],
        "ideas": ["Los límites de la ciencia.", "La responsabilidad del creador.",
                  "El rechazo y la soledad como origen del mal.", "La naturaleza frente a la ambición humana."],
        "faq": [("¿Frankenstein es el monstruo?", "No. Frankenstein es el científico, Victor; la criatura no tiene nombre."),
                ("¿Cómo termina?", "Victor muere en el barco de Walton y la criatura anuncia que se quitará la vida en el hielo."),
                ("¿Cuándo se publicó?", "En 1818. Mary Shelley tenía veinte años.")],
    },
    "dracula-bram-stoker": {
        "color": "negro", "genero": "Novela", "tema": "el vampiro, el miedo y la lucha contra el mal",
        "resumen": [
            "Jonathan Harker, un joven abogado inglés, viaja a Transilvania para cerrar la compra de una casa en Londres por parte del conde Drácula. En el castillo descubre que es prisionero de un ser que no se refleja en los espejos y duerme en un ataúd. Mientras, Drácula viaja a Inglaterra.",
            "En Whitby, Lucy Westenra, amiga de Mina, la prometida de Jonathan, enferma y muere convertida en vampira. El profesor Van Helsing reúne a sus pretendientes, a Jonathan y a Mina para perseguir a Drácula hasta su castillo. La novela está contada a través de diarios, cartas y recortes de periódico.",
        ],
        "personajes": [("El conde Drácula", "Noble vampiro de Transilvania."), ("Jonathan Harker", "Abogado prisionero en el castillo."),
                       ("Mina Murray", "Prometida y luego esposa de Jonathan."), ("Lucy Westenra", "Amiga de Mina, víctima del conde."),
                       ("Abraham Van Helsing", "Médico y sabio que dirige la caza del vampiro.")],
        "ideas": ["El miedo a lo desconocido.", "La modernidad frente a lo arcaico.",
                  "El deseo y la sexualidad reprimida.", "La unión de un grupo contra el mal."],
        "faq": [("¿Cómo está contada?", "Mediante diarios, cartas, telegramas y artículos de prensa de los personajes."),
                ("¿Cómo termina?", "Los cazadores alcanzan a Drácula en Transilvania y lo matan antes de la puesta del sol."),
                ("¿Cuándo se publicó?", "En 1897.")],
    },
    "alicia-en-el-pais-de-las-maravillas-lewis-carroll": {
        "color": "azul", "genero": "Novela", "tema": "el absurdo, la lógica y el mundo de los sueños",
        "resumen": [
            "Una tarde de verano, Alicia ve pasar a un conejo blanco con chaleco y reloj, lo sigue por una madriguera y cae a un mundo absurdo. Allí cambia de tamaño al comer y beber, llora un mar de lágrimas y conoce a criaturas extrañas: la Oruga, el Gato de Cheshire, el Sombrerero Loco y la Liebre de Marzo.",
            "Llega al jardín de la Reina de Corazones, que manda cortar la cabeza a todo el mundo, juega a un croquet con flamencos y asiste al juicio por el robo de unas tartas. Cuando se enfrenta a la corte, despierta: todo había sido un sueño.",
        ],
        "personajes": [("Alicia", "Niña curiosa y razonadora."), ("El Conejo Blanco", "Siempre llega tarde."),
                       ("El Sombrerero Loco", "Anfitrión de una merienda sin fin."), ("El Gato de Cheshire", "Desaparece dejando su sonrisa."),
                       ("La Reina de Corazones", "Grita «¡Que le corten la cabeza!».")],
        "ideas": ["El absurdo y los juegos de lógica.", "La identidad: Alicia no sabe quién es al cambiar de tamaño.",
                  "La crítica al mundo adulto.", "El sueño como mundo alternativo."],
        "faq": [("¿Cómo termina Alicia?", "Alicia despierta junto a su hermana y descubre que todo fue un sueño."),
                ("¿Quién fue Lewis Carroll?", "Seudónimo de Charles Dodgson, matemático de Oxford."),
                ("¿Cuándo se publicó?", "En 1865.")],
    },
}


if __name__ == "__main__":
    clasicos.BOOKS = BOOKS
    clasicos.NUMBER_START = NUMBER_START
    clasicos.main()
