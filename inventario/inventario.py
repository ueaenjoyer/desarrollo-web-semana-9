# ============================================
# inventario.py - Blueprint de Persistencia
# Semana 12 - TechByte
# ============================================
#
# Este módulo define un Blueprint de Flask con las rutas
# para manejar persistencia de datos en 4 formatos:
#   1. Archivos TXT (usando open())
#   2. Archivos JSON (usando librería json)
#   3. Archivos CSV (usando librería csv)
#   4. Base de datos SQLite usando SQLAlchemy (ORM)
#
# Un Blueprint agrupa rutas relacionadas y permite registrarlo
# en la aplicación principal (app.py) con un prefijo de URL.
# ============================================

from flask import Blueprint, render_template, request, redirect, url_for, flash

# Importamos las funciones de persistencia de archivos
from inventario.productos import (
    guardar_txt, leer_txt,
    guardar_json, leer_json,
    guardar_csv, leer_csv
)

# Importamos el modelo SQLAlchemy y la instancia db
from inventario.bd import db, ProductoDB

# Importamos el formulario de validación
from form import DatosForm


# ============================================
# CREACIÓN DEL BLUEPRINT
# 'datos' = nombre del blueprint
# __name__ = módulo actual
# url_prefix = prefijo de URL para todas las rutas del blueprint
# ============================================
datos_bp = Blueprint('datos', __name__, url_prefix='/datos')


# ============================================
# RUTA PRINCIPAL - Ver todos los datos
# GET /datos → Muestra datos de los 4 formatos
# POST /datos → Guarda nuevos datos en los 4 formatos
# ============================================

@datos_bp.route('/', methods=['GET', 'POST'])
def datos_index():
    """
    Ruta principal de persistencia de datos.

    GET: Lee datos de TXT, JSON, CSV y SQLAlchemy y los muestra en datos.html.
    POST: Procesa el formulario y guarda los datos en los 4 formatos.
    """
    if request.method == 'POST':
        # Usamos la clase DatosForm para extraer y validar los datos
        formulario = DatosForm.desde_request(request.form)

        if not formulario.es_valido():
            # Si hay errores, mostramos mensajes flash
            for error in formulario.errores:
                flash(error, 'error')
        else:
            datos = formulario.to_dict()

            # 1. Guardar en TXT usando open()
            guardar_txt(datos)

            # 2. Guardar en JSON usando librería json
            guardar_json(datos)

            # 3. Guardar en CSV usando librería csv
            guardar_csv(datos)

            # 4. Guardar en SQLite usando SQLAlchemy ORM
            nuevo_producto = ProductoDB(
                nombre=datos['nombre'],
                precio=datos['precio'],
                cantidad=datos['cantidad'],
                descripcion=datos['descripcion']
            )
            db.session.add(nuevo_producto)    # Agrega a la sesión
            db.session.commit()               # Confirma los cambios en la DB

            flash(f"✅ Datos de '{datos['nombre']}' guardados en TXT, JSON, CSV y SQLAlchemy.", 'success')
            return redirect(url_for('datos.datos_index'))

    # Leemos los datos almacenados en cada formato para mostrarlos
    datos_txt  = leer_txt()
    datos_json = leer_json()
    datos_csv  = leer_csv()
    # SQLAlchemy: consulta todos los registros ordenados por ID
    datos_sqlalchemy = ProductoDB.query.order_by(ProductoDB.id).all()

    return render_template('datos.html',
                           datos_txt=datos_txt,
                           datos_json=datos_json,
                           datos_csv=datos_csv,
                           datos_sqlalchemy=datos_sqlalchemy)


# ============================================
# RUTAS CRUD PARA SQLALCHEMY
# ============================================

@datos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_dato(id):
    """
    Edita un registro de SQLAlchemy por ID.

    GET: Muestra formulario con datos actuales.
    POST: Actualiza el registro en la base de datos.

    Args:
        id (int): ID del registro a editar.
    """
    # Buscar el producto o retornar 404 si no existe
    producto = ProductoDB.query.get_or_404(id)

    if request.method == 'POST':
        formulario = DatosForm.desde_request(request.form)

        if not formulario.es_valido():
            for error in formulario.errores:
                flash(error, 'error')
        else:
            # Actualizamos los atributos del objeto SQLAlchemy
            producto.nombre = formulario.nombre
            producto.precio = formulario.precio
            producto.cantidad = formulario.cantidad
            producto.descripcion = formulario.descripcion
            db.session.commit()  # Guardamos los cambios

            flash(f"✅ Registro '{producto.nombre}' actualizado correctamente.", 'success')
            return redirect(url_for('datos.datos_index'))

    return render_template('datos_form.html', producto=producto, accion='Editar')


@datos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_dato(id):
    """
    Elimina un registro de SQLAlchemy por ID.
    Solo acepta método POST por seguridad.

    Args:
        id (int): ID del registro a eliminar.
    """
    producto = ProductoDB.query.get_or_404(id)
    nombre = producto.nombre
    db.session.delete(producto)  # Marca para eliminación
    db.session.commit()          # Confirma la eliminación

    flash(f"✅ Registro '{nombre}' eliminado de la base de datos.", 'success')
    return redirect(url_for('datos.datos_index'))
