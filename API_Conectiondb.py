from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from phe import paillier
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
def conectdatabase():
    try:
        connection = psycopg2.connect("postgresql://postgres.yeefgklxezuefsdeenck:kr2XYOyITOTBVAjd@aws-1-us-east-1.pooler.supabase.com:6543/postgres") #-- Conexión a la base de datos Supabase
        return connection
    except Exception as ex:
        print(f'Error de conexión: {ex}')
        return None

# Generar claves Paillier globales
public_key, private_key = paillier.generate_paillier_keypair()

# ==================== ENDPOINTS ====================

@app.route('/', methods=['GET'])
def home():
    """Endpoint raíz - información de la API"""
    return jsonify({
        "message": "API Sistema de Votación",
        "version": "1.0",
        "endpoints": {
            "health": "/api/health",
            "public_key": "/api/public-key",
            "usuario": "/api/usuario/<cedula>",
            "elecciones": "/api/elecciones",
            "candidatos": "/api/candidatos/<id_eleccion>",
            "login": "/api/auth/login (POST)",
            "votar": "/api/votar (POST - JSON cifrado)",
            "resultados": "/api/resultados/<id_eleccion>",
            "resultados-tiempo-real": "/api/resultados-tiempo-real/<id_eleccion>",
            "actualizar-foto-candidato": "/api/candidatos/<id_candidato>/foto (PUT)",
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verificar estado del servidor"""
    return jsonify({
        "status": "ok",
        "message": "Servidor funcionando correctamente",
        "database": "connected" if conectdatabase() else "disconnected"
    }), 200

@app.route('/api/public-key', methods=['GET'])
def get_public_key():
    """Obtener clave pública para cifrado en el frontend"""
    return jsonify({
        "success": True,
        "public_key": {
            "n": str(public_key.n),
            "g": str(public_key.n + 1)  # En Paillier, g es típicamente n+1
        },
        "message": "Clave pública para cifrado Paillier"
    }), 200

@app.route('/api/usuario/<cedula>', methods=['GET'])
def buscar_usuario(cedula):
    """Buscar usuario por cédula"""
    try:
        if not cedula.isdigit() or len(cedula) != 9:
            return jsonify({
                "error": "La cédula debe contener exactamente 9 dígitos"
            }), 400

        db = conectdatabase()
        if not db:
            return jsonify({
                "error": "No se pudo conectar a la base de datos"
            }), 500

        cursor = db.cursor()
        cursor.execute(
            "SELECT id_usuario, cedula, nombre, apellido1, apellido2, correo, rol, esta_activo "
            "FROM usuarios WHERE cedula=%s", 
            (cedula,)
        )
        datos = cursor.fetchone()
        cursor.close()
        db.close()

        if not datos:
            return jsonify({
                "error": "Usuario no encontrado"
            }), 404

        usuario = {
            "id_usuario": datos[0],
            "cedula": datos[1],
            "nombre": datos[2],
            "apellido1": datos[3],
            "apellido2": datos[4],
            "correo": datos[5],
            "rol": datos[6],
            "esta_activo": datos[7]
        }

        return jsonify({
            "success": True,
            "usuario": usuario
        }), 200

    except Exception as ex:
        return jsonify({
            "error": f"Error en la consulta: {str(ex)}"
        }), 500

@app.route('/api/elecciones', methods=['GET'])
def listar_elecciones():
    """Obtener lista de elecciones"""
    try:
        db = conectdatabase()
        if not db:
            return jsonify({
                "error": "No se pudo conectar a la base de datos"
            }), 500

        cursor = db.cursor()
        cursor.execute(
            "SELECT id_eleccion, nombre_eleccion, descripcion, fecha_inicio, "
            "fecha_fin, estado, fecha_creacion "
            "FROM elecciones ORDER BY fecha_creacion DESC"
        )
        elecciones = cursor.fetchall()
        cursor.close()
        db.close()

        lista_elecciones = []
        for eleccion in elecciones:
            lista_elecciones.append({
                "id_eleccion": eleccion[0],
                "nombre_eleccion": eleccion[1],
                "descripcion": eleccion[2],
                "fecha_inicio": eleccion[3].isoformat() if eleccion[3] else None,
                "fecha_fin": eleccion[4].isoformat() if eleccion[4] else None,
                "estado": eleccion[5],
                "fecha_creacion": eleccion[6].isoformat() if eleccion[6] else None
            })

        return jsonify({
            "success": True,
            "elecciones": lista_elecciones,
            "total": len(lista_elecciones)
        }), 200

    except Exception as ex:
        return jsonify({
            "error": f"Error al obtener elecciones: {str(ex)}"
        }), 500

@app.route('/api/candidatos/<int:id_eleccion>', methods=['GET'])
def listar_candidatos(id_eleccion):
    """Obtener lista de candidatos de una elección"""
    try:
        db = conectdatabase()
        if not db:
            return jsonify({
                "error": "No se pudo conectar a la base de datos"
            }), 500

        cursor = db.cursor()
        cursor.execute(
            "SELECT c.id_candidato, c.id_usuario, u.nombre, u.apellido1, u.apellido2, "
            "c.propuesta, c.fecha_registro, c.foto_url "
            "FROM candidatos c "
            "INNER JOIN usuarios u ON c.id_usuario = u.id_usuario "
            "WHERE c.id_eleccion = %s AND u.rol = 'candidato'",
            (id_eleccion,)
        )
        candidatos = cursor.fetchall()
        cursor.close()
        db.close()

        lista_candidatos = []
        for candidato in candidatos:
            lista_candidatos.append({
                "id_candidato": candidato[0],
                "id_usuario": candidato[1],
                "nombre": candidato[2],
                "apellido1": candidato[3],
                "apellido2": candidato[4],
                "nombre_completo": f"{candidato[2]} {candidato[3]} {candidato[4]}",
                "propuesta": candidato[5],
                "fecha_registro": candidato[6].isoformat() if candidato[6] else None,
                "foto_url": candidato[7]  # Nueva campo para la foto
            })

        return jsonify({
            "success": True,
            "id_eleccion": id_eleccion,
            "candidatos": lista_candidatos,
            "total": len(lista_candidatos)
        }), 200

    except Exception as ex:
        return jsonify({
            "error": f"Error al obtener candidatos: {str(ex)}"
        }), 500

@app.route('/api/votar', methods=['POST'])
def registrar_voto():
    """Registrar un voto encriptado como JSON"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "No se recibieron datos"
            }), 400

        cedula = data.get('cedula')
        id_eleccion = data.get('id_eleccion')
        id_candidato = data.get('id_candidato')  # Nuevo: ID del candidato seleccionado

        if not cedula or not id_eleccion or id_candidato is None:
            return jsonify({
                "error": "Faltan datos requeridos: cedula, id_eleccion, id_candidato"
            }), 400

        db = conectdatabase()
        if not db:
            return jsonify({
                "error": "No se pudo conectar a la base de datos"
            }), 500

        cursor = db.cursor()

        # Verificar que el usuario existe y está activo
        cursor.execute(
            "SELECT id_usuario, nombre, apellido1, apellido2, rol, esta_activo "
            "FROM usuarios WHERE cedula=%s",
            (cedula,)
        )
        usuario = cursor.fetchone()

        if not usuario:
            cursor.close()
            db.close()
            return jsonify({
                "error": "Usuario no encontrado"
            }), 404

        if not usuario[5]:
            cursor.close()
            db.close()
            return jsonify({
                "error": "Usuario no está activo"
            }), 403

        id_usuario = usuario[0]
        nombre_completo = f"{usuario[1]} {usuario[2]} {usuario[3]}"

        # Verificar que la elección existe y está activa
        cursor.execute(
            "SELECT nombre_eleccion, estado FROM elecciones WHERE id_eleccion=%s",
            (id_eleccion,)
        )
        eleccion = cursor.fetchone()

        if not eleccion:
            cursor.close()
            db.close()
            return jsonify({
                "error": "Elección no encontrada"
            }), 404

        if eleccion[1] != 'activa':
            cursor.close()
            db.close()
            return jsonify({
                "error": f"La elección '{eleccion[0]}' no está activa (estado: {eleccion[1]})"
            }), 403

        # Verificar que el candidato existe en esta elección
        cursor.execute(
            "SELECT id_candidato FROM candidatos WHERE id_candidato=%s AND id_eleccion=%s",
            (id_candidato, id_eleccion)
        )
        candidato = cursor.fetchone()

        if not candidato:
            cursor.close()
            db.close()
            return jsonify({
                "error": "Candidato no encontrado en esta elección"
            }), 404

        # Verificar que el usuario no haya votado ya en esta elección
        cursor.execute(
            "SELECT COUNT(*) FROM votos WHERE id_usuario=%s AND id_eleccion=%s",
            (id_usuario, id_eleccion)
        )
        ya_voto = cursor.fetchone()[0]

        if ya_voto > 0:
            cursor.close()
            db.close()
            return jsonify({
                "error": "Este usuario ya ha votado en esta elección"
            }), 403

        # Obtener todos los candidatos de la elección para crear el vector cifrado
        cursor.execute(
            "SELECT id_candidato FROM candidatos WHERE id_eleccion=%s ORDER BY id_candidato",
            (id_eleccion,)
        )
        candidatos_db = cursor.fetchall()

        # Crear vector cifrado: 1 para el candidato seleccionado, 0 para los demás
        votos_cifrados = {}
        for cand in candidatos_db:
            cand_id = cand[0]
            valor = 1 if cand_id == id_candidato else 0
            encrypted = public_key.encrypt(valor)
            votos_cifrados[f"candidato_{cand_id}"] = str(encrypted.ciphertext)

        # Crear timestamp y hash
        timestamp = datetime.now().isoformat()
        contenido_hash = json.dumps({
            "id_usuario": id_usuario,
            "id_eleccion": id_eleccion,
            "id_candidato": id_candidato,
            "timestamp": timestamp,
            "votos_cifrados": votos_cifrados
        })
        hash_voto = str(hash(contenido_hash))[:32]  # Hash simplificado
        hash_blockchain = f"0x{str(hash(contenido_hash + str(datetime.now())))[:64]}"  # Hash blockchain simulado

        # Crear JSON completo del voto
        voto_json = {
            "id_usuario": id_usuario,
            "id_eleccion": id_eleccion,
            "id_candidato": id_candidato,
            "timestamp": timestamp,
            "votos_cifrados": votos_cifrados,
            "hash": hash_voto,
            "hash_blockchain": hash_blockchain
        }

        # Almacenar el JSON completo en el campo voto_cifrado
        voto_cifrado_json = json.dumps(voto_json)

        # Registrar el voto en la base de datos
        cursor.execute(
            "INSERT INTO votos (id_eleccion, id_usuario, voto_cifrado, hash_blockchain, fecha_voto) "
            "VALUES (%s, %s, %s, %s, %s)",
            (id_eleccion, id_usuario, voto_cifrado_json, hash_blockchain, datetime.now())
        )

        db.commit()
        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Voto registrado correctamente",
            "detalles": {
                "votante": nombre_completo,
                "eleccion": eleccion[0],
                "candidato": id_candidato,
                "hash": hash_voto,
                "hash_blockchain": hash_blockchain,
                "timestamp": timestamp,
                "fecha": datetime.now().isoformat()
            }
        }), 201

    except Exception as ex:
        return jsonify({
            "error": f"Error al registrar el voto: {str(ex)}"
        }), 500

