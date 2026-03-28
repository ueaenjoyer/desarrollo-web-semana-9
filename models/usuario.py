# ============================================
# Modelo: Usuario
# Semana 15 - TechByte
# ============================================

class Usuario:
    """
    Representa un usuario administrador del sistema.

    Atributos:
        id_usuario (int): Identificador único.
        nombre (str): Nombre del usuario.
        mail (str): Correo electrónico (único).
        password (str): Contraseña hasheada.
    """

    def __init__(self, id_usuario, nombre, mail, password=""):
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._mail = mail
        self._password = password

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if valor and isinstance(valor, str):
            self._nombre = valor

    @property
    def mail(self):
        return self._mail

    @mail.setter
    def mail(self, valor):
        if valor and isinstance(valor, str):
            self._mail = valor

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, valor):
        self._password = str(valor)

    def to_dict(self):
        """Convierte el usuario a un diccionario (sin password)."""
        return {
            "id_usuario": self._id_usuario,
            "nombre": self._nombre,
            "mail": self._mail,
        }

    def __repr__(self):
        return f"Usuario(id={self._id_usuario}, nombre='{self._nombre}')"
