import psycopg2
def conectdatabase():
    try:
        
        connection = psycopg2.connect("postgresql://postgres.yeefgklxezuefsdeenck:kr2XYOyITOTBVAjd@aws-1-us-east-1.pooler.supabase.com:6543/postgres") #-- Conexión a la base de datos Supabase
        """
        Docstring for conectdatabase
        connection = psycopg2.connect( #-- Conexión a la base de datos local
            host="localhost",
            user="postgres",
            password="luis2006",
            database="prueba-proyCripto"
        )
        """
        #print(f'Conección exitosa a la base de datos{connection}')
        return connection
    except Exception as ex:
        print(f'Error de conexión: {ex}') 