from flask import Flask, jsonify
import psycopg2


app = Flask(__name__)

def get_db_conection():
    return psycopg2.connect(
        host="localhost",
        database="nico_db",
        user="nico",
        password="1234"
    )

@app.route("/productos")
def get_productos():
    conexion = get_db_conection()
    cursor = conexion.cursor()

    consulta = 'SELECT id, price FROM productos;'
    cursor.execute(consulta)

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    lista = []
    for fila in resultados:
        productos = {
            "id": fila[0],
            "price": float(fila[1])
        }

        lista.append(productos)
    return jsonify(lista)

if __name__ == "__main__":
    app.run(debug=True)


