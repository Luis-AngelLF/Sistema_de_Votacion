from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import test_connection

# Importar los routers
from routes import usuarios, elecciones, candidatos, votos, resultados, logs

# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================

app = FastAPI(
    title="Sistema de Votación Blockchain",
    description="""
    API REST para sistema de votación electrónico con:
    - Encriptación homomórfica (Paillier)
    - Registro en blockchain
    - Auditoría completa
    - Anonimato garantizado
    """,
    version="1.0.0",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "contacto@votacion.com"
    }
)

# ============================================
# CONFIGURACIÓN DE CORS
# ============================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# REGISTRAR ROUTERS
# ============================================

app.include_router(usuarios.router)
app.include_router(elecciones.router)
app.include_router(candidatos.router)
app.include_router(votos.router)
app.include_router(resultados.router)
app.include_router(logs.router)

# ============================================
# ENDPOINTS RAÍZ
# ============================================

@app.get("/")
def root():
    """Endpoint principal con información de la API"""
    return {
        "message": "API Sistema de Votación Blockchain",
        "version": "1.0.0",
        "status": "online",
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "usuarios": "/usuarios",
            "elecciones": "/elecciones",
            "candidatos": "/candidatos",
            "votos": "/votos",
            "resultados": "/resultados",
            "logs": "/logs"
        }
    }

@app.get("/health")
def health_check():
    """Verificar el estado de salud de la API y la conexión a la base de datos"""
    db_status = test_connection()
    
    return {
        "status": "healthy" if db_status else "unhealthy",
        "api": "online",
        "database": "connected" if db_status else "disconnected"
    }

@app.get("/info")
def api_info():
    """Información detallada sobre la API"""
    return {
        "nombre": "Sistema de Votación Blockchain",
        "version": "1.0.0",
        "características": [
            "Votación electrónica segura",
            "Encriptación homomórfica Paillier",
            "Registro en blockchain",
            "Anonimato garantizado",
            "Auditoría completa",
            "API RESTful"
        ],
        "tecnologías": {
            "framework": "FastAPI",
            "base_de_datos": "PostgreSQL",
            "lenguaje": "Python 3.8+"
        }
    }

# ============================================
# EVENTOS DE INICIO Y CIERRE
# ============================================

@app.on_event("startup")
async def startup_event():
    """Ejecutar al iniciar la aplicación"""
    print("🚀 Iniciando Sistema de Votación Blockchain...")
    print("📊 Verificando conexión a la base de datos...")
    
    if test_connection():
        print("✅ Base de datos conectada correctamente")
    else:
        print("❌ ERROR: No se pudo conectar a la base de datos")
        print("   Verifica tu archivo .env y la configuración de PostgreSQL")
    
    print("📚 Documentación disponible en: http://localhost:8000/docs")
    print("✨ API lista para recibir peticiones")

@app.on_event("shutdown")
async def shutdown_event():
    """Ejecutar al cerrar la aplicación"""
    print("👋 Cerrando Sistema de Votación Blockchain...")

# ============================================
# EJECUTAR LA APLICACIÓN
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload en desarrollo
        log_level="info"
    )