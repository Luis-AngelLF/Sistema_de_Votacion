from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2

from config.database import get_db_connection
from models.schemas import VotoCreate, VotoResponse, VotoVerificacion, VotoConteo, MessageResponse

router = APIRouter(
    prefix="/votos",
    tags=["Votos"]
)

@router.post("/", response_model=MessageResponse, status_code=201)
def emitir_voto(voto: VotoCreate):
    """
    Emitir un voto cifrado en una elección.
    Verifica que el usuario no haya votado previamente en la misma elección.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Verificar que el usuario no haya votado ya
            cursor.execute(
                "SELECT id_voto FROM votos WHERE id_eleccion = %s AND id_usuario = %s",
                (voto.id_eleccion, voto.id_usuario)
            )
            if cursor.fetchone():
                raise HTTPException(
                    status_code=400, 
                    detail="El usuario ya ha votado en esta elección"
                )
            
            # Verificar que la elección esté activa
            cursor.execute(
                "SELECT estado FROM elecciones WHERE id_eleccion = %s",
                (voto.id_eleccion,)
            )
            eleccion = cursor.fetchone()
            if not eleccion:
                raise HTTPException(status_code=404, detail="Elección no encontrada")
            if eleccion['estado'] != 'activa':
                raise HTTPException(
                    status_code=400, 
                    detail=f"La elección no está activa. Estado actual: {eleccion['estado']}"
                )
            
            # Insertar el voto
            query = """
                INSERT INTO votos (id_eleccion, id_usuario, voto_cifrado, hash_blockchain)
                VALUES (%s, %s, %s, %s)
                RETURNING id_voto
            """
            cursor.execute(query, (
                voto.id_eleccion, 
                voto.id_usuario, 
                voto.voto_cifrado, 
                voto.hash_blockchain
            ))
            id_voto = cursor.fetchone()['id_voto']
            conn.commit()
            
            return MessageResponse(
                message="Voto registrado exitosamente",
                id=id_voto
            )
        except HTTPException:
            raise
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al emitir voto: {str(e)}")

@router.get("/eleccion/{id_eleccion}/total", response_model=VotoConteo)
def contar_votos_eleccion(id_eleccion: int):
    """Obtener el número total de votos emitidos en una elección"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) as total_votos FROM votos WHERE id_eleccion = %s",
            (id_eleccion,)
        )
        resultado = cursor.fetchone()
        return VotoConteo(
            id_eleccion=id_eleccion, 
            total_votos=resultado['total_votos']
        )

@router.get("/usuario/{id_usuario}/verificar/{id_eleccion}", response_model=VotoVerificacion)
def verificar_voto_usuario(id_usuario: int, id_eleccion: int):
    """
    Verificar si un usuario ya votó en una elección específica.
    No revela el contenido del voto, solo si existe o no.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_voto, fecha_voto FROM votos WHERE id_usuario = %s AND id_eleccion = %s",
            (id_usuario, id_eleccion)
        )
        voto = cursor.fetchone()
        
        if voto:
            return VotoVerificacion(
                ha_votado=True, 
                fecha_voto=voto['fecha_voto']
            )
        return VotoVerificacion(ha_votado=False)

@router.get("/eleccion/{id_eleccion}/cifrados", response_model=List[dict])
def obtener_votos_cifrados(id_eleccion: int):
    """
    Obtener todos los votos cifrados de una elección.
    Útil para realizar el conteo homomórfico.
    No incluye información del votante para mantener anonimato.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                id_voto,
                voto_cifrado,
                hash_blockchain,
                fecha_voto
            FROM votos
            WHERE id_eleccion = %s
            ORDER BY fecha_voto
        """
        cursor.execute(query, (id_eleccion,))
        votos = cursor.fetchall()
        return votos

@router.get("/usuario/{id_usuario}/historial", response_model=List[dict])
def historial_votos_usuario(id_usuario: int):
    """
    Obtener el historial de participación de un usuario en elecciones.
    Solo muestra en qué elecciones ha votado, no el contenido de los votos.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                v.id_voto,
                v.id_eleccion,
                v.fecha_voto,
                v.hash_blockchain,
                e.nombre_eleccion,
                e.estado
            FROM votos v
            JOIN elecciones e ON v.id_eleccion = e.id_eleccion
            WHERE v.id_usuario = %s
            ORDER BY v.fecha_voto DESC
        """
        cursor.execute(query, (id_usuario,))
        historial = cursor.fetchall()
        return historial

@router.get("/{id_voto}/verificar-blockchain", response_model=dict)
def verificar_voto_blockchain(id_voto: int):
    """
    Obtener el hash blockchain de un voto específico para verificación externa.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_voto, hash_blockchain, fecha_voto FROM votos WHERE id_voto = %s",
            (id_voto,)
        )
        voto = cursor.fetchone()
        
        if not voto:
            raise HTTPException(status_code=404, detail="Voto no encontrado")
        
        return voto

@router.delete("/{id_voto}", response_model=MessageResponse)
def eliminar_voto(id_voto: int):
    """
    Eliminar un voto (solo para casos excepcionales de administración).
    ADVERTENCIA: Esta operación puede comprometer la integridad del sistema de votación.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM votos WHERE id_voto = %s", (id_voto,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Voto no encontrado")
            conn.commit()
            return MessageResponse(message="Voto eliminado (operación administrativa)")
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al eliminar voto: {str(e)}")