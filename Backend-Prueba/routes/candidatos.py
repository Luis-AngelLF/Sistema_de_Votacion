from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2

from config.database import get_db_connection
from models.schemas import CandidatoCreate, CandidatoResponse, MessageResponse

router = APIRouter(
    prefix="/candidatos",
    tags=["Candidatos"]
)

@router.post("/", response_model=MessageResponse, status_code=201)
def crear_candidato(candidato: CandidatoCreate):
    """Registrar un candidato para una elección"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO candidatos (id_eleccion, id_usuario, propuesta)
                VALUES (%s, %s, %s)
                RETURNING id_candidato
            """
            cursor.execute(query, (
                candidato.id_eleccion, 
                candidato.id_usuario, 
                candidato.propuesta
            ))
            id_candidato = cursor.fetchone()['id_candidato']
            conn.commit()
            return MessageResponse(
                message="Candidato registrado exitosamente",
                id=id_candidato
            )
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if "unq_candidato_eleccion_usuario" in str(e):
                raise HTTPException(
                    status_code=400, 
                    detail="Este usuario ya es candidato en esta elección"
                )
            raise HTTPException(status_code=400, detail=str(e))
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al registrar candidato: {str(e)}")

@router.get("/eleccion/{id_eleccion}", response_model=List[dict])
def listar_candidatos_por_eleccion(id_eleccion: int):
    """Obtener todos los candidatos de una elección específica con sus datos personales"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                c.id_candidato,
                c.id_eleccion,
                c.id_usuario,
                c.propuesta,
                c.fecha_registro,
                u.cedula,
                u.nombre,
                u.apellido1,
                u.apellido2,
                u.correo
            FROM candidatos c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE c.id_eleccion = %s
            ORDER BY c.fecha_registro
        """
        cursor.execute(query, (id_eleccion,))
        candidatos = cursor.fetchall()
        return candidatos

@router.get("/{id_candidato}", response_model=dict)
def obtener_candidato(id_candidato: int):
    """Obtener información detallada de un candidato específico"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                c.id_candidato,
                c.id_eleccion,
                c.id_usuario,
                c.propuesta,
                c.fecha_registro,
                u.cedula,
                u.nombre,
                u.apellido1,
                u.apellido2,
                u.correo,
                e.nombre_eleccion,
                e.estado as estado_eleccion
            FROM candidatos c
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            JOIN elecciones e ON c.id_eleccion = e.id_eleccion
            WHERE c.id_candidato = %s
        """
        cursor.execute(query, (id_candidato,))
        candidato = cursor.fetchone()
        
        if not candidato:
            raise HTTPException(status_code=404, detail="Candidato no encontrado")
        
        return candidato

@router.get("/usuario/{id_usuario}", response_model=List[dict])
def listar_candidaturas_usuario(id_usuario: int):
    """Obtener todas las elecciones en las que un usuario es candidato"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                c.id_candidato,
                c.id_eleccion,
                c.propuesta,
                c.fecha_registro,
                e.nombre_eleccion,
                e.estado,
                e.fecha_inicio,
                e.fecha_fin
            FROM candidatos c
            JOIN elecciones e ON c.id_eleccion = e.id_eleccion
            WHERE c.id_usuario = %s
            ORDER BY e.fecha_inicio DESC
        """
        cursor.execute(query, (id_usuario,))
        candidaturas = cursor.fetchall()
        return candidaturas

@router.put("/{id_candidato}/propuesta", response_model=MessageResponse)
def actualizar_propuesta(id_candidato: int, propuesta: str):
    """Actualizar la propuesta de un candidato"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE candidatos SET propuesta = %s WHERE id_candidato = %s",
                (propuesta, id_candidato)
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Candidato no encontrado")
            conn.commit()
            return MessageResponse(message="Propuesta actualizada exitosamente")
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_candidato}", response_model=MessageResponse)
def eliminar_candidato(id_candidato: int):
    """Eliminar un candidato de una elección"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM candidatos WHERE id_candidato = %s", (id_candidato,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Candidato no encontrado")
            conn.commit()
            return MessageResponse(message="Candidato eliminado exitosamente")
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al eliminar candidato: {str(e)}")