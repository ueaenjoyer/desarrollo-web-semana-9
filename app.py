# ============================================
# IMPORTACIONES
# ============================================

# Flask: El framework web principal que usamos para crear la aplicación
from flask import Flask, render_template, request, redirect, url_for, flash

# render_template: Renderiza plantillas HTML con Jinja2
# request: Accede a los datos enviados por el usuario (formularios, parámetros)
# redirect: Redirige al usuario a otra ruta
# url_for: Genera URLs a partir del nombre de la función
# flash: Muestra mensajes temporales al usuario (éxito, error, etc.)

import os  # Para construir la ruta absoluta al archivo de base de datos

# Importamos las clases POO del módulo models.py (Semana 11)
from models import Producto, Inventario, DatabaseManager

# Importamos el Blueprint de persistencia (Semana 12)
# Un Blueprint es un conjunto de rutas que se registra en la aplicación
from inventario.inventario import datos_bp

# Importamos la instancia de SQLAlchemy y la función de inicialización
from inventario.bd import db, init_app as init_sqlalchemy


# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================

# Creamos la instancia de la aplicación Flask
# __name__ le dice a Flask dónde buscar recursos (templates, static, etc.)
app = Flask(__name__)

# Clave secreta necesaria para usar flash messages
app.secret_key = "techbyte_semana12_secret_key"

# ============================================
# CONFIGURACIÓN SQLALCHEMY (Semana 12)
# Conecta Flask con SQLite usando el ORM SQLAlchemy
# ============================================
# Ruta absoluta al archivo de base de datos SQLite
# Se guarda en la misma carpeta del proyecto para facilitar su gestión
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'tiendagadget.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Ahorra memoria desactivando el tracking

# Registramos el Blueprint de datos con todas sus rutas (/datos/...)
# El Blueprint agrupa las rutas de persistencia en un módulo separado
app.register_blueprint(datos_bp)

# Inicializamos SQLAlchemy con la app y creamos las tablas del ORM
init_sqlalchemy(app)

# Inicializamos la base de datos SQLite (Semana 11) y el inventario con POO
db_manager = DatabaseManager()
inventario = Inventario(db_manager)


# ============================================
# RUTAS ORIGINALES (Semanas 9, 10, 11)
# ============================================

@app.route("/")  # Decorador que asocia la URL "/" con la función index()
def index():
    """
    Página principal de TechByte - Tienda de Gadgets.
    Renderiza la plantilla index.html.
    """
    return render_template("index.html")


@app.route("/about")  # Ruta para la página "Acerca de"
def about():
    """
    Página "Acerca de" - Información sobre TechByte.
    Renderiza la plantilla about.html.
    """
    return render_template("about.html")


@app.route("/productos")  # Ruta para el catálogo de productos
def productos():
    """
    Página de Productos - Catálogo completo de gadgets.

    SEMANA 11: Ahora consulta la base de datos SQLite para obtener
    los productos reales y los pasa a la plantilla usando una LISTA.
    La plantilla usa {% for %} de Jinja2 para renderizar cada producto.
    """
    # Obtenemos todos los productos desde el DICCIONARIO del inventario
    # mostrar_todos() retorna una LISTA de diccionarios
    lista_productos = inventario.mostrar_todos()

    # Pasamos la LISTA a la plantilla para renderizado dinámico
    return render_template("productos.html", productos=lista_productos)


@app.route("/contacto")  # Ruta para la página de contacto
def contacto():
    """
    Página de Contacto - Información de contacto y formulario.
    Renderiza la plantilla contacto.html.
    """
    return render_template("contacto.html")


# ============================================
# RUTAS CRUD DEL INVENTARIO (Semana 11)
# Implementan operaciones CRUD conectadas a SQLite
# ============================================

@app.route("/inventario")
def inventario_lista():
    """
    Muestra todos los productos del inventario en una tabla HTML.

    Usa el método mostrar_todos() de la clase Inventario que retorna
    una LISTA de diccionarios. Cada diccionario contiene los datos
    de un producto obtenidos desde SQLite.
    """
    # Recargamos datos desde la DB para asegurar consistencia
    inventario.recargar()

    # Obtenemos la LISTA de todos los productos
    productos_lista = inventario.mostrar_todos()

    # Pasamos la TUPLA de categorías para filtros en la plantilla
    categorias = Producto.CATEGORIAS_VALIDAS

    return render_template("inventario.html",
                           productos=productos_lista,
                           categorias=categorias)


