from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host='localhost',
        database='nico_db',
        user='nico',
        password='1234'
    )

# HELPER

def fila_a_dict(fila):
    if fila is None:
        return None
    
    producto = {
        "id": fila[0],
        "nombre": fila[1],
        "email": fila[2],
        "telefono": fila[3]
    }

    return producto

@app.ruote('/clientes',methods=['GET'])
def get_clientes():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        'SELECT id, nombre, email, telefono FROM productos;'
    )

    filas = cursor.fetchall()

    cursor.close()
    conexion.close()
    
    resultado = []
    for fila in filas:
        resultado.append(fila_a_dict(fila))
    return jsonify(resultado), 200

@app.route('/clientes/<int:producto_id>',methods=['GET'])
def get_id(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        'SELECT id, nombre, email, telefono FROM productos WHERE id = %s',
        (producto_id,)
    )

    fila = cursor.fetchone()

    if fila is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': f'el producto con id {producto_id} no existe'}), 404
    
    cursor.close()
    conexion.close()

    """
        primer error escribi esto de mas es un solo resultado no hace falta 
    resultado = []
    for traido in fila:
        resultado.append(fila_a_dict(traido)) """
    return jsonify(fila_a_dict(fila)), 200

@app.ruote('/clientes',methods=['POST'])
def crear_producto():
    datos = request.get_json() or {} # me faltaba el or {}

    campos = ('nombre','email','telefono')

    for campo in campos:
        if datos.get(campo) is None:
            return jsonify({'error': f'falta el campo {campo} obligatorio'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO clientes(nombre, email, telefono)
        VALUES(%s,%s,%s)
        RETURNING id, nombre, email, telefono;
    """ 

    # hice esto: cursor.execute(consulta,(nombre, email, telefono)) y va esto
    # me olvide esta parte
    valores = []

    for campo in campos:
        valores.append(datos[campo])
    
    cursor.execute(consulta, valores)

    fila = cursor.fetchone()

    #me faltó el commit
    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 201

@app.route('/clientes/<int:producto_id>',methods=['PUT'])
def editar_producto(producto_id):
    datos = request.get_json() or {}

    campos = ('nombre','email','telefono')

    for campo in campos:
        if datos.get(campo) is None:
            return jsonify({'error': f'falta campo {campo} obligatorio'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()
    
    #OTRO ERROR PUSE INSERT EN VEZ DE UPDATE
    consulta = """
        UPDATE clientes
        SET nombre = %s,
            email = %s,
            telefono = %s
        WHERE id = %s
        RETURNING id, nombre, email, telefono;
    """

    valor = []
    for campo in campos:
        valor.append(datos[campo])

    cursor.execute(
        consulta,
        (*valor, producto_id)
    )

    # ubiqué esto muy por abajo
    resultado = cursor.fetchone()

    # me faltó esta validacion
    if resultado is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': f'producto con id {producto_id} no encontrado'}), 404
    
    # me falto el commit
    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(resultado)), 200

@app.route('/clientes/<int:producto_id>',methods=['DELETE'])
def eliminar_producto(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    #error retorné todo y era solo retornar id y ademas no pasé producto_id
    cursor.execute("""DELETE FROM clientes 
                      WHERE id = %s 
                      RETURNING id;
                   """, (producto_id,))
    
    fila = cursor.fetchone()

    if fila is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': f'no existe el producto id {id}'}), 404


    conexion.commit()

    cursor.close()
    conexion.close()

    return '', 204

    