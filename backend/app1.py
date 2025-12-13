from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conexion_db = psycopg2.connect(
        host="localhost",
        database="nico_fullstack",
        user="postgres",
        password="1234"
    )

    return conexion_db

@app.route('/productos')
def obtener_productos():
    #abro la conexion
    conexion_db = get_db_connection()
    # creo un cursor sobre la conexion que creé
    cursor_db = conexion_db.cursor()
    # creamos la conulta
    consulta_sql = 'SELECT id, nombre, precio, stock FROM productos;'
    #ejecutá en la bd esa consulta amigo cursor
    cursor_db.execute(consulta_sql)
    #cursor traeme todo lo que devolció la consulta sql
    resultados_sql = cursor_db.fetchall()
    # cerrar cursor y conexion para que la base no quede ocupada
    cursor_db.close()
    conexion_db.close()

    lista_productos= []
    for fila in resultados_sql:
        producto = {
            "id": fila[0],
            "nombre": fila[1],
            "precio": float(fila[2]),
            "stock": fila[3]
        }

        lista_productos.append(producto)

    return jsonify(lista_productos)

if __name__ == '__main__':
    app.run(debug=True)