@app.route("/inventario/agregar", methods=["GET", "POST"])
def inventario_agregar():
    """
    Formulario para agregar un nuevo producto.

    GET: Muestra el formulario vacío.
    POST: Procesa los datos del formulario y agrega el producto
          a la base de datos SQLite usando el método agregar() de Inventario.
    """
    if request.method == "POST":
        # Obtenemos los datos del formulario (request.form es un diccionario)
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "Otros")
        precio = request.form.get("precio", 0)
        cantidad = request.form.get("cantidad", 0)
        descripcion = request.form.get("descripcion", "").strip()

        # Validaciones básicas
        if not nombre:
            flash("❌ El nombre del producto es obligatorio.", "error")
            return render_template("inventario_form.html",
                                   categorias=Producto.CATEGORIAS_VALIDAS,
                                   accion="Agregar")

        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except ValueError:
            flash("❌ Precio o cantidad inválidos.", "error")
            return render_template("inventario_form.html",
                                   categorias=Producto.CATEGORIAS_VALIDAS,
                                   accion="Agregar")

        # Usamos el método agregar() de la clase Inventario
        # Internamente guarda en el DICCIONARIO, CONJUNTO y SQLite
        producto = inventario.agregar(nombre, categoria, precio, cantidad, descripcion)

        flash(f"✅ Producto '{producto.nombre}' agregado con éxito (ID: {producto.id}).", "success")
        return redirect(url_for("inventario_lista"))

    # GET: Mostramos el formulario vacío
    return render_template("inventario_form.html",
                           categorias=Producto.CATEGORIAS_VALIDAS,
                           accion="Agregar")


@app.route("/inventario/editar/<int:id>", methods=["GET", "POST"])
def inventario_editar(id):
    """
    Formulario para editar un producto existente.

    GET: Muestra el formulario con los datos actuales del producto.
    POST: Procesa los datos actualizados y los guarda en SQLite.

    Usa búsqueda O(1) en el DICCIONARIO del inventario por ID.
    """
    # Buscamos el producto en el DICCIONARIO (O(1))
    producto = inventario.obtener_por_id(id)

    if not producto:
        flash(f"❌ No se encontró producto con ID {id}.", "error")
        return redirect(url_for("inventario_lista"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        categoria = request.form.get("categoria", "Otros")
        precio = request.form.get("precio", 0)
        cantidad = request.form.get("cantidad", 0)
        descripcion = request.form.get("descripcion", "").strip()

        if not nombre:
            flash("❌ El nombre del producto es obligatorio.", "error")
            return render_template("inventario_form.html",
                                   categorias=Producto.CATEGORIAS_VALIDAS,
                                   producto=producto,
                                   accion="Editar")

        try:
            precio = float(precio)
            cantidad = int(cantidad)
        except ValueError:
            flash("❌ Precio o cantidad inválidos.", "error")
            return render_template("inventario_form.html",
                                   categorias=Producto.CATEGORIAS_VALIDAS,
                                   producto=producto,
                                   accion="Editar")

        # Actualizamos usando el método de la clase Inventario
        # Sincroniza DICCIONARIO en memoria + SQLite
        if inventario.actualizar(id, nombre, categoria, precio, cantidad, descripcion):
            flash(f"✅ Producto '{nombre}' actualizado correctamente.", "success")
        else:
            flash("❌ Error al actualizar el producto.", "error")

        return redirect(url_for("inventario_lista"))

    # GET: Mostramos el formulario con datos ya cargados
    return render_template("inventario_form.html",
                           categorias=Producto.CATEGORIAS_VALIDAS,
                           producto=producto,
                           accion="Editar")


@app.route("/inventario/eliminar/<int:id>", methods=["POST"])
def inventario_eliminar(id):
    """
    Elimina un producto del inventario y de la base de datos SQLite.

    Solo acepta método POST por seguridad (evita eliminaciones accidentales por URL).
    Usa el método eliminar() de Inventario que remueve del
    DICCIONARIO, CONJUNTO e SQLite.
    """
    producto = inventario.obtener_por_id(id)
    nombre_producto = producto["nombre"] if producto else f"ID {id}"

    # Eliminamos del DICCIONARIO, CONJUNTO y SQLite
    if inventario.eliminar(id):
        flash(f"✅ Producto '{nombre_producto}' eliminado correctamente.", "success")
    else:
        flash(f"❌ No se pudo eliminar el producto con ID {id}.", "error")

    return redirect(url_for("inventario_lista"))


@app.route("/inventario/buscar")
def inventario_buscar():
    """
    Busca productos por nombre.

    Toma el parámetro 'q' de la URL (?q=término) y busca en la base
    de datos usando LIKE de SQL. Retorna una LISTA de resultados.
    """
    termino = request.args.get("q", "").strip()
    resultados = []

    if termino:
        # buscar_por_nombre() retorna una LISTA de diccionarios
        resultados = inventario.buscar_por_nombre(termino)

    return render_template("inventario.html",
                           productos=resultados,
                           categorias=Producto.CATEGORIAS_VALIDAS,
                           busqueda=termino)


# ============================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ============================================

if __name__ == "__main__":
    """
    Este bloque se ejecuta solo cuando ejecutas este archivo directamente.

    app.run() inicia el servidor de desarrollo de Flask.
    - debug=True: Reinicia automáticamente al cambiar código y muestra errores.
    """
    app.run(debug=True)
