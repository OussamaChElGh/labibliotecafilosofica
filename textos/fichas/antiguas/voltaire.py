"""Fichas de Voltaire en el formato nuevo (fichas_antiguas.py)."""

AUTOR = "Voltaire"
RUTA = "/libros-pdf-gratis/autores/voltaire/"


def book(**data):
    data.setdefault("autor", AUTOR)
    data.setdefault("ruta_autor", RUTA)
    return data


BOOKS = {
    "/voltaire-candido/": book(
        titulo="Cándido", genero="Cuento filosófico", año="1759", tema="el optimismo y el mal en el mundo",
        descripcion="Cándido o el optimismo de Voltaire: resumen, personajes, ideas principales y preguntas frecuentes sobre la sátira de Pangloss y el «mejor de los mundos posibles».",
        resumen=[
            "Cándido es un joven ingenuo criado en el castillo del barón de Thunder-ten-tronckh, en Westfalia, donde su preceptor Pangloss le enseña que todo ocurre para bien en el mejor de los mundos posibles. Cuando lo sorprenden besando a Cunegunda, la hija del barón, lo expulsan a patadas y empieza un viaje por un mundo lleno de desgracias.",
            "Cándido sufre la guerra, el terremoto de Lisboa, la Inquisición, los jesuitas del Paraguay, el engaño y el robo; solo encuentra la felicidad en el país utópico de El Dorado, que abandona por amor. Acompañado de su criado Cacambo y del pesimista Martín, acaba en una granja de Turquía con Cunegunda, envejecida, y con Pangloss. Su conclusión pone fin a la filosofía: hay que cultivar nuestro jardín.",
        ],
        personajes=[("Cándido", "Joven bondadoso e ingenuo que aprende a pensar por sí mismo a fuerza de desgracias."),
                    ("Pangloss", "Preceptor que defiende el optimismo hasta el absurdo, pase lo que pase."),
                    ("Cunegunda", "Hija del barón y amor de Cándido, víctima de todos los abusos."),
                    ("Cacambo", "Criado mestizo, astuto y leal."),
                    ("Martín", "Sabio pesimista que acompaña a Cándido en la segunda parte."),
                    ("La vieja", "Criada de Cunegunda, hija de un papa, que cuenta una vida de desdichas.")],
        ideas=["Sátira del optimismo de Leibniz: el mundo no es el mejor de los posibles.",
               "Crítica de la guerra, la Inquisición, la esclavitud y el fanatismo.",
               "El Dorado como utopía de razón y tolerancia.",
               "Cultivar el propio jardín: el trabajo útil frente a la especulación."],
        faq=[("¿De qué trata Cándido de Voltaire?", "De un joven ingenuo educado en la idea de que vivimos en el mejor de los mundos posibles, que recorre el mundo y comprueba, a través de catástrofes y crueldades, que esa filosofía es absurda."),
             ("¿Qué significa «hay que cultivar nuestro jardín»?", "Es la conclusión de Cándido: en lugar de especular sobre el sentido del mal, hay que trabajar y hacer algo útil en el pequeño mundo que está a nuestro alcance."),
             ("¿A quién critica Voltaire en Cándido?", "Al optimismo filosófico de Leibniz y Wolff, representado por Pangloss, y además a la Iglesia, la nobleza, la guerra y la Inquisición."),
             ("¿Qué es El Dorado en Cándido?", "Un país utópico de América del Sur donde reinan la riqueza, la razón y la tolerancia, y del que Cándido se marcha para buscar a Cunegunda.")]),
    "/voltaire-zadig/": book(
        titulo="Zadig", genero="Cuento filosófico", año="1747", tema="el destino y la providencia",
        resumen=[
            "Zadig es un joven sabio y virtuoso de Babilonia que solo desea ser feliz, pero cada una de sus buenas acciones le trae una desgracia y algunas torpezas le traen fortuna. Es traicionado en el amor, acusado injustamente, nombrado primer ministro del rey Moabdar y obligado a huir por el amor que siente por la reina Astarté.",
            "En su exilio es esclavo, consejero, juez y viajero. Un ermitaño, que resulta ser el ángel Jesrad, le muestra que incluso los hechos que parecen injustos forman parte de un orden superior. Al final Zadig vence en un torneo, resuelve los enigmas de los sabios, se casa con Astarté y gobierna Babilonia con justicia.",
        ],
        personajes=[("Zadig", "Joven babilonio sabio y honrado, zarandeado por el destino."),
                    ("Astarté", "Reina de Babilonia, amada de Zadig."),
                    ("Moabdar", "Rey de Babilonia, celoso y caprichoso."),
                    ("Sétoc", "Mercader árabe que compra a Zadig como esclavo y se hace su amigo."),
                    ("Jesrad", "Ángel disfrazado de ermitaño que le explica el sentido del destino.")],
        ideas=["La virtud no garantiza la felicidad en este mundo.",
               "El destino parece arbitrario, pero quizá obedece a un orden que no comprendemos.",
               "Sátira de la corte, de los celos y de la superstición.",
               "El razonamiento por indicios: Zadig deduce cómo son el perro de la reina y el caballo del rey sin haberlos visto."],
        faq=[("¿De qué trata Zadig de Voltaire?", "De un joven sabio de Babilonia que sufre toda clase de desgracias inmerecidas hasta que un ángel le revela que el destino obedece a un orden superior. Al final llega a ser rey."),
             ("¿Por qué Zadig se relaciona con la novela policiaca?", "Porque en el capítulo del perro y el caballo Zadig deduce cómo eran los animales a partir de sus huellas, un método que anticipa a los detectives como Sherlock Holmes."),
             ("¿Cuál es el subtítulo de Zadig?", "Zadig o el destino. Historia oriental.")]),
    "/voltaire-el-ingenuo/": book(
        titulo="El ingenuo", genero="Cuento filosófico", año="1767", tema="la mirada natural frente a las instituciones",
        resumen=[
            "Un joven hurón llega desde Canadá a la Baja Bretaña y descubre que es sobrino del prior de Nuestra Señora de la Montaña. Lo llaman el Ingenuo porque dice siempre lo que piensa. Su sentido común choca con la Iglesia, las costumbres y las leyes de Francia, como cuando pretende bautizarse en un río o casarse sin más con la señorita de Saint-Yves, de la que se enamora.",
            "Tras defender la costa contra los ingleses viaja a Versalles para pedir una recompensa y acaba encerrado en la Bastilla, donde un jansenista, Gordon, lo inicia en la lectura y la filosofía. Para liberarlo, la señorita de Saint-Yves se entrega a un ministro corrupto y muere de vergüenza. El tono cómico se vuelve trágico.",
        ],
        personajes=[("El Ingenuo", "Joven criado entre los hurones, franco, valiente y lleno de sentido común."),
                    ("La señorita de Saint-Yves", "Joven bretona que ama al Ingenuo y se sacrifica por él."),
                    ("El prior de Kerkabon", "Tío del Ingenuo, buen hombre y un poco simple."),
                    ("Gordon", "Jansenista encarcelado en la Bastilla que se vuelve su maestro y amigo.")],
        ideas=["El buen salvaje revela lo absurdo de las costumbres europeas.",
               "Crítica de la arbitrariedad del poder absoluto: las cartas de detención y la Bastilla.",
               "La educación y la lectura forman al ser humano.",
               "La corrupción de la corte destruye a los inocentes."],
        faq=[("¿De qué trata El ingenuo de Voltaire?", "De un joven criado entre los hurones de Canadá que llega a Francia y, con su sentido común, deja en evidencia las contradicciones de la religión, la ley y la corte de Luis XIV."),
             ("¿Cómo termina El ingenuo?", "La señorita de Saint-Yves consigue la libertad del Ingenuo a cambio de entregarse a un ministro y muere de pena. El Ingenuo se convierte en un oficial respetado."),
             ("¿Cuándo se publicó El ingenuo?", "En 1767.")]),
    "/voltaire-la-princesa-de-babilonia/": book(
        titulo="La princesa de Babilonia", genero="Cuento filosófico", año="1768", tema="un viaje satírico por las naciones",
        resumen=[
            "El rey Belo de Babilonia organiza un concurso para casar a su hija Formosante: la ganará quien tense el arco de Nemrod y venza a un león. Gana un joven pastor desconocido, Amazán, de un país utópico a orillas del Ganges, que se marcha antes de recibir el premio. Formosante sale a buscarlo acompañada de un fénix que habla.",
            "El viaje la lleva por China, Escitia, Rusia, Escandinavia, Inglaterra, Venecia, Roma y España, siempre un paso por detrás de Amazán, que huye creyéndose traicionado. Voltaire aprovecha cada etapa para elogiar o satirizar a los pueblos de Europa, especialmente la Inquisición española. Al final los amantes se reencuentran y se casan.",
        ],
        personajes=[("Formosante", "Princesa de Babilonia que recorre el mundo en busca de Amazán."),
                    ("Amazán", "Pastor de los gangáridas, perfecto y celoso."),
                    ("El fénix", "Ave sabia que acompaña y aconseja a la princesa."),
                    ("Belo", "Rey de Babilonia, padre de Formosante.")],
        ideas=["Comparación satírica de las naciones europeas.",
               "Elogio de la tolerancia y crítica de la Inquisición.",
               "La utopía de los gangáridas, pueblo sabio y vegetariano.",
               "El viaje como forma de conocimiento."],
        faq=[("¿De qué trata La princesa de Babilonia?", "De Formosante, que recorre medio mundo buscando a Amazán, el pastor que la ganó en un concurso. Su viaje sirve a Voltaire para satirizar las costumbres de Europa."),
             ("¿Cuándo se publicó La princesa de Babilonia?", "En 1768.")]),
    "/voltaire-el-hombre-de-los-cuarenta-escudos/": book(
        titulo="El hombre de los cuarenta escudos", genero="Cuento filosófico", año="1768", tema="los impuestos y la economía",
        resumen=[
            "Un francés corriente, que vive de una tierra que le rinde cuarenta escudos al año, la renta media del país según los cálculos de la época, ve cómo los nuevos economistas proponen un impuesto único sobre la tierra que le quita la mitad de lo que tiene, mientras un rico financiero sin tierras no paga nada.",
            "En conversaciones con un geómetra, el hombre de los cuarenta escudos aprende sobre población, riqueza, comercio, monjes y enfermedades. Voltaire se burla de las teorías de los fisiócratas y defiende el sentido común en la economía.",
        ],
        personajes=[("El hombre de los cuarenta escudos", "Campesino honrado que padece las teorías de los economistas."),
                    ("El geómetra", "Interlocutor sabio que le explica cómo funciona el mundo.")],
        ideas=["Crítica del impuesto único de los fisiócratas.",
               "La injusticia fiscal entre propietarios y financieros.",
               "Reflexiones sobre población, riqueza y comercio.",
               "El sentido común frente a los sistemas abstractos."],
        faq=[("¿De qué trata El hombre de los cuarenta escudos?", "De un campesino que sufre el impuesto único propuesto por los fisiócratas; Voltaire lo usa para burlarse de las teorías económicas de su época."),
             ("¿Qué eran los fisiócratas?", "Economistas franceses del siglo XVIII que defendían que la tierra era la única fuente de riqueza y que debía pagar un impuesto único.")]),
    "/voltaire-el-toro-blanco/": book(
        titulo="El toro blanco", genero="Cuento filosófico", año="1774", tema="la Biblia vista con ironía",
        resumen=[
            "La princesa Amasidia, hija del rey Amasis de Egipto, pasea por la orilla del Nilo acompañada del sabio Mambrés y descubre un toro blanco del que se enamora. El toro es en realidad Nabucodonosor, rey de Babilonia y su antiguo amante, transformado en animal como castigo divino.",
            "A su alrededor aparecen animales famosos de la Biblia, como la serpiente del Edén, el asno de Balaam o la ballena de Jonás, que conversan con ingenio. Voltaire mezcla el cuento oriental con la parodia de los relatos bíblicos. Tras muchas peripecias, Nabucodonosor recupera su forma humana y se casa con la princesa.",
        ],
        personajes=[("Amasidia", "Princesa egipcia enamorada del toro blanco."),
                    ("El toro blanco", "Nabucodonosor, rey de Babilonia, transformado en animal."),
                    ("Mambrés", "Antiguo mago y sabio que protege a la princesa."),
                    ("La serpiente", "La serpiente del Edén, elocuente consejera.")],
        ideas=["Parodia de los relatos de la Biblia.",
               "Crítica de la credulidad y la superstición.",
               "El amor vence las metamorfosis y los castigos."],
        faq=[("¿De qué trata El toro blanco de Voltaire?", "De una princesa egipcia enamorada de un toro blanco que es en realidad el rey Nabucodonosor transformado. Es una parodia de los relatos bíblicos."),
             ("¿Cuándo se publicó El toro blanco?", "En 1774, en los últimos años de Voltaire.")]),
    "/voltaire-historia-de-jenni-o-el-sabio-y-el-ateo/": book(
        titulo="Historia de Jenni, o el sabio y el ateo", genero="Cuento filosófico", año="1775", tema="la existencia de Dios y la moral",
        resumen=[
            "Freind, un sabio inglés, acompaña al ejército a España, donde su hijo Jenni es apresado por la Inquisición y salvado en el último momento. De vuelta en Londres, Jenni se deja arrastrar por malas compañías, cae en el desenfreno y el ateísmo, y huye a América.",
            "Freind lo sigue hasta el Nuevo Mundo y allí sostiene una larga discusión con el ateo Birton. Con argumentos sobre el orden del universo y la necesidad de la moral, Freind lo convence de la existencia de un Dios remunerador y vengador. Jenni se arrepiente y vuelve a la virtud. Es una defensa del deísmo frente al ateísmo y al fanatismo.",
        ],
        personajes=[("Freind", "Sabio y deísta inglés, portavoz de Voltaire."),
                    ("Jenni", "Hijo de Freind, que se descarría y se redime."),
                    ("Birton", "Ateo con quien Freind debate en América.")],
        ideas=["Defensa del deísmo frente al ateísmo y al fanatismo.",
               "El orden del universo como prueba de un creador.",
               "La creencia en Dios como fundamento de la moral social."],
        faq=[("¿De qué trata Historia de Jenni?", "De un sabio deísta que rescata a su hijo del desenfreno y convence a un ateo de la existencia de Dios mediante un largo diálogo filosófico."),
             ("¿Era Voltaire ateo?", "No. Era deísta: creía en un Dios creador y garante de la moral, pero rechazaba las religiones reveladas y el fanatismo.")]),
    "/voltaire-asi-va-el-mundo/": book(
        titulo="Así va el mundo", genero="Cuento filosófico", año="1748", tema="el bien y el mal mezclados en la sociedad",
        resumen=[
            "El ángel Ituriel encarga al escita Babuc que visite Persépolis y le informe de si la ciudad merece ser destruida por sus vicios. Babuc recorre la capital y ve guerras absurdas, templos ruidosos, jueces que compran sus cargos y mujeres infieles, y se indigna.",
            "Pero también descubre generosidad, cultura, comercio honrado y personas virtuosas. Para dar su veredicto encarga una estatua hecha con todos los metales y piedras, preciosos y viles, y pregunta al ángel si destruiría una figura tan bella por no ser toda de oro. Ituriel decide dejar que el mundo siga como va.",
        ],
        personajes=[("Babuc", "Escita enviado a juzgar Persépolis."),
                    ("Ituriel", "Ángel que debe decidir el destino de la ciudad.")],
        ideas=["En toda sociedad se mezclan el bien y el mal.",
               "Juzgar con prudencia antes de condenar.",
               "Sátira de París bajo el disfraz de Persépolis."],
        faq=[("¿De qué trata Así va el mundo de Voltaire?", "Un ángel envía a Babuc a Persépolis para decidir si debe destruirse por sus vicios; Babuc descubre que el bien y el mal están mezclados y la ciudad se salva."),
             ("¿Cuál es el título completo?", "Así va el mundo, visión de Babuc escrita por él mismo.")]),
    "/voltaire-diccionario-filosofico/": book(
        titulo="Diccionario filosófico", genero="Ensayo", año="1764", tema="la crítica de la superstición y el fanatismo",
        resumen=[
            "El Diccionario filosófico portátil es una colección de artículos breves ordenados alfabéticamente, de Abraham a Virtud, pensado para circular con facilidad y burlar la censura. Voltaire lo publicó de forma anónima y lo fue ampliando en sucesivas ediciones.",
            "Con ironía, erudición y mala intención, Voltaire somete a examen la Biblia, los dogmas, los milagros y la historia de la Iglesia, y defiende la razón, la tolerancia y una moral natural común a todos los pueblos. Artículos como Fanatismo, Tolerancia o Tortura siguen siendo citados hoy.",
        ],
        ideas=["La razón como juez de las creencias.",
               "La tolerancia frente al fanatismo religioso.",
               "La moral es universal y no depende de los dogmas.",
               "La forma de diccionario como arma ilustrada contra la censura."],
        faq=[("¿Qué es el Diccionario filosófico de Voltaire?", "Una colección de artículos breves ordenados alfabéticamente en los que Voltaire critica la superstición, el fanatismo y los dogmas, y defiende la razón y la tolerancia."),
             ("¿Por qué fue condenado?", "Por su crítica de la religión: fue quemado en Ginebra y en París, y Voltaire negó ser su autor."),
             ("¿Cuándo se publicó?", "En 1764, como Diccionario filosófico portátil.")]),
    "/voltaire-tratado-sobre-la-intolerancia/": book(
        titulo="Tratado sobre la tolerancia", genero="Ensayo", año="1763", tema="la tolerancia religiosa",
        resumen=[
            "En 1762, el comerciante protestante Jean Calas fue torturado y ejecutado en Toulouse, acusado sin pruebas de matar a su hijo para impedir que se convirtiera al catolicismo. Voltaire se indignó, estudió el caso y escribió este tratado para denunciar el fanatismo que había llevado a la muerte a un inocente.",
            "Repasa la historia para mostrar que la intolerancia nunca ha sido útil a ninguna religión ni a ningún Estado, y que las persecuciones han causado más males que las herejías. Termina con una oración a Dios por la fraternidad entre todos los seres humanos. Su campaña consiguió la rehabilitación de Calas en 1765.",
        ],
        ideas=["La intolerancia es contraria a la razón, a la naturaleza y al propio cristianismo.",
               "El Estado no debe perseguir a nadie por sus creencias.",
               "El caso Calas como ejemplo de los crímenes del fanatismo.",
               "Todos los seres humanos son hermanos."],
        faq=[("¿De qué trata el Tratado sobre la tolerancia?", "Es una defensa de la tolerancia religiosa escrita a raíz del caso Calas, un protestante ejecutado injustamente en Toulouse en 1762."),
             ("¿Quién fue Jean Calas?", "Un comerciante protestante acusado de matar a su hijo para que no se hiciera católico. Fue ejecutado en 1762 y rehabilitado en 1765 gracias a la campaña de Voltaire."),
             ("¿Se titula sobre la tolerancia o sobre la intolerancia?", "El título original es Tratado sobre la tolerancia; la obra denuncia la intolerancia y el fanatismo.")]),
    "/voltaire-el-siglo-de-luis-xiv/": book(
        titulo="El siglo de Luis XIV", genero="Historia", año="1751", tema="la época de Luis XIV y su cultura",
        resumen=[
            "Voltaire dedica casi veinte años a reconstruir la época de Luis XIV, que considera uno de los grandes siglos de la humanidad junto a la Grecia de Pericles, la Roma de Augusto y la Florencia de los Médicis. Narra las guerras, la política y la vida de la corte de Versalles.",
            "Su originalidad está en que no se limita a las batallas y los reyes: dedica capítulos al comercio, la administración, las ciencias, las artes, la literatura y las disputas religiosas. Por eso se le considera uno de los primeros ejemplos de historia de la civilización.",
        ],
        ideas=["La historia debe contar el progreso del espíritu humano, no solo las guerras.",
               "El siglo de Luis XIV como cumbre de la civilización francesa.",
               "Crítica de las persecuciones religiosas, como la de los hugonotes."],
        faq=[("¿Qué es El siglo de Luis XIV?", "Una obra histórica de Voltaire sobre el reinado de Luis XIV que presta tanta atención a las artes, las ciencias y la cultura como a la política y la guerra."),
             ("¿Por qué es importante en la historiografía?", "Porque es uno de los primeros libros que entienden la historia como historia de la civilización y no solo de reyes y batallas.")]),
    "/voltaire-historia-del-imperio-ruso-bajo-pedro-el-grande/": book(
        titulo="Historia del imperio ruso bajo Pedro el Grande", genero="Historia", año="1759-1763", tema="la modernización de Rusia",
        resumen=[
            "Encargada por la corte de la emperatriz Isabel de Rusia, esta obra narra el reinado de Pedro el Grande, el zar que quiso transformar un país atrasado en una potencia europea. Voltaire describe el territorio y los pueblos del imperio antes de contar la vida de Pedro.",
            "Cuenta sus viajes de aprendizaje por Europa, la fundación de San Petersburgo, la creación de una flota y un ejército modernos, y la guerra contra Carlos XII de Suecia, vencido en Poltava. Voltaire presenta a Pedro como un legislador ilustrado.",
        ],
        ideas=["El soberano ilustrado como motor del progreso.",
               "La modernización de Rusia según el modelo europeo.",
               "La historia escrita a partir de documentos de archivo."],
        faq=[("¿De qué trata la Historia del imperio ruso bajo Pedro el Grande?", "Del reinado de Pedro I, que modernizó Rusia, fundó San Petersburgo y venció a Suecia en la batalla de Poltava."),
             ("¿Quién encargó la obra a Voltaire?", "La corte de la emperatriz Isabel I de Rusia, hija de Pedro el Grande, que le proporcionó documentos de los archivos rusos.")]),
    "/voltaire-la-henriada/": book(
        titulo="La Henriada", genero="Poema épico", año="1728", tema="las guerras de religión y la tolerancia",
        resumen=[
            "La Henriada es un poema épico en diez cantos sobre Enrique de Navarra, el futuro Enrique IV de Francia, durante las guerras de religión del siglo XVI. Enrique narra a la reina Isabel de Inglaterra la matanza de San Bartolomé y las luchas entre católicos y protestantes.",
            "El poema culmina con el asedio de París, la conversión de Enrique al catolicismo y la paz del reino. Voltaire convierte a Enrique IV en el modelo de rey tolerante y denuncia el fanatismo de la Liga católica. Fue la obra que le dio fama en su tiempo.",
        ],
        personajes=[("Enrique IV", "Rey de Navarra y de Francia, héroe tolerante del poema."),
                    ("Isabel I de Inglaterra", "Reina a la que Enrique cuenta la historia de las guerras."),
                    ("Mayenne", "Jefe de la Liga católica, enemigo de Enrique.")],
        ideas=["El fanatismo religioso como origen de las guerras civiles.",
               "Enrique IV como modelo de rey tolerante.",
               "La epopeya puesta al servicio de las ideas ilustradas."],
        faq=[("¿De qué trata La Henriada?", "Es un poema épico sobre Enrique IV de Francia y las guerras de religión entre católicos y protestantes, con la matanza de San Bartolomé y el asedio de París."),
             ("¿Cuándo se publicó La Henriada?", "Una primera versión apareció en 1723 con el título La Liga; la edición definitiva se publicó en Londres en 1728.")]),
}
