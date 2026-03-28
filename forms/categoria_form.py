# ============================================
# Formulario: Categoría
# Semana 15 - TechByte
# ============================================

class CategoriaForm:
    """Valida los datos del formulario de categorías."""

    def __init__(self, nombre='', descripcion=''):
        self.nombre = nombre.strip() if nombre else ''
        self.descripcion = descripcion.strip() if descripcion else ''
        self.errores = []

    @classmethod
    def desde_request(cls, form_data):
        """Crea una instancia desde request.form."""
        return cls(
            nombre=form_data.get('nombre', ''),
            descripcion=form_data.get('descripcion', '')
        )

    def es_valido(self):
        """Valida los datos del formulario."""
        self.errores = []
        if not self.nombre:
            self.errores.append("❌ El nombre de la categoría es obligatorio.")
        return len(self.errores) == 0
