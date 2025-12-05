from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2

from config.database import get_db_connection
from models.schemas import ResultadoCreate, ResultadoResponse, MessageResponse

router = APIRouter(
    prefix="/resultados",
    tags=["Resultados"]
)

@router.post("/", response_model=MessageResponse, status_code=201)
def guardar_resultado(resultado: ResultadoCreate):
    """
    Guardar o actualizar el resultado cifrado de un candidato en una elección.
    Este resultado es la suma homomórfica de todos los votos.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO resultados (id_eleccion, id_candidato, resultado_cifrado, hash_blockchain)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_eleccion, id_candidato) 
                DO UPDATE SET 
                    resultado_cifrado = EXCLUDED.resultado_cifrado,
                    hash_blockchain = EXCLUDED.hash_blockchain,
                    fecha_calculo = NOW()
                RETURNING id_eleccion, id_candidato
            """
            cursor.execute(query, (
                resultado.id_eleccion, 
                resultado.id_candidato, 
                resultado.resultado_cifrado, 
                resultado.hash_blockchain
            ))
            result = cursor.fetchone()
            conn.commit()
            return MessageResponse(
                message="Resultado guardado exitosamente",
                id=result['id_candidato']
            )
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al guardar resultado: {str(e)}")

@router.get("/eleccion/{id_eleccion}", response_model=List[dict])
def obtener_resultados_eleccion(id_eleccion: int):
    """
    Obtener todos los resultados cifrados de una elección con información de candidatos.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                r.id_eleccion,
                r.id_candidato,
                r.resultado_cifrado,
                r.hash_blockchain,
                r.fecha_calculo,
                c.propuesta,
                u.cedula,
                u.nombre,
                u.apellido1,
                u.apellido2
            FROM resultados r
            JOIN candidatos c ON r.id_candidato = c.id_candidato
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE r.id_eleccion = %s
            ORDER BY r.fecha_calculo DESC
        """
        cursor.execute(query, (id_eleccion,))
        resultados = cursor.fetchall()
        return resultados

@router.get("/eleccion/{id_eleccion}/candidato/{id_candidato}", response_model=dict)
def obtener_resultado_candidato(id_eleccion: int, id_candidato: int):
    """
    Obtener el resultado cifrado específico de un candidato en una elección.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                r.id_eleccion,
                r.id_candidato,
                r.resultado_cifrado,
                r.hash_blockchain,
                r.fecha_calculo,
                c.propuesta,
                u.nombre,
                u.apellido1,
                u.apellido2,
                e.nombre_eleccion,
                e.estado
            FROM resultados r
            JOIN candidatos c ON r.id_candidato = c.id_candidato
            JOIN usuarios u ON c.id_usuario = u.id_usuario
            JOIN elecciones e ON r.id_eleccion = e.id_eleccion
            WHERE r.id_eleccion = %s AND r.id_candidato = %s
        """
        cursor.execute(query, (id_eleccion, id_candidato))
        resultado = cursor.fetchone()
        
        if not resultado:
            raise HTTPException(status_code=404, detail="Resultado no encontrado")
        
        return resultado

@router.get("/eleccion/{id_eleccion}/verificar-integridad", response_model=dict)
def verificar_integridad_resultados(id_eleccion: int):
    """
    Verificar la integridad de los resultados comparando con el número de votos.
    Retorna información útil para auditoría.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Contar votos totales
        cursor.execute(
            "SELECT COUNT(*) as total_votos FROM votos WHERE id_eleccion = %s",
            (id_eleccion,)
        )
        total_votos = cursor.fetchone()['total_votos']
        
        # Contar candidatos
        cursor.execute(
            "SELECT COUNT(*) as total_candidatos FROM candidatos WHERE id_eleccion = %s",
            (id_eleccion,)
        )
        total_candidatos = cursor.fetchone()['total_candidatos']
        
        # Contar resultados calculados
        cursor.execute(
            "SELECT COUNT(*) as total_resultados FROM resultados WHERE id_eleccion = %s",
            (id_eleccion,)
        )
        total_resultados = cursor.fetchone()['total_resultados']
        
        # Obtener hashes blockchain
        cursor.execute(
            "SELECT hash_blockchain FROM resultados WHERE id_eleccion = %s",
            (id_eleccion,)
        )
        hashes = [row['hash_blockchain'] for row in cursor.fetchall()]
        
        return {
            "id_eleccion": id_eleccion,
            "total_votos": total_votos,
            "total_candidatos": total_candidatos,
            "total_resultados_calculados": total_resultados,
            "resultados_completos": total_candidatos == total_resultados,
            "hashes_blockchain": hashes
        }

@router.delete("/eleccion/{id_eleccion}", response_model=MessageResponse)
def eliminar_resultados_eleccion(id_eleccion: int):
    """
    Eliminar todos los resultados de una elección.
    Útil para recalcular resultados.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "DELETE FROM resultados WHERE id_eleccion = %s",
                (id_eleccion,)
            )
            count = cursor.rowcount
            conn.commit()
            return MessageResponse(
                message=f"Se eliminaron {count} resultado(s) de la elección"
            )
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al eliminar resultados: {str(e)}")