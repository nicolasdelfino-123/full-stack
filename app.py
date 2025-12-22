from flask import Flask, request, jsonify
import psycopg2


app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host='localhost',
        user='nico',
        database='nico_fullstack',
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


@app.route('/productos', methods=['GET'])
def get_productos():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute('' \
    'SELECT id, nombre, precio, stock FROM productos;'
    )

    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    resultados = []

    for fila in filas:
        resultados.append(fila_a_dict(fila))

    return jsonify(resultados), 200

@app.route('/productos<int:producto_id>', methods=['GET'])
def get_por_id(producto_id):
    conexion =  get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        'SELECT id, nombre, precio, stock FROM productos WHERE id = %s;',
        (producto_id,)
    )

    fila = cursor.fetchone()

    if fila is None:
        cursor.close()
        conexion.close()
        return jsonify({f'error: producto con id{producto_id} no encontrado'}), 404
    
    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 200

@app.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json() or {}

    campos = ('nombre', 'precio', 'stock')

    for campo in campos:
        if datos.get(campo) is None:
            return jsonify({f'falta el campo {campo} obligatorio'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = """
            INSERT INTO productos(nombre, stock, precio)
            VALUES(%s,%s,%s)
            RETURNING id, nombre, stock, precio;
    """
    
    valores = []
    for campo in campos:
        valores.append(datos[campo])

    cursor.execute(consulta, valores)

    fila = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 201

@app.route('/productos<int:producto_id>',methods=['PUT'])
def editar_prodcuto(producto_id):
    datos = request.get_json()

    campos = ('nombre', 'precio', 'stock')

    for campo in campos:
        if datos.get(campo) is None:
            return jsonify({f'error: falta campo {campo} obligatorio'}), 400
    
    conexion =  get_connection()
    cursor = conexion.cursor()

    consulta = """
        UPDATE productos
        SET nombre = %s,
            precio = %s,
            stock = %s
        WHERE id = %s
        RETURNING id, nombre, precio, stock;
    """
    valores = []
    for campo in campos:
        valores.append(datos[campo])
    
    cursor.execute(
        consulta,
        (*valores, producto_id)
    )

    fila = cursor.fetchone()

    if fila is None:
        cursor.close()
        conexion.close()
        return jsonify({f'error: producto con id {producto_id} no encontrado'}), 404
    
    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)),200

@app.route('/productos<int:producto_id>',methods=['DELETE'])
def eliminar_producto(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = """
        DELETE FROM productos 
        WHERE id = %s
        RETURNING id, nombre, precio, stock;
    """
    cursor.execute(consulta, (producto_id,))

    fila = cursor.fetchone()

    if fila is None:
        cursor.close()
        conexion.close()
        return jsonify({f'error: producto con id {producto_id} no encontrado'}), 404
    
    conexion.commit()

    cursor.close()
    conexion.close()

    return '', 204
