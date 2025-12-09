# -----------------------------------------
# IMPORTS NECESARIOS PARA LEVANTAR LA APP
# -----------------------------------------

from flask import Flask, jsonify        # Flask crea la aplicación web. jsonify convierte datos Python a JSON.
import psycopg2                         # psycopg2 permite conectar Python con una base de datos PostgreSQL.


# =======================================================
# IMPORTS: herramientas que necesitamos para laburar
# =======================================================

from flask import Flask, jsonify        # Flask = el servidor web. jsonify = hablar en JSON.
import psycopg2                         # psycopg2 = la llave para entrar a PostgreSQL.


# =======================================================
# CREAR LA APP (el servidor)
# =======================================================

# Acá básicamente le decimos a Flask:
# "Creá un servidor acá mismo, en este archivo."
# __name__ = nombre del archivo actual.
# Flask necesita saber eso para ubicar rutas, archivos, etc.
app = Flask(__name__)


# =======================================================
# FUNCIÓN PARA CONECTARSE A LA BASE
# =======================================================

def get_db_connection():
    """
    Esta función es LA PUERTA a tu base de datos.

    Cada vez que necesites hablar con Postgres,
    vas a llamar a get_db_connection().

    Devuelve una conexión REAL, viva,
    con la base nico_fullstack.
    """

    # psycopg2.connect abre la puerta hacia la base.
    # Si la contraseña está mal → no entrás.
    conexion_db = psycopg2.connect(
        host="localhost",            # La base está en tu PC.
        database="nico_fullstack",   # Nombre de tu base.
        user="TU_USUARIO",           # Cambiar por tu usuario (ej: postgres o nico).
        password="TU_PASSWORD"       # Tu contraseña real.
    )

    return conexion_db               # Te entrega la conexión viva.



  # -----------------------------------------
# RUTA PARA OBTENER TODOS LOS PRODUCTOS
# -----------------------------------------

# @app.route('/productos')
# Esto significa: "Flask, cuando alguien escriba en el navegador
# http://localhost:5000/productos ... corré la función obtener_productos()".
@app.route('/productos')
def obtener_productos():
    """
    Esta función es lo que se ejecuta cuando visitan /productos.

    TRADUCCIÓN DEL FLUJO PASO A PASO:

    1. "Necesito hablar con la base" → abro una conexión.
    2. "Necesito ejecutar SQL" → creo un cursor.
    3. "Quiero traer todos los productos" → hago SELECT.
    4. "Dame todo lo que encontraste" → fetchall().
    5. "Listo, ya leí todo" → cierro cursor y conexión.
    6. "Tengo tuplas (1, 'Lapicera', etc.)" → las convierto a diccionarios.
    7. "El frontend no entiende Python, entiende JSON" → jsonify().
    """
    """  Esta ruta devuelve la lista completa de productos en formato JSON.

    FLUJO DE ESTA FUNCIÓN:
    1. Abrimos conexión con la base.
    2. Creamos un cursor (objeto que ejecuta SQL).
    3. Ejecutamos SELECT para traer datos de la tabla.
    4. Leemos los resultados.
    5. Cerramos cursor y conexión.
    6. Convertimos los resultados SQL (tuplas) a diccionarios Python.
    7. Flask convierte esa lista a JSON y la devuelve al usuario.
    """

    # 1. Conectarse a la base
    # Pensalo así: "tocamos timbre" en la base y nos abre la puerta.
    conexion_db = get_db_connection()

    # 2. Crear cursor para ejecutar SQL
    # El cursor es la persona que entra a la base y ejecuta la consulta que vos le das.
    cursor_db = conexion_db.cursor()

    # 3. Consulta SQL para traer todos los productos
    # Este es EL MENSAJE que le damos al cursor para que vaya a la base
    # y diga: "Che Postgres, dame todas las filas de la tabla productos".
    consulta_sql = 'SELECT id, nombre, precio, stock FROM productos;'

    # ACRIOLLADO:
    # Esto es como decirle al cursor:
    # "Andá a la base y ejecutá este texto tal cual".
    cursor_db.execute(consulta_sql)

    # 4. Obtener todas las filas devueltas por la consulta
    # fetchall() significa:
    # "Traeme TODO lo que devolvió ese SELECT".
    # Lo que vuelve es una lista de tuplas:
    # [(1, 'Lapicera', Decimal('150.00'), 80), (...), ...]
    resultados_sql = cursor_db.fetchall()

    # 5. Cerrar cursor y conexión
    # ACRIOLLADO IMPORTANTE:
    # Cerramos porque:
    # - Si dejamos esto abierto, la base queda ocupada.
    # - En sistemas reales eso rompe todo.
    cursor_db.close()
    conexion_db.close()

    # 6. Convertir cada fila en un diccionario para JSON
    # Acá transformamos tuplas en dicts para que el frontend pueda entenderlo.
    # El navegador NO sabe leer tuplas de Python.
    lista_productos = []
    for fila in resultados_sql:

        # ACRIOLLADO:
        # fila[0] → id
        # fila[1] → nombre
        # fila[2] → precio (viene como Decimal)
        # fila[3] → stock
        # Hacemos float porque JSON no entiende Decimal.
        producto = {
            "id": fila[0],
            "nombre": fila[1],
            "precio": float(fila[2]),
            "stock": fila[3]
        }

        # Agregamos el diccionario a la lista final de productos.
        lista_productos.append(producto)

    # 7. Devolver la lista completa en formato JSON
    # jsonify toma tu lista de dicts y la convierte en JSON real.
    # Al frontend le va a llegar algo así:
    # [
    #   {"id":1,"nombre":"Lapicera","precio":150.0,"stock":80},
    #   ...
    # ]
    return jsonify(lista_productos)




# -----------------------------------------
# ARRANCAR EL SERVIDOR FLASK
# -----------------------------------------

if __name__ == '__main__':
    """
    Este bloque se ejecuta SOLO cuando corrés este archivo directamente:
        python app.py

    ¿Qué hace app.run(debug=True)?
    - Arranca el servidor web Flask.
    - Levanta la aplicación en http://localhost:5000
    - Deja la app escuchando peticiones.
    - debug=True:
        * recarga la app automáticamente cuando guardás cambios
        * muestra errores detallados para facilitar el aprendizaje
    """
    app.run(debug=True)
