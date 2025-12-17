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


🧩 DÍA 2 – app.py ultra explicado (CRUD completo)
⚠️ Solo tenés que cambiar TU_USUARIO y TU_PASSWORD.
El resto lo podés copiar tal cual para practicar.
# ============================================================
# app.py — Backend mínimo REAL con Flask + PostgreSQL
# Día 2: CRUD COMPLETO en un solo archivo (versión "fea" pero clara)
# ============================================================

# -----------------------------------------
# 1) IMPORTS NECESARIOS
# -----------------------------------------

# Flask: framework para crear servidores web en Python.
# jsonify: función que convierte estructuras de Python (listas, dicts)
#          a JSON para poder enviarlas al navegador/cliente.
# request: objeto que representa la petición HTTP que hace el cliente
#          (acá leemos el body JSON que nos manda, por ejemplo en POST/PUT).
from flask import Flask, jsonify, request

# psycopg2: librería que permite a Python conectarse a una base de datos PostgreSQL.
import psycopg2


# -----------------------------------------
# 2) CREAR LA APLICACIÓN FLASK
# -----------------------------------------

# app = Flask(__name__)
# - Creamos una instancia de la aplicación Flask.
# - __name__ le indica a Flask en qué módulo (archivo) está la app.
#   Se usa internamente para ubicar recursos, rutas, etc.
app = Flask(__name__)


# -----------------------------------------
# 3) FUNCIÓN AUXILIAR: CONECTAR A LA BASE DE DATOS
# -----------------------------------------

def get_db_connection():
    """
    Crea y devuelve una CONEXIÓN NUEVA a la base de datos PostgreSQL.

    Esta función:
    - Usa psycopg2.connect(...)
    - Devuelve un objeto "connection".
    - No ejecuta SQL todavía, solo abre la puerta a la DB.

    La idea es:
    SIEMPRE que necesitemos hablar con la DB,
    llamamos a get_db_connection() y luego creamos un cursor.
    """

    # psycopg2.connect recibe varios argumentos con nombre:
    # - host: dónde está la DB (acá 'localhost' = tu propia PC).
    # - database: nombre de la base de datos que creaste (nico_fullstack).
    # - user: tu usuario de PostgreSQL (ej: postgres).
    # - password: la contraseña de ese usuario.
    conexion_db = psycopg2.connect(
        host="localhost",
        database="nico_fullstack",
        user="TU_USUARIO",        # <-- CAMBIAR por tu usuario real
        password="TU_PASSWORD"    # <-- CAMBIAR por tu contraseña real
    )

    # Devolvemos el objeto conexión al que nos conectamos recién.
    return conexion_db


# -----------------------------------------
# 4) FUNCIÓN AUXILIAR: CONVERTIR UNA FILA A DICCIONARIO
# -----------------------------------------

def fila_a_producto_dict(fila):
    """
    Recibe una 'fila' (row) devuelta por la DB y la convierte en un dict.

    - Cuando ejecutamos cursor.fetchall() o cursor.fetchone(),
      psycopg2 nos devuelve tuplas, por ejemplo:
      (1, 'Lapicera', Decimal('150.00'), 80)

    - Para trabajar cómodo en Python y para convertir a JSON,
      es mejor tener un diccionario:
      {
        "id": 1,
        "nombre": "Lapicera",
        "precio": 150.0,
        "stock": 80
      }

    Esta función hace esa transformación.
    """

    # Si fila es None, significa que no se encontró nada (ej: producto inexistente).
    if fila is None:
        return None

    # fila[0] corresponde a la columna id
    # fila[1] corresponde a la columna nombre
    # fila[2] corresponde a la columna precio (NUMERIC en Postgres -> Decimal en Python)
    # fila[3] corresponde a la columna stock
    producto = {
        "id": fila[0],
        "nombre": fila[1],
        # Convertimos el valor numérico de la DB a float
        # porque JSON no sabe qué es Decimal, pero sí entiende float.
        "precio": float(fila[2]),
        "stock": fila[3]
    }

    return producto


# ============================================================
# 5) RUTAS CRUD PARA /productos
# ============================================================

# -------------------------------------------------------------------
# GET /productos  → LISTAR TODOS LOS PRODUCTOS
# -------------------------------------------------------------------

