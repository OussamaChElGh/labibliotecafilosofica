"""Cuarta tanda: los clásicos más buscados (mismo formato que clasicos.py).

python textos/fichas/clasicos4.py  →  ficha, descripción, portada y resúmenes de capítulo en textos/<slug>.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import clasicos  # noqa: E402

NUMBER_START = 50

BOOKS = {
    "la-odisea-homero": {
        "color": "azul", "genero": "Poema épico", "unidad": "cantos", "tema": "el regreso de Ulises a Ítaca tras la guerra de Troya",
        "resumen": [
            "Diez años después de la caída de Troya, Ulises (Odiseo) sigue sin volver a Ítaca. La ninfa Calipso lo retiene en su isla, mientras en su palacio un centenar de pretendientes se comen su hacienda y presionan a su esposa, Penélope, para que elija nuevo marido. Su hijo Telémaco, aconsejado por la diosa Minerva (Atenea), sale en busca de noticias de su padre.",
            "Liberado por orden de Júpiter (Zeus), Ulises naufraga en la isla de los feacios y les cuenta sus aventuras: los lotófagos, el cíclope Polifemo, la hechicera Circe, el descenso al Hades, las sirenas, Escila y Caribdis. Los feacios lo llevan a Ítaca, donde, disfrazado de mendigo, se reúne con Telémaco, prepara su venganza y mata a los pretendientes. Penélope lo reconoce por el secreto del lecho conyugal.",
        ],
        "personajes": [("Ulises (Odiseo)", "Rey de Ítaca, astuto y paciente, que tarda diez años en volver a casa."),
                       ("Penélope", "Esposa de Ulises, fiel e ingeniosa, que engaña a los pretendientes tejiendo y destejiendo un sudario."),
                       ("Telémaco", "Hijo de Ulises, que madura a lo largo del poema."),
                       ("Minerva (Atenea)", "Diosa de la sabiduría, protectora de Ulises y de su hijo."),
                       ("Neptuno (Poseidón)", "Dios del mar, enemigo de Ulises por haber cegado a su hijo Polifemo."),
                       ("Polifemo", "Cíclope que encierra a Ulises y sus compañeros en su cueva."),
                       ("Circe y Calipso", "Diosas que retienen a Ulises en sus islas."),
                       ("Antínoo", "El más insolente de los pretendientes de Penélope.")],
        "ideas": ["El nóstos: el viaje de regreso al hogar como aventura y como prueba.",
                  "La astucia y la inteligencia valen más que la fuerza.",
                  "La hospitalidad como ley sagrada y su violación.",
                  "La fidelidad, la paciencia y la identidad."],
        "faq": [("¿De qué trata La Odisea?", "Del largo regreso de Ulises a su reino de Ítaca tras la guerra de Troya, y de cómo, al llegar, recupera su casa y a su esposa Penélope matando a los pretendientes."),
                ("¿Cuántos cantos tiene La Odisea?", "Veinticuatro. Los cuatro primeros se centran en Telémaco; los relatos de las aventuras de Ulises están en los cantos IX a XII."),
                ("¿Qué diferencia hay entre la Ilíada y la Odisea?", "La Ilíada cuenta un episodio de la guerra de Troya, la cólera de Aquiles. La Odisea narra el regreso de Ulises después de la guerra."),
                ("¿Por qué salen Júpiter y Minerva en lugar de Zeus y Atenea?", "Porque Segalá, como era costumbre en su época, usó los nombres latinos de los dioses griegos: Júpiter es Zeus, Minerva es Atenea, Neptuno es Poseidón y Juno es Hera."),
                ("¿Quién hizo esta traducción?", "Luis Segalá y Estalella, helenista catalán. Su versión en prosa (1910) sigue siendo una de las más leídas en español.")],
    },
    "la-iliada-homero": {
        "color": "burdeos", "genero": "Poema épico", "unidad": "cantos", "tema": "la cólera de Aquiles en la guerra de Troya",
        "resumen": [
            "En el décimo año del asedio de Troya, el rey Agamenón arrebata a Aquiles, el mejor guerrero griego, su esclava Briseida. Ofendido, Aquiles se retira del combate y pide a su madre, la diosa Tetis, que Júpiter (Zeus) dé ventaja a los troyanos. Sin él, los aqueos sufren derrota tras derrota ante Héctor, hijo del rey Príamo, mientras los dioses toman partido en la lucha.",
            "Cuando los troyanos llegan a las naves griegas, Patroclo, el amigo íntimo de Aquiles, sale a combatir con sus armas y muere a manos de Héctor. Aquiles, enloquecido de dolor, vuelve a la batalla, mata a Héctor y arrastra su cadáver. El poema termina cuando el anciano Príamo entra de noche en la tienda de Aquiles para pedirle el cuerpo de su hijo, y Aquiles, conmovido, se lo devuelve.",
        ],
        "personajes": [("Aquiles", "El mejor guerrero de los aqueos, orgulloso y colérico."),
                       ("Héctor", "Príncipe y defensor de Troya, valiente y humano."),
                       ("Agamenón", "Rey de Micenas y jefe de los griegos, cuya soberbia provoca la cólera de Aquiles."),
                       ("Patroclo", "Compañero inseparable de Aquiles, cuya muerte lo cambia todo."),
                       ("Príamo", "Anciano rey de Troya, padre de Héctor y de Paris."),
                       ("Andrómaca", "Esposa de Héctor, que presiente su muerte."),
                       ("Ulises, Áyax y Diomedes", "Otros grandes héroes aqueos."),
                       ("Paris y Helena", "La pareja cuyo rapto originó la guerra.")],
        "ideas": ["La cólera y sus consecuencias: el orgullo herido arrastra a todos.",
                  "La gloria (kléos) frente a la muerte inevitable.",
                  "Los dioses intervienen, pero los hombres cargan con sus actos.",
                  "La compasión final: enemigos que se reconocen en el dolor."],
        "faq": [("¿De qué trata La Ilíada?", "De la cólera de Aquiles durante el asedio de Troya: su retirada del combate, la muerte de su amigo Patroclo, su venganza sobre Héctor y la devolución del cadáver a Príamo."),
                ("¿Aparece el caballo de Troya en la Ilíada?", "No. El poema termina con los funerales de Héctor. El caballo de Troya se menciona en la Odisea y lo cuenta Virgilio en la Eneida."),
                ("¿Cuántos cantos tiene La Ilíada?", "Veinticuatro, como la Odisea."),
                ("¿Por qué salen Júpiter y Minerva en lugar de Zeus y Atenea?", "Porque Segalá, como era costumbre en su época, usó los nombres latinos de los dioses griegos: Júpiter es Zeus, Minerva es Atenea, Neptuno es Poseidón y Juno es Hera."),
                ("¿Quién hizo esta traducción?", "Luis Segalá y Estalella, que la publicó en prosa en 1908. Es la versión española clásica del poema.")],
    },
    "la-celestina-fernando-de-rojas": {
        "color": "burdeos", "genero": "Tragicomedia", "unidad": "actos", "tema": "el amor, la codicia y la muerte",
        "resumen": [
            "Calisto, un joven noble, entra persiguiendo a su halcón en el huerto de Melibea y se enamora de ella, pero es rechazado. Su criado Sempronio le aconseja recurrir a Celestina, una vieja alcahueta y hechicera. Celestina, con astucia y un conjuro, consigue entrar en casa de Melibea y despertar su amor, y a cambio recibe de Calisto una cadena de oro.",
            "Los criados Sempronio y Pármeno exigen su parte de la recompensa. Celestina se niega y ellos la matan; huyendo, saltan por una ventana y son ajusticiados. Calisto y Melibea se ven a escondidas en el huerto, pero una noche Calisto cae de la escala y muere. Melibea, desesperada, se arroja desde una torre ante su padre, Pleberio, que cierra la obra con un amargo lamento.",
        ],
        "personajes": [("Celestina", "Vieja alcahueta, astuta y codiciosa, maestra en manipular a todos."),
                       ("Calisto", "Joven noble, enamorado de forma obsesiva de Melibea."),
                       ("Melibea", "Hija de Pleberio, que acaba entregándose a la pasión."),
                       ("Sempronio", "Criado de Calisto, interesado y desleal."),
                       ("Pármeno", "Criado de Calisto, al principio fiel, luego corrompido por Celestina."),
                       ("Elicia y Areúsa", "Jóvenes vinculadas a Celestina, amantes de los criados."),
                       ("Pleberio", "Padre de Melibea, cuyo llanto cierra la obra.")],
        "ideas": ["El amor pasional que lleva a la destrucción.",
                  "La codicia rompe todas las lealtades.",
                  "El cambio de una sociedad medieval a otra moderna, movida por el dinero.",
                  "La fortuna y la muerte que alcanzan a todos."],
        "faq": [("¿De qué trata La Celestina?", "De los amores de Calisto y Melibea, facilitados por la alcahueta Celestina, y de cómo la codicia y la pasión terminan con la muerte de casi todos los personajes."),
                ("¿Quién escribió La Celestina?", "Fernando de Rojas, aunque él mismo dijo haber encontrado escrito el primer acto. Se publicó en 1499 como comedia y en 1502 como tragicomedia de 21 actos."),
                ("¿Es una novela o una obra de teatro?", "Está escrita en diálogo como el teatro, pero es demasiado larga para representarse tal cual. Se considera un género a caballo entre los dos."),
                ("¿Cómo muere Celestina?", "La matan Sempronio y Pármeno cuando se niega a repartir con ellos la cadena de oro que le dio Calisto.")],
    },
}


if __name__ == "__main__":
    clasicos.BOOKS = BOOKS
    clasicos.NUMBER_START = NUMBER_START
    clasicos.main()
