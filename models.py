# ============================================
# MODELOS POO + CONEXIÓN POSTGRESQL (SUPABASE)
# Semana 13 - Sistema Avanzado de Gestión de Inventario
# TechByte - Tienda de Gadgets
# ============================================
#
# Migración de SQLite → PostgreSQL (Supabase)
# Se usa psycopg2 como conector y las credenciales
# se leen desde el archivo .env a través de Conexión/conexion.py
# ============================================

import os

# Importamos la función de conexión desde el módulo Conexión
from Conexión.conexion import get_connection


# ============================================
# CLASE PRODUCTO
# Representa un producto individual del inventario.
# Usa una TUPLA para definir las categorías válidas (inmutable).
# Implementa @property (getters/setters) para encapsulamiento.
# ============================================

class Producto:
    """
    Clase que representa un producto en el inventario de TechByte.

    Atributos:
        id (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        categoria (str): Categoría a la que pertenece (debe ser de CATEGORIAS_VALIDAS).
        precio (float): Precio en dólares.
        cantidad (int): Unidades disponibles en stock.
        descripcion (str): Descripción detallada del producto.

    Colecciones utilizadas:
        - TUPLA: CATEGORIAS_VALIDAS es una tupla inmutable con las categorías permitidas.
          Se eligió tupla porque las categorías no deben cambiar en tiempo de ejecución.
    """

    # TUPLA inmutable con las categorías válidas de la tienda
    # Se usa tupla porque las categorías son fijas y no deben modificarse
    CATEGORIAS_VALIDAS = (
        "Laptops",
        "Smartphones",
        "Audio",
        "Accesorios",
        "Gaming",
        "Tablets",
        "Wearables",
        "Otros"
    )

    def __init__(self, id, nombre, categoria, precio, cantidad, descripcion=""):
        """
        Constructor de la clase Producto.

        Args:
            id (int): ID único del producto.
            nombre (str): Nombre del producto.
            categoria (str): Categoría (debe estar en CATEGORIAS_VALIDAS).
            precio (float): Precio unitario.
            cantidad (int): Cantidad en stock.
            descripcion (str): Descripción opcional del producto.
        """
        self._id = id
        self._nombre = nombre
        self._categoria = categoria if categoria in self.CATEGORIAS_VALIDAS else "Otros"
        self._precio = float(precio)
        self._cantidad = int(cantidad)
        self._descripcion = descripcion

    # --- Getters y Setters con @property ---

    @property
    def id(self):
        """Obtener el ID del producto (solo lectura)."""
        return self._id

    @property
    def nombre(self):
        """Obtener el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Establecer el nombre del producto."""
        if valor and isinstance(valor, str):
            self._nombre = valor

    @property
    def categoria(self):
        """Obtener la categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor):
        """Establecer la categoría, validando que sea una categoría válida."""
        if valor in self.CATEGORIAS_VALIDAS:
            self._categoria = valor

    @property
    def precio(self):
        """Obtener el precio del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor):
        """Establecer el precio del producto (debe ser positivo)."""
        if valor >= 0:
            self._precio = float(valor)

    @property
    def cantidad(self):
        """Obtener la cantidad en stock."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        """Establecer la cantidad en stock (debe ser >= 0)."""
        if valor >= 0:
            self._cantidad = int(valor)

    @property
    def descripcion(self):
        """Obtener la descripción del producto."""
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        """Establecer la descripción del producto."""
        self._descripcion = str(valor)

    def to_dict(self):
        """
        Convierte el producto a un DICCIONARIO para facilitar su uso
        en plantillas Jinja2 y operaciones de datos.

        Returns:
            dict: Diccionario con todos los atributos del producto.
        """
        return {
            "id": self._id,
            "nombre": self._nombre,
            "categoria": self._categoria,
            "precio": self._precio,
            "cantidad": self._cantidad,
            "descripcion": self._descripcion
        }

    def __repr__(self):
        """Representación en texto del producto (útil para depuración)."""
        return (f"Producto(id={self._id}, nombre='{self._nombre}', "
                f"categoria='{self._categoria}', precio=${self._precio:.2f}, "
                f"cantidad={self._cantidad})")


# ============================================
# CLASE DATABASEMANAGER
# Gestiona la conexión y operaciones CRUD con PostgreSQL (Supabase).
# Crea las tablas: productos, categorias, clientes, usuarios.
# ============================================

class DatabaseManager:
    """
    Clase que gestiona la conexión y las operaciones CRUD con la
    base de datos PostgreSQL en Supabase.

    Semana 13: Migración de SQLite a PostgreSQL.
    Se usa psycopg2 como conector y las credenciales se leen desde .env

    Crea y administra 4 tablas:
        - productos: Almacena el inventario de la tienda.
        - categorias: Catálogo de categorías disponibles.
        - clientes: Registro de clientes de la tienda.
        - usuarios: Usuarios del sistema (Semana 13).
    """

    def __init__(self):
        """
        Inicializa el gestor de base de datos PostgreSQL.
        La conexión se obtiene desde Conexión/conexion.py que lee el .env
        """
        self.init_db()

    def _get_connection(self):
        """
        Crea y retorna una conexión a la base de datos PostgreSQL (Supabase).
        Usa RealDictCursor que permite acceder a columnas por nombre.

        Returns:
            psycopg2.connection: Conexión activa a la base de datos.
        """
        return get_connection()

    def init_db(self):
        """
        Inicializa la base de datos creando las tablas necesarias
        si no existen. También inserta las categorías iniciales.

        Tablas creadas:
            - productos: id, nombre, categoria, precio, cantidad, descripcion
            - categorias: id, nombre, descripcion
            - clientes: id, nombre, email, telefono, fecha_registro
            - usuarios: id_usuario, nombre, mail, password (Semana 13)
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Tabla de PRODUCTOS - Almacena el inventario
        # SERIAL reemplaza a INTEGER PRIMARY KEY AUTOINCREMENT de SQLite
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(200) NOT NULL,
                categoria VARCHAR(100) NOT NULL,
                precio NUMERIC(10,2) NOT NULL,
                cantidad INTEGER NOT NULL DEFAULT 0,
                descripcion TEXT DEFAULT ''
            )
        ''')

        # Tabla de CATEGORÍAS - Catálogo de categorías
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL UNIQUE,
                descripcion TEXT DEFAULT ''
            )
        ''')

        # Tabla de CLIENTES - Registro de clientes de la tienda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(200) NOT NULL,
                email VARCHAR(200) UNIQUE,
                telefono VARCHAR(50),
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # ============================================
        # TABLA DE USUARIOS - Semana 13
        # Requerida por la tarea: usuarios(id_usuario, nombre, mail, password)
        # ============================================
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario SERIAL PRIMARY KEY,
                nombre VARCHAR(200) NOT NULL,
                mail VARCHAR(200) UNIQUE NOT NULL,
                password VARCHAR(200) NOT NULL
            )
        ''')

        # Insertar categorías iniciales desde la tupla de Producto
        # ON CONFLICT DO NOTHING es el equivalente PostgreSQL de INSERT OR IGNORE
        for cat in Producto.CATEGORIAS_VALIDAS:
            cursor.execute(
                "INSERT INTO categorias (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING",
                (cat,)
            )

        conn.commit()
        conn.close()

    # --- Operaciones CRUD para PRODUCTOS ---

    def insertar_producto(self, producto):
        """
        Inserta un nuevo producto en la base de datos PostgreSQL.

        Args:
            producto (Producto): Instancia de Producto a insertar.

        Returns:
            int: ID del producto insertado.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        # RETURNING id es la forma PostgreSQL de obtener el ID generado
        cursor.execute(
            """INSERT INTO productos (nombre, categoria, precio, cantidad, descripcion)
               VALUES (%s, %s, %s, %s, %s) RETURNING id""",
            (producto.nombre, producto.categoria, producto.precio,
             producto.cantidad, producto.descripcion)
        )
        producto_id = cursor.fetchone()['id']
        conn.commit()
        conn.close()
        return producto_id

    def obtener_todos(self):
        """
        Obtiene todos los productos de la base de datos.

        Returns:
            list: LISTA de diccionarios con los datos de cada producto.
                  Se retorna una LISTA porque necesitamos iterar sobre todos
                  los productos y mantener el orden de inserción.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id")
        # RealDictCursor ya retorna diccionarios directamente
        productos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return productos

    def obtener_por_id(self, producto_id):
        """
        Busca un producto específico por su ID.

        Args:
            producto_id (int): ID del producto a buscar.

        Returns:
            dict o None: Diccionario con los datos del producto, o None si no existe.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = %s", (producto_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def actualizar_producto(self, producto_id, nombre, categoria, precio, cantidad, descripcion):
        """
        Actualiza los datos de un producto existente en la base de datos.

        Args:
            producto_id (int): ID del producto a actualizar.
            nombre (str): Nuevo nombre.
            categoria (str): Nueva categoría.
            precio (float): Nuevo precio.
            cantidad (int): Nueva cantidad.
            descripcion (str): Nueva descripción.

        Returns:
            bool: True si se actualizó exitosamente, False si no se encontró.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE productos
               SET nombre=%s, categoria=%s, precio=%s, cantidad=%s, descripcion=%s
               WHERE id=%s""",
            (nombre, categoria, float(precio), int(cantidad), descripcion, producto_id)
        )
        actualizado = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return actualizado

    def eliminar_producto(self, producto_id):
        """
        Elimina un producto de la base de datos por su ID.

        Args:
            producto_id (int): ID del producto a eliminar.

        Returns:
            bool: True si se eliminó exitosamente, False si no se encontró.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
        eliminado = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return eliminado

    def buscar_por_nombre(self, termino):
        """
        Busca productos cuyo nombre contenga el término de búsqueda.
        Usa ILIKE de PostgreSQL para búsqueda parcial (case-insensitive).

        Args:
            termino (str): Término de búsqueda.

        Returns:
            list: LISTA de diccionarios con los productos encontrados.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        # ILIKE es la versión case-insensitive de LIKE en PostgreSQL
        cursor.execute(
            "SELECT * FROM productos WHERE nombre ILIKE %s ORDER BY id",
            (f"%{termino}%",)
        )
        productos = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return productos

    # --- Operaciones para CLIENTES ---

    def insertar_cliente(self, nombre, email, telefono=""):
        """Inserta un nuevo cliente en la base de datos."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)",
            (nombre, email, telefono)
        )
        conn.commit()
        conn.close()

    def obtener_clientes(self):
        """Obtiene todos los clientes registrados."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes ORDER BY id")
        clientes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return clientes

    # ============================================
    # OPERACIONES CRUD PARA USUARIOS (Semana 13)
    # Tabla: usuarios(id_usuario, nombre, mail, password)
    # ============================================

    def insertar_usuario(self, nombre, mail, password):
        """
        Inserta un nuevo usuario en la base de datos.

        Args:
            nombre (str): Nombre del usuario.
            mail (str): Correo electrónico (único).
            password (str): Contraseña del usuario.

        Returns:
            int: ID del usuario insertado.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO usuarios (nombre, mail, password)
               VALUES (%s, %s, %s) RETURNING id_usuario""",
            (nombre, mail, password)
        )
        usuario_id = cursor.fetchone()['id_usuario']
        conn.commit()
        conn.close()
        return usuario_id

    def obtener_usuarios(self):
        """
        Obtiene todos los usuarios registrados.

        Returns:
            list: LISTA de diccionarios con los datos de cada usuario.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios ORDER BY id_usuario")
        usuarios = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return usuarios

    def obtener_usuario_por_id(self, usuario_id):
        """
        Busca un usuario específico por su ID.

        Args:
            usuario_id (int): ID del usuario a buscar.

        Returns:
            dict o None: Diccionario con los datos del usuario, o None si no existe.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def actualizar_usuario(self, usuario_id, nombre, mail, password):
        """
        Actualiza los datos de un usuario existente.

        Args:
            usuario_id (int): ID del usuario a actualizar.
            nombre (str): Nuevo nombre.
            mail (str): Nuevo correo.
            password (str): Nueva contraseña.

        Returns:
            bool: True si se actualizó exitosamente.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE usuarios
               SET nombre=%s, mail=%s, password=%s
               WHERE id_usuario=%s""",
            (nombre, mail, password, usuario_id)
        )
        actualizado = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return actualizado

    def eliminar_usuario(self, usuario_id):
        """
        Elimina un usuario de la base de datos por su ID.

        Args:
            usuario_id (int): ID del usuario a eliminar.

        Returns:
            bool: True si se eliminó exitosamente.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (usuario_id,))
        eliminado = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return eliminado


# ============================================
# CLASE INVENTARIO
# Gestiona los productos en memoria usando colecciones (diccionario,
# conjunto, lista) y sincroniza con PostgreSQL (Supabase).
# ============================================

class Inventario:
    """
    Clase que gestiona el inventario de productos de TechByte.

    Colecciones utilizadas:
        - DICCIONARIO (_productos): Estructura principal {id: Producto}.
          Se eligió diccionario porque permite acceso O(1) por ID,
          ideal para operaciones CRUD frecuentes.
        - CONJUNTO (_ids_usados): Almacena los IDs utilizados para
          garantizar unicidad en O(1). Más eficiente que buscar en lista.
        - LISTA: Se usa en los métodos de búsqueda y mostrar para
          retornar resultados ordenados e iterables.
        - TUPLA: Las categorías válidas están en Producto.CATEGORIAS_VALIDAS.
    """

    def __init__(self, db_manager=None):
        """
        Inicializa el inventario conectado a la base de datos.

        Args:
            db_manager (DatabaseManager): Instancia del gestor de base de datos.
        """
        # DICCIONARIO: estructura principal {id: Producto} para acceso rápido O(1)
        self._productos = {}

        # CONJUNTO: almacena IDs usados para verificación rápida de unicidad O(1)
        self._ids_usados = set()

        # Conexión a la base de datos PostgreSQL (Supabase)
        self._db = db_manager if db_manager else DatabaseManager()

        # Cargar productos existentes de la DB al diccionario en memoria
        self._cargar_desde_db()

    def _cargar_desde_db(self):
        """
        Carga todos los productos de la base de datos PostgreSQL
        al DICCIONARIO en memoria y al CONJUNTO de IDs.
        Esto permite operaciones rápidas sin consultar la DB cada vez.
        """
        productos_db = self._db.obtener_todos()  # Retorna una LISTA de diccionarios
        for datos in productos_db:
            # Convertir Decimal a float si viene de PostgreSQL
            precio = float(datos["precio"]) if datos["precio"] else 0.0
            producto = Producto(
                id=datos["id"],
                nombre=datos["nombre"],
                categoria=datos["categoria"],
                precio=precio,
                cantidad=datos["cantidad"],
                descripcion=datos["descripcion"]
            )
            # Guardamos en el DICCIONARIO con el ID como clave
            self._productos[producto.id] = producto
            # Añadimos el ID al CONJUNTO de IDs usados
            self._ids_usados.add(producto.id)

    def agregar(self, nombre, categoria, precio, cantidad, descripcion=""):
        """
        Añade un nuevo producto al inventario y a la base de datos.

        Args:
            nombre (str): Nombre del producto.
            categoria (str): Categoría del producto.
            precio (float): Precio unitario.
            cantidad (int): Cantidad en stock.
            descripcion (str): Descripción del producto.

        Returns:
            Producto: El producto creado.
        """
        # Creamos el objeto Producto con ID temporal (0)
        producto = Producto(0, nombre, categoria, precio, cantidad, descripcion)

        # Insertamos en la DB y obtenemos el ID real generado por PostgreSQL
        nuevo_id = self._db.insertar_producto(producto)
        producto._id = nuevo_id

        # Guardamos en el DICCIONARIO en memoria
        self._productos[nuevo_id] = producto

        # Añadimos al CONJUNTO de IDs usados
        self._ids_usados.add(nuevo_id)

        return producto

    def eliminar(self, producto_id):
        """
        Elimina un producto del inventario y de la base de datos.

        Args:
            producto_id (int): ID del producto a eliminar.

        Returns:
            bool: True si se eliminó exitosamente.
        """
        # Verificamos si el ID existe en el CONJUNTO (O(1))
        if producto_id not in self._ids_usados:
            return False

        # Eliminamos de la base de datos
        self._db.eliminar_producto(producto_id)

        # Eliminamos del DICCIONARIO en memoria
        del self._productos[producto_id]

        # Removemos del CONJUNTO de IDs
        self._ids_usados.discard(producto_id)

        return True

    def actualizar(self, producto_id, nombre, categoria, precio, cantidad, descripcion):
        """
        Actualiza los datos de un producto existente.

        Args:
            producto_id (int): ID del producto a actualizar.
            nombre (str): Nuevo nombre.
            categoria (str): Nueva categoría.
            precio (float): Nuevo precio.
            cantidad (int): Nueva cantidad.
            descripcion (str): Nueva descripción.

        Returns:
            bool: True si se actualizó exitosamente.
        """
        # Verificamos existencia en el CONJUNTO (O(1))
        if producto_id not in self._ids_usados:
            return False

        # Actualizamos en la base de datos
        self._db.actualizar_producto(
            producto_id, nombre, categoria, float(precio), int(cantidad), descripcion
        )

        # Actualizamos el objeto en el DICCIONARIO en memoria
        producto = self._productos[producto_id]
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = float(precio)
        producto.cantidad = int(cantidad)
        producto.descripcion = descripcion

        return True

    def buscar_por_nombre(self, termino):
        """
        Busca productos por nombre usando la base de datos.

        Args:
            termino (str): Término de búsqueda parcial.

        Returns:
            list: LISTA de diccionarios con los productos encontrados.
                  Se retorna LISTA porque los resultados necesitan orden
                  y pueden contener duplicados.
        """
        resultados_db = self._db.buscar_por_nombre(termino)
        # Retornamos una LISTA de diccionarios
        return resultados_db

    def mostrar_todos(self):
        """
        Muestra todos los productos del inventario.

        Returns:
            list: LISTA de diccionarios con todos los productos.
                  Usamos LISTA para mantener el orden y facilitar la iteración
                  en las plantillas Jinja2 con {% for %}.
        """
        # Convertimos el DICCIONARIO a una LISTA de diccionarios
        return [producto.to_dict() for producto in self._productos.values()]

    def obtener_por_id(self, producto_id):
        """
        Obtiene un producto específico por su ID.

        Args:
            producto_id (int): ID del producto.

        Returns:
            dict o None: Diccionario con los datos del producto, o None.
        """
        # Búsqueda O(1) en el DICCIONARIO
        producto = self._productos.get(producto_id)
        return producto.to_dict() if producto else None

    def obtener_estadisticas(self):
        """
        Calcula estadísticas del inventario usando colecciones.

        Returns:
            dict: Diccionario con estadísticas generales.
        """
        todos = self.mostrar_todos()  # LISTA de diccionarios

        if not todos:
            return {
                "total_productos": 0,
                "total_unidades": 0,
                "valor_total": 0,
                "categorias_activas": [],
                "producto_mas_caro": None,
                "producto_mas_barato": None
            }

        # LISTA de precios para cálculos
        precios = [p["precio"] for p in todos]

        # CONJUNTO de categorías activas (elimina duplicados automáticamente)
        categorias_activas = {p["categoria"] for p in todos}

        return {
            "total_productos": len(todos),
            "total_unidades": sum(p["cantidad"] for p in todos),
            "valor_total": sum(p["precio"] * p["cantidad"] for p in todos),
            "categorias_activas": sorted(list(categorias_activas)),  # CONJUNTO → LISTA ordenada
            "producto_mas_caro": max(todos, key=lambda p: p["precio"]),
            "producto_mas_barato": min(todos, key=lambda p: p["precio"])
        }

    def recargar(self):
        """
        Recarga los datos desde la base de datos al diccionario en memoria.
        Útil cuando se han hecho cambios directos a la DB.
        """
        self._productos.clear()
        self._ids_usados.clear()
        self._cargar_desde_db()
