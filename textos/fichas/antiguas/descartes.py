"""Fichas de Descartes en el formato nuevo (fichas_antiguas.py)."""

AUTOR = "René Descartes"


def book(**data):
    data.setdefault("autor", AUTOR)
    data.setdefault("ruta_autor", "")
    return data


BOOKS = {
    "/descartes-discurso-del-metodo-pdf/": book(
        titulo="Discurso del método", genero="Tratado filosófico", año="1637", tema="el método para buscar la verdad en las ciencias",
        descripcion="Discurso del método de Descartes: resumen de sus seis partes, las cuatro reglas del método, la moral provisional y el «pienso, luego existo», con preguntas frecuentes.",
        resumen=[
            "Descartes cuenta en primera persona cómo, tras estudiar en los mejores colegios, salió de ellos sin certezas y decidió buscar la verdad por sí mismo. Escrito en francés y no en latín para que pudiera leerlo cualquiera con buen sentido, el Discurso se publicó como prólogo de tres ensayos científicos: la Dióptrica, los Meteoros y la Geometría.",
            "Se divide en seis partes. En la segunda propone cuatro reglas: no aceptar nada que no sea evidente, dividir cada dificultad, ir de lo simple a lo complejo y hacer revisiones completas. En la tercera fija una moral provisional. En la cuarta, dudando de todo, llega a la primera certeza, pienso, luego existo, y de ella a Dios y al mundo. Las últimas resumen su física, el cuerpo como máquina y sus razones para publicar.",
        ],
        ideas=["Las cuatro reglas del método: evidencia, análisis, síntesis y enumeración.",
               "La duda metódica como camino hacia la certeza.",
               "Pienso, luego existo: la primera verdad indudable.",
               "La moral provisional: vivir con decisión mientras se busca la verdad.",
               "El cuerpo de los animales y del ser humano funciona como una máquina."],
        faq=[("¿De qué trata el Discurso del método?", "De cómo conducir bien la razón para encontrar la verdad en las ciencias. Descartes expone su camino intelectual, cuatro reglas de método, una moral provisional y la certeza del cogito."),
             ("¿Cuáles son las cuatro reglas del método de Descartes?", "Evidencia (aceptar solo lo claro y distinto), análisis (dividir los problemas), síntesis (ordenar los pensamientos de lo simple a lo complejo) y enumeración (revisarlo todo sin omitir nada)."),
             ("¿En qué parte aparece «pienso, luego existo»?", "En la cuarta parte del Discurso del método."),
             ("¿Cuántas partes tiene el Discurso del método?", "Seis: consideraciones sobre las ciencias, reglas del método, moral provisional, metafísica, física y razones para publicar.")]),
    "/descartes-meditaciones-metafisicas/": book(
        titulo="Meditaciones metafísicas", genero="Tratado filosófico", año="1641", tema="la duda, el yo, Dios y la distinción entre alma y cuerpo",
        resumen=[
            "En seis meditaciones, como si fueran seis días de reflexión, Descartes se propone derribar todas sus opiniones para construir el conocimiento sobre bases firmes. En la primera duda de los sentidos, de la diferencia entre la vigilia y el sueño y, con la hipótesis de un genio maligno, incluso de las matemáticas.",
            "En la segunda encuentra la certeza del yo que piensa y muestra con el ejemplo del trozo de cera que la mente se conoce mejor que el cuerpo. En la tercera y la quinta demuestra la existencia de Dios, en la cuarta explica el origen del error y en la sexta prueba la existencia del mundo material y la distinción real entre alma y cuerpo. El libro se publicó con las objeciones de Hobbes, Arnauld, Gassendi y otros, y las respuestas de Descartes.",
        ],
        ideas=["La duda hiperbólica y el genio maligno.",
               "El cogito: el yo es una cosa que piensa.",
               "Las pruebas de la existencia de Dios por la idea de infinito y por su esencia.",
               "El error nace de una voluntad que va más allá del entendimiento.",
               "El dualismo: alma y cuerpo son sustancias distintas."],
        faq=[("¿Cuántas meditaciones metafísicas hay?", "Seis: sobre la duda, la naturaleza de la mente, Dios, la verdad y el error, la esencia de las cosas materiales y la existencia del mundo y la distinción entre alma y cuerpo."),
             ("¿Qué es el genio maligno de Descartes?", "La hipótesis de un ser poderoso y engañador que podría hacernos equivocar incluso en lo más evidente. Sirve para llevar la duda al extremo."),
             ("¿Qué significa el ejemplo del trozo de cera?", "Que lo que conocemos de los cuerpos no lo captan los sentidos, que cambian, sino el entendimiento."),
             ("¿Quiénes escribieron objeciones a las Meditaciones?", "Entre otros, Thomas Hobbes, Antoine Arnauld, Pierre Gassendi y Marin Mersenne.")]),
    "/descartes-meditaciones-sobre-la-existencia-de-dios/": book(
        titulo="Meditaciones sobre la existencia de Dios", genero="Tratado filosófico", año="1641", tema="las pruebas de la existencia de Dios y del alma",
        resumen=[
            "Es otra forma de titular las Meditaciones metafísicas, cuyo título completo anuncia que en ellas se demuestran la existencia de Dios y la distinción real entre el alma y el cuerpo. Descartes las dedicó a la Facultad de Teología de la Sorbona, presentándolas como una defensa racional de la fe.",
            "Las pruebas de Dios ocupan el centro del libro. En la tercera meditación, Descartes parte de que tiene la idea de un ser infinito y perfecto, que no puede proceder de él mismo, ser finito. En la quinta, la existencia se deduce de la esencia de Dios como un teorema geométrico. Dios garantiza después que lo que concebimos con claridad y distinción es verdadero.",
        ],
        ideas=["La idea de infinito como huella de Dios en la mente.",
               "El argumento ontológico: la existencia pertenece a la esencia de Dios.",
               "Dios como garantía de la verdad de las ideas claras y distintas.",
               "La filosofía al servicio de la defensa de la fe."],
        faq=[("¿Es la misma obra que las Meditaciones metafísicas?", "Sí. El título completo en latín es Meditaciones de filosofía primera, en las que se demuestra la existencia de Dios y la distinción real entre el alma y el cuerpo."),
             ("¿Cómo demuestra Descartes la existencia de Dios?", "Con dos argumentos: tenemos la idea de un ser infinito que solo puede venir de un ser infinito, y la existencia forma parte de la esencia de un ser perfecto."),
             ("¿Qué es el círculo cartesiano?", "La objeción de Arnauld: Descartes usa las ideas claras y distintas para probar a Dios y luego usa a Dios para garantizar esas ideas.")]),
    "/descartes-los-principios-de-la-filosofia/": book(
        titulo="Los principios de la filosofía", genero="Tratado filosófico", año="1644", tema="el sistema completo de la filosofía cartesiana",
        resumen=[
            "Descartes concibió los Principios como un manual que pudiera sustituir a los de la escolástica en las escuelas. En cuatro partes expone de forma ordenada todo su sistema: los principios del conocimiento humano, los principios de las cosas materiales, el mundo visible y la Tierra.",
            "La primera parte resume su metafísica; las siguientes desarrollan una física mecanicista en la que la materia es pura extensión y todos los fenómenos se explican por figura y movimiento, incluidos los torbellinos que mueven los planetas. En el prefacio a la traducción francesa de 1647 presenta la filosofía como un árbol cuyas raíces son la metafísica, el tronco la física y las ramas la medicina, la mecánica y la moral.",
        ],
        ideas=["La filosofía como un árbol: metafísica, física y ciencias aplicadas.",
               "La materia es extensión y se explica por figura y movimiento.",
               "Las leyes del movimiento y la teoría de los torbellinos.",
               "Un manual pensado para sustituir a la escolástica."],
        faq=[("¿Qué son Los principios de la filosofía?", "La exposición sistemática del pensamiento de Descartes, desde la metafísica hasta la física del universo y de la Tierra, en cuatro partes."),
             ("¿Qué es el árbol de la filosofía de Descartes?", "La imagen del prefacio de 1647: las raíces son la metafísica, el tronco la física y las ramas la medicina, la mecánica y la moral."),
             ("¿A quién dedicó Descartes los Principios?", "A la princesa Isabel de Bohemia, con quien mantenía una importante correspondencia.")]),
    "/descartes-tratado-de-las-pasiones-del-alma/": book(
        titulo="Las pasiones del alma", genero="Tratado filosófico", año="1649", tema="las emociones y su relación con el cuerpo",
        resumen=[
            "Última obra publicada por Descartes, nació de su correspondencia con la princesa Isabel de Bohemia, que le preguntaba cómo se relacionan el alma y el cuerpo. Descartes explica las pasiones como efectos en el alma de los movimientos de los espíritus animales en el cuerpo, que se encuentran en la glándula pineal.",
            "Distingue seis pasiones primitivas, admiración, amor, odio, deseo, alegría y tristeza, de las que derivan todas las demás. Las pasiones son buenas por naturaleza; lo que importa es aprender a dirigirlas. La virtud principal es la generosidad: saber que solo nos pertenece el buen uso de nuestra libertad y estar resuelto a usarla bien.",
        ],
        ideas=["Las pasiones nacen de la unión entre el alma y el cuerpo.",
               "Seis pasiones primitivas: admiración, amor, odio, deseo, alegría y tristeza.",
               "La glándula pineal como punto de encuentro de alma y cuerpo.",
               "La generosidad como clave de la vida moral."],
        faq=[("¿Cuáles son las seis pasiones primitivas según Descartes?", "Admiración, amor, odio, deseo, alegría y tristeza."),
             ("¿Qué es la generosidad para Descartes?", "La virtud de quien sabe que solo depende de él el buen uso de su libre voluntad y está decidido a usarla siempre bien."),
             ("¿Por qué escribió Descartes este tratado?", "A raíz de las preguntas de Isabel de Bohemia sobre cómo puede el alma, inmaterial, actuar sobre el cuerpo.")]),
    "/descartes-tratado-del-hombre/": book(
        titulo="Tratado del hombre", genero="Tratado científico", año="1664 (póstumo)", tema="el cuerpo humano como máquina",
        resumen=[
            "Escrito hacia 1633 como parte de El mundo, el Tratado del hombre quedó inédito cuando Descartes supo de la condena de Galileo. Se publicó tras su muerte, primero en latín en 1662 y después en francés en 1664.",
            "Descartes imagina un cuerpo construido por Dios como una máquina y explica sus funciones, la digestión, la circulación de la sangre, la respiración, los sentidos, los reflejos y la memoria, solo por la disposición de sus órganos y el movimiento de los espíritus animales, como las fuentes y autómatas de los jardines reales.",
        ],
        ideas=["El cuerpo funciona como una máquina sin necesidad de alma.",
               "Los espíritus animales recorren los nervios como agua por tuberías.",
               "Una de las primeras explicaciones mecanicistas del sistema nervioso.",
               "La fisiología como parte de la física."],
        faq=[("¿Qué es el Tratado del hombre de Descartes?", "Una obra en la que Descartes explica el cuerpo humano como una máquina que funciona por la disposición de sus órganos, sin intervención del alma."),
             ("¿Por qué no lo publicó en vida?", "Porque formaba parte de El mundo, que Descartes guardó tras la condena de Galileo en 1633.")]),
    "/descartes-el-mundo-o-el-tratado-de-la-luz-pdf/": book(
        titulo="El mundo o Tratado de la luz", genero="Tratado científico", año="1664 (póstumo)", tema="la física mecanicista y el origen del universo",
        resumen=[
            "Descartes escribió El mundo entre 1629 y 1633 para explicar toda la naturaleza a partir de la materia y el movimiento. Para evitar problemas con la Iglesia, lo presenta como una fábula: Dios crea un mundo nuevo en espacios imaginarios y lo deja evolucionar según las leyes de la naturaleza.",
            "La materia es extensión, no hay vacío y los cuerpos se mueven en grandes torbellinos que explican la formación del Sol, los planetas y la luz. El libro defendía el movimiento de la Tierra, y cuando Descartes supo de la condena de Galileo en 1633 renunció a publicarlo. Apareció tras su muerte, en 1664.",
        ],
        ideas=["Todo el mundo físico se explica por materia extensa y movimiento.",
               "Las leyes de la naturaleza y la conservación del movimiento.",
               "La teoría de los torbellinos.",
               "La prudencia de Descartes ante la condena de Galileo."],
        faq=[("¿De qué trata El mundo de Descartes?", "De una explicación mecanicista del universo, desde la luz y la formación de los astros hasta las leyes del movimiento, presentada como la fábula de un mundo nuevo."),
             ("¿Por qué Descartes no publicó El mundo?", "Porque defendía el movimiento de la Tierra y en 1633 la Inquisición condenó a Galileo por esa misma tesis.")]),
    "/descartes-los-meteoros/": book(
        titulo="Los meteoros", genero="Tratado científico", año="1637", tema="los fenómenos atmosféricos",
        resumen=[
            "Los meteoros es uno de los tres ensayos que Descartes publicó con el Discurso del método, junto con la Dióptrica y la Geometría, para mostrar la fecundidad de su método. Explica los fenómenos del cielo, vapores, vientos, nubes, lluvia, nieve, granizo, tormentas y rayos, a partir del movimiento de pequeñas partículas.",
            "Su capítulo más famoso es el del arco iris: con experimentos sobre una esfera de vidrio llena de agua, Descartes calcula el ángulo en que la luz refractada en las gotas produce el arco principal y el secundario. Es un ejemplo temprano de física matemática y experimental.",
        ],
        ideas=["Los fenómenos naturales se explican por partículas en movimiento.",
               "La explicación del arco iris por la refracción de la luz en las gotas.",
               "La ciencia como aplicación del método."],
        faq=[("¿Qué son Los meteoros de Descartes?", "Un ensayo de 1637 sobre los fenómenos atmosféricos que acompaña al Discurso del método como ejemplo de su aplicación."),
             ("¿Cómo explicó Descartes el arco iris?", "Por la refracción y reflexión de la luz en las gotas de lluvia, y calculó el ángulo en que se ven el arco principal y el secundario.")]),
    "/descartes-correspondencia-con-isabel-de-bohemia-y-otras-cartas/": book(
        titulo="Correspondencia con Isabel de Bohemia", genero="Cartas", año="1643-1649", tema="la unión del alma y el cuerpo y la vida feliz",
        resumen=[
            "En 1643, la princesa Isabel del Palatinado, exiliada en La Haya, escribe a Descartes con una pregunta que pone en apuros su filosofía: si el alma es inmaterial, ¿cómo puede mover el cuerpo? Así empieza una de las correspondencias más importantes de la filosofía, que dura hasta la muerte de Descartes.",
            "Las cartas tratan de la unión de alma y cuerpo, de las pasiones, de la felicidad a partir del De vita beata de Séneca, de la providencia, de la libertad y de la política de Maquiavelo. Isabel aparece como una interlocutora aguda, y de sus preguntas nació el Tratado de las pasiones del alma.",
        ],
        personajes=[("René Descartes", "Filósofo, que responde a las objeciones de la princesa."),
                    ("Isabel de Bohemia", "Princesa del Palatinado, filósofa y crítica de su dualismo.")],
        ideas=["El problema de la interacción entre alma y cuerpo.",
               "La felicidad como contento del espíritu y buen uso de la razón.",
               "La moral cartesiana en la vida práctica.",
               "Isabel de Bohemia como filósofa por derecho propio."],
        faq=[("¿Qué pregunta hizo Isabel de Bohemia a Descartes?", "Cómo puede el alma, que no tiene extensión, mover el cuerpo, que es materia. Es la formulación clásica del problema mente-cuerpo."),
             ("¿Qué obra nació de esta correspondencia?", "El Tratado de las pasiones del alma, de 1649."),
             ("¿Quién era Isabel de Bohemia?", "Isabel del Palatinado (1618-1680), princesa exiliada, matemática y filósofa, a quien Descartes dedicó los Principios de la filosofía.")]),
}
