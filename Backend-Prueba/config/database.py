import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo `.env` si está presente.
# Esto evita dejar credenciales en el código fuente y hace más sencillo
# cambiar entornos (desarrollo/producción).
load_dotenv()

# Configuración de la base de datos.
# Lee las credenciales y parámetros de conexión desde variables de entorno.
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "Votacion"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD")
}

@contextmanager
def get_db_connection():
    """
    Context manager para manejar conexiones a PostgreSQL
    
    Uso:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            ...
    """
    # Inicializamos la variable de conexión. Se asigna cuando `connect` tiene éxito.
    conexion = None
    try:
        # Abrir la conexión usando la configuración y un cursor que retorna dicts
        conexion = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        # Entregar la conexión al bloque `with` del llamador
        yield conexion
    except psycopg2.Error as e:
        # Si ocurre un error de la base de datos, revertir cualquier transacción
        # abierta y propagar la excepción para que el llamador la maneje.
        if conexion:
            conexion.rollback()
        raise e
    finally:
        # Asegurarse de cerrar la conexión al salir del contexto
        if conexion:
            conexion.close()

def test_connection():
    """Probar la conexión a la base de datos"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Conexión exitosa a PostgreSQL")
            print(f"Versión: {version['version']}")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False