# @app.route('/productos', methods=['GET'])
# - Este decorador registra una ruta en Flask.
# - '/productos' es el path de la URL.
# - methods=['GET'] indica que esta función responde a peticiones GET.
@app.route('/productos', methods=['GET'])
def obtener_todos_los_productos():
    """
    Devuelve la lista completa de productos en formato JSON.

    Flujo:
    1. Abrimos conexión a la DB.
    2. Creamos cursor.
    3. Ejecutamos SELECT.
    4. Traemos todas las filas.
    5. Cerramos cursor y conexión.
    6. Convertimos cada fila a dict.
    7. Devolvemos lista de productos como JSON.
    """

    # 1) Abrir conexión a la base.
    conexion_db = get_db_connection()

    # 2) Crear cursor.
    #    El cursor es el objeto que ejecuta las consultas SQL.
    cursor_db = conexion_db.cursor()

    # 3) Escribir la consulta SQL.
    #    Ojo: esto es un string normal de Python.
    consulta_sql = 'SELECT id, nombre, precio, stock FROM productos;'

    # 4) Ejecutar la consulta.
    #    - Usamos cursor_db.execute(consulta_sql)
    #    - No pasamos parámetros porque esta consulta no tiene WHERE.
    cursor_db.execute(consulta_sql)

    # 5) Traer TODAS las filas con fetchall().
    #    - filas será una lista de tuplas.
    #      Ej: [(1, 'Lapicera', Decimal('150.00'), 80), (...), ...]
    filas = cursor_db.fetchall()

    # 6) Cerrar cursor y conexión para no dejar recursos abiertos.
    cursor_db.close()
    conexion_db.close()

    # 7) Convertir cada tupla a diccionario usando la función auxiliar.
    lista_productos = []
    for fila in filas:
        producto_dict = fila_a_producto_dict(fila)  # convertimos fila -> dict
        lista_productos.append(producto_dict)       # lo agregamos a la lista

    # 8) Devolver lista como JSON.
    #    - jsonify(lista_productos) convierte la lista de dicts a JSON.
    #    - 200 es el código de estado HTTP (OK).
    return jsonify(lista_productos), 200


# -------------------------------------------------------------------
# GET /productos/<id>  → OBTENER UN PRODUCTO POR ID
# -------------------------------------------------------------------

# @app.route('/productos/<int:producto_id>', methods=['GET'])
# - '<int:producto_id>' significa que:
#   * Flask espera un entero en esa parte de la URL.
#   * Lo convierte a int automáticamente.
#   * Lo pasa como argumento a la función obtener_producto_por_id.
@app.route('/productos/<int:producto_id>', methods=['GET'])
def obtener_producto_por_id(producto_id):
    """
    Devuelve un solo producto según su id.
    Si no existe, devuelve error 404.

    Ejemplo:
    GET /productos/3
    """

    # 1) Abrir conexión y cursor.
    conexion_db = get_db_connection()
    cursor_db = conexion_db.cursor()

    # 2) Armar consulta SQL con un placeholder %s.
    #    IMPORTANTE:
    #      - %s acá NO es comodín.
    #      - Es un "placeholder" para psycopg2.
    #      - El valor real va en la segunda parte de cursor.execute().
    consulta_sql = 'SELECT id, nombre, precio, stock FROM productos WHERE id = %s;'

    # 3) Ejecutar la consulta con parámetro.
    #    cursor_db.execute(consulta_sql, (producto_id,))
    #    - Primer argumento: el string SQL.
    #    - Segundo argumento: una tupla con los valores para cada %s.
    #    En este caso, hay un solo %s, por eso la tupla tiene un solo elemento.
    #    OJO: (producto_id,) con coma -> eso lo convierte en tupla de 1 elemento.
    cursor_db.execute(consulta_sql, (producto_id,))

    # 4) Traer UNA sola fila con fetchone().
    #    - Si existe un producto con ese id, devuelve una tupla.
    #    - Si no existe, devuelve None.
    fila = cursor_db.fetchone()

    # 5) Cerrar cursor y conexión.
    cursor_db.close()
    conexion_db.close()

    # 6) Verificar si se encontró algo.
    if fila is None:
        # No se encontró producto con ese id.
        # Devolvemos JSON con error y código 404.
        return jsonify({"error": "Producto no encontrado"}), 404

    # 7) Convertir la fila a dict.
    producto_dict = fila_a_producto_dict(fila)

    # 8) Devolver el producto como JSON.
    return jsonify(producto_dict), 200


# -------------------------------------------------------------------
# POST /productos  → CREAR UN NUEVO PRODUCTO
# -------------------------------------------------------------------