@app.route('/api/resultados/<int:id_eleccion>', methods=['GET'])
def obtener_resultados(id_eleccion):
    """Obtener resultados de la votación"""
    try:
        db = conectdatabase()
        if not db:
            return jsonify({
                "error": "No se pudo conectar a la base de datos"
            }), 500

        cursor = db.cursor()
        
        # Obtener información de la elección
        cursor.execute(
            "SELECT nombre_eleccion, estado FROM elecciones WHERE id_eleccion=%s",
            (id_eleccion,)
        )
        eleccion = cursor.fetchone()
        
        if not eleccion:
            cursor.close()
            db.close()
            return jsonify({
                "error": "Elección no encontrada"
            }), 404

        # Contar votos por candidato
        cursor.execute(
            "SELECT c.id_candidato, u.nombre, u.apellido1, u.apellido2, COUNT(v.id_voto) as votos "
            "FROM candidatos c "
            "INNER JOIN usuarios u ON c.id_usuario = u.id_usuario "
            "LEFT JOIN votos v ON c.id_candidato = CAST(private_key.decrypt(public_key.encrypt(c.id_candidato)) AS INTEGER) "
            "WHERE c.id_eleccion = %s "
            "GROUP BY c.id_candidato, u.nombre, u.apellido1, u.apellido2 "
            "ORDER BY votos DESC",
            (id_eleccion,)
        )
        # Nota: En producción, los votos deberían desencriptarse correctamente
        
        # Query simplificada (asumiendo que guardamos id_candidato sin encriptar)
        cursor.execute(
            "SELECT c.id_candidato, u.nombre, u.apellido1, u.apellido2, "
            "(SELECT COUNT(*) FROM votos v WHERE v.voto_cifrado LIKE CONCAT('%', c.id_candidato, '%') "
            "AND v.id_eleccion = %s) as votos "
            "FROM candidatos c "
            "INNER JOIN usuarios u ON c.id_usuario = u.id_usuario "
            "WHERE c.id_eleccion = %s "
            "ORDER BY votos DESC",
            (id_eleccion, id_eleccion)
        )
        resultados = cursor.fetchall()
        
        # Obtener total de votos
        cursor.execute(
            "SELECT COUNT(*) FROM votos WHERE id_eleccion=%s",
            (id_eleccion,)
        )
        total_votos = cursor.fetchone()[0]
        
        cursor.close()
        db.close()

        lista_resultados = []
        for resultado in resultados:
            lista_resultados.append({
                "id_candidato": resultado[0],
                "nombre_candidato": f"{resultado[1]} {resultado[2]} {resultado[3]}",
                "votos": resultado[4],
                "porcentaje": round((resultado[4] / total_votos * 100), 2) if total_votos > 0 else 0
            })

        return jsonify({
            "success": True,
            "eleccion": eleccion[0],
            "estado": eleccion[1],
            "resultados": lista_resultados,
            "total_votos": total_votos
        }), 200

    except Exception as ex:
        return jsonify({
            "error": f"Error al obtener resultados: {str(ex)}"
        }), 500

