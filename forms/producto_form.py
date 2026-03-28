# ============================================
# Formulario: Producto
# Semana 15 - TechByte
# ============================================

class ProductoForm:
    """Valida los datos del formulario de productos."""

    def __init__(self, nombre='', id_categoria=None, precio=0.0, stock=0, descripcion=''):
        self.nombre = nombre.strip() if nombre else ''
        self.descripcion = descripcion.strip() if descripcion else ''
        self.errores = []

        try:
            self.id_categoria = int(id_categoria) if id_categoria else None
        except (ValueError, TypeError):
            self.id_categoria = None
            self.errores.append("❌ La categoría seleccionada no es válida.")

        try:
            self.precio = float(precio)
        except (ValueError, TypeError):
            self.precio = 0.0
            self.errores.append("❌ El precio debe ser un número válido.")

        try:
            self.stock = int(stock)
        except (ValueError, TypeError):
            self.stock = 0
            self.errores.append("❌ El stock debe ser un número entero.")

    @classmethod
    def desde_request(cls, form_data):
        """Crea una instancia desde request.form."""
        return cls(
            nombre=form_data.get('nombre', ''),
            id_categoria=form_data.get('id_categoria'),
            precio=form_data.get('precio', 0),
            stock=form_data.get('stock', 0),
            descripcion=form_data.get('descripcion', '')
        )

    def es_valido(self):
        """Valida los datos del formulario."""
        errores_tipo = [e for e in self.errores if "número" in e or "válida" in e]
        self.errores = errores_tipo

        if not self.nombre:
            self.errores.append("❌ El nombre del producto es obligatorio.")
        if self.id_categoria is None:
            self.errores.append("❌ Debe seleccionar una categoría.")
        if self.precio < 0:
            self.errores.append("❌ El precio no puede ser negativo.")
        if self.stock < 0:
            self.errores.append("❌ El stock no puede ser negativo.")

        return len(self.errores) == 0
