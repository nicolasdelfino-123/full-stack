from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

# ---------------------------
# DB connection
# ---------------------------
def get_connection():
    return psycopg2.connect(
        host='localhost',
        database='nico_fullstack',
        user='postgres',
        password='1234'
    )

# ---------------------------
# Helper
# ---------------------------
def fila_a_dict(fila):
    if fila is None:
        return None

    return {
        "id": fila[0],
        "nombre": fila[1],
        "precio": float(fila[2]),
        "stock": fila[3]
    }

# =========================================================
# GET /productos  → listar todos
# =========================================================
@app.route('/productos', methods=['GET'])
def get_productos():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        'SELECT id, nombre, precio, stock FROM productos;'
    )
    filas = cursor.fetchall()

    cursor.close()
    conexion.close()

    # LOS GUARDO PORQUE SON MUCHAS FILAS
    resultado = []
    for fila in filas:
        resultado.append(fila_a_dict(fila))

    return jsonify(resultado), 200

# =========================================================
# GET /productos/<id>  → obtener uno
# =========================================================
@app.route('/productos/<int:producto_id>', methods=['GET'])
def get_producto_id(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        'SELECT id, nombre, precio, stock FROM productos WHERE id = %s;',
        (producto_id,)
    )
    fila = cursor.fetchone()

    if fila is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': 'producto no encontrado'}), 404

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 200

# =========================================================
# POST /productos  → crear
# =========================================================
@app.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json() or {}

    campos = ('nombre', 'precio', 'stock')

    # validar body
    for campo in campos:
        if datos.get(campo) is None:
            return jsonify({'error': f'falta el {campo} obligatorio'}), 400

    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO productos (nombre, precio, stock)
        VALUES (%s, %s, %s)
        RETURNING id, nombre, precio, stock;
    """

    # los guardo porque es la lista de valores q voy a ejecutar
    valores = []
    for campo in campos:
        valores.append(datos[campo])

    cursor.execute(consulta, valores)
    fila = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 201

# =========================================================
# PUT /productos/<id>  → editar
# =========================================================
@app.route('/productos/<int:producto_id>', methods=['PUT'])
def editar_producto(producto_id):
    datos = request.get_json() or {}

    campos = ('nombre', 'precio', 'stock')

    # validar body
    for campo in campos:
        if datos.get(campo) is None:
            return jsonify({'error': f'falta el {campo} obligatorio'}), 400


    conexion = get_connection()
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
        return jsonify({'error': f'producto con id {producto_id} no encontrado'}), 404

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 200

# =========================================================
# DELETE /productos/<id>  → eliminar
# =========================================================
@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = """
        DELETE FROM productos
        WHERE id = %s
        RETURNING id;
    """

    cursor.execute(consulta, (producto_id,))
    fila = cursor.fetchone()

    if fila is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': f'producto con id {producto_id} no encontrado'}), 404

    conexion.commit()

    cursor.close()
    conexion.close()

    return '', 204

# ---------------------------
# Run
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
