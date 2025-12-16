from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host='localhost',
        database='nico_fullsatck',
        user='postgres',
        password='1234'
    )

def fila_a_dict(fila):
    if fila is None:
        return None
    
    producto = {
        "id" : fila[0],
        "nombre" : fila[1],
        "precio" : float(fila[2]),
        "stock" : fila[3],
    }

    return producto

@app.route('/productos', methods=['GET'])
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
    

@app.route('/productos/<int:producto_id>', methods=['GET'])
def get_por_id(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = 'SELECT id, nombre, precio, stock FROM productos WHERE id = %s;'

    cursor.execute(consulta,(producto_id,))

    fila = cursor.fetchone()

    cursor.close()
    conexion.close()


    if fila is None:
        jsonify({'error': 'producto no encontrado'}), 404
    return jsonify(fila_a_dict(fila)) 

@app.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()

    nombre = datos.get('nombre')
    precio = datos.get('pecio')
    stock = datos.get('stock')

    if nombre is None or precio is None or stock is None:
        return jsonify({'error': ' faltan datos obligatorios'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO productos(nombre, precio, stock)
        VALUE (%s,%s,%s)
        RETURNING id, nombre, precio, stock;
        """
    cursor.execute(consulta,(nombre,precio,stock))

    fila = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 201

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def editar_producto(producto_id):
    datos = request.get_json()

    nombre = datos.get('nombre')
    precio = datos.get('pecio')
    stock = datos.get('stock')

    if nombre is None or precio is None or stock is None:
        return jsonify({'error': 'faltan datos obligatorios'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta_existe = 'SELECT id FROM producto WHERE id = %s;'
    cursor.execute(consulta_existe,(producto_id,))

    fila_existe = cursor.fetchone()

    if fila_existe is None:
        return jsonify({'error': 'producto no encontrado'}), 404
    
    consulta_update = """
        UPDATE productos
        SET nombre = %s,
            precio = %s,
            stock = %s
        WHERE id = %s
        RETURNING id, nombre, precio, stock;
    """