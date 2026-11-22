"""Fichas del marqués de Sade en el formato nuevo (fichas_antiguas.py)."""

AUTOR = "Marqués de Sade"
RUTA = "/libros-pdf-gratis/autores/marques-de-sade/"


def book(**data):
    data.setdefault("autor", AUTOR)
    data.setdefault("ruta_autor", RUTA)
    return data


BOOKS = {
    "/marques-de-sade-justine-o-los-infortunios-de-la-virtud/": book(
        titulo="Justine o los infortunios de la virtud", genero="Novela", año="1791", tema="la virtud castigada y el vicio recompensado",
        resumen=[
            "Al quedar huérfanas y sin dinero, dos hermanas eligen caminos opuestos: Juliette se entrega al vicio y prospera, mientras Justine decide conservar su virtud a cualquier precio. Años después, Justine cuenta su vida a una dama que resulta ser su hermana.",
            "Cada vez que Justine intenta hacer el bien cae en manos de un nuevo verdugo: un noble que planea envenenar a su tía, un cirujano, unos monjes en un convento apartado, una banda de falsificadores. La virtud solo le trae sufrimientos y castigos. Al final, cuando parece a salvo, muere fulminada por un rayo. Sade invierte la novela moral de su tiempo para mostrar una naturaleza indiferente al bien.",
        ],
        personajes=[("Justine", "Joven virtuosa e ingenua, víctima de todos los que encuentra."),
                    ("Juliette", "Su hermana, que elige el vicio y triunfa en la sociedad."),
                    ("Bressac", "Joven noble que intenta convertir a Justine en cómplice de un crimen."),
                    ("Los monjes de Sainte-Marie-des-Bois", "Libertinos que la retienen en su convento.")],
        ideas=["La virtud no es recompensada: la naturaleza es indiferente a la moral.",
               "Inversión de la novela sentimental del siglo XVIII.",
               "Crítica de la hipocresía de la Iglesia y de los poderosos.",
               "Los libertinos justifican sus crímenes con argumentos filosóficos."],
        faq=[("¿De qué trata Justine de Sade?", "De una joven que intenta vivir de forma virtuosa y, por ello, sufre una desgracia tras otra a manos de libertinos, mientras su hermana Juliette prospera gracias al vicio."),
             ("¿Cuántas versiones hay de Justine?", "Tres: Los infortunios de la virtud (1787), Justine o los infortunios de la virtud (1791) y La nueva Justine (1797), cada vez más extensas y extremas."),
             ("¿Cómo termina Justine?", "Muere alcanzada por un rayo justo cuando parecía haber encontrado la paz, una última ironía sobre la recompensa de la virtud.")]),
    "/marques-de-sade-juliette-o-las-prosperidades-del-vicio/": book(
        titulo="Juliette o las prosperidades del vicio", genero="Novela", año="1797-1801", tema="el triunfo del vicio",
        resumen=[
            "Juliette es la contrapartida de Justine: educada en un convento por libertinas que le enseñan a despreciar la moral, decide entregarse al placer y al crimen sin remordimientos. Su ascenso social es imparable: se une a ministros, aristócratas y criminales poderosos.",
            "La novela sigue sus viajes por Francia e Italia, donde conoce a papas, reyes y envenenadoras, entre largas disertaciones filosóficas sobre la naturaleza, la religión y el crimen. A diferencia de su hermana, Juliette termina rica y feliz. Es la obra más extensa y radical de Sade.",
        ],
        personajes=[("Juliette", "Hermana de Justine, libertina implacable que prospera con el vicio."),
                    ("Clairwil", "Amiga y cómplice de Juliette, aún más cruel que ella."),
                    ("Noirceuil", "Libertino poderoso que guía la carrera de Juliette."),
                    ("Saint-Fond", "Ministro corrupto, aliado de Juliette.")],
        ideas=["El vicio, y no la virtud, es recompensado en la sociedad.",
               "Ateísmo radical y crítica de la religión.",
               "El poder político como instrumento de los libertinos.",
               "La filosofía usada para justificar cualquier crimen."],
        faq=[("¿De qué trata Juliette de Sade?", "Es la historia de la hermana de Justine, que elige el vicio y el crimen y alcanza la riqueza y el poder sin sufrir castigo."),
             ("¿Qué relación tiene con Justine?", "Son dos caras de la misma historia: Justine muestra los infortunios de la virtud y Juliette las prosperidades del vicio. Se publicaron juntas en la versión de 1797.")]),
    "/marques-de-sade-la-filosofia-en-el-tocador/": book(
        titulo="La filosofía en el tocador", genero="Diálogos", año="1795", tema="la educación libertina y la moral revolucionaria",
        resumen=[
            "En siete diálogos, la señora de Saint-Ange y el libertino Dolmancé se proponen educar a la joven Eugenia de Mistival, de quince años, en el placer y en una filosofía sin dios ni moral tradicional. Las escenas eróticas se alternan con largas discusiones sobre la religión, la familia y la virtud.",
            "En el centro de la obra se lee un panfleto, Franceses, un esfuerzo más si queréis ser republicanos, que lleva hasta el extremo las ideas de la Revolución: abolir la religión, la propiedad de las personas y la pena de muerte. La obra termina con un castigo cruel a la madre de Eugenia, símbolo de la moral que se rechaza.",
        ],
        personajes=[("Eugenia de Mistival", "Joven alumna que es iniciada en el libertinaje."),
                    ("La señora de Saint-Ange", "Aristócrata libertina que organiza la educación de Eugenia."),
                    ("Dolmancé", "Libertino ateo, maestro y portavoz filosófico."),
                    ("La señora de Mistival", "Madre de Eugenia, que representa la moral tradicional.")],
        ideas=["La educación como iniciación al placer y a la libertad absoluta.",
               "Ateísmo y rechazo de toda moral religiosa.",
               "Franceses, un esfuerzo más: la Revolución llevada a sus últimas consecuencias.",
               "La naturaleza como única ley."],
        faq=[("¿De qué trata La filosofía en el tocador?", "De la educación libertina de una joven, Eugenia, a cargo de dos libertinos que combinan el placer con discursos filosóficos contra la religión y la moral."),
             ("¿Qué es «Franceses, un esfuerzo más si queréis ser republicanos»?", "Un panfleto incluido en la obra que propone llevar la Revolución hasta abolir la religión y las leyes morales tradicionales.")]),
    "/marques-de-sade-los-120-dias-de-sodoma/": book(
        titulo="Los 120 días de Sodoma", genero="Novela", año="1785 (publicada en 1904)", tema="el poder absoluto y el exceso",
        resumen=[
            "Al final del reinado de Luis XIV, cuatro libertinos ricos y poderosos, el duque de Blangis, su hermano el obispo, el presidente Curval y el financiero Durcet, se encierran durante cuatro meses en el castillo de Silling, en la Selva Negra, con un grupo de víctimas. Cuatro narradoras deben contar cada día pasiones cada vez más extremas.",
            "Sade escribió la obra en la Bastilla, en 1785, en un rollo de papel de doce metros que perdió al ser trasladado en 1789 y que creyó destruido. Solo terminó la primera parte; el resto quedó en forma de notas. Es su obra más extrema, una enciclopedia del exceso que Pier Paolo Pasolini llevó al cine en Saló.",
        ],
        personajes=[("El duque de Blangis", "El más poderoso de los cuatro libertinos."),
                    ("El obispo", "Hermano del duque."),
                    ("El presidente Curval", "Magistrado libertino."),
                    ("Durcet", "Financiero, el cuarto de los amos de Silling.")],
        ideas=["El poder absoluto sin ningún límite moral ni legal.",
               "Clasificación sistemática de las pasiones humanas.",
               "Crítica de las élites del Antiguo Régimen.",
               "Una obra inacabada y escrita en prisión."],
        faq=[("¿De qué trata Los 120 días de Sodoma?", "Cuatro libertinos poderosos se encierran en un castillo con sus víctimas durante cuatro meses mientras unas narradoras cuentan pasiones cada vez más extremas."),
             ("¿Dónde escribió Sade Los 120 días de Sodoma?", "En la Bastilla, en 1785, en un largo rollo de papel que se perdió en 1789 y se publicó por primera vez en 1904."),
             ("¿Qué película se basa en Los 120 días de Sodoma?", "Saló o los 120 días de Sodoma (1975), de Pier Paolo Pasolini, que traslada la historia a la Italia fascista.")]),
    "/marques-de-sade-dialogo-entre-un-sacerdote-y-un-moribundo/": book(
        titulo="Diálogo entre un sacerdote y un moribundo", genero="Diálogo filosófico", año="1782", tema="el ateísmo y la naturaleza",
        resumen=[
            "Un sacerdote acude junto al lecho de un moribundo para obtener su arrepentimiento antes de la muerte. En lugar de confesarse, el moribundo discute con él y le expone una filosofía materialista: no hay más que la naturaleza, la religión es una invención y la moral debe basarse en hacer felices a los demás y a uno mismo.",
            "Con argumentos sencillos, el moribundo desmonta las pruebas de la existencia de Dios y la amenaza del infierno. Es uno de los primeros textos de Sade, escrito en la prisión de Vincennes, y el más claro resumen de su ateísmo.",
        ],
        personajes=[("El moribundo", "Libertino ateo que argumenta contra la religión en sus últimas horas."),
                    ("El sacerdote", "Acude a confesarlo y acaba escuchando sus razones.")],
        ideas=["La naturaleza basta para explicar el mundo, sin necesidad de Dios.",
               "La religión como instrumento de miedo y de poder.",
               "Una moral basada en la felicidad y no en el castigo."],
        faq=[("¿De qué trata el Diálogo entre un sacerdote y un moribundo?", "Un moribundo rechaza confesarse y convence al sacerdote, con argumentos materialistas, de que la religión no tiene fundamento."),
             ("¿Cuándo lo escribió Sade?", "En 1782, en la prisión de Vincennes. No se publicó hasta 1926.")]),
    "/marques-de-sade-los-crimenes-del-amor/": book(
        titulo="Los crímenes del amor", genero="Novelas cortas", año="1800", tema="las pasiones que llevan a la tragedia",
        resumen=[
            "Los crímenes del amor reúne once novelas cortas que Sade llamó heroicas y trágicas, entre ellas Florville y Courval, Eugenia de Franval, Ernestina, La condesa de Sancerre y Dorgeville. Es una de las pocas obras que publicó con su nombre, y va precedida del ensayo Ideas sobre las novelas.",
            "Las historias, ambientadas en distintas épocas y países, muestran cómo las pasiones desatadas conducen a crímenes y catástrofes: incestos, venganzas, engaños y muertes. A diferencia de sus obras clandestinas, el tono es el de la novela sentimental y gótica de su tiempo.",
        ],
        ideas=["Las pasiones sin freno llevan a la desgracia.",
               "La novela trágica como espejo de la naturaleza humana.",
               "Influencia de la novela gótica inglesa."],
        faq=[("¿Qué contiene Los crímenes del amor?", "Once novelas cortas trágicas y el ensayo Ideas sobre las novelas, en el que Sade expone su teoría del género."),
             ("¿Es una obra erótica?", "No en el sentido de Justine o Juliette: Sade la publicó con su nombre y sigue el modelo de la novela sentimental y trágica de la época.")]),
    "/marques-de-sade-eugenia-de-franval/": book(
        titulo="Eugenia de Franval", genero="Novela corta", año="1800", tema="la corrupción y sus consecuencias",
        resumen=[
            "Franval, un hombre rico y sin principios, educa a su hija Eugenia lejos de la religión y de la moral, y la convierte en su amante. Juntos traman contra la esposa de Franval, que intenta salvar a su hija con la ayuda de su madre y de un sacerdote, Clervil.",
            "Las intrigas de Franval terminan en desastre: su esposa muere envenenada, Eugenia muere de remordimiento y Franval, arruinado y arrepentido, se quita la vida. Forma parte de Los crímenes del amor y es una de las novelas cortas más conocidas de Sade.",
        ],
        personajes=[("Franval", "Padre libertino que corrompe a su hija."),
                    ("Eugenia", "Hija de Franval, educada por él en el desprecio de la moral."),
                    ("La señora de Franval", "Esposa virtuosa que intenta salvar a su hija."),
                    ("Clervil", "Sacerdote que ayuda a la familia.")],
        ideas=["La educación sin principios conduce a la catástrofe.",
               "El remordimiento como castigo final.",
               "La familia destruida por las pasiones."],
        faq=[("¿De qué trata Eugenia de Franval?", "De un padre que corrompe a su hija y conspira contra su esposa, lo que acaba con la muerte de los tres."),
             ("¿En qué libro aparece?", "Es una de las once novelas cortas de Los crímenes del amor, publicado en 1800.")]),
    "/marques-de-sade-oxtiern-o-las-desdichas-del-libertinaje/": book(
        titulo="Oxtiern o las desdichas del libertinaje", genero="Teatro", año="1791", tema="el abuso de poder de un libertino",
        resumen=[
            "Oxtiern es un drama en tres actos basado en la novela corta Ernestina, que Sade incluyó después en Los crímenes del amor. Se estrenó en París en 1791 y fue una de las pocas obras de teatro de Sade que llegaron a representarse.",
            "En Suecia, el conde Oxtiern, un noble poderoso y sin escrúpulos, persigue a la joven Ernestina, abusa de ella y maquina contra su padre, el coronel Falkenheim. La obra denuncia la impunidad de los poderosos y termina con el castigo del libertino.",
        ],
        personajes=[("El conde Oxtiern", "Noble sueco libertino y cruel."),
                    ("Ernestina", "Joven víctima de Oxtiern."),
                    ("Falkenheim", "Coronel, padre de Ernestina.")],
        ideas=["La impunidad de los poderosos.",
               "El libertinaje como destrucción del otro.",
               "La justicia que finalmente alcanza al culpable."],
        faq=[("¿Qué es Oxtiern de Sade?", "Un drama en tres actos estrenado en 1791, basado en su novela corta Ernestina, sobre un noble sueco que abusa de una joven y de su familia."),
             ("¿Se representó en vida de Sade?", "Sí, en el teatro Molière de París en 1791, y de nuevo en Versalles en 1799.")]),
    "/marques-de-sade-la-marquesa-de-gange/": book(
        titulo="La marquesa de Gange", genero="Novela histórica", año="1813", tema="la virtud perseguida",
        resumen=[
            "La última novela de Sade, publicada de forma anónima, recrea un crimen real del siglo XVII: el asesinato de la marquesa de Ganges, una mujer joven, rica y virtuosa, a manos de sus cuñados en el Languedoc en 1667.",
            "Sade narra con un estilo contenido las intrigas del abate y del caballero de Ganges, que la acosan y la acusan para quedarse con su fortuna, hasta el ataque final. Lejos de sus obras clandestinas, es una novela histórica y moral que vuelve al tema de la virtud perseguida.",
        ],
        personajes=[("La marquesa de Gange", "Mujer virtuosa perseguida por la familia de su marido."),
                    ("El abate de Gange", "Cuñado que la acosa y planea su muerte."),
                    ("El caballero de Gange", "Cuñado y cómplice del abate.")],
        ideas=["La virtud perseguida por la codicia y el deseo.",
               "La novela histórica basada en un crimen real.",
               "Un Sade contenido y moralista al final de su vida."],
        faq=[("¿Es real la historia de La marquesa de Gange?", "Sí. La marquesa de Ganges fue asesinada por sus cuñados en 1667, un caso célebre en la Francia del siglo XVII."),
             ("¿Cuándo se publicó?", "En 1813, de forma anónima, un año antes de la muerte de Sade en el asilo de Charenton.")]),
    "/marques-de-sade-historia-de-aline-y-valcour/": book(
        titulo="Aline y Valcour", genero="Novela epistolar", año="1795", tema="el amor, la sociedad y las utopías",
        resumen=[
            "Aline y Valcour se aman, pero el padre de Aline, el presidente de Blamont, un magistrado libertino, quiere casarla con su amigo Dolbourg, tan corrupto como él. La madre de Aline intenta protegerla. Las cartas de los personajes cuentan la lucha contra ese matrimonio, que acaba en tragedia.",
            "Dentro de la novela se incluyen largos relatos de viaje, como los de Sainville y Leonor, que describen el cruel reino africano de Butua y la isla utópica de Tamoé, gobernada con justicia por el sabio Zamé. Es la gran novela filosófica de Sade y la que firmó con su nombre.",
        ],
        personajes=[("Aline", "Joven virtuosa enamorada de Valcour."),
                    ("Valcour", "Joven pobre y honrado, amado por Aline."),
                    ("El presidente de Blamont", "Padre de Aline, magistrado libertino."),
                    ("Zamé", "Sabio legislador de la isla utópica de Tamoé.")],
        ideas=["La novela epistolar como vehículo de ideas filosóficas.",
               "El contraste entre una sociedad despótica y una utopía.",
               "La crítica de la justicia y de la familia patriarcal."],
        faq=[("¿De qué trata Aline y Valcour?", "Del amor entre Aline y Valcour, impedido por el padre de ella, y de los viajes de otros personajes a un reino despótico y a una isla utópica."),
             ("¿Cuándo se publicó?", "En 1795, aunque Sade la escribió en la Bastilla en los años ochenta.")]),
    "/marques-de-sade-ideas-sobre-las-novelas/": book(
        titulo="Ideas sobre las novelas", genero="Ensayo", año="1800", tema="la historia y el arte de la novela",
        resumen=[
            "Ideas sobre las novelas es el ensayo con el que Sade abrió Los crímenes del amor. En él recorre la historia del género, desde la Antigüedad y la Edad Media hasta su tiempo, y comenta a autores como Cervantes, Madame de La Fayette, Richardson, Fielding, Prévost y Rousseau.",
            "Sade defiende que el novelista debe conocer el corazón humano en todos sus pliegues y mostrar el vicio sin disimulos para que el lector lo comprenda. También explica el éxito de la novela gótica como fruto de las conmociones de la Revolución.",
        ],
        ideas=["El novelista debe conocer a fondo el corazón humano.",
               "La novela como retrato verdadero de las costumbres.",
               "La novela gótica como respuesta a los horrores de la Revolución."],
        faq=[("¿Qué es Ideas sobre las novelas?", "Un ensayo de Sade sobre la historia y el arte de la novela, publicado como prólogo de Los crímenes del amor en 1800."),
             ("¿Qué opina Sade de la novela gótica?", "Que surgió como respuesta inevitable a las convulsiones de la Revolución, que habían hecho insuficientes las ficciones ordinarias.")]),
    "/marques-de-sade-cuentos-historietas-y-fabulas/": book(
        titulo="Cuentos, historietas y fábulas", genero="Relatos", año="Publicados en 1926", tema="la sátira de las costumbres",
        resumen=[
            "Este volumen reúne relatos breves que Sade escribió durante su encierro en la Bastilla en los años ochenta del siglo XVIII y que no se publicaron hasta 1926. Son cuentos cómicos y picantes al modo de los antiguos fabliaux franceses.",
            "En ellos aparecen maridos engañados, clérigos hipócritas, magistrados ridículos y damas astutas. Muestran a un Sade ingenioso y burlón, más cercano a Boccaccio y a La Fontaine que a sus novelas clandestinas.",
        ],
        ideas=["La sátira de la Iglesia, la justicia y el matrimonio.",
               "El humor y el ingenio de la tradición de los fabliaux.",
               "Una cara poco conocida de Sade."],
        faq=[("¿Qué son los Cuentos, historietas y fábulas de Sade?", "Relatos breves y cómicos escritos en la Bastilla que satirizan a clérigos, jueces y maridos engañados."),
             ("¿Cuándo se publicaron?", "Por primera vez en 1926, a partir de los manuscritos de Sade.")]),
}