@app.route('/productos', methods=['POST'])
def crear_producto():
    """
    Crea un nuevo producto en la base.

    Espera un JSON en el body de la petición, por ejemplo:
    {
        "nombre": "Lapicera azul",
        "precio": 150.0,
        "stock": 80
    }
    """

    # 1) Leer el body JSON que manda el cliente.
    #    - request.get_json() lee el cuerpo de la petición HTTP.
    #    - Flask espera que el Content-Type sea application/json.
    # trae el json del frontend y lo convierte a dict
    datos = request.get_json()

    # 2) Extraer los campos del diccionario 'datos'.
    #    - .get("nombre") devuelve el valor de la clave "nombre" o None si no existe.
    nombre = datos.get("nombre")
    precio = datos.get("precio")
    stock = datos.get("stock")

    # 3) Validación mínima:
    #    Verificamos que los 3 campos estén presentes.
    if nombre is None or precio is None or stock is None:
        # Devolvemos error 400 (Bad Request).
        return jsonify({"error": "Faltan campos obligatorios: nombre, precio, stock"}), 400

    # 4) Abrimos conexión y cursor.
    conexion_db = get_db_connection()
    cursor_db = conexion_db.cursor()

    # 5) Escribimos la consulta INSERT con placeholders %s.
    #    - RETURNING id, nombre, precio, stock:
    #      hace que Postgres devuelva la fila recién insertada.
    consulta_sql = """
        INSERT INTO productos (nombre, precio, stock)
        VALUES (%s, %s, %s)
        RETURNING id, nombre, precio, stock;
    """

    # 6) Ejecutamos el INSERT.
    #    Segundo argumento: tupla con (nombre, precio, stock)
    cursor_db.execute(consulta_sql, (nombre, precio, stock))

    # 7) Obtenemos la fila que Postgres devolvió gracias al RETURNING.
    fila_nueva = cursor_db.fetchone()

    # 8) Confirmamos los cambios con commit().
    #    - Hasta que no hacemos commit(), los cambios no se guardan en la DB.
    conexion_db.commit()

    # 9) Cerramos cursor y conexión.
    cursor_db.close()
    conexion_db.close()

    # 10) Convertimos la fila nueva a dict.
    producto_creado = fila_a_producto_dict(fila_nueva)

    # 11) Devolvemos el producto creado con código 201 (Created).
    return jsonify(producto_creado), 201


# -------------------------------------------------------------------
# PUT /productos/<id>  → ACTUALIZAR UN PRODUCTO EXISTENTE
# -------------------------------------------------------------------

