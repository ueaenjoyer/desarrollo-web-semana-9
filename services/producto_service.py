# ============================================
# Service: Productos
# Semana 15 - TechByte
# ============================================
# CRUD completo para la tabla productos en PostgreSQL.
# Usa JOIN con categorias para obtener el nombre de categoría.
# ============================================

from conexion.conexion import get_connection


def init_tabla():
    """
    Crea la tabla productos si no existe.
    Si existe con el esquema viejo (categoria VARCHAR, cantidad),
    la migra al nuevo esquema (id_categoria FK, stock).
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si la tabla existe y tiene el esquema viejo
    cursor.execute("""
        SELECT column_name FROM information_schema.columns
        WHERE table_name = 'productos' AND column_name = 'categoria'
    """)
    tiene_esquema_viejo = cursor.fetchone() is not None

    if tiene_esquema_viejo:
        # Migrar: eliminar la tabla vieja y crear la nueva
        cursor.execute("DROP TABLE IF EXISTS ventas")  # Depende de productos
        cursor.execute("DROP TABLE IF EXISTS productos")
        conn.commit()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(200) NOT NULL,
            id_categoria INTEGER REFERENCES categorias(id) ON DELETE SET NULL,
            precio NUMERIC(10,2) NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            descripcion TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()


def obtener_todos():
    """Obtiene todos los productos con el nombre de su categoría (JOIN)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        ORDER BY p.id
    ''')
    productos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    # Convertir Decimal a float
    for p in productos:
        p['precio'] = float(p['precio']) if p['precio'] else 0.0
    return productos


def obtener_por_id(producto_id):
    """Obtiene un producto por su ID con nombre de categoría."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.id = %s
    ''', (producto_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        resultado = dict(row)
        resultado['precio'] = float(resultado['precio']) if resultado['precio'] else 0.0
        return resultado
    return None


def obtener_por_categoria(categoria_id):
    """Obtiene todos los productos de una categoría específica."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.id_categoria = %s
        ORDER BY p.nombre
    ''', (categoria_id,))
    productos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    for p in productos:
        p['precio'] = float(p['precio']) if p['precio'] else 0.0
    return productos


def insertar(nombre, id_categoria, precio, stock, descripcion=""):
    """Inserta un nuevo producto. Retorna el ID generado."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO productos (nombre, id_categoria, precio, stock, descripcion)
           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
        (nombre, id_categoria, float(precio), int(stock), descripcion)
    )
    producto_id = cursor.fetchone()['id']
    conn.commit()
    conn.close()
    return producto_id


def actualizar(producto_id, nombre, id_categoria, precio, stock, descripcion):
    """Actualiza un producto existente."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE productos
           SET nombre=%s, id_categoria=%s, precio=%s, stock=%s, descripcion=%s
           WHERE id=%s""",
        (nombre, id_categoria, float(precio), int(stock), descripcion, producto_id)
    )
    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return actualizado


def eliminar(producto_id):
    """Elimina un producto por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    eliminado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return eliminado


def buscar(termino):
    """Busca productos por nombre (case-insensitive)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, c.nombre AS categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id
        WHERE p.nombre ILIKE %s
        ORDER BY p.id
    ''', (f"%{termino}%",))
    productos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    for p in productos:
        p['precio'] = float(p['precio']) if p['precio'] else 0.0
    return productos


def contar():
    """Retorna el total de productos."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM productos")
    total = cursor.fetchone()['total']
    conn.close()
    return total
