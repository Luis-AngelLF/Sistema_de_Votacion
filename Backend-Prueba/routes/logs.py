from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import psycopg2

from config.database import get_db_connection
from models.schemas import LogCreate, LogResponse, MessageResponse

router = APIRouter(
    prefix="/logs",
    tags=["Logs de Auditoría"]
)

@router.post("/", response_model=MessageResponse, status_code=201)
def crear_log(log: LogCreate):
    """
    Registrar un nuevo log de auditoría en el sistema.
    Puede incluir o no un usuario asociado (para logs del sistema).
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO logs_auditoria (id_usuario, accion, detalles, hash_blockchain)
                VALUES (%s, %s, %s, %s)
                RETURNING id_log
            """
            cursor.execute(query, (
                log.id_usuario, 
                log.accion, 
                log.detalles, 
                log.hash_blockchain
            ))
            id_log = cursor.fetchone()['id_log']
            conn.commit()
            return MessageResponse(
                message="Log registrado exitosamente",
                id=id_log
            )
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al crear log: {str(e)}")

@router.get("/", response_model=List[dict])
def listar_logs(
    limit: int = Query(100, description="Número máximo de logs a retornar"),
    accion: Optional[str] = Query(None, description="Filtrar por tipo de acción")
):
    """
    Obtener los logs de auditoría más recientes.
    Permite filtrar por tipo de acción y limitar resultados.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        if accion:
            query = """
                SELECT 
                    l.id_log,
                    l.id_usuario,
                    l.fecha_hora,
                    l.accion,
                    l.detalles,
                    l.hash_blockchain,
                    u.nombre,
                    u.apellido1,
                    u.correo
                FROM logs_auditoria l
                LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
                WHERE l.accion = %s
                ORDER BY l.fecha_hora DESC
                LIMIT %s
            """
            cursor.execute(query, (accion, limit))
        else:
            query = """
                SELECT 
                    l.id_log,
                    l.id_usuario,
                    l.fecha_hora,
                    l.accion,
                    l.detalles,
                    l.hash_blockchain,
                    u.nombre,
                    u.apellido1,
                    u.correo
                FROM logs_auditoria l
                LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
                ORDER BY l.fecha_hora DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
        
        logs = cursor.fetchall()
        return logs

@router.get("/usuario/{id_usuario}", response_model=List[dict])
def listar_logs_usuario(id_usuario: int, limit: int = Query(50, description="Número máximo de logs")):
    """
    Obtener todos los logs de auditoría de un usuario específico.
    Útil para ver el historial de actividad de un usuario.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                id_log,
                id_usuario,
                fecha_hora,
                accion,
                detalles,
                hash_blockchain
            FROM logs_auditoria 
            WHERE id_usuario = %s 
            ORDER BY fecha_hora DESC
            LIMIT %s
        """
        cursor.execute(query, (id_usuario, limit))
        logs = cursor.fetchall()
        return logs

@router.get("/accion/{accion}", response_model=List[dict])
def listar_logs_por_accion(accion: str, limit: int = Query(100, description="Número máximo de logs")):
    """
    Obtener logs filtrados por un tipo de acción específico.
    Ejemplos: LOGIN, VOTO_EMITIDO, CREAR_ELECCION, etc.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                l.id_log,
                l.id_usuario,
                l.fecha_hora,
                l.accion,
                l.detalles,
                l.hash_blockchain,
                u.nombre,
                u.apellido1
            FROM logs_auditoria l
            LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
            WHERE l.accion = %s
            ORDER BY l.fecha_hora DESC
            LIMIT %s
        """
        cursor.execute(query, (accion, limit))
        logs = cursor.fetchall()
        return logs

@router.get("/fecha-rango/", response_model=List[dict])
def listar_logs_por_fecha(
    fecha_inicio: str = Query(..., description="Fecha inicio en formato YYYY-MM-DD HH:MM:SS"),
    fecha_fin: str = Query(..., description="Fecha fin en formato YYYY-MM-DD HH:MM:SS")
):
    """
    Obtener logs dentro de un rango de fechas específico.
    Útil para auditorías y reportes periódicos.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                l.id_log,
                l.id_usuario,
                l.fecha_hora,
                l.accion,
                l.detalles,
                l.hash_blockchain,
                u.nombre,
                u.apellido1
            FROM logs_auditoria l
            LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
            WHERE l.fecha_hora BETWEEN %s AND %s
            ORDER BY l.fecha_hora DESC
        """
        cursor.execute(query, (fecha_inicio, fecha_fin))
        logs = cursor.fetchall()
        return logs

@router.get("/estadisticas", response_model=dict)
def obtener_estadisticas_logs():
    """
    Obtener estadísticas generales de los logs de auditoría.
    Incluye conteo por tipo de acción y actividad reciente.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Total de logs
        cursor.execute("SELECT COUNT(*) as total FROM logs_auditoria")
        total_logs = cursor.fetchone()['total']
        
        # Logs por acción
        cursor.execute("""
            SELECT accion, COUNT(*) as cantidad
            FROM logs_auditoria
            GROUP BY accion
            ORDER BY cantidad DESC
        """)
        por_accion = cursor.fetchall()
        
        # Logs de hoy
        cursor.execute("""
            SELECT COUNT(*) as hoy
            FROM logs_auditoria
            WHERE DATE(fecha_hora) = CURRENT_DATE
        """)
        logs_hoy = cursor.fetchone()['hoy']
        
        # Usuarios más activos
        cursor.execute("""
            SELECT 
                u.nombre,
                u.apellido1,
                COUNT(l.id_log) as actividad
            FROM logs_auditoria l
            JOIN usuarios u ON l.id_usuario = u.id_usuario
            GROUP BY u.id_usuario, u.nombre, u.apellido1
            ORDER BY actividad DESC
            LIMIT 5
        """)
        usuarios_activos = cursor.fetchall()
        
        return {
            "total_logs": total_logs,
            "logs_hoy": logs_hoy,
            "distribucion_por_accion": por_accion,
            "usuarios_mas_activos": usuarios_activos
        }

@router.get("/{id_log}", response_model=dict)
def obtener_log(id_log: int):
    """
    Obtener información detallada de un log específico.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                l.id_log,
                l.id_usuario,
                l.fecha_hora,
                l.accion,
                l.detalles,
                l.hash_blockchain,
                u.nombre,
                u.apellido1,
                u.correo
            FROM logs_auditoria l
            LEFT JOIN usuarios u ON l.id_usuario = u.id_usuario
            WHERE l.id_log = %s
        """
        cursor.execute(query, (id_log,))
        log = cursor.fetchone()
        
        if not log:
            raise HTTPException(status_code=404, detail="Log no encontrado")
        
        return log

@router.delete("/antiguo/{dias}", response_model=MessageResponse)
def eliminar_logs_antiguos(dias: int):
    """
    Eliminar logs más antiguos que X días.
    ADVERTENCIA: Esta operación es irreversible.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            query = """
                DELETE FROM logs_auditoria 
                WHERE fecha_hora < NOW() - INTERVAL '%s days'
            """
            cursor.execute(query, (dias,))
            count = cursor.rowcount
            conn.commit()
            return MessageResponse(
                message=f"Se eliminaron {count} log(s) con más de {dias} días de antigüedad"
            )
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al eliminar logs: {str(e)}")