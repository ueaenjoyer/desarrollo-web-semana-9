# ============================================
# Service: Categorías
# Semana 15 - TechByte
# ============================================
# CRUD completo para la tabla categorias en PostgreSQL.
# ============================================

from conexion.conexion import get_connection


def init_tabla():
    """Crea la tabla categorias si no existe e inserta categorías iniciales."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL UNIQUE,
            descripcion TEXT DEFAULT ''
        )
    ''')
    # Categorías iniciales de la tienda
    categorias_iniciales = [
        ("Laptops", "Computadoras portátiles de alto rendimiento"),
        ("Smartphones", "Teléfonos inteligentes de última generación"),
        ("Audio", "Audífonos, parlantes y equipos de sonido"),
        ("Accesorios", "Cargadores, cables, fundas y más"),
        ("Gaming", "Consolas, controles y periféricos para gamers"),
        ("Tablets", "Tablets para trabajo y entretenimiento"),
        ("Wearables", "Relojes inteligentes y dispositivos portátiles"),
        ("Otros", "Otros productos tecnológicos"),
    ]
    for nombre, desc in categorias_iniciales:
        cursor.execute(
            "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s) ON CONFLICT (nombre) DO NOTHING",
            (nombre, desc)
        )
    conn.commit()
    conn.close()


def obtener_todas():
    """Obtiene todas las categorías ordenadas por nombre."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias ORDER BY nombre")
    categorias = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return categorias


def obtener_por_id(categoria_id):
    """Obtiene una categoría por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias WHERE id = %s", (categoria_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def insertar(nombre, descripcion=""):
    """Inserta una nueva categoría. Retorna el ID generado."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categorias (nombre, descripcion) VALUES (%s, %s) RETURNING id",
        (nombre, descripcion)
    )
    categoria_id = cursor.fetchone()['id']
    conn.commit()
    conn.close()
    return categoria_id


def actualizar(categoria_id, nombre, descripcion):
    """Actualiza una categoría existente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE categorias SET nombre=%s, descripcion=%s WHERE id=%s",
        (nombre, descripcion, categoria_id)
    )
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado


def eliminar(categoria_id):
    """Elimina una categoría por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE id = %s", (categoria_id,))
    eliminado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return eliminado
