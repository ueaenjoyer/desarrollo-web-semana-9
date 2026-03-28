# ============================================
# Service: Ventas
# Semana 15 - TechByte
# ============================================
# CRUD completo para la tabla ventas en PostgreSQL.
# Registrar una venta descuenta stock del producto.
# ============================================

from conexion.conexion import get_connection


def init_tabla():
    """Crea la tabla ventas si no existe."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id SERIAL PRIMARY KEY,
            id_producto INTEGER NOT NULL REFERENCES productos(id) ON DELETE CASCADE,
            cliente_nombre VARCHAR(200) NOT NULL,
            cliente_email VARCHAR(200) DEFAULT '',
            cantidad INTEGER NOT NULL,
            precio_unitario NUMERIC(10,2) NOT NULL,
            total NUMERIC(10,2) NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def obtener_todas():
    """Obtiene todas las ventas con el nombre del producto (JOIN)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT v.*, p.nombre AS producto_nombre
        FROM ventas v
        LEFT JOIN productos p ON v.id_producto = p.id
        ORDER BY v.fecha DESC
    ''')
    ventas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    for v in ventas:
        v['precio_unitario'] = float(v['precio_unitario']) if v['precio_unitario'] else 0.0
        v['total'] = float(v['total']) if v['total'] else 0.0
    return ventas


def obtener_por_id(venta_id):
    """Obtiene una venta por su ID con nombre del producto."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT v.*, p.nombre AS producto_nombre
        FROM ventas v
        LEFT JOIN productos p ON v.id_producto = p.id
        WHERE v.id = %s
    ''', (venta_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        resultado = dict(row)
        resultado['precio_unitario'] = float(resultado['precio_unitario']) if resultado['precio_unitario'] else 0.0
        resultado['total'] = float(resultado['total']) if resultado['total'] else 0.0
        return resultado
    return None


def registrar(id_producto, cliente_nombre, cliente_email, cantidad, precio_unitario):
    """
    Registra una nueva venta y descuenta stock del producto.
    
    Returns:
        int: ID de la venta creada, o None si no hay stock suficiente.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar stock disponible
    cursor.execute("SELECT stock FROM productos WHERE id = %s", (id_producto,))
    producto = cursor.fetchone()
    if not producto or producto['stock'] < cantidad:
        conn.close()
        return None  # Stock insuficiente

    total = float(precio_unitario) * int(cantidad)

    # Insertar la venta
    cursor.execute(
        """INSERT INTO ventas (id_producto, cliente_nombre, cliente_email, cantidad, precio_unitario, total)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
        (id_producto, cliente_nombre, cliente_email, int(cantidad), float(precio_unitario), total)
    )
    venta_id = cursor.fetchone()['id']

    # Descontar stock del producto
    cursor.execute(
        "UPDATE productos SET stock = stock - %s WHERE id = %s",
        (int(cantidad), id_producto)
    )

    conn.commit()
    conn.close()
    return venta_id


def eliminar(venta_id):
    """Elimina una venta por su ID (sin restaurar stock)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ventas WHERE id = %s", (venta_id,))
    eliminado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return eliminado


def contar():
    """Retorna el total de ventas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM ventas")
    total = cursor.fetchone()['total']
    conn.close()
    return total


def total_ingresos():
    """Retorna el total de ingresos por ventas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(SUM(total), 0) AS ingresos FROM ventas")
    ingresos = float(cursor.fetchone()['ingresos'])
    conn.close()
    return ingresos
