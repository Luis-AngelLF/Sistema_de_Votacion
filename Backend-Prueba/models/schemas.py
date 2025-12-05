from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ============================================
# USUARIOS
# ============================================

class UsuarioBase(BaseModel):
    cedula: str
    nombre: str
    apellido1: str
    apellido2: Optional[str] = None
    correo: EmailStr
    rol: str

class UsuarioCreate(UsuarioBase):
    hash_contrasena: str

class UsuarioResponse(UsuarioBase):
    id_usuario: int
    esta_activo: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True

# ============================================
# ELECCIONES
# ============================================

class EleccionBase(BaseModel):
    nombre_eleccion: str
    descripcion: Optional[str] = None
    fecha_inicio: datetime
    fecha_fin: datetime

class EleccionCreate(EleccionBase):
    estado: str = "pendiente"

class EleccionResponse(EleccionBase):
    id_eleccion: int
    estado: str
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class EleccionEstadoUpdate(BaseModel):
    estado: str

# ============================================
# CANDIDATOS
# ============================================

class CandidatoBase(BaseModel):
    id_eleccion: int
    id_usuario: int
    propuesta: Optional[str] = None

class CandidatoCreate(CandidatoBase):
    pass

class CandidatoResponse(CandidatoBase):
    id_candidato: int
    fecha_registro: datetime

    class Config:
        from_attributes = True

class CandidatoDetailResponse(CandidatoResponse):
    nombre: Optional[str] = None
    apellido1: Optional[str] = None
    apellido2: Optional[str] = None
    correo: Optional[str] = None

# ============================================
# VOTOS
# ============================================

class VotoBase(BaseModel):
    id_eleccion: int
    id_usuario: int
    voto_cifrado: str
    hash_blockchain: str

class VotoCreate(VotoBase):
    pass

class VotoResponse(VotoBase):
    id_voto: int
    fecha_voto: datetime

    class Config:
        from_attributes = True

class VotoVerificacion(BaseModel):
    ha_votado: bool
    fecha_voto: Optional[datetime] = None

class VotoConteo(BaseModel):
    id_eleccion: int
    total_votos: int

# ============================================
# RESULTADOS
# ============================================

class ResultadoBase(BaseModel):
    id_eleccion: int
    id_candidato: int
    resultado_cifrado: str
    hash_blockchain: Optional[str] = None

class ResultadoCreate(ResultadoBase):
    pass

class ResultadoResponse(ResultadoBase):
    fecha_calculo: datetime

    class Config:
        from_attributes = True

class ResultadoDetailResponse(ResultadoResponse):
    propuesta: Optional[str] = None
    nombre: Optional[str] = None
    apellido1: Optional[str] = None
    apellido2: Optional[str] = None

# ============================================
# LOGS DE AUDITORÍA
# ============================================

class LogBase(BaseModel):
    accion: str
    detalles: Optional[str] = None
    hash_blockchain: Optional[str] = None

class LogCreate(LogBase):
    id_usuario: Optional[int] = None

class LogResponse(LogBase):
    id_log: int
    id_usuario: Optional[int] = None
    fecha_hora: datetime

    class Config:
        from_attributes = True

class LogDetailResponse(LogResponse):
    nombre: Optional[str] = None
    apellido1: Optional[str] = None

# ============================================
# RESPUESTAS GENÉRICAS
# ============================================

class MessageResponse(BaseModel):
    message: str
    id: Optional[int] = None

class ErrorResponse(BaseModel):
    detail: str