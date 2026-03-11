# ============================================
# conexion.py - Configuración de Conexión a PostgreSQL (Supabase)
# Semana 13 - TechByte
# ============================================
#
# Este archivo contiene la configuración de conexión entre
# Flask y la base de datos PostgreSQL en Supabase.
#
# Soporta dos modos de configuración:
#   1. DATABASE_URL (variable única) → para Render, Vercel, etc.
#   2. Variables individuales (user, password, host, port, dbname) → local con .env
# ============================================

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Cargamos las variables de entorno desde el archivo .env (solo funciona en local)
# En Render/producción las variables se configuran en el dashboard
load_dotenv()

# ============================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================

# Opción 1: DATABASE_URL completa (preferida para hosting como Render)
DATABASE_URL = os.getenv('DATABASE_URL')

# Opción 2: Variables individuales (para desarrollo local con .env)
DB_USER = os.getenv('user')
DB_PASSWORD = os.getenv('password')
DB_HOST = os.getenv('host')
DB_PORT = os.getenv('port', '5432')
DB_NAME = os.getenv('dbname', 'postgres')

# Si no hay DATABASE_URL, la construimos desde las variables individuales
if not DATABASE_URL and DB_HOST:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# URI para SQLAlchemy (Flask-SQLAlchemy)
SQLALCHEMY_DATABASE_URI = DATABASE_URL


def get_connection():
    """
    Crea y retorna una conexión directa a PostgreSQL usando psycopg2.

    Usa RealDictCursor para que los resultados se retornen como
    diccionarios (acceso por nombre de columna en vez de índice).

    Returns:
        psycopg2.connection: Conexión activa a la base de datos PostgreSQL.
    """
    if not DATABASE_URL:
        raise ValueError(
            "❌ No se encontró configuración de base de datos.\n"
            "   LOCAL: Configura el archivo .env con user, password, host, port, dbname\n"
            "   RENDER: Configura DATABASE_URL en Environment Variables del dashboard"
        )

    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
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
