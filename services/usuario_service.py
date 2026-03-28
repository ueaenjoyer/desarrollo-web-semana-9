# ============================================
# Service: Usuarios
# Semana 15 - TechByte
# ============================================
# CRUD de usuarios + autenticación con hash de passwords.
# ============================================

from conexion.conexion import get_connection
from werkzeug.security import generate_password_hash, check_password_hash


def init_tabla():
    """Crea la tabla usuarios si no existe y crea admin por defecto."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario SERIAL PRIMARY KEY,
            nombre VARCHAR(200) NOT NULL,
            mail VARCHAR(200) UNIQUE NOT NULL,
            password VARCHAR(300) NOT NULL
        )
    ''')
    # Crear usuario admin por defecto si no existe
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    if cursor.fetchone()['total'] == 0:
        password_hash = generate_password_hash('admin123')
        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
            ('Administrador', 'admin@techbyte.com', password_hash)
        )
    conn.commit()
    conn.close()


def obtener_todos():
    """Obtiene todos los usuarios registrados."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, nombre, mail FROM usuarios ORDER BY id_usuario")
    usuarios = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return usuarios


def obtener_por_id(usuario_id):
    """Obtiene un usuario por su ID (sin password)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id_usuario, nombre, mail FROM usuarios WHERE id_usuario = %s",
        (usuario_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def autenticar(mail, password):
    """
    Autentica un usuario por email y contraseña.
    
    Returns:
        dict: Datos del usuario si las credenciales son correctas, None si no.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE mail = %s", (mail,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario and check_password_hash(usuario['password'], password):
        return {
            'id_usuario': usuario['id_usuario'],
            'nombre': usuario['nombre'],
            'mail': usuario['mail']
        }
    
    # Compatibilidad: si el password no es hash, comparar directo y actualizar
    if usuario and usuario['password'] == password:
        # Actualizar a hash
        actualizar_password(usuario['id_usuario'], password)
        return {
            'id_usuario': usuario['id_usuario'],
            'nombre': usuario['nombre'],
            'mail': usuario['mail']
        }

    return None


def actualizar_password(usuario_id, password_plano):
    """Actualiza la contraseña de un usuario (la hashea)."""
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password_plano)
    cursor.execute(
        "UPDATE usuarios SET password = %s WHERE id_usuario = %s",
        (password_hash, usuario_id)
    )
    conn.commit()
    conn.close()


def insertar(nombre, mail, password):
    """Inserta un nuevo usuario con password hasheado."""
    conn = get_connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    cursor.execute(
        "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s) RETURNING id_usuario",
        (nombre, mail, password_hash)
    )
    usuario_id = cursor.fetchone()['id_usuario']
    conn.commit()
    conn.close()
    return usuario_id


def eliminar(usuario_id):
    """Elimina un usuario por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (usuario_id,))
    eliminado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return eliminado
