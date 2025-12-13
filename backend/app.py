"""from flask import Flask, jsonify, request
import psycopg2


app = Flask(__name__)

def get_db_conection():
    return psycopg2.connect(
        host="localhost",
        database="nico_db",
        user="nico",
        password="1234"
    )

def fila_a_producto_dict(fila):
    if fila is None:
        return None
    
    producto = {
        "id": fila[0],
        "nombre": fila[1],
        "precio": float(fila[2]),
        "stock": fila[3]
    }
    return producto


@app.route("/productos", methods=['GET'])
def get_productos():
    conexion = get_db_conection()
    cursor = conexion.cursor()

    consulta = 'SELECT id, nombre, precio, stock FROM productos;'
    cursor.execute(consulta)

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    lista = []
    for fila in resultados:
        producto_dict = fila_a_producto_dict(fila)

        lista.append(producto_dict)
    return jsonify(lista), 200


@app.route("/productos/<int:producto_id>", methods=["GET"])
def obtender_producto_por_id(producto_id):
    conexion = get_db_conection()
    cursor = conexion.cursor()

    consulta_sql = 'SELECT id, nombre, precio, stock FROM productos WHERE id = %s;'

    cursor.execute(consulta_sql, (producto_id,))

    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado is None:
        return jsonify({"error": "producto no encontrado"}), 404
    
    producto_dict = fila_a_producto_dict(resultado)

    return jsonify(producto_dict), 200
##########################################"""

from flask import Flask, jsonify, request
import psycopg2


app = Flask(__name__)

def get_conection():
    return psycopg2.connect(
        host="localhost",
        database="fullstack_db",
        user="nico",
        password="1234"
    )

#funcion auxiliar connvierte resultado sql a diccionario python

def fila_a_dict(fila):
    if fila is None:
        return None
    
    producto = {
        "id": fila[0],
        "nombre": fila[1],
        "precio": float(fila[2]),
        "stock": fila[3]
    }

    return producto

@app.route("/productos", methods=["GET"])
def get_productos():
    conexion = get_conection()
    cursor = conexion.cursor()

    consulta = 'SELECT id, nombre, precio, stock FROM productos;'
    cursor.execute(consulta)

    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    resultado = []
    for fila in filas:
        resultado.append(fila_a_dict(fila))
    return jsonify(resultado), 200

@app.route("/productos/<int:producto_id>", methods=["GET"])
def get_producto_id(producto_id):
    conexion = get_conection()
    cursor = conexion.cursor()

    consulta = 'SELECT id, nombre, precio, stock FROM productos WHERE id = %s'
    cursor.execute(consulta, (producto_id,))

    fila = cursor.fetchone()

    cursor.close()
    conexion.close()

    if fila is None:
        return jsonify({"error":"producto no encontrado"}), 404

    return jsonify(fila_a_dict(fila)), 200



##################################3
@app.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()
    




if __name__ == "__main__":
    app.run(debug=True)


