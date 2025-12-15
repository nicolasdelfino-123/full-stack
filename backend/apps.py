from flask import Flask, jsonify, request
import psycopg2

apps = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="nico_fullstack",
        user="postgres",
        password="1234"
    )

def fila_a_dict(fila):
    if fila is None:
        return None
    
    productos = {
        "id": fila[0],
        "nombre": fila[1],
        "precio": float(fila[2]),
        "stock": fila[3],
    }

    return productos
@apps.route('/productos', methods=['GET'])
def get_productos():
    conexion = get_connection()
    cursor = conexion.cursor()
    
    consulta = 'SELECT id, nombre, precio, stock FROM productos;'
    cursor.execute(consulta)

    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    resultado_dict = []
    for fila in filas:
        resultado_dict.append(fila_a_dict(fila))
    return jsonify(resultado_dict), 200

@apps.route('/productos/<int:producto_id>', methods=['GET'])
def get_producto_id(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = 'SELECT id, nombre, precio, stock FROM productos WHERE id = %s'
    cursor.execute(consulta,(producto_id,))

    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if resultado is None:
        return jsonify({'error': ' producto no encontrado'}), 404
    return jsonify(fila_a_dict(resultado)), 200


@apps.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()

    nombre = datos.get('nombre')
    precio = datos.get('precio')
    stock = datos.get('stock')

    #######################################

    if nombre is None or precio is None or stock is None:
        return jsonify({"error": 'falta alguno de los campos obligatorios'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta_sql = """
        INSERT INTO productos(nombre,precio,stock)
        VALUES(%s, %s, %s)
        RETURNING id, nombre, precio, stock
        """
    cursor.execute(consulta_sql,(nombre,precio,stock))

    fila = cursor.fetchone()

    conexion.commit()
    
    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 201

@apps.route('/productos/<int:producto_id>', methods=['PUT'])
def editar_producto(producto_id):
    datos = request.get_json()

    nombre = datos.get('nombre')
    precio = datos.get('precio')
    stock = datos.get('stock')

    #######################################

    if nombre is None or precio is None or stock is None:
        return jsonify({'error': 'falta un campo obligatorio'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta_existe = 'SELECT id, nombre, precio, stock FROM productos WHERE id = %s;'

    cursor.execute(consulta_existe,(producto_id,))
    fila_existe = cursor.fetchone()

    if fila_existe is None:
        cursor.close()
        conexion.close()

        return jsonify({"error": 'producto no encontrado'}), 404
    
    consulta_update = """
        UPDATE productos
        SET nombre = %s,
            precio = %s,
            stock = %s,
        WHERE id = %s
        RETURNING id, nombre, precio, stock;
    """
    cursor.execute(consulta_update,(nombre, precio, stock, producto_id))

    fila_actualizada = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila_actualizada)), 200

@apps.rout('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta_existe = 'SELECT id FROM productos WHERE id = %s'
    cursor.execute(consulta_existe,(producto_id,))

    fila = cursor.fetchone()

    if fila is None:
        cursor.close()
        conexion.close()
        return jsonify({'error':'producto no encontrado'}), 404
    consulta_delete = 'DELETE FROM productos WHERE id = %s;'
    cursor.execute(consulta_delete,(producto_id,))

    conexion.commit()

    cursor.close()
    conexion.close()

    return '', 204

if __name__ == '__main__':
    apps.run(debug=True)








##################################3