@app.route('/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    """
    Actualiza un producto existente según su id.

    Espera un JSON como:
    {
        "nombre": "Nuevo nombre",
        "precio": 999.99,
        "stock": 10
    }

    Flujo:
    1. Leer JSON y extraer los datos.
    2. Verificar que el producto exista.
    3. Si no existe -> 404.
    4. Si existe -> UPDATE con nuevos valores.
    5. Devolver el producto actualizado.
    """

    # 1) Leer el JSON del body.
    datos = request.get_json()

    nombre = datos.get("nombre")
    precio = datos.get("precio")
    stock = datos.get("stock")

    # 2) Validación mínima de campos.
    if nombre is None or precio is None or stock is None:
        return jsonify({"error": "Faltan campos obligatorios: nombre, precio, stock"}), 400

    # 3) Abrir conexión y cursor.
    conexion_db = get_db_connection()
    cursor_db = conexion_db.cursor()

    # 4) Verificar si el producto existe.
    consulta_existe = 'SELECT id, nombre, precio, stock FROM productos WHERE id = %s;'
    cursor_db.execute(consulta_existe, (producto_id,))
    fila_existente = cursor_db.fetchone()

    if fila_existente is None:
        # Cerramos antes de devolver, para no dejar recursos abiertos.
        cursor_db.close()
        conexion_db.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    # 5) Si existe, hacemos el UPDATE.
    consulta_update = """
        UPDATE productos
        SET nombre = %s,
            precio = %s,
            stock = %s
        WHERE id = %s
        RETURNING id, nombre, precio, stock;
    """

    # 6) Ejecutamos el UPDATE.
    #    Orden de parámetros:
    #      nombre -> primer %s
    #      precio -> segundo %s
    #      stock  -> tercer %s
    #      producto_id -> cuarto %s (el del WHERE id = %s)
    cursor_db.execute(consulta_update, (nombre, precio, stock, producto_id))

    # 7) Obtenemos la fila actualizada gracias al RETURNING.
    fila_actualizada = cursor_db.fetchone()

    # 8) Confirmamos los cambios.
    conexion_db.commit()

    # 9) Cerramos cursor y conexión.
    cursor_db.close()
    conexion_db.close()

    # 10) Convertimos la fila a dict.
    producto_actualizado = fila_a_producto_dict(fila_actualizada)

    # 11) Devolvemos producto actualizado.
    return jsonify(producto_actualizado), 200


# -------------------------------------------------------------------
# DELETE /productos/<id>  → ELIMINAR UN PRODUCTO
# -------------------------------------------------------------------

@app.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    """
    Elimina un producto por id.

    Flujo:
    1. Verificar si el producto existe.
    2. Si no existe -> 404.
    3. Si existe -> DELETE.
    4. Devolver 204 (sin contenido) si se borró correctamente.
    """

    # 1) Abrir conexión y cursor.
    conexion_db = get_db_connection()
    cursor_db = conexion_db.cursor()

    # 2) Verificar existencia.
    consulta_existe = 'SELECT id FROM productos WHERE id = %s;'
    cursor_db.execute(consulta_existe, (producto_id,))
    fila = cursor_db.fetchone()

    if fila is None:
        cursor_db.close()
        conexion_db.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    # 3) Ejecutar el DELETE.
    consulta_delete = 'DELETE FROM productos WHERE id = %s;'
    cursor_db.execute(consulta_delete, (producto_id,))

    # 4) Confirmar cambios.
    conexion_db.commit()

    # 5) Cerrar cursor y conexión.
    cursor_db.close()
    conexion_db.close()

    # 6) 204 No Content = borrado exitoso sin body.
    return '', 204


# ============================================================
# 6) ARRANCAR EL SERVIDOR FLASK
# ============================================================

if __name__ == '__main__':
    """
    Este bloque se ejecuta SOLO cuando corrés:

        python app.py

    app.run(debug=True):
    - Levanta el servidor en http://localhost:5000
    - debug=True:
        * recarga automática al guardar cambios
        * muestra errores con stacktrace detallado
    """
    app.run(debug=True)

Nico, con esto:
    • podés copiar-pegar y probar,
    • y al mismo tiempo usarlo como apunte para leer en frío.
Cuando lo empieces a codear de verdad y en algún lugar sientas:
“pará, acá no entendí qué pasa”,
me pegás ese pedacito puntual y lo destripamos todavía más, si hace falta hasta el nivel de:
    • qué tipo de dato es cada cosa,
    • qué devuelve cada función,
    • cuánto mide cada lista.

🧠 2. Qué hicimos, bien pasito a pasito
Te resumo endpoint por endpoint para que lo leas tranquilo mañana:
    1. GET /productos
        ◦ Conecta a la DB
        ◦ Hace SELECT *
        ◦ Convierte cada fila con fila_a_producto_dict
        ◦ Devuelve lista_productos como JSON
    2. GET /productos/<id>
        ◦ Lee producto_id desde la URL
        ◦ Busca en la DB con WHERE id = %s
        ◦ Si no hay fila → 404
        ◦ Si hay fila → dict → JSON
    3. POST /productos
        ◦ Lee JSON del body (request.get_json())
        ◦ Toma nombre, precio, stock
        ◦ Valida que no sean None
        ◦ INSERT ... RETURNING ...
        ◦ commit()
        ◦ Devuelve el producto creado + 201
    4. PUT /productos/<id>
        ◦ Lee JSON (mismos campos que POST)
        ◦ Verifica que el producto exista
        ◦ Si no existe → 404
        ◦ UPDATE ... RETURNING ...
        ◦ commit()
        ◦ Devuelve producto actualizado
    5. DELETE /productos/<id>
        ◦ Verifica que el producto exista
        ◦ Si no existe → 404
        ◦ DELETE ...
        ◦ commit()
        ◦ Devuelve 204 sin contenido (estándar pro)

🧪 3. Próximo paso (cuando te sientes a codear)
Cuando tengas ganas de hacerlo:
    1. Copiá este app.py
    2. Ajustá user y password
    3. Probá cada endpoint con Postman:
    • GET http://localhost:5000/productos
    • GET http://localhost:5000/productos/1
    • POST http://localhost:5000/productos con JSON
    • PUT http://localhost:5000/productos/1
    • DELETE http://localhost:5000/productos/1


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