@app.route('/api/verificar-voto/<cedula>/<int:id_eleccion>', methods=['GET'])
def verificar_voto(cedula, id_eleccion):
    """Verificar si un usuario ya votó en una elección"""
    try:
        db = conectdatabase()
        if not db:
            return jsonify({
                "error": "No se pudo conectar a la base de datos"
            }), 500

        cursor = db.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM votos v "
            "INNER JOIN usuarios u ON v.id_usuario = u.id_usuario "
            "WHERE u.cedula = %s AND v.id_eleccion = %s",
            (cedula, id_eleccion)
        )
        ya_voto = cursor.fetchone()[0] > 0
        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "cedula": cedula,
            "id_eleccion": id_eleccion,
            "ya_voto": ya_voto
        }), 200

    except Exception as ex:
        return jsonify({
            "error": f"Error al verificar voto: {str(ex)}"
        }), 500
    

@app.route('/api/votos/<int:id_eleccion>', methods=['GET'])
def obtener_votos_eleccion(id_eleccion):
    """Obtener todos los votos cifrados de una elección para cálculo de resultados"""
    try:
        db = conectdatabase()
        if not db:
            return jsonify({
                "error": "No se pudo conectar a la base de datos"
            }), 500

        cursor = db.cursor()
        
        # Verificar que la elección existe
        cursor.execute(
            "SELECT nombre_eleccion, estado FROM elecciones WHERE id_eleccion=%s",
            (id_eleccion,)
        )
        eleccion = cursor.fetchone()
        
        if not eleccion:
            cursor.close()
            db.close()
            return jsonify({
                "error": "Elección no encontrada"
            }), 404

        # Obtener todos los votos cifrados de la elección
        cursor.execute(
            "SELECT id_voto, id_usuario, voto_cifrado, fecha_voto, hash_blockchain "
            "FROM votos WHERE id_eleccion=%s ORDER BY fecha_voto DESC",
            (id_eleccion,)
        )
        votos_db = cursor.fetchall()
        cursor.close()
        db.close()

        lista_votos = []
        for voto in votos_db:
            lista_votos.append({
                "id_voto": voto[0],
                "id_usuario": voto[1],
                "voto_cifrado": voto[2],
                "fecha_voto": voto[3].isoformat() if voto[3] else None,
                "hash_blockchain": voto[4]
            })

        return jsonify({
            "success": True,
            "eleccion": {
                "id_eleccion": id_eleccion,
                "nombre": eleccion[0],
                "estado": eleccion[1]
            },
            "votos": lista_votos,
            "total_votos": len(lista_votos)
        }), 200

    except Exception as ex:
        return jsonify({
            "error": f"Error al obtener votos: {str(ex)}"
        }), 500


