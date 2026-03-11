# ============================================
# usuarios.py - Blueprint de Gestión de Usuarios
# Semana 13 - TechByte
# ============================================
#
# Este módulo define un Blueprint de Flask con las rutas
# para manejar el CRUD completo de usuarios:
#   - Listar usuarios
#   - Agregar nuevo usuario
#   - Editar usuario existente
#   - Eliminar usuario
#
# La tabla usuarios tiene: id_usuario, nombre, mail, password
# ============================================

from flask import Blueprint, render_template, request, redirect, url_for, flash

# Creamos el Blueprint de usuarios
# url_prefix = '/usuarios' → todas las rutas empiezan con /usuarios
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Variable global para el db_manager (se inicializa desde app.py)
_db_manager = None


def init_usuarios(db_manager):
    """
    Inicializa el módulo de usuarios con el DatabaseManager.
    Se llama desde app.py después de crear el db_manager.

    Args:
        db_manager (DatabaseManager): Instancia del gestor de base de datos.
    """
    global _db_manager
    _db_manager = db_manager


# ============================================
# RUTA: LISTAR USUARIOS
# GET /usuarios → Muestra todos los usuarios en una tabla
# ============================================

@usuarios_bp.route('/')
def usuarios_lista():
    """
    Muestra todos los usuarios registrados en una tabla HTML.
    Consulta la tabla 'usuarios' en PostgreSQL (Supabase).
    """
    usuarios = _db_manager.obtener_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)


# ============================================
# RUTA: AGREGAR USUARIO
# GET /usuarios/agregar → Muestra formulario vacío
# POST /usuarios/agregar → Procesa y guarda nuevo usuario
# ============================================

@usuarios_bp.route('/agregar', methods=['GET', 'POST'])
def usuarios_agregar():
    """
    Formulario para agregar un nuevo usuario.

    GET: Muestra el formulario vacío.
    POST: Valida los datos y los inserta en la base de datos.
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        mail = request.form.get('mail', '').strip()
        password = request.form.get('password', '').strip()

        # Validaciones básicas
        if not nombre:
            flash('❌ El nombre es obligatorio.', 'error')
            return render_template('usuarios_form.html', accion='Agregar')

        if not mail:
            flash('❌ El correo electrónico es obligatorio.', 'error')
            return render_template('usuarios_form.html', accion='Agregar')

        if not password:
            flash('❌ La contraseña es obligatoria.', 'error')
            return render_template('usuarios_form.html', accion='Agregar')

        try:
            usuario_id = _db_manager.insertar_usuario(nombre, mail, password)
            flash(f"✅ Usuario '{nombre}' agregado con éxito (ID: {usuario_id}).", 'success')
            return redirect(url_for('usuarios.usuarios_lista'))
        except Exception as e:
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                flash(f'❌ Ya existe un usuario con el correo "{mail}".', 'error')
            else:
                flash(f'❌ Error al agregar usuario: {e}', 'error')
            return render_template('usuarios_form.html', accion='Agregar')

    # GET: Mostramos el formulario vacío
    return render_template('usuarios_form.html', accion='Agregar')


# ============================================
# RUTA: EDITAR USUARIO
# GET /usuarios/editar/<id> → Muestra formulario con datos actuales
# POST /usuarios/editar/<id> → Actualiza los datos del usuario
# ============================================

@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def usuarios_editar(id):
    """
    Formulario para editar un usuario existente.

    GET: Muestra el formulario con los datos actuales.
    POST: Procesa los datos actualizados y los guarda.
    """
    usuario = _db_manager.obtener_usuario_por_id(id)

    if not usuario:
        flash(f'❌ No se encontró usuario con ID {id}.', 'error')
        return redirect(url_for('usuarios.usuarios_lista'))

    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        mail = request.form.get('mail', '').strip()
        password = request.form.get('password', '').strip()

        if not nombre:
            flash('❌ El nombre es obligatorio.', 'error')
            return render_template('usuarios_form.html', usuario=usuario, accion='Editar')

        if not mail:
            flash('❌ El correo electrónico es obligatorio.', 'error')
            return render_template('usuarios_form.html', usuario=usuario, accion='Editar')

        if not password:
            flash('❌ La contraseña es obligatoria.', 'error')
            return render_template('usuarios_form.html', usuario=usuario, accion='Editar')

        try:
            if _db_manager.actualizar_usuario(id, nombre, mail, password):
                flash(f"✅ Usuario '{nombre}' actualizado correctamente.", 'success')
            else:
                flash('❌ Error al actualizar el usuario.', 'error')
        except Exception as e:
            if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
                flash(f'❌ Ya existe otro usuario con el correo "{mail}".', 'error')
            else:
                flash(f'❌ Error al actualizar: {e}', 'error')
            return render_template('usuarios_form.html', usuario=usuario, accion='Editar')

        return redirect(url_for('usuarios.usuarios_lista'))

    # GET: Mostramos el formulario con datos ya cargados
    return render_template('usuarios_form.html', usuario=usuario, accion='Editar')


# ============================================
# RUTA: ELIMINAR USUARIO
# POST /usuarios/eliminar/<id> → Elimina el usuario
# ============================================

@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
def usuarios_eliminar(id):
    """
    Elimina un usuario de la base de datos por su ID.
    Solo acepta método POST por seguridad.
    """
    usuario = _db_manager.obtener_usuario_por_id(id)
    nombre_usuario = usuario['nombre'] if usuario else f'ID {id}'

    if _db_manager.eliminar_usuario(id):
        flash(f"✅ Usuario '{nombre_usuario}' eliminado correctamente.", 'success')
    else:
        flash(f'❌ No se pudo eliminar el usuario con ID {id}.', 'error')

    return redirect(url_for('usuarios.usuarios_lista'))
