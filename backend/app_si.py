from flask import Flask, jsonify, request
import psycopg2


app3 = Flask(__name__)

def get_connection():
    return psycopg2.connect(
       hots='localhost',
       database='nico_fullstack',
       user='nico',
       password='1234'
    )
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

@app3.route('/productos', methods=['GET'])
def get_productos():
    conexion = get_connection()
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

@app3.route('/productos/<int:producto_id>', methods=['GET'])
def get_id(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = 'SELECT id, nombre, precio, stock FROM productos WHERE id = %s;'
    cursor.execute(consulta,(producto_id,))
    fila_existe = cursor.fetchone()

    cursor.close()
    conexion.close()

    if fila_existe in None:
        return jsonify({'error': 'producto no encontrado'}), 404
    return jsonify(fila_a_dict(fila_existe)), 200

@app3.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()

    nombre = datos.get('nombre')
    precio = datos.get('precio')
    stock = datos.get('stock')

    if nombre is None or precio is None or stock is None:
        return jsonify({'error': 'faltan campos obligatorios'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO productos(nombre, precio, stock)
        VALUES(%s,%s,%s)
        RETURNING id, nombre, precio, stock;    
        """ 
    cursor.execute(consulta,(nombre,precio,stock))
    fila = cursor.fetchone()

    # Me faltó esto
    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 201

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def editar_producto(producto_id):
    datos = request.get_json()

    campos = ('nombre', 'precio', 'stock')

    if any(datos.get(campo) is None for campo in campos):
        return jsonify({'error': 'faltan campos obligatorios'}), 400

    conexion = get_connection()
    cursor = conexion.cursor()

    consulta_update = """
        UPDATE productos
        SET nombre = %s,
            precio = %s,
            stock = %s
        WHERE id = %s
        RETURNING id, nombre, precio, stock;
    """

    #valores = tuple(datos[campo] for campo in campos)
    valores = []
    for campo in campos:
        valores.append(datos[campo])

    cursor.execute(
        consulta_update,
        (*valores, producto_id)
    )

    fila_actualizada = cursor.fetchone()

    if fila_actualizada is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': 'producto no encontrado'}), 404

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila_actualizada)), 200

    

@app3.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = """
        DELETE FROM productos
        WHERE id = %s
        RETURNING id;
    """
    cursor.execute(consulta, (producto_id,))
    fila_borrada = cursor.fetchone()

    if fila_borrada is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': 'producto no encontrado'}), 404

    conexion.commit()

    cursor.close()
    conexion.close()

    return '', 204


if __name__ == '__main__':
    app3.run(debug=True)

