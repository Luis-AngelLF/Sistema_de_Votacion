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
            "votar": "/api/votar (POST)",
            "resultados": "/api/resultados/<id_eleccion>",
            "verificar_voto": "/api/verificar-voto/<cedula>/<id_eleccion>"
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
            "c.propuesta, c.fecha_registro "
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
                "fecha_registro": candidato[6].isoformat() if candidato[6] else None
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
    """Registrar un voto encriptado (vector de votos cifrados desde el frontend)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No se recibieron datos"
            }), 400
        
        cedula = data.get('cedula')
        id_eleccion = data.get('id_eleccion')
        voto_cifrado_array = data.get('voto_cifrado')  # Array de strings cifrados

        if not cedula or not id_eleccion or not voto_cifrado_array:
            return jsonify({
                "error": "Faltan datos requeridos: cedula, id_eleccion, voto_cifrado"
            }), 400

        # Validar que voto_cifrado sea una lista
        if not isinstance(voto_cifrado_array, list) or len(voto_cifrado_array) == 0:
            return jsonify({
                "error": "voto_cifrado debe ser un array de valores cifrados"
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

        # Convertir el array de votos cifrados a JSON para almacenar
        voto_cifrado_json = json.dumps(voto_cifrado_array)

        # Generar hash para blockchain basado en el vector completo
        hash_blockchain = f"0x{hash(voto_cifrado_json + str(datetime.now()) + cedula)}"

        # Registrar el voto en la base de datos
        cursor.execute(
            "INSERT INTO votos (id_eleccion, id_usuario, voto_cifrado, hash_blockchain, fecha_voto) "
            "VALUES (%s, %s, %s, %s, %s)",
            (id_eleccion, id_usuario, voto_cifrado_json, hash_blockchain, datetime.now())
        )
        
        # Registrar en logs de auditoría
        cursor.execute(
            "INSERT INTO logs_auditoria (id_usuario, accion, detalles, hash_blockchain) "
            "VALUES (%s, %s, %s, %s)",
            (id_usuario, 'VOTO_EMITIDO', 
             f"Usuario {nombre_completo} votó en elección {eleccion[0]} (vector cifrado)", 
             hash_blockchain)
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
                "vector_size": len(voto_cifrado_array),
                "hash_blockchain": hash_blockchain,
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
    app.run(debug=True, host='0.0.0.0', port=5000)