from flask import Flask, jsonify, request
import psycopg2


app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host='localhost',
        database='nico_fullstack',
        user='postgres',
        password='1234'
    )

#--------------------
#HELPER NICO
#-----------------------

def fila_a_dict(fila):
    if fila is None:
        return None
    
    producto = {
        'id': fila[0],
        'nombre': fila[1],
        'precio': float(fila[2]),
        'stock': fila[3]
    }

    return producto

@app.route('/productos',methods=['GET'])
def get_productos():
    conexion = get_conn()
    cursor = conexion.cursor()

    cursor.execute(
        'SELECT id, nombre, precio, stock FROM productos'
    )

    filas = cursor.fetchall()

    # me olvidé cerrar con y cursor
    cursor.close()
    conexion.close()

    resultado = []
    for fila in filas:
        resultado. append(fila_a_dict(fila))
    return jsonify(resultado), 200

@app.route('/productos<int:producto_id>',methods=['GET'])
def get_productos(producto_id):
    conexion = get_conn()
    cursor = conexion.cursor()

    cursor.execute('SELECT id, nombre, precio, stock FROM productos WHERE id = %s', (producto_id,))

    fila = cursor.fetchone()

    if fila is None:
        cursor.close()
        conexion.close()
        return jsonify({f'error: el id {producto_id} del producto es incorrecto'}), 404
    
    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 200

@app.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json() or {}

    campos = ('nombre', 'precio', 'stock')

    for campo in campos:
        if datos.get(campo) is None:
            return jsonify({f'error: falta campo {campo} o su valor es none'}), 400
    
    conexion = get_conn()
    cursor = conexion.cursor()
    consulta = """
        INSERT INTO productos(nombre,precio,stock)
        VALUES(%s,%s,%s)
        RETURNING id, nombre, precio, stock;
    """

    resultado = []
    for campo in campos:
        resultado.append(datos[campo])

    cursor.execute(consulta, resultado)
    fila = cursor.fetchone()

