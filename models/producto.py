# ============================================
# Modelo: Producto
# Semana 15 - TechByte
# ============================================

class Producto:
    """
    Representa un producto en la tienda TechByte.

    Atributos:
        id (int): Identificador único.
        nombre (str): Nombre del producto.
        id_categoria (int): FK a la tabla categorias.
        precio (float): Precio en dólares.
        stock (int): Unidades disponibles.
        descripcion (str): Descripción del producto.
        categoria_nombre (str): Nombre de la categoría (JOIN).
    """

    def __init__(self, id, nombre, id_categoria, precio, stock, descripcion="", categoria_nombre=""):
        self._id = id
        self._nombre = nombre
        self._id_categoria = int(id_categoria) if id_categoria else None
        self._precio = float(precio)
        self._stock = int(stock)
        self._descripcion = descripcion
        self._categoria_nombre = categoria_nombre

    # --- Properties ---

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor and isinstance(valor, str):
            self._nombre = valor

    @property
    def id_categoria(self):
        return self._id_categoria

    @id_categoria.setter
    def id_categoria(self, valor):
        self._id_categoria = int(valor) if valor else None

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor >= 0:
            self._precio = float(valor)

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if valor >= 0:
            self._stock = int(valor)

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = str(valor)

    @property
    def categoria_nombre(self):
        return self._categoria_nombre

    def to_dict(self):
        """Convierte el producto a un diccionario para Jinja2."""
        return {
            "id": self._id,
            "nombre": self._nombre,
            "id_categoria": self._id_categoria,
            "precio": self._precio,
            "stock": self._stock,
            "descripcion": self._descripcion,
            "categoria_nombre": self._categoria_nombre,
        }

    def __repr__(self):
        return f"Producto(id={self._id}, nombre='{self._nombre}', precio=${self._precio:.2f})"
