# ============================================
# bd.py - Base de Datos con SQLAlchemy (ORM)
# Semana 12 - TechByte
# ============================================
#
# SQLAlchemy es un ORM (Object-Relational Mapper) que nos permite
# interactuar con la base de datos usando clases Python en lugar de SQL
# directamente. Define el modelo ProductoDB como tabla en SQLite.
# ============================================

from flask_sqlalchemy import SQLAlchemy

# Instancia global de SQLAlchemy
# Se inicializa sin app por ahora (patrón Application Factory)
db = SQLAlchemy()


def init_app(app):
    """
    Inicializa SQLAlchemy con la aplicación Flask.

    Crea todas las tablas definidas en los modelos si no existen.
    Se llama desde app.py después de configurar la URI de la base de datos.

    Args:
        app (Flask): Instancia de la aplicación Flask.
    """
    db.init_app(app)
    with app.app_context():
        db.create_all()


# ============================================
# MODELO DE DATOS - ProductoDB
# Clase que mapea a la tabla 'productos_sqlalchemy' en SQLite
# ============================================

class ProductoDB(db.Model):
    """
    Modelo de datos para productos usando SQLAlchemy ORM.

    Cada instancia de esta clase representa una fila en la tabla
    'productos_sqlalchemy' de la base de datos SQLite.

    Atributos (columnas de la tabla):
        id (int): Clave primaria, autoincremental.
        nombre (str): Nombre del producto. No puede ser nulo.
        precio (float): Precio unitario del producto.
        cantidad (int): Unidades disponibles en stock.
        descripcion (str): Descripción opcional del producto.
    """

    # Nombre de la tabla en SQLite
    __tablename__ = 'productos_sqlalchemy'

    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False, default=0.0)
    cantidad = db.Column(db.Integer, nullable=False, default=0)
    descripcion = db.Column(db.String(500), default='')

    def to_dict(self):
        """
        Convierte el modelo a un diccionario Python.
        Útil para pasar datos a plantillas Jinja2.

        Returns:
            dict: Diccionario con los atributos del producto.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'descripcion': self.descripcion
        }

    def __repr__(self):
        """Representación en texto del producto (útil para depuración)."""
        return f'<ProductoDB {self.id}: {self.nombre} - ${self.precio:.2f}>'
