@app3.route('/productos<int:producto_id>', methods=['PUT'])
def editar_producto(producto_id):
    datos = request.get_json()

    campos = ('nombre', 'precio', 'stock')

    if any(datos.get(campo) is None for campo in campos):
        return jsonify({'error': 'faltan campos obligatorios'}), 400

    
    conexion = get_connection()
    cursor = conexion.cursor()

    consulta_existe = 'SELECT id, nombre, stock, precio FROM productos WHERE id = %s;'

    cursor.execute(consulta_existe,(producto_id,))

    fila_existe = cursor.fetchone()

    conexion.commit()

    if fila_existe is None:
        cursor.close()
        conexion.close()
        return jsonify({'error': 'producto no encontrado'}), 404
    
    consulta_update = """
        UPDATE productos
        SET nombre = %s,
            stock = %s,
            precio = %s
        WHERE id = %s
        RETURNING id, nombre, stock, precio;
        """
    valores = tuple(datos[campo] for campo in campos)

    cursor.execute(
        consulta_update,
        (*valores, producto_id)
    )
    fila_actualizada = cursor.fetchone()

    conexion.commit()

    cursor.close()
    conexion.close()

    return jsonify(fila_a_dict(fila_actualizada)), 200