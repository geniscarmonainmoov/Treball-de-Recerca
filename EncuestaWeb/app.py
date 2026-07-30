from flask import Flask, render_template, request
import sqlite3
import time

app = Flask(__name__)


with open("preguntas.txt", "r", encoding="utf-8") as f:
    preguntas = [linea.strip() for linea in f if linea.strip()]

def crear_db():

    conexion = sqlite3.connect("encuesta.db")

    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS respuestas(
        id INTEGER PRIMARY KEY,
        pregunta TEXT,
        respuesta TEXT,
        tiempo REAL
    )
    """)

    conexion.commit()
    conexion.close()



crear_db()



@app.route("/")
def inicio():

    return render_template(
        "encuesta.html",
        numero=0,
        pregunta=preguntas[0]
    )



@app.route("/responder/<int:num>", methods=["POST"])
def responder(num):

    respuesta = request.form["respuesta"]

    inicio = float(request.form["inicio"])

    tiempo = time.time() - inicio


    conexion = sqlite3.connect("encuesta.db")

    cursor = conexion.cursor()


    cursor.execute(
    """
    INSERT INTO respuestas
    (pregunta,respuesta,tiempo)

    VALUES(?,?,?)
    """,
    (
        preguntas[num],
        respuesta,
        tiempo
    ))


    conexion.commit()

    conexion.close()



    siguiente=num+1


    if siguiente < len(preguntas):

        return render_template(
            "encuesta.html",
            numero=siguiente,
            pregunta=preguntas[siguiente]
        )


    return render_template("final.html")




if __name__ == "__main__":
    print("EJECUTANDO MI APP.PY CORRECTO")
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )