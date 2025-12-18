from flask import Flask, request, jsonify

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def editar_producto(producto_id):
    datos = request.get_json()

    campos = ('nombre', 'stock', 'precio')

    if any(datos.get(campo) is None for campo in campos):
        return jsonify({'error': 'faltan campos obligatorios'}), 400
    
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta = """
        UPDATE productos
        SET nombre = %s,
            stock = %s,
            precio = %s
        WHERE id = %s
        RETURNING id, nombre, stock, precio;
    """
    valores = []
    for campo in campos:
        valores.append(datos[campo])

    cursor.execute(
            consulta, (*valores, producto_id)
    )

    fila_actualizada = cursor.fetchone()
    
    if fila_actualizada is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': 'producto no encuntrado'}),404