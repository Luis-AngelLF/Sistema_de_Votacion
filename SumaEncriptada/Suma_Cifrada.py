from phe import paillier

def generate_keys():
    # 1. Generar las claves pública y privada
    public_key, private_key = paillier.generate_paillier_keypair()

    print("--- Claves Generadas ---")
    print(f"Clave Pública (n): {public_key.n}")
    print(f"Clave Privada: {private_key}")
    print("-" * 30)
    return public_key, private_key

def cifrar_y_sumar(public_key, private_key):
    # 2. Cifrar dos mensajes
    def sumar_enteros():
        while True:
            try:
                m1 = int(input("Ingrese un número para la suma (m1): "))
                m2 = int(input("Ingrese otro número para la suma (m2): "))
                return m1, m2
            except ValueError:
                print("ERROR: Por favor, ingrese números enteros válidos. Se intentará de nuevo.")
                continue

    m1, m2 = sumar_enteros()
        
    ciphertext1 = public_key.encrypt(m1)
    ciphertext2 = public_key.encrypt(m2)

    print(f"Mensaje 1 (m1): {m1}")
    print(f"Cifrado 1 (c1): {ciphertext1.ciphertext()}")
    print(f"Mensaje 2 (m2): {m2}")
    print(f"Cifrado 2 (c2): {ciphertext2.ciphertext()}")
    print("-" * 30)

    # 3. Suma homomórfica (m1 + m2)
    result_ciphertext = ciphertext1 + ciphertext2

    # 4. Descifrar los resultados
    plaintext_c1 = private_key.decrypt(ciphertext1)
    plaintext_c2 = private_key.decrypt(ciphertext2)
    plaintext_result = private_key.decrypt(result_ciphertext)

    print("--- Verificación ---")
    print(f"Descifrado de c1: {plaintext_c1} (igual a m1)")
    print(f"Descifrado de c2: {plaintext_c2} (igual a m2)")
    print(f"Descifrado del resultado: {plaintext_result} (igual a {m1} + {m2} = {m1 + m2})")

if __name__ == "__main__":
    public_key, private_key = generate_keys()
    cifrar_y_sumar(public_key, private_key)
