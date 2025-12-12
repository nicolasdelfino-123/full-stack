from flask import Flask, jsonify, request
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

@app.route("/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json()

    nombre = datos.get("nombre")
    precio = datos.get("precio")
    stock = datos.get("stock")

    if nombre is None or precio in None or stock is None:
        return jsonify({"error": "faltan campos obligatorios"}), 400
    
    conexion = get_db_conection()
    cursor = conexion.cursor()

    consulta_sql = """
        INSERT INTO productos (nombre, precio, stock)
        VALUES (%s, %s, %s)
        RETURNING id, nombre, precio, stock;
        """
    cursor.execute(consulta_sql, (nombre,precio,stock))

    fila = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    producto_creado = fila_a_producto_dict(fila)

    return jsonify(producto_creado), 201








if __name__ == "__main__":
    app.run(debug=True)


