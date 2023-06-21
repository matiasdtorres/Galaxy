import sqlite3

conexion = sqlite3.connect("./database/db.db")
conexion.execute('''CREATE TABLE IF NOT EXISTS puntuacion
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                nick TEXT,
                score INTEGER)''')

# Funcion para insertar una nueva puntuacion en la db
def insertar_score(NICK,SCORE):
    cursor = conexion.execute("SELECT score FROM puntuacion WHERE NICK=?",(NICK,))
    score_existente = cursor.fetchone()

    if score_existente is None or SCORE > score_existente[0]:
        if score_existente is None:
            conexion.execute("INSERT INTO puntuacion (nick,score) VALUES (?,?)",(NICK,SCORE))
        else:
            #aca manipulo datos y actualizo la db con el nuevo score utilizando update
            conexion.execute("UPDATE puntuacion SET score=? WHERE nick=?",(SCORE,NICK))
        conexion.commit()