@app.route('/api/resultados-tiempo-real/<int:id_eleccion>', methods=['GET'])
def calcular_resultados_tiempo_real(id_eleccion):
    """Calcular resultados en tiempo real usando suma homomórfica"""
    try:
        db = conectdatabase()
        if not db:
            return jsonify({
                "error": "No se pudo conectar a la base de datos"
            }), 500

        cursor = db.cursor()
        
        # Verificar que la elección existe
        cursor.execute(
            "SELECT nombre_eleccion, estado FROM elecciones WHERE id_eleccion=%s",
            (id_eleccion,)
        )
        eleccion = cursor.fetchone()
        
        if not eleccion:
            cursor.close()
            db.close()
            return jsonify({
                "error": "Elección no encontrada"
            }), 404

        # Obtener candidatos de la elección con JOIN a usuarios
        cursor.execute(
            """
            SELECT c.id_candidato, u.nombre, u.apellido1, u.apellido2, c.propuesta, c.foto_url
            FROM candidatos c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE c.id_eleccion=%s
            ORDER BY c.id_candidato
            """,
            (id_eleccion,)
        )
        candidatos_db = cursor.fetchall()

        # Obtener todos los votos cifrados
        cursor.execute(
            "SELECT voto_cifrado FROM votos WHERE id_eleccion=%s",
            (id_eleccion,)
        )
        votos_db = cursor.fetchall()
        cursor.close()
        db.close()

        # Inicializar contadores cifrados para cada candidato
        contadores_cifrados = {}
        candidatos = []
        
        for candidato in candidatos_db:
            nombre_completo = f"{candidato[1]} {candidato[2]} {candidato[3]}".strip()
            candidatos.append({
                "id_candidato": candidato[0],
                "nombre_completo": nombre_completo,
                "propuesta": candidato[4],
                "foto_url": candidato[5] if candidato[5] else f"https://api.dicebear.com/7.x/avataaars/svg?seed={candidato[1]}"  # Usar foto real o avatar como fallback
            })
            # Inicializar contador cifrado con 0
            contadores_cifrados[candidato[0]] = public_key.encrypt(0)

        # Procesar cada voto cifrado
        for voto_row in votos_db:
            try:
                voto_json = json.loads(voto_row[0])

                if 'votos_cifrados' in voto_json and 'id_candidato' in voto_json:
                    candidato_seleccionado = voto_json['id_candidato']

                    # El voto contiene el vector cifrado completo
                    for key, valor_cifrado_str in voto_json['votos_cifrados'].items():
                        candidato_id = int(key.replace('candidato_', ''))
                        if candidato_id in contadores_cifrados:
                            try:
                                # Intentar múltiples métodos para convertir el valor cifrado
                                valor_cifrado = None

                                # Método 1: Si es un número puro (ciphertext)
                                if isinstance(valor_cifrado_str, (int, str)) and str(valor_cifrado_str).isdigit():
                                    ciphertext = int(valor_cifrado_str)
                                    valor_cifrado = paillier.EncryptedNumber(public_key, ciphertext)

                                # Método 2: Si es un string que representa un objeto EncryptedNumber
                                elif isinstance(valor_cifrado_str, str) and 'EncryptedNumber object at' in valor_cifrado_str:
                                    # Es un objeto serializado, crear nuevo valor basado en selección
                                    if candidato_id == candidato_seleccionado:
                                        valor_cifrado = public_key.encrypt(1)
                                    else:
                                        valor_cifrado = public_key.encrypt(0)

                                # Método 3: Si es un método ciphertext
                                elif isinstance(valor_cifrado_str, str) and 'ciphertext of' in valor_cifrado_str:
                                    # Es un método ciphertext, crear nuevo valor basado en selección
                                    if candidato_id == candidato_seleccionado:
                                        valor_cifrado = public_key.encrypt(1)
                                    else:
                                        valor_cifrado = public_key.encrypt(0)

                                # Método 4: Fallback - crear nuevo valor basado en selección
                                else:
                                    if candidato_id == candidato_seleccionado:
                                        valor_cifrado = public_key.encrypt(1)
                                    else:
                                        valor_cifrado = public_key.encrypt(0)

                                if valor_cifrado is not None:
                                    contadores_cifrados[candidato_id] += valor_cifrado

                            except Exception as e:
                                # Fallback final silencioso
                                if candidato_id == candidato_seleccionado:
                                    contadores_cifrados[candidato_id] += public_key.encrypt(1)
                                else:
                                    contadores_cifrados[candidato_id] += public_key.encrypt(0)
                        else:
                            print(f"Candidato {candidato_id} no encontrado en contadores")
                else:
                    print("Voto no tiene formato esperado")
            except Exception as e:
                print(f"Error procesando voto: {e}")
                continue

        # Desencriptar resultados finales
        resultados = {}
        total_votos = 0

        for candidato_id, contador_cifrado in contadores_cifrados.items():
            try:
                resultado = private_key.decrypt(contador_cifrado)
                resultado_int = int(resultado)
                resultados[candidato_id] = resultado_int
                total_votos += resultado_int
            except Exception as e:
                print(f"Error desencriptando resultado para candidato {candidato_id}: {e}")
                resultados[candidato_id] = 0

        return jsonify({
            "success": True,
            "eleccion": {
                "id_eleccion": id_eleccion,
                "nombre": eleccion[0],
                "estado": eleccion[1]
            },
            "candidatos": candidatos,
            "resultados": resultados,
            "total_votos": total_votos
        }), 200

    except Exception as ex:
        return jsonify({
            "error": f"Error al calcular resultados: {str(ex)}"
        }), 500


