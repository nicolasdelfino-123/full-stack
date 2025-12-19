@app.route('/productos', methods=['POST'])
def crear_producto():
    datos = request.get_json()
    
    campos = ('nombre','precio','stock')

    for campo in campos:
        if datos.get(campo) is None:
            return jsonify({'error': f'falta el {campo} obligatorio'}), 400
    
    conexion = get_conn()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO productos(nombre,precio,stock)
        VALUES(%s,%s,%s)
        RETURNING id, nombre, precio, stock;
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
