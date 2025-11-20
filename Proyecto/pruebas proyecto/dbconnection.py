import psycopg2
def conectdatabase():
    try:
        connection=psycopg2.connect(
            host='localhost', #Acá si lo hosteamos habrá que cambiarlo
            user='postgres',
            password='luis2006', #Acá hay que poner la contraseña de conección a la base de datos
            database='prueba-proyCripto'
        )
        #print(f'Conección exitosa a la base de datos{connection}')
        return connection
    except Exception as ex:
        print(f'Error de conección: {ex}')

        