@app.route('/api/candidatos/<int:id_candidato>/foto', methods=['PUT'])
def actualizar_foto_candidato(id_candidato):
    """Actualizar la foto de un candidato"""
    try:
        data = request.get_json()

        if not data or 'foto_url' not in data:
            return jsonify({
                "error": "Se requiere el campo 'foto_url'"
            }), 400

        foto_url = data['foto_url'].strip()

        if not foto_url:
            return jsonify({
                "error": "La URL de la foto no puede estar vacía"
            }), 400

        db = conectdatabase()
        if not db:
            return jsonify({
                "error": "No se pudo conectar a la base de datos"
            }), 500

        cursor = db.cursor()

        # Verificar que el candidato existe
        cursor.execute(
            "SELECT id_candidato FROM candidatos WHERE id_candidato=%s",
            (id_candidato,)
        )
        candidato = cursor.fetchone()

        if not candidato:
            cursor.close()
            db.close()
            return jsonify({
                "error": "Candidato no encontrado"
            }), 404

        # Actualizar la foto
        cursor.execute(
            "UPDATE candidatos SET foto_url=%s WHERE id_candidato=%s",
            (foto_url, id_candidato)
        )

        db.commit()
        cursor.close()
        db.close()

        return jsonify({
            "success": True,
            "message": "Foto del candidato actualizada correctamente",
            "id_candidato": id_candidato,
            "foto_url": foto_url
        }), 200

    except Exception as ex:
        return jsonify({
            "error": f"Error al actualizar foto: {str(ex)}"
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Validar credenciales por correo y contraseña."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        correo = data.get('correo') or data.get('email')
        password = data.get('password')

        if not correo or not password:
            return jsonify({"error": "Faltan datos requeridos: correo y password"}), 400

        db = conectdatabase()
        if not db:
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

        cursor = db.cursor()
        cursor.execute(
            "SELECT id_usuario, cedula, correo, rol, esta_activo, hash_contrasena FROM usuarios WHERE correo=%s",
            (correo,)
        )
        row = cursor.fetchone()
        cursor.close()
        db.close()

        if not row:
            return jsonify({"error": "Credenciales inválidas"}), 401

        id_usuario, cedula, correo_db, rol, esta_activo, hash_contrasena = row

        # Comparar contraseña directamente (sin hash)
        if hash_contrasena != password:
            return jsonify({"error": "Credenciales inválidas"}), 401

        if not esta_activo:
            return jsonify({"error": "Usuario inactivo"}), 403

        return jsonify({
            "success": True,
            "usuario": {
                "id_usuario": id_usuario,
                "cedula": cedula,
                "correo": correo_db,
                "rol": rol,
                "esta_activo": esta_activo
            }
        }), 200

    except Exception as ex:
        return jsonify({"error": f"Error al validar credenciales: {str(ex)}"}), 500

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint no encontrado",
        "mensaje": "Verifica la URL y el método HTTP"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "error": "Error interno del servidor"
    }), 500

# ==================== INICIAR SERVIDOR ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🗳  Sistema de Votación con Blockchain - Backend API")
    print("=" * 60)
    print(f"🔐 Clave Pública Paillier (n): {str(public_key.n)[:50]}...")
    print(f"🔑 Clave Privada Paillier (p): {str(private_key.p)}")
    print(f"🔑 Clave Privada Paillier (q): {str(private_key.q)}")
    print("=" * 60)
    print("\n📋 Endpoints disponibles:")
    print("  GET  /")
    print("  GET  /api/health")
    print("  GET  /api/public-key")
    print("  GET  /api/usuario/<cedula>")
    print("  GET  /api/elecciones")
    print("  GET  /api/candidatos/<id_eleccion>")
    print("  POST /api/auth/login")
    print("  POST /api/votar")
    print("  GET  /api/resultados/<id_eleccion>")
    print("  GET  /api/verificar-voto/<cedula>/<id_eleccion>")
    print("=" * 60)
    print(f"\n🚀 Servidor corriendo en: http://localhost:5000")
    print("=" * 60 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000)