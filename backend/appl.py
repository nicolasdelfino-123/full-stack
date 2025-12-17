
from flask import Flask, jsonify, request



@appl.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()

    nombre = datos.get('nombre')
    precio = datos.get('precio')
    stock = datos.get('stock')

    if nombre in None or precio is None or stock in None:
        return jsonify({'error': 'faltan campos obligatorios'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()
    
    consulta = """
            INSERT INTO productos(nombre,precio,stock)
            VALUES(%s,%s,%s)
            RETURNING id, nombre, precio, stock;
            """ 
    cursor.execute(consulta,(nombre,precio,stock))

    fila = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila)), 201

@app.rout('/productos<int: producto_id>', methods=['PUT'])
def editar_producto(producto_id):
    datos = request.get_json()

    nombre = datos.get('nombre')
    precio = datos.get('precio')
    stock = datos.get('stock')

    if nombre is None or precio is None or stock is None:
        return jsonify({'error': 'faltan datos obligatorios'}), 400
    
    cursor = get_connection()
    conexion = conexion.cursor()

    consulta = 'SELECT id FROM productos WHERE id = %s;'

    cursor.execute(consulta,(producto_id,))

    fila_existe = cursor.fetchone()

    if fila_existe is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': 'no existe el producto con ese id'}),404
    
    consulta_update = """
            UPDATE productos
            SET nombre = %s
                precio = %s
                stock = %s
            FROM productos
            WHERE id = %s;
            """ 
    cursor.execute(consulta_update,(nombre, precio, stock, producto_id))

    fila_update = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila_update)), 200