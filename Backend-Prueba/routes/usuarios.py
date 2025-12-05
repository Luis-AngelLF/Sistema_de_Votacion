from fastapi import APIRouter, HTTPException
from typing import List
import psycopg2

from config.database import get_db_connection
from models.schemas import UsuarioCreate, UsuarioResponse, MessageResponse

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/", response_model=MessageResponse, status_code=201)
def crear_usuario(usuario: UsuarioCreate):
    """Crear un nuevo usuario en el sistema"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            query = """
                INSERT INTO usuarios (cedula, nombre, apellido1, apellido2, correo, hash_contrasena, rol)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_usuario
            """
            cursor.execute(query, (
                usuario.cedula, 
                usuario.nombre, 
                usuario.apellido1, 
                usuario.apellido2, 
                usuario.correo, 
                usuario.hash_contrasena, 
                usuario.rol
            ))
            id_usuario = cursor.fetchone()['id_usuario']
            conn.commit()
            return MessageResponse(
                message="Usuario creado exitosamente",
                id=id_usuario
            )
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if "unique constraint" in str(e).lower():
                raise HTTPException(
                    status_code=400, 
                    detail="La cédula o correo ya están registrados"
                )
            raise HTTPException(status_code=400, detail=str(e))
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al crear usuario: {str(e)}")

@router.get("/", response_model=List[dict])
def listar_usuarios():
    """Obtener lista de todos los usuarios"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT id_usuario, cedula, nombre, apellido1, apellido2, 
                   correo, rol, esta_activo, fecha_creacion
            FROM usuarios 
            ORDER BY id_usuario
        """
        cursor.execute(query)
        usuarios = cursor.fetchall()
        return usuarios

@router.get("/{id_usuario}", response_model=dict)
def obtener_usuario(id_usuario: int):
    """Obtener información de un usuario específico por su ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT id_usuario, cedula, nombre, apellido1, apellido2, 
                   correo, rol, esta_activo, fecha_creacion
            FROM usuarios 
            WHERE id_usuario = %s
        """
        cursor.execute(query, (id_usuario,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return usuario

@router.get("/cedula/{cedula}", response_model=dict)
def obtener_usuario_por_cedula(cedula: str):
    """Obtener información de un usuario por su cédula"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = """
            SELECT id_usuario, cedula, nombre, apellido1, apellido2, 
                   correo, rol, esta_activo, fecha_creacion
            FROM usuarios 
            WHERE cedula = %s
        """
        cursor.execute(query, (cedula,))
        usuario = cursor.fetchone()
        
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return usuario

@router.put("/{id_usuario}/activar", response_model=MessageResponse)
def activar_usuario(id_usuario: int):
    """Activar un usuario"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET esta_activo = TRUE WHERE id_usuario = %s",
                (id_usuario,)
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            conn.commit()
            return MessageResponse(message="Usuario activado exitosamente")
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.put("/{id_usuario}/desactivar", response_model=MessageResponse)
def desactivar_usuario(id_usuario: int):
    """Desactivar un usuario"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET esta_activo = FALSE WHERE id_usuario = %s",
                (id_usuario,)
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            conn.commit()
            return MessageResponse(message="Usuario desactivado exitosamente")
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{id_usuario}", response_model=MessageResponse)
def eliminar_usuario(id_usuario: int):
    """Eliminar un usuario del sistema"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            conn.commit()
            return MessageResponse(message="Usuario eliminado exitosamente")
        except psycopg2.Error as e:
            conn.rollback()
            raise HTTPException(status_code=400, detail=f"Error al eliminar usuario: {str(e)}")