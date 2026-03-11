# ============================================
# conexion.py - Configuración de Conexión a PostgreSQL (Supabase)
# Semana 13 - TechByte
# ============================================
#
# Este archivo contiene la configuración de conexión entre
# Flask y la base de datos PostgreSQL en Supabase.
#
# Las credenciales se leen desde el archivo .env para
# mantener la seguridad (nunca se suben a GitHub).
# ============================================

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Cargamos las variables de entorno desde el archivo .env
# load_dotenv() busca el archivo .env en la carpeta del proyecto
load_dotenv()

# ============================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# Variables individuales leídas desde .env
# ============================================

DB_USER = os.getenv('user')
DB_PASSWORD = os.getenv('password')
DB_HOST = os.getenv('host')
DB_PORT = os.getenv('port', '5432')
DB_NAME = os.getenv('dbname', 'postgres')

# URI para SQLAlchemy (Flask-SQLAlchemy)
# SQLAlchemy usa esta URI para conectarse automáticamente
SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def get_connection():
    """
    Crea y retorna una conexión directa a PostgreSQL usando psycopg2.

    Usa RealDictCursor para que los resultados se retornen como
    diccionarios (acceso por nombre de columna en vez de índice).

    Returns:
        psycopg2.connection: Conexión activa a la base de datos PostgreSQL.

    Raises:
        Exception: Si no se puede conectar (credenciales inválidas, etc.)
    """
    if not DB_HOST or DB_HOST == 'PEGA_AQUI_EL_HOST_DEL_SESSION_POOLER':
        raise ValueError(
            "❌ No se encontró el host de la base de datos en el archivo .env\n"
            "   Asegúrate de configurar el archivo .env con tus credenciales de Supabase.\n"
            "   Ve a Supabase → Project Settings → Database → Session Pooler → View parameters"
        )

    conn = psycopg2.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        cursor_factory=RealDictCursor
    )
    return conn


def verificar_conexion():
    """
    Verifica que la conexión a la base de datos funcione correctamente.

    Returns:
        bool: True si la conexión es exitosa, False si falla.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT NOW()")
        resultado = cursor.fetchone()
        print(f"✅ Conexión a PostgreSQL (Supabase) exitosa!")
        print(f"   Hora del servidor: {resultado['now']}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error al conectar a PostgreSQL: {e}")
        return False


# ============================================
# Si ejecutas este archivo directamente, verifica la conexión
# ============================================
if __name__ == "__main__":
    verificar_conexion()
