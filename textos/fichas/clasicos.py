"""Textos editoriales de los clásicos escritos en español: ficha, resumen, personajes y preguntas.

python textos/fichas/clasicos.py  →  los añade a textos/<slug>.json (no toca capítulos ni texto).
Solo procesa las obras cuyo texto ya se descargó con wikisource.py.
"""
import json
from pathlib import Path

TEXTS = Path(__file__).resolve().parents[1]

BOOKS = {
    "marianela-benito-perez-galdos": {
        "color": "ocre", "genero": "Novela", "tema": "la belleza, la ceguera y la mirada de los demás",
        "edition": "Madrid, Imprenta de J. Noguera, 1878",
        "resumen": [
            "En las minas de Socartes vive la Nela, una huérfana pequeña, frágil y considerada fea por todos, que trabaja como lazarillo de Pablo Penáguilas, el hijo ciego de un rico propietario. Pablo, inteligente y sensible, conoce el mundo a través de las palabras de Marianela y se enamora de ella: como no puede verla, la imagina tan hermosa como su alma.",
            "La llegada del oculista Teodoro Golfín cambia todo: la operación puede devolver la vista a Pablo. Marianela, que desea su curación, teme a la vez el momento en que él la vea. Cuando Pablo recobra la vista descubre la belleza de su prima Florentina, y la Nela, convencida de que ya no tiene lugar en su vida, se consume hasta morir. Galdós enfrenta así la ciencia y el sentimiento, la apariencia y la verdad interior.",
        ],
        "personajes": [("Marianela (la Nela)", "Huérfana de dieciséis años, menuda y sin belleza, lazarillo de Pablo y narradora de la naturaleza para él."),
                       ("Pablo Penáguilas", "Joven ciego de nacimiento, culto e idealista, enamorado de la Nela."),
                       ("Teodoro Golfín", "Médico oculista que se hizo a sí mismo; representa la ciencia y la razón."),
                       ("Florentina", "Prima de Pablo, bella y bondadosa, que quiere proteger a Marianela."),
                       ("Francisco Penáguilas", "Padre de Pablo, rico propietario de Aldeacorba."),
                       ("Celipín Centeno", "Niño de las minas que sueña con marcharse a estudiar y ser alguien.")],
        "ideas": ["La belleza física y la belleza interior: Pablo ama a la Nela mientras no la ve.",
                  "La ciencia positivista cura el cuerpo, pero no puede salvar el sentimiento.",
                  "La pobreza y el abandono de los niños en la España industrial del siglo XIX.",
                  "Ver no siempre es conocer: la vista también engaña."],
        "faq": [("¿De qué trata Marianela de Galdós?", "De la Nela, una huérfana fea y pobre que guía a Pablo, un joven ciego que la ama sin haberla visto. Cuando una operación le devuelve la vista, Pablo se enamora de su prima Florentina y Marianela muere de pena."),
                ("¿Cómo muere Marianela?", "Muere de tristeza y debilidad después de que Pablo, ya curado, la ve por primera vez. El médico Golfín no encuentra causa física: la Nela se deja morir al sentirse rechazada."),
                ("¿Qué representa Teodoro Golfín?", "La ciencia y el progreso positivista. Su operación tiene éxito, pero la novela muestra sus límites ante el dolor humano."),
                ("¿Cuándo se publicó Marianela?", "En 1878. Es una de las novelas de tesis de la primera etapa de Benito Pérez Galdós.")],
    },
    "dona-perfecta-benito-perez-galdos": {
        "color": "negro", "genero": "Novela", "tema": "la intolerancia y el choque entre tradición y progreso",
        "resumen": [
            "Pepe Rey, un joven ingeniero madrileño de ideas modernas, llega a la ciudad episcopal de Orbajosa para casarse con su prima Rosario, hija de su tía doña Perfecta. El matrimonio, arreglado por las familias, parece sencillo, y los dos jóvenes se enamoran enseguida. Pero el pueblo recibe con desconfianza al forastero y a sus opiniones sobre la ciencia y la religión.",
            "Doña Perfecta, aconsejada por el canónigo don Inocencio, se va volviendo contra su sobrino con pleitos, desaires e intrigas, mientras Orbajosa se cierra en torno a sus tradiciones. Cuando Pepe intenta llevarse a Rosario, la tía ordena a Caballuco que lo mate. Rosario enloquece. La novela retrata la intransigencia que enfrentaba a las dos Españas del siglo XIX.",
        ],
        "personajes": [("Doña Perfecta", "Viuda rica y devota, respetada en Orbajosa, que se opone con dureza a su sobrino."),
                       ("Pepe Rey", "Ingeniero de treinta y cuatro años, racional y liberal, sobrino de doña Perfecta."),
                       ("Rosario", "Hija de doña Perfecta, dulce y sumisa, enamorada de Pepe."),
                       ("Don Inocencio", "Canónigo de la catedral, consejero de doña Perfecta, que maneja la intriga."),
                       ("María Remedios", "Sobrina de don Inocencio, que quiere casar a su hijo con Rosario."),
                       ("Caballuco", "Cristóbal Ramos, jefe de los hombres del pueblo, brazo ejecutor de doña Perfecta.")],
        "ideas": ["El fanatismo religioso y la intolerancia frente a las ideas nuevas.",
                  "Orbajosa como símbolo de la España rural cerrada al progreso.",
                  "La hipocresía de quienes aparentan virtud y actúan con crueldad.",
                  "La imposibilidad del diálogo entre dos maneras de entender el país."],
        "faq": [("¿De qué trata Doña Perfecta?", "Del enfrentamiento entre Pepe Rey, un ingeniero liberal, y su tía doña Perfecta, que representa la tradición intransigente de Orbajosa. La lucha por casarse con Rosario termina con la muerte de Pepe."),
                ("¿Quién mata a Pepe Rey?", "Caballuco, por orden de doña Perfecta, cuando Pepe entra en la huerta de la casa para llevarse a Rosario."),
                ("¿Qué simboliza Orbajosa?", "Una ciudad imaginaria que resume la España provinciana, clerical y hostil a la modernidad del siglo XIX."),
                ("¿Cuándo se publicó Doña Perfecta?", "En 1876. Es la primera de las novelas de tesis de Galdós, junto con Gloria y La familia de León Roch.")],
    },
    "misericordia-benito-perez-galdos": {
        "color": "burdeos", "genero": "Novela", "tema": "la caridad y la pobreza en el Madrid de fin de siglo",
        "resumen": [
            "Benina es la criada de doña Francisca Juárez, una señora arruinada que no sabe vivir sin las apariencias de su antigua posición. Para que a su ama no le falte nada, Benina pide limosna a escondidas a la puerta de la iglesia de San Sebastián y le hace creer que trabaja para un sacerdote, don Romualdo. Entre los mendigos conoce a Almudena, un ciego de origen marroquí que la quiere con devoción.",
            "Galdós recorre el Madrid de los pobres con ternura y humor. Cuando a doña Paca le llega por sorpresa una herencia, la familia se avergüenza de Benina y la despide. Ella, sin rencor, se queda con Almudena y sigue ayudando a quien lo necesita. Su bondad sin cálculo hace de ella una de las grandes figuras de la novela española.",
        ],
        "personajes": [("Benina", "Criada anciana, generosa y fantasiosa, que mendiga para sostener a su señora."),
                       ("Doña Francisca (doña Paca)", "Señora venida a menos, derrochadora y orgullosa."),
                       ("Almudena", "Mendigo ciego de origen marroquí, enamorado de Benina."),
                       ("Obdulia", "Hija soñadora de doña Paca, casada con un hombre que la abandonó."),
                       ("Antoñito", "Hijo de doña Paca, gandul y tramposo."),
                       ("Juliana", "Nuera de doña Paca, mujer dominante que acaba expulsando a Benina.")],
        "ideas": ["La caridad verdadera es la que se da sin esperar nada a cambio.",
                  "La pobreza vergonzante: quienes prefieren el hambre a perder las apariencias.",
                  "La imaginación como forma de sobrevivir: las mentiras piadosas de Benina.",
                  "La ingratitud de los que suben de posición."],
        "faq": [("¿De qué trata Misericordia de Galdós?", "De Benina, una criada que pide limosna a escondidas para mantener a su señora arruinada, doña Paca. Cuando la familia hereda, la despiden, pero ella responde con perdón."),
                ("¿Quién es don Romualdo en Misericordia?", "El sacerdote que Benina inventa para justificar el dinero que trae a casa. En la novela aparece después un clérigo real con ese nombre, lo que da a la obra un toque de misterio."),
                ("¿Por qué se considera a Benina una santa laica?", "Porque practica la caridad sin interés, perdona a quienes la tratan mal y se entrega a los más pobres. Galdós la presenta como ejemplo de bondad humana."),
                ("¿Cuándo se publicó Misericordia?", "En 1897, dentro de la etapa espiritualista de Galdós.")],
    },
    "trafalgar-benito-perez-galdos": {
        "color": "azul", "genero": "Novela histórica", "tema": "la batalla de Trafalgar contada por un testigo",
        "resumen": [
            "Gabriel Araceli, ya anciano, recuerda cómo de niño, huérfano y pícaro en Cádiz, entró a servir en casa de don Alonso Gutiérrez de Cisniega, un viejo marino retirado. En 1805, contra la voluntad de su esposa doña Francisca, don Alonso decide embarcarse con la escuadra hispano-francesa acompañado de Marcial, un marinero mutilado al que llaman Medio-hombre, y del propio Gabriel.",
            "A bordo del Santísima Trinidad, Gabriel vive la batalla de Trafalgar: el combate contra la flota de Nelson, la muerte de oficiales como Churruca, el hundimiento de los barcos y la tormenta que siguió. La experiencia le enseña el valor del sacrificio y lo absurdo de la guerra. Trafalgar abre los Episodios nacionales, la gran historia novelada de la España del siglo XIX.",
        ],
        "personajes": [("Gabriel Araceli", "Narrador y protagonista; un muchacho de catorce años que crece a través de la guerra."),
                       ("Don Alonso Gutiérrez de Cisniega", "Viejo marino que quiere participar en una última batalla."),
                       ("Marcial (Medio-hombre)", "Marinero veterano, mutilado en combates anteriores, entrañable y valiente."),
                       ("Doña Francisca", "Esposa de don Alonso, que se opone a que vuelva a la mar."),
                       ("Rosita", "Hija de don Alonso, de la que Gabriel está enamorado en secreto."),
                       ("Rafael Malespina", "Joven oficial, prometido de Rosita.")],
        "ideas": ["La historia vista por un hombre corriente y no por los generales.",
                  "El patriotismo y el heroísmo frente al horror de la guerra.",
                  "El paso de la niñez a la madurez del narrador.",
                  "La decadencia de la marina española a principios del siglo XIX."],
        "faq": [("¿De qué trata Trafalgar de Galdós?", "Gabriel Araceli, un muchacho de Cádiz, acompaña a su amo don Alonso a la batalla de Trafalgar de 1805 y cuenta lo que vivió a bordo del Santísima Trinidad."),
                ("¿Qué son los Episodios nacionales?", "Una serie de 46 novelas históricas de Galdós sobre la España del siglo XIX, desde Trafalgar hasta la Restauración. Trafalgar es la primera."),
                ("¿Quién narra Trafalgar?", "Gabriel Araceli, que en su vejez recuerda los hechos que vivió con catorce años. Protagoniza toda la primera serie de los Episodios."),
                ("¿Cuándo se publicó Trafalgar?", "En 1873.")],
    },
    "niebla-miguel-de-unamuno": {
        "color": "verde", "genero": "Nivola", "tema": "la existencia, el amor y la libertad del personaje",
        "edition": "Madrid, Renacimiento, 1914",
        "resumen": [
            "Augusto Pérez es un joven rico y desocupado que vive sin rumbo, como entre niebla, hasta que se enamora a primera vista de Eugenia Domingo del Arco, una profesora de piano. Ella tiene novio, Mauricio, y desprecia los regalos de Augusto, que incluso paga la hipoteca de su casa. Mientras tanto, Augusto conversa con su perro Orfeo y con su amigo Víctor Goti y se deja atraer por la planchadora Rosario.",
            "Eugenia acepta por fin casarse con él, pero huye con Mauricio poco antes de la boda. Desesperado, Augusto decide suicidarse y viaja a Salamanca para consultarlo con Miguel de Unamuno, el autor de la novela. Este le revela que no es más que un personaje de ficción y que ha decidido que muera. Augusto se rebela contra su creador. Unamuno llamó a este libro nivola para separarlo de la novela realista.",
        ],
        "personajes": [("Augusto Pérez", "Joven acomodado, soñador e indeciso, que busca dar sentido a su existencia."),
                       ("Eugenia Domingo del Arco", "Profesora de piano, independiente y calculadora."),
                       ("Mauricio", "Novio de Eugenia, holgazán y aprovechado."),
                       ("Víctor Goti", "Amigo de Augusto, que escribe a su vez una nivola."),
                       ("Rosario", "Joven planchadora por la que Augusto siente afecto."),
                       ("Orfeo", "Perro de Augusto, confidente de sus monólogos."),
                       ("Miguel de Unamuno", "El propio autor, que aparece como personaje.")],
        "ideas": ["La duda existencial: ¿qué distingue a una persona de un personaje?",
                  "La relación entre el creador y su criatura, imagen de la de Dios y el hombre.",
                  "El amor como despertar a la vida consciente.",
                  "La nivola: una novela libre de las reglas del realismo."],
        "faq": [("¿Qué es una nivola?", "El nombre que inventó Unamuno para Niebla y otras obras suyas: una novela sin descripciones realistas, hecha sobre todo de diálogo y reflexión, que rompe las normas del género."),
                ("¿Cómo termina Niebla?", "Augusto visita a Unamuno para hablar de su suicidio; el autor le dice que es un ente de ficción y que morirá. Augusto vuelve a casa y muere tras darse un atracón. Su perro Orfeo pronuncia una oración fúnebre."),
                ("¿Por qué aparece Unamuno en Niebla?", "Para plantear la relación entre autor y personaje, y con ella la pregunta de si los seres humanos somos libres o sueño de alguien."),
                ("¿Cuándo se publicó Niebla?", "En 1914.")],
    },
    "el-buscon-francisco-de-quevedo": {
        "color": "burdeos", "genero": "Novela picaresca", "tema": "las andanzas de un pícaro que quiere ser caballero",
        "resumen": [
            "Pablos, hijo de un barbero ladrón y de una madre acusada de bruja, cuenta su vida desde Segovia. Quiere ser caballero y entra al servicio de don Diego Coronel, un niño rico. Juntos pasan hambre en el pupilaje del dómine Cabra y luego estudian en Alcalá, donde Pablos sufre novatadas crueles y aprende a engañar para sobrevivir.",
            "Tras recibir la herencia de sus padres, que le entrega su tío, el verdugo Alonso Ramplón, Pablos marcha a Madrid. Allí se une a una cofradía de falsos hidalgos y finge ser noble para casarse con una dama rica, pero es descubierto y apaleado. Termina como mendigo, actor y delincuente en Sevilla, y decide pasar a las Indias, donde le fue peor. Quevedo convierte la picaresca en un juego de ingenio verbal y sátira feroz.",
        ],
        "personajes": [("Pablos", "Narrador y protagonista, pícaro de origen humilde que intenta ascender socialmente."),
                       ("Don Diego Coronel", "Hijo de un caballero segoviano, primer amo y compañero de Pablos."),
                       ("El dómine Cabra", "Clérigo avaro que mata de hambre a sus pupilos."),
                       ("Alonso Ramplón", "Tío de Pablos, verdugo de Segovia."),
                       ("Don Toribio", "Falso hidalgo que introduce a Pablos en la cofradía de estafadores de Madrid.")],
        "ideas": ["La imposibilidad de cambiar de clase social en la España del Siglo de Oro.",
                  "La sátira de la hidalguía vacía y la obsesión por la honra.",
                  "El hambre como motor de la picaresca.",
                  "El virtuosismo del lenguaje: chistes, juegos de palabras y caricaturas."],
        "faq": [("¿De qué trata El Buscón de Quevedo?", "De la vida de Pablos, un pícaro segoviano que intenta hacerse pasar por caballero y fracasa una y otra vez, hasta acabar emigrando a América."),
                ("¿Quién es el dómine Cabra?", "El clérigo que regenta el pupilaje donde Pablos y don Diego casi mueren de hambre. Su retrato es una de las caricaturas más famosas de la literatura española."),
                ("¿Cuál es el título completo de El Buscón?", "Historia de la vida del Buscón, llamado don Pablos, ejemplo de vagabundos y espejo de tacaños."),
                ("¿Cuándo se publicó El Buscón?", "En 1626, en Zaragoza, aunque Quevedo lo había escrito años antes y circulaba manuscrito.")],
    },
    "maria-jorge-isaacs": {
        "color": "verde", "genero": "Novela", "tema": "el primer amor y la pérdida",
        "resumen": [
            "Efraín vuelve a la hacienda familiar del valle del Cauca, en Colombia, después de estudiar seis años en Bogotá. Allí reencuentra a su prima María, huérfana criada por sus padres, y entre los dos nace un amor delicado, hecho de miradas, flores y paseos por los campos. La felicidad se ve amenazada cuando María sufre un ataque de la misma enfermedad que mató a su madre.",
            "El padre de Efraín decide enviarlo a estudiar medicina a Londres y le pide que espere para casarse. Las cartas cruzan el océano mientras la salud de María empeora. Cuando por fin lo llaman para que regrese, Efraín llega tarde: María ha muerto. La novela, contada como un recuerdo, es la obra cumbre del romanticismo hispanoamericano.",
        ],
        "personajes": [("Efraín", "Narrador y protagonista, joven sensible que recuerda su amor de juventud."),
                       ("María", "Prima de Efraín, de origen judío, dulce y frágil, enferma de epilepsia."),
                       ("El padre de Efraín", "Hacendado que antepone el porvenir de su hijo a su felicidad inmediata."),
                       ("Emma", "Hermana de Efraín y confidente de María."),
                       ("Carlos", "Amigo de Efraín que pide la mano de María."),
                       ("Tránsito y Braulio", "Pareja campesina cuyo amor sencillo contrasta con el de los protagonistas.")],
        "ideas": ["El amor idealizado y la fatalidad propios del romanticismo.",
                  "La naturaleza del valle del Cauca como reflejo de los sentimientos.",
                  "La memoria y la nostalgia: la historia se cuenta desde la pérdida.",
                  "El presagio: el ave negra anuncia la desgracia."],
        "faq": [("¿De qué trata María de Jorge Isaacs?", "Del amor entre Efraín y su prima María en una hacienda del valle del Cauca. Él viaja a Londres a estudiar medicina y, cuando regresa, ella ya ha muerto de su enfermedad."),
                ("¿De qué muere María?", "De una enfermedad nerviosa, descrita como epilepsia, que había heredado de su madre."),
                ("¿Qué significa el ave negra en María?", "Es un presagio de la desgracia que aparece en los momentos clave de la novela."),
                ("¿Cuándo se publicó María?", "En 1867, en Bogotá.")],
    },
    "ariel-jose-enrique-rodo": {
        "color": "azul", "genero": "Ensayo", "unidad": "partes", "tema": "la juventud, el ideal y la identidad de América Latina",
        "resumen": [
            "Al terminar el curso, un viejo maestro al que sus alumnos llaman Próspero se despide de ellos junto a una estatua de Ariel, el espíritu del aire de La tempestad de Shakespeare. Su discurso es una lección sobre cómo deben vivir los jóvenes: cultivar la vida interior, la belleza y el sentimiento moral, y no reducir la existencia a lo útil.",
            "Próspero opone Ariel, la parte noble y espiritual del ser humano, a Calibán, la sensualidad y el utilitarismo. Critica la admiración ciega por los Estados Unidos, la nordomanía, cuya prosperidad material reconoce pero cuya cultura considera vacía de ideales. Propone a la juventud latinoamericana una democracia que eleve a los mejores sin perder su herencia grecolatina y cristiana. Ariel fue durante décadas un libro de referencia para la juventud del continente.",
        ],
        "personajes": [("Próspero", "Maestro venerado que pronuncia el discurso a sus alumnos."),
                       ("Los jóvenes discípulos", "Destinatarios de la lección, en quienes Próspero deposita su esperanza."),
                       ("Ariel", "Símbolo del espíritu, la razón y el ideal."),
                       ("Calibán", "Símbolo de la sensualidad, el egoísmo y el materialismo.")],
        "ideas": ["La juventud tiene el deber de mantener vivo el ideal.",
                  "La vida plena exige cultivar todas las facultades y no solo la utilidad.",
                  "Crítica del utilitarismo y de la imitación de los Estados Unidos.",
                  "Una democracia de la cultura y del mérito frente a la mediocridad."],
        "faq": [("¿De qué trata Ariel de Rodó?", "Es un ensayo en forma de discurso: el maestro Próspero aconseja a sus alumnos que defiendan los valores del espíritu frente al materialismo y que no imiten ciegamente a los Estados Unidos."),
                ("¿Qué representan Ariel y Calibán?", "Ariel, el espíritu, la belleza y la razón; Calibán, el instinto, la sensualidad y el utilitarismo. Rodó toma ambas figuras de La tempestad de Shakespeare."),
                ("¿Qué es el arielismo?", "El movimiento de ideas inspirado en este ensayo, que defendía una identidad latinoamericana basada en la cultura y el idealismo."),
                ("¿Cuándo se publicó Ariel?", "En 1900, en Montevideo.")],
    },
    "pepita-jimenez-juan-valera": {
        "color": "ocre", "genero": "Novela", "tema": "la vocación religiosa y el amor",
        "resumen": [
            "Luis de Vargas, un joven seminarista a punto de ordenarse sacerdote, pasa unas semanas en su pueblo andaluz con su padre, don Pedro. En cartas a su tío, el deán, cuenta la vida del lugar y habla cada vez más de Pepita Jiménez, una viuda joven, rica y discreta a la que su propio padre pretende.",
            "Las cartas muestran, a veces sin que él lo advierta, cómo Luis se enamora de Pepita y lucha entre su vocación mística y el amor. Con la ayuda de la criada Antoñona, los dos jóvenes se encuentran; Luis se bate en duelo con el conde de Genazahar, que había ofendido a Pepita, y acaba renunciando al sacerdocio para casarse con ella, con la bendición de don Pedro. Valera escribe con ironía y elegancia una de las mejores novelas psicológicas del siglo XIX.",
        ],
        "personajes": [("Luis de Vargas", "Seminarista de veintidós años, idealista, que descubre el amor."),
                       ("Pepita Jiménez", "Viuda de veinte años, hermosa, inteligente y respetada en el pueblo."),
                       ("Don Pedro de Vargas", "Padre de Luis, cacique del lugar y pretendiente de Pepita."),
                       ("El deán", "Tío de Luis, destinatario de sus cartas y narrador de la segunda parte."),
                       ("Antoñona", "Antigua nodriza y criada de Pepita, astuta y decidida."),
                       ("El conde de Genazahar", "Pretendiente despechado de Pepita.")],
        "ideas": ["El conflicto entre el amor divino y el amor humano.",
                  "El autoengaño: Luis se cuenta a sí mismo una vocación que no siente.",
                  "La novela epistolar como retrato psicológico.",
                  "La ironía y el humor de Valera frente al dramatismo romántico."],
        "faq": [("¿De qué trata Pepita Jiménez?", "De Luis de Vargas, un seminarista que, de visita en su pueblo, se enamora de la joven viuda Pepita Jiménez, pretendida por su padre. Al final deja el sacerdocio y se casa con ella."),
                ("¿Cómo está estructurada Pepita Jiménez?", "En tres partes: las cartas de Luis a su tío el deán, un relato llamado Paralipómenos y un epílogo con cartas de don Pedro."),
                ("¿Termina bien Pepita Jiménez?", "Sí. Luis y Pepita se casan y viven felices, y don Pedro acepta el matrimonio."),
                ("¿Cuándo se publicó Pepita Jiménez?", "En 1874.")],
    },
    "la-regenta-leopoldo-alas-clarin": {
        "color": "negro", "genero": "Novela", "tema": "la insatisfacción, el deseo y la hipocresía de una ciudad",
        "resumen": [
            "En Vetusta, una ciudad provinciana inspirada en Oviedo, vive Ana Ozores, conocida como la Regenta por estar casada con don Víctor Quintanar, antiguo regente de la Audiencia, mucho mayor que ella. Ana es sensible, soñadora y se siente sola en un matrimonio sin pasión. Dos hombres la rodean: el magistral don Fermín de Pas, su confesor, ambicioso y enamorado en secreto, y don Álvaro Mesía, el seductor de la ciudad.",
            "Ana oscila entre el misticismo que le propone Fermín y la tentación que representa Álvaro, mientras Vetusta entera espía y murmura. Cuando por fin cae en el adulterio, don Víctor lo descubre, se bate en duelo con Mesía y muere. Ana queda aislada y despreciada por la misma sociedad que alimentó el escándalo. La Regenta es la gran novela naturalista española y un retrato implacable de la hipocresía.",
        ],
        "personajes": [("Ana Ozores (la Regenta)", "Mujer joven, inteligente e insatisfecha, atrapada entre el deseo y la culpa."),
                       ("Don Fermín de Pas", "Magistral de la catedral y confesor de Ana; ambicioso y dominante."),
                       ("Don Álvaro Mesía", "Presidente del Casino, donjuán vanidoso que se propone conquistar a Ana."),
                       ("Don Víctor Quintanar", "Marido de Ana, bondadoso, aficionado a la caza y al teatro del Siglo de Oro."),
                       ("Doña Paula", "Madre de don Fermín, que controla su carrera con mano de hierro."),
                       ("Frígilis", "Amigo inseparable de don Víctor.")],
        "ideas": ["La asfixia de la vida provinciana y la murmuración como forma de poder.",
                  "La hipocresía religiosa y social.",
                  "El deseo femenino reprimido y la falta de salidas para la mujer.",
                  "El naturalismo: la influencia del ambiente y la herencia en los personajes."],
        "faq": [("¿De qué trata La Regenta?", "De Ana Ozores, una mujer casada con un hombre mayor en la ciudad de Vetusta, disputada por su confesor, el magistral Fermín de Pas, y por el seductor Álvaro Mesía. Su adulterio termina en tragedia."),
                ("¿Qué ciudad es Vetusta?", "Una ciudad inventada que retrata a Oviedo, donde Clarín vivió y fue catedrático."),
                ("¿Cómo termina La Regenta?", "Don Víctor muere en duelo con Mesía, que huye a Madrid. Ana queda sola y rechazada, y en la última escena, en la catedral, el magistral la aparta con violencia."),
                ("¿Cuándo se publicó La Regenta?", "En dos tomos, entre 1884 y 1885.")],
    },
    "cumanda-juan-leon-mera": {
        "color": "verde", "genero": "Novela", "tema": "el amor imposible en la selva amazónica",
        "resumen": [
            "En la selva oriental del Ecuador, Carlos, hijo del misionero dominico fray Domingo Orozco, se enamora de Cumandá, una joven de belleza extraordinaria que vive entre los pueblos indígenas del río Palora. Fray Domingo había sido un hacendado cruel; tras perder a su mujer y a sus hijos en una sublevación indígena, se hizo religioso para expiar sus culpas.",
            "El amor de los jóvenes choca con las costumbres de la tribu: el padre adoptivo de Cumandá la casa con el viejo jefe Yahuarmaqui. Cuando este muere, la tradición exige que su esposa sea sacrificada, y Cumandá se entrega para salvar la vida de Carlos. Demasiado tarde se descubre que era la hija perdida de fray Domingo y, por tanto, hermana de Carlos. Es la novela más representativa del indianismo romántico ecuatoriano.",
        ],
        "personajes": [("Cumandá", "Joven criada entre los indígenas, valiente y bondadosa."),
                       ("Carlos Orozco", "Hijo del misionero, enamorado de Cumandá."),
                       ("Fray Domingo Orozco", "Antiguo hacendado convertido en misionero tras una tragedia familiar."),
                       ("Yahuarmaqui", "Viejo y poderoso jefe indígena con quien obligan a casarse a Cumandá."),
                       ("Tongana", "Padre adoptivo de Cumandá.")],
        "ideas": ["El amor romántico frente a las barreras sociales y culturales.",
                  "La naturaleza amazónica como escenario grandioso y peligroso.",
                  "La culpa, la expiación y el perdón.",
                  "La visión del indígena en el romanticismo hispanoamericano."],
        "faq": [("¿De qué trata Cumandá?", "Del amor entre Carlos, hijo de un misionero, y Cumandá, una joven que vive entre los indígenas de la selva ecuatoriana. Ella muere sacrificada y luego se descubre que eran hermanos."),
                ("¿Quién es Cumandá en realidad?", "Julia, la hija de fray Domingo que se creía muerta en la sublevación de Guamote; por eso era hermana de Carlos."),
                ("¿Cuándo se publicó Cumandá?", "En 1879. Su subtítulo es Un drama entre salvajes.")],
    },
    "amalia-jose-marmol": {
        "color": "burdeos", "genero": "Novela", "tema": "el amor y la persecución política bajo Rosas",
        "resumen": [
            "Buenos Aires, mayo de 1840. Eduardo Belgrano, joven unitario, sobrevive herido a una emboscada de la Mazorca, la policía política del gobernador Juan Manuel de Rosas, cuando intentaba huir a Montevideo. Su amigo Daniel Bello, que finge apoyar al régimen, lo esconde en la casa de su prima Amalia, una joven viuda tucumana.",
            "Mientras Eduardo se recupera, él y Amalia se enamoran, y Daniel conspira desde dentro del círculo de Rosas, burlando a espías como doña María Josefa Ezcurra. La novela mezcla la historia de amor con el retrato del terror político en la ciudad. La noche de la boda, la Mazorca asalta la casa y la tragedia se impone. Amalia es considerada la primera novela argentina.",
        ],
        "personajes": [("Amalia", "Joven viuda, culta y valiente, que da refugio a Eduardo."),
                       ("Eduardo Belgrano", "Joven unitario perseguido por el régimen de Rosas."),
                       ("Daniel Bello", "Amigo de Eduardo, conspirador astuto que aparenta lealtad al gobierno."),
                       ("Florencia Dupasquier", "Novia de Daniel."),
                       ("Juan Manuel de Rosas", "Gobernador de Buenos Aires, retratado como tirano."),
                       ("María Josefa Ezcurra", "Cuñada de Rosas, jefa de una red de delatores.")],
        "ideas": ["El amor romántico amenazado por la violencia política.",
                  "La denuncia de la dictadura de Rosas desde el bando unitario.",
                  "El miedo y la delación como forma de gobierno.",
                  "La novela como documento histórico de su tiempo."],
        "faq": [("¿De qué trata Amalia de José Mármol?", "Del amor entre Amalia y Eduardo Belgrano, un unitario perseguido por la Mazorca, en el Buenos Aires de 1840 gobernado por Rosas."),
                ("¿Por qué Amalia es la primera novela argentina?", "Porque se publicó por entregas entre 1851 y 1855 y es la primera novela extensa escrita en Argentina con tema nacional."),
                ("¿Qué era la Mazorca?", "La Sociedad Popular Restauradora, un grupo armado que perseguía a los opositores de Rosas."),
                ("¿Cuándo transcurre Amalia?", "En Buenos Aires, en 1840, durante el segundo gobierno de Juan Manuel de Rosas.")],
    },
}

