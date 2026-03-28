# ============================================
# Modelo: Venta
# Semana 15 - TechByte
# ============================================

class Venta:
    """
    Representa una venta registrada en la tienda.

    Atributos:
        id (int): Identificador único.
        id_producto (int): FK al producto vendido.
        cliente_nombre (str): Nombre del cliente.
        cliente_email (str): Email del cliente.
        cantidad (int): Cantidad vendida.
        precio_unitario (float): Precio al momento de la venta.
        total (float): Total de la venta (cantidad * precio_unitario).
        fecha (str): Fecha de la venta.
        producto_nombre (str): Nombre del producto (JOIN).
    """

    def __init__(self, id, id_producto, cliente_nombre, cliente_email,
                 cantidad, precio_unitario, total, fecha, producto_nombre=""):
        self._id = id
        self._id_producto = int(id_producto)
        self._cliente_nombre = cliente_nombre
        self._cliente_email = cliente_email
        self._cantidad = int(cantidad)
        self._precio_unitario = float(precio_unitario)
        self._total = float(total)
        self._fecha = fecha
        self._producto_nombre = producto_nombre

    @property
    def id(self):
        return self._id

    @property
    def id_producto(self):
        return self._id_producto

    @property
    def cliente_nombre(self):
        return self._cliente_nombre

    @property
    def cliente_email(self):
        return self._cliente_email

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @property
    def total(self):
        return self._total

    @property
    def fecha(self):
        return self._fecha

    @property
    def producto_nombre(self):
        return self._producto_nombre

    def to_dict(self):
        """Convierte la venta a un diccionario para Jinja2."""
        return {
            "id": self._id,
            "id_producto": self._id_producto,
            "cliente_nombre": self._cliente_nombre,
            "cliente_email": self._cliente_email,
            "cantidad": self._cantidad,
            "precio_unitario": self._precio_unitario,
            "total": self._total,
            "fecha": self._fecha,
            "producto_nombre": self._producto_nombre,
        }

    def __repr__(self):
        return f"Venta(id={self._id}, producto={self._producto_nombre}, total=${self._total:.2f})"
