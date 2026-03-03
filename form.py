# ============================================
# form.py - Clase de Formulario para Datos
# Semana 12 - TechByte
# ============================================
#
# Este módulo define la clase DatosForm que encapsula
# la validación y extracción de datos del formulario
# de persistencia. Sigue el patrón de formularios
# que separa la lógica de validación de las rutas.
# ============================================


class DatosForm:
    """
    Clase que representa y valida el formulario de datos
    para persistencia en TXT, JSON, CSV y SQLAlchemy.

    Attributes:
        nombre (str): Nombre del producto.
        precio (float): Precio del producto.
        cantidad (int): Cantidad en stock.
        descripcion (str): Descripción del producto.
        errores (list): Lista de mensajes de error de validación.
    """

    def __init__(self, nombre='', precio=0.0, cantidad=0, descripcion=''):
        """
        Constructor del formulario de datos.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio del producto.
            cantidad (int): Cantidad en stock.
            descripcion (str): Descripción del producto.
        """
        self.nombre = nombre.strip() if nombre else ''
        self.descripcion = descripcion.strip() if descripcion else ''
        self.errores = []

        # Convertimos precio y cantidad, capturando posibles errores
        try:
            self.precio = float(precio)
        except (ValueError, TypeError):
            self.precio = 0.0
            self.errores.append("❌ El precio debe ser un número válido.")

        try:
            self.cantidad = int(cantidad)
        except (ValueError, TypeError):
            self.cantidad = 0
            self.errores.append("❌ La cantidad debe ser un número entero.")

    @classmethod
    def desde_request(cls, form_data):
        """
        Crea una instancia del formulario a partir de request.form.

        Método de clase (classmethod) que facilita la construcción
        del objeto desde los datos enviados por el usuario.

        Args:
            form_data (ImmutableMultiDict): Datos del formulario de Flask.

        Returns:
            DatosForm: Instancia del formulario con los datos extraídos.
        """
        return cls(
            nombre=form_data.get('nombre', ''),
            precio=form_data.get('precio', 0),
            cantidad=form_data.get('cantidad', 0),
            descripcion=form_data.get('descripcion', '')
        )

    def es_valido(self):
        """
        Valida los datos del formulario.

        Verifica que:
        - El nombre no esté vacío.
        - El precio sea positivo.
        - La cantidad sea >= 0.

        Returns:
            bool: True si los datos son válidos, False en caso contrario.
        """
        # Limpiamos errores previos de validación de campos
        errores_tipo = [e for e in self.errores if "número" in e]
        self.errores = errores_tipo  # Mantenemos errores de tipo

        if not self.nombre:
            self.errores.append("❌ El nombre del producto es obligatorio.")

        if self.precio < 0:
            self.errores.append("❌ El precio no puede ser negativo.")

        if self.cantidad < 0:
            self.errores.append("❌ La cantidad no puede ser negativa.")

        return len(self.errores) == 0

    def to_dict(self):
        """
        Convierte los datos del formulario a un diccionario.

        Returns:
            dict: Diccionario con los datos del formulario.
        """
        return {
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'descripcion': self.descripcion
        }