NUMBER_START = 18


def main():
    for number, (slug, data) in enumerate(BOOKS.items(), start=NUMBER_START):
        config = TEXTS / f"{slug}.json"
        if not config.exists():
            print("sin texto:", slug)
            continue
        meta = json.loads(config.read_text(encoding="utf-8"))
        title, author = meta["title"], meta["author"]
        unit = data.get("unidad", "capítulos")
        if data.get("edition"):
            meta["edition"] = data["edition"]
        meta["description"] = (f"{title} de {author}: resumen, personajes e ideas principales, y el libro completo para leer online "
                               f"gratis o descargar en PDF. {data['genero']} sobre {data['tema']}.")[:300]
        meta["intro"] = "".join(f"<p>{p}</p>" for p in data["resumen"][:1]) + (
            f"<p>Aquí puedes leer {title} completo, dividido en {unit}. Se respeta la ortografía de la edición original.</p>")
        meta.setdefault("cover", {}).update({"color": data["color"], "number": number})
        blocks = (TEXTS / f"{slug}.txt").read_text(encoding="utf-8").split("\n")
        for chapter in meta["chapters"]:
            if not chapter.get("summary"):
                first = next((b[2:] for b in blocks[chapter["start"]:chapter["end"] + 1] if b.startswith("P|")), "")
                words = first.lstrip("—-– ").split()
                chapter["summary"] = "Empieza: «" + " ".join(words[:22]) + ("…»" if len(words) > 22 else "»")
        meta["ficha"] = {"genero": data["genero"], "unidad": unit, "tema": data["tema"], "resumen": data["resumen"],
                         "personajes": data["personajes"], "ideas": data["ideas"], "faq": data["faq"]}
        config.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(number, slug)


if __name__ == "__main__":
    main()
