from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2

from config.database import get_db_connection
from models.schemas import EleccionCreate, EleccionResponse, EleccionEstadoUpdate, MessageResponse

router = APIRouter(
    prefix="/elecciones",
    tags=["Elecciones"]
)

@router.post("/", response_model=MessageResponse, status_code=201)
def crear_eleccion(eleccion: EleccionCreate):
    """Crear una nueva elección"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO elecciones (nombre_eleccion, descripcion, fecha_inicio, fecha_fin, estado)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id_eleccion
            """
            cursor.execute(query, (
                eleccion.nombre_eleccion, 
                eleccion.descripcion,
                eleccion.fecha_inicio, 
                eleccion.fecha_fin, 
                eleccion.estado
            ))
            id_eleccion = cursor.fetchone()['id_eleccion']
            conn.commit()
            return MessageResponse(
                message="Elección creada exitosamente",
                id=id_eleccion
            )
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al crear elección: {str(e)}")

@router.get("/", response_model=List[dict])
def listar_elecciones():
    """Obtener todas las elecciones"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM elecciones ORDER BY fecha_creacion DESC")
        elecciones = cursor.fetchall()
        return elecciones

@router.get("/activas", response_model=List[dict])
def listar_elecciones_activas():
    """Obtener solo las elecciones activas"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM elecciones WHERE estado = 'activa' ORDER BY fecha_inicio"
        )
        elecciones = cursor.fetchall()
        return elecciones

@router.get("/{id_eleccion}", response_model=dict)
def obtener_eleccion(id_eleccion: int):
    """Obtener información de una elección específica"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM elecciones WHERE id_eleccion = %s", (id_eleccion,))
        eleccion = cursor.fetchone()
        
        if not eleccion:
            raise HTTPException(status_code=404, detail="Elección no encontrada")
        
        return eleccion

@router.put("/{id_eleccion}/estado", response_model=MessageResponse)
def actualizar_estado_eleccion(id_eleccion: int, estado_update: EleccionEstadoUpdate):
    """Actualizar el estado de una elección (pendiente, activa, cerrada)"""
    estados_validos = ['pendiente', 'activa', 'cerrada']
    
    if estado_update.estado not in estados_validos:
        raise HTTPException(
            status_code=400, 
            detail=f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
        )
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE elecciones SET estado = %s WHERE id_eleccion = %s",
                (estado_update.estado, id_eleccion)
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Elección no encontrada")
            conn.commit()
            return MessageResponse(
                message=f"Estado de la elección actualizado a '{estado_update.estado}'"
            )
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id_eleccion}", response_model=MessageResponse)
def actualizar_eleccion(id_eleccion: int, eleccion: EleccionCreate):
    """Actualizar información completa de una elección"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            query = """
                UPDATE elecciones 
                SET nombre_eleccion = %s, 
                    descripcion = %s, 
                    fecha_inicio = %s, 
                    fecha_fin = %s,
                    estado = %s
                WHERE id_eleccion = %s
            """
            cursor.execute(query, (
                eleccion.nombre_eleccion,
                eleccion.descripcion,
                eleccion.fecha_inicio,
                eleccion.fecha_fin,
                eleccion.estado,
                id_eleccion
            ))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Elección no encontrada")
            conn.commit()
            return MessageResponse(message="Elección actualizada exitosamente")
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_eleccion}", response_model=MessageResponse)
def eliminar_eleccion(id_eleccion: int):
    """Eliminar una elección (y todos sus datos relacionados en cascada)"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM elecciones WHERE id_eleccion = %s", (id_eleccion,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Elección no encontrada")
            conn.commit()
            return MessageResponse(message="Elección eliminada exitosamente")
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al eliminar elección: {str(e)}")