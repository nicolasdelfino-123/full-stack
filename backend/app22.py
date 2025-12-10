from flask import Flask, jsonify
import psycopg2


app = Flask(__name__)


""" def get_db_conection():
    conexion_db = psycopg2.connect(
        host= "localhost",
        database="nico_fullstack",
        user="postgres",
        password="1234"
    )

    return conexion_db """

def get_conection_db():
    conection_db = psycopg2.connect(
        host="localhost",
        database="nico_fullstack",
        user="postgres",
        password="1234"
    )
    return conection_db

@app.route("/productos")
def get_products():
    conexion = get_conection_db()
    cursor = conexion.cursor()

    consulta = 'SELECT id, precio, stock FROM productos;'
    cursor.execute(consulta)

    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    lista = []
    for fila in resultados:
        producto = {
            "id": fila[0],
            "precio": float(fila[1]),
            "stock": fila[2]
        }

        lista.append(producto)
    return jsonify(lista)

if __name__ == '__main__':
    app.run(debug=True)
   

    

    
    

    
    
    #cerrar cursor
    cursor.close()
    # cerrar conexion
    conexion.close()
    
    #covertimos las tuplas que nos dio la consulta a la bd a diccionario
    lista = []
    for fila in resultados:
        producto = {
            "id": fila[0],
            "nombre": fila[1],
            "precio": float(fila[2]),
            "stock": fila[3]
        }

        
        #agregamos el dict a la lista final de productos
        lista.append(producto)
    return jsonify(lista)
    
    
if __name__ == '__main__':
    app.run(debug=True)








