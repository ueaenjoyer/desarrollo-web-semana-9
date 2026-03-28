# ============================================
# Formulario: Venta
# Semana 15 - TechByte
# ============================================

class VentaForm:
    """Valida los datos del formulario de ventas."""

    def __init__(self, id_producto=None, cliente_nombre='', cliente_email='', cantidad=0):
        self.cliente_nombre = cliente_nombre.strip() if cliente_nombre else ''
        self.cliente_email = cliente_email.strip() if cliente_email else ''
        self.errores = []

        try:
            self.id_producto = int(id_producto) if id_producto else None
        except (ValueError, TypeError):
            self.id_producto = None
            self.errores.append("❌ El producto seleccionado no es válido.")

        try:
            self.cantidad = int(cantidad)
        except (ValueError, TypeError):
            self.cantidad = 0
            self.errores.append("❌ La cantidad debe ser un número entero.")

    @classmethod
    def desde_request(cls, form_data):
        """Crea una instancia desde request.form."""
        return cls(
            id_producto=form_data.get('id_producto'),
            cliente_nombre=form_data.get('cliente_nombre', ''),
            cliente_email=form_data.get('cliente_email', ''),
            cantidad=form_data.get('cantidad', 0)
        )

    def es_valido(self):
        """Valida los datos del formulario."""
        errores_tipo = [e for e in self.errores if "número" in e or "válido" in e]
        self.errores = errores_tipo

        if self.id_producto is None:
            self.errores.append("❌ Debe seleccionar un producto.")
        if not self.cliente_nombre:
            self.errores.append("❌ El nombre del cliente es obligatorio.")
        if self.cantidad <= 0:
            self.errores.append("❌ La cantidad debe ser mayor a 0.")

        return len(self.errores) == 0
