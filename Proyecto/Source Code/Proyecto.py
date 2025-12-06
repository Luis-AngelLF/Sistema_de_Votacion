from dbconnection import conectdatabase 
from phe import paillier
# Función para buscar clientes en la base de datos
def BusquedaClientes():
    print("------------------------------")
    try:
        ced = input("Ingrese su número de cédula: ").strip()
        if not ced.isdigit():
            raise ValueError

        db = conectdatabase()
        if not db:
            print("No se pudo conectar a la base de datos.")
            return None

        cursor = db.cursor()
        cursor.execute("SELECT id_usuario, cedula, nombre, apellido1, apellido2 FROM usuarios WHERE cedula=%s", (ced,))
        datos = cursor.fetchall()

        for row in datos:
            print(f"ID: {row[0]}")
            print(f"Cédula: {row[1]}")
            print(f"Nombre: {row[2]}")
            print(f"1er Apellido: {row[3]}")
            print(f"2do Apellido: {row[4]}")

        cursor.close()
        db.close()
        print("------------------------------")
        return datos

    except ValueError:
        print("ERROR: Por favor, ingrese un número de cédula válido. SIN ESPACIOS")
        return BusquedaClientes()
    except Exception as ex:
        print(f"Error en la consulta: {ex}")
        return None
# Función para mostrar los candidatos disponibles
def mostrar_candidatos():
    print("Candidatos para las elecciones: ")
    try:
        db=conectdatabase()
        if not db:
            print("No se pudo conectar a la base de datos.")
            return
        cursor=db.cursor()
        cursor.execute(
            "SELECT usuarios.id_usuario, usuarios.nombre, usuarios.apellido1, usuarios.apellido2 "
            "FROM usuarios "
            "INNER JOIN Candidatos ON usuarios.id_usuario = Candidatos.id_usuario "
            "WHERE rol = 'candidato'"
        )
        candidatos=cursor.fetchall()
        cursor.close()
        db.close()
        print("------------------------------")
        print("Lista de Candidatos:")
        for candidato in candidatos:
            print(f"ID Candidato: {candidato[0]}, Nombre: {candidato[1]} {candidato[2]} {candidato[3]}")
    except Exception as ex:
        print(f"Error de conexión a la base de datos: {ex}")
        return
# Función principal para realizar la votación
def votar():
    db=conectdatabase()
    if not db:
        print("No se pudo conectar a la base de datos.")
        return
    mostrar_candidatos()
    datos_usuario = BusquedaClientes()
    if not datos_usuario:
        print("No se encontraron datos del usuario.")
        print("------------------------------")
        votar()
        return
    try:
        public_key, private_key = paillier.generate_paillier_keypair()
        print("Clave pública:", public_key)
        print("Clave privada:", private_key)

        voto = int(input("Ingrese su voto (1-4): "))
        if voto < 1 or voto > 4:
            raise ValueError("El voto debe estar entre 1 y 4.")
        cursor=db.cursor()
        cursor.execute(
                    "SELECT usuarios.id_usuario, usuarios.nombre, usuarios.apellido1, usuarios.apellido2 "
                    "FROM usuarios "
                    "INNER JOIN Candidatos ON usuarios.id_usuario = Candidatos.id_usuario "
                    "WHERE id_candidato=%s", (voto,))
        candidato=cursor.fetchall()
        if not candidato:
            raise ValueError("Candidato no válido. Por favor, intente de nuevo.")
            votar()
            return
        cursor.close()
        db.close()
        voto_encriptado = public_key.encrypt(voto)
        print(f"Voto encriptado: { voto_encriptado.ciphertext() } ")
        print(f"Voto desencriptado: { private_key.decrypt(voto_encriptado) } ")
        for row in candidato:
            print(f"El usuario {datos_usuario[0][2]} ha votado correctamente. Por el candidato con ID: {row[0]} Nombre: {row[1]} {row[2]} {row[3]}")
        print("------------------------------")
        print("Gracias por su participación.")
    except ValueError as ve:
        print(f"Error: {ve}")
        
if __name__ == "__main__":
    votar()