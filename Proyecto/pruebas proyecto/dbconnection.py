import psycopg2
def conectdatabase():
    try:
        connection=psycopg2.connect(
            host='localhost',
            user='postgres',
            password='luis2006',
            database='prueba-proyCripto'
        )
        #print(f'Conección exitosa a la base de datos{connection}')
        return connection
    except Exception as ex:
        print(f'Error de conección: {ex}')
        