# ============================================
# Modelo: Categoria
# Semana 15 - TechByte
# ============================================

class Categoria:
    """
    Representa una categoría de productos.

    Atributos:
        id (int): Identificador único.
        nombre (str): Nombre de la categoría.
        descripcion (str): Descripción de la categoría.
    """

    def __init__(self, id, nombre, descripcion=""):
        self._id = id
        self._nombre = nombre
        self._descripcion = descripcion

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
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self._descripcion = str(valor)

    def to_dict(self):
        """Convierte la categoría a un diccionario para Jinja2."""
        return {
            "id": self._id,
            "nombre": self._nombre,
            "descripcion": self._descripcion,
        }

    def __repr__(self):
        return f"Categoria(id={self._id}, nombre='{self._nombre}')"
