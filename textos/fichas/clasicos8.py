"""Octava tanda: clásicos con ficha antigua y sin lectura online (mismo formato que clasicos.py).

1. python wikisource.py "Conde Lucanor" el-conde-lucanor-don-juan-manuel --titulo "El conde Lucanor" --autor "Don Juan Manuel" \
       --ficha /el-conde-lucanor-pdf-don-juan-manuel/ --capitulos
   python wikisource.py "Libro de Buen Amor" libro-de-buen-amor-arcipreste-de-hita --titulo "Libro de buen amor" \
       --autor "Arcipreste de Hita" --ficha /el-libro-de-buen-amor-pdf-arcipreste-de-hita/ --capitulos
   python wikisource.py "Colección de poesías castellanas anteriores al siglo XV/Tomo I/Poema del Cid" cantar-de-mio-cid \
       --titulo "Cantar de mio Cid" --autor "Anónimo" --ficha /cantar-de-mio-cid-pdf/ --edicion "…"
   python teatro.py "El mercader de Venecia (Menéndez y Pelayo tr.)" el-mercader-de-venecia-shakespeare        --titulo "El mercader de Venecia" --autor "William Shakespeare" --ficha /el-mercader-de-venecia-pdf-shakespeare/        --traductor "Marcelino Menéndez y Pelayo" --edicion "Dramas de Guillermo Shakespeare, Barcelona, 1881"
   python wikisource.py "Orgullo y prejuicio" orgullo-y-prejuicio-jane-austen --titulo "Orgullo y prejuicio" --autor "Jane Austen"        --ruta-autor /libros-pdf-gratis/autores/jane-austen/ --ficha /orgullo-y-prejuicio-pdf-jane-austen/ --edicion "Madrid, Calpe, 1924" --capitulos
   En Git Bash, anteponer MSYS_NO_PATHCONV=1 para que no convierta las rutas /… en rutas de Windows.
   Después: autor del Mercader en author_route, Nerisa/Porcia/Eldux → Nerissa/Pórcia/Dux en speakers; sin el glosario
   vacío del Buen amor ni la numeración «001.» en sus títulos.
2. python textos/fichas/clasicos8.py  →  ficha, descripción, portada y resúmenes de capítulo en textos/<slug>.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clasicos  # noqa: E402

NUMBER_START = 61

BOOKS = {
    "el-conde-lucanor-don-juan-manuel": {
        "color": "burdeos", "genero": "Cuentos", "unidad": "ejemplos", "tema": "la prudencia, el engaño y el buen gobierno",
        "resumen": [
            "El conde Lucanor es una colección de cuentos que don Juan Manuel, sobrino del rey Alfonso X el Sabio, terminó en 1335. Todos siguen el mismo esquema: el conde Lucanor plantea un problema a su consejero Patronio, y este le responde con una historia, un «ejemplo», de la que el conde saca la lección. Cada ejemplo termina con unos versos que resumen la moraleja.",
            "Las historias vienen de fuentes muy distintas: fábulas de animales, cuentos árabes y orientales, anécdotas de reyes y de la historia de Castilla. Entre las más conocidas están la del mancebo que se casó con una mujer muy brava, la del deán de Santiago y el mago don Illán, la de doña Truhana y la del rey que se vistió con una tela que solo veían los hijos legítimos. Es una de las primeras obras de prosa narrativa en castellano.",
        ],
        "personajes": [("El conde Lucanor", "Noble que pide consejo a Patronio sobre los problemas de su casa y su gobierno."),
                       ("Patronio", "Consejero sabio y prudente, que responde siempre con un cuento."),
                       ("Don Illán", "Mago de Toledo que pone a prueba la gratitud del deán de Santiago."),
                       ("Doña Truhana", "Mujer pobre que sueña con hacerse rica mientras lleva una olla de miel al mercado."),
                       ("El mancebo casado", "Joven que doma desde la primera noche a su mujer, famosa por su mal carácter.")],
        "ideas": ["Enseñar deleitando: la lección moral se transmite a través de un cuento.",
                  "La prudencia y la desconfianza ante los aduladores y los engañadores.",
                  "El buen gobierno de la casa y del estado, según la mentalidad de la nobleza medieval.",
                  "La salvación del alma y la honra en este mundo como fines del hombre."],
        "faq": [("¿Cuántos cuentos tiene El conde Lucanor?", "La primera parte, la más conocida, reúne cincuenta y un ejemplos. Las partes siguientes son colecciones de proverbios y un tratado doctrinal."),
                ("¿Cuál es la estructura de los cuentos?", "El conde plantea un problema, Patronio cuenta una historia parecida, el conde sigue el consejo y le va bien, y don Juan Manuel cierra el ejemplo con dos versos que resumen la moraleja."),
                ("¿Qué cuento de El conde Lucanor inspiró El traje nuevo del emperador?", "El ejemplo XXXII, «De lo que aconteció a un rey con los burladores que hicieron el paño». Andersen escribió su versión cinco siglos después."),
                ("¿Cuándo se escribió?", "Don Juan Manuel lo terminó en 1335, en la Castilla de Alfonso XI.")],
    },
    "libro-de-buen-amor-arcipreste-de-hita": {
        "color": "ocre", "genero": "Poesía", "unidad": "partes", "tema": "el amor loco, el amor de Dios y la vida del siglo XIV",
        "resumen": [
            "El Libro de buen amor es una obra en verso que Juan Ruiz, arcipreste de Hita, compuso en la primera mitad del siglo XIV. Está escrita como una falsa autobiografía: el arcipreste cuenta sus intentos de conquistar a distintas mujeres, casi siempre fracasados, y los adorna con fábulas, cantigas, oraciones y parodias. Él mismo dice que su libro enseña el «buen amor», el de Dios, mostrando los peligros del «loco amor».",
            "Los episodios más célebres son el de don Melón y doña Endrina, en el que la vieja Trotaconventos actúa de alcahueta; los encuentros con las serranas de la sierra de Guadarrama; la batalla entre don Carnal y doña Cuaresma, y el elogio de las mujeres pequeñas. La mezcla de lo religioso y lo burlesco, la ironía y la variedad de tonos lo hacen uno de los libros más vivos de la Edad Media.",
        ],
        "personajes": [("El arcipreste", "Narrador y protagonista, enamoradizo y casi siempre burlado."),
                       ("Trotaconventos", "Vieja alcahueta que hace de mensajera en los amores del arcipreste."),
                       ("Don Melón y doña Endrina", "Pareja de amantes del episodio central, adaptado de una comedia latina."),
                       ("Don Amor", "Personificación del amor, con quien el arcipreste discute."),
                       ("Las serranas", "Mujeres de la sierra, fuertes y dominantes, que asaltan al viajero."),
                       ("Don Carnal y doña Cuaresma", "Personajes de la batalla alegórica entre los placeres y la penitencia.")],
        "ideas": ["La ambigüedad entre el buen amor (de Dios) y el loco amor (el deseo).",
                  "La parodia de los géneros cultos y religiosos de la época.",
                  "El retrato vivo de la sociedad del siglo XIV: clérigos, villanos, mercaderes y alcahuetas.",
                  "La cuaderna vía mezclada con canciones de metros variados."],
        "faq": [("¿Quién escribió el Libro de buen amor?", "Juan Ruiz, arcipreste de Hita (Guadalajara). Apenas se sabe de él más que lo que cuenta el propio libro."),
                ("¿Qué es el buen amor?", "Para el autor, el amor de Dios, frente al loco amor del deseo carnal. Pero el libro juega con la ambigüedad y deja al lector decidir."),
                ("¿Quién es Trotaconventos?", "La vieja alcahueta que lleva los mensajes del arcipreste. Es la antecesora directa de La Celestina."),
                ("¿En qué métrica está escrito?", "Sobre todo en cuaderna vía, estrofas de cuatro versos alejandrinos con la misma rima, del mester de clerecía."),
                ("¿Cuándo se escribió?", "Los manuscritos conservados están fechados en 1330 y 1343.")],
    },
    "el-mercader-de-venecia-shakespeare": {
        "color": "azul", "genero": "Comedia", "unidad": "actos", "tema": "la justicia, la misericordia y el precio de una deuda",
        "resumen": [
            "En Venecia, el joven Bassanio necesita dinero para pretender a Porcia, una rica heredera de Belmont. Su amigo Antonio, un mercader cuyos barcos están en el mar, pide un préstamo a Shylock, un usurero judío al que ha despreciado en público. Shylock acepta sin cobrar intereses, pero con una condición: si Antonio no paga a tiempo, le cortará una libra de su carne.",
            "Bassanio gana la mano de Porcia en la prueba de los tres cofres. Pero los barcos de Antonio naufragan y Shylock, herido además por la fuga de su hija Jessica con un cristiano, exige que se cumpla el contrato. En el juicio, Porcia, disfrazada de doctor en leyes, le concede la libra de carne, siempre que no derrame una gota de sangre. Shylock lo pierde todo. La obra mezcla la comedia amorosa con uno de los personajes más complejos y discutidos de Shakespeare.",
        ],
        "personajes": [("Shylock", "Prestamista judío, humillado por los cristianos, que exige su libra de carne."),
                       ("Antonio", "El mercader de Venecia, generoso con su amigo y despectivo con Shylock."),
                       ("Porcia", "Heredera de Belmont, inteligente, que salva a Antonio disfrazada de juez."),
                       ("Bassanio", "Amigo de Antonio y pretendiente de Porcia."),
                       ("Jessica", "Hija de Shylock, que huye con el cristiano Lorenzo."),
                       ("Graciano y Nerisa", "Amigo de Bassanio y dama de Porcia, la segunda pareja de la comedia.")],
        "ideas": ["La ley escrita frente a la misericordia.",
                  "El antisemitismo de la sociedad veneciana y la humanidad de Shylock («¿No tiene ojos un judío?»).",
                  "El dinero, la amistad y el amor como formas de deuda.",
                  "Las apariencias engañan: la prueba de los cofres."],
        "faq": [("¿De qué trata El mercader de Venecia?", "Antonio pide un préstamo al usurero Shylock y ofrece como garantía una libra de su carne. Cuando no puede pagar, Porcia lo salva en el juicio disfrazada de abogado."),
                ("¿Cómo termina El mercader de Venecia?", "Shylock pierde el juicio, la mitad de sus bienes y es obligado a hacerse cristiano. Las parejas de enamorados se reúnen en Belmont y Antonio recupera sus barcos."),
                ("¿Qué son los tres cofres?", "La prueba que dejó el padre de Porcia: oro, plata y plomo. Quien elija el que guarda su retrato se casará con ella. Bassanio acierta con el de plomo."),
                ("¿Es una comedia o una tragedia?", "Una comedia, por su final feliz, aunque la historia de Shylock tiene un tono trágico."),
                ("¿Quién hizo esta traducción?", "Marcelino Menéndez y Pelayo, en prosa, para los Dramas de Guillermo Shakespeare (Barcelona, 1881).")],
    },
    "orgullo-y-prejuicio-jane-austen": {
        "color": "verde", "genero": "Novela", "tema": "el amor, el matrimonio y las primeras impresiones",
        "resumen": [
            "La señora Bennet tiene cinco hijas y una obsesión: casarlas bien, porque la casa familiar pasará a un primo cuando muera el señor Bennet. La llegada a la comarca del rico y amable señor Bingley y de su amigo, el todavía más rico señor Darcy, revoluciona la familia. Jane, la mayor, y Bingley se enamoran enseguida. Elizabeth, la segunda, inteligente e ingeniosa, siente antipatía por Darcy, que en un baile la ha despreciado.",
            "Las intrigas de las hermanas de Bingley, las mentiras del encantador Wickham y el orgullo de Darcy alimentan los prejuicios de Elizabeth, que rechaza su primera declaración de amor. Una carta, una visita a Pemberley y la fuga de la hermana pequeña, Lydia, con Wickham le muestran poco a poco quién es Darcy en realidad. Los dos tienen que vencer su orgullo y sus prejuicios para entenderse. Es la novela más leída de Jane Austen.",
        ],
        "personajes": [("Elizabeth Bennet", "Segunda de las hermanas, ingeniosa e independiente, rápida en juzgar."),
                       ("Fitzwilliam Darcy", "Caballero rico y orgulloso que acaba enamorándose de Elizabeth."),
                       ("Jane Bennet", "La hermana mayor, dulce y bondadosa, enamorada de Bingley."),
                       ("Charles Bingley", "Joven rico y afable, amigo de Darcy."),
                       ("George Wickham", "Oficial encantador y mentiroso, que se fuga con Lydia."),
                       ("El señor y la señora Bennet", "Un padre irónico y distante y una madre empeñada en casar a sus hijas."),
                       ("Lady Catherine de Bourgh (lady Catalina)", "Tía de Darcy, aristócrata altiva que se opone a su boda.")],
        "ideas": ["Las primeras impresiones engañan: el orgullo de él y el prejuicio de ella.",
                  "El matrimonio como necesidad económica para las mujeres de la época.",
                  "La ironía como forma de retratar a la sociedad rural inglesa.",
                  "El amor basado en el conocimiento y el respeto mutuo."],
        "faq": [("¿De qué trata Orgullo y prejuicio?", "De Elizabeth Bennet y el señor Darcy, que empiezan detestándose por el orgullo de él y los prejuicios de ella, y terminan casándose cuando aprenden a conocerse."),
                ("¿Cómo termina Orgullo y prejuicio?", "Darcy salva en secreto el honor de la familia Bennet tras la fuga de Lydia. Elizabeth acepta su segunda declaración y Jane se casa con Bingley."),
                ("¿Quién es el orgulloso y quién el prejuicioso?", "Suele decirse que Darcy es el orgullo y Elizabeth el prejuicio, pero los dos tienen algo de ambos."),
                ("¿Cuándo se publicó?", "En 1813. Esta traducción al español es de la edición de Calpe de 1924.")],
    },
}


if __name__ == "__main__":
    clasicos.BOOKS = BOOKS
    clasicos.NUMBER_START = NUMBER_START
    clasicos.main()
