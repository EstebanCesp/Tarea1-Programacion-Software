"""
Sistema de gestión de productos con ORM SQLAlchemy y Neon PostgreSQL
API REST con FastAPI - Sin interfaz de consola
"""

import uvicorn
from apis import auth, categoria, producto, usuario
from database.config import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Crear la aplicación FastAPI
app = FastAPI(
    title="Sistema de Gestión de Productos",
    description="API REST para gestión de usuarios, categorías y productos con autenticación",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers de las APIs
app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(categoria.router)
app.include_router(producto.router)


@app.on_event("startup")
async def startup_event():
    """Evento de inicio de la aplicación"""
    print("Iniciando Sistema de Gestión de Productos...")
    print("Configurando base de datos...")
    create_tables()
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:8000/docs")


@app.get("/", tags=["raíz"])
async def root():
    """Endpoint raíz que devuelve información básica de la API."""
    return {
        "mensaje": "Bienvenido al Sistema de Gestión de Productos",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "autenticacion": "/auth",
            "usuarios": "/usuarios",
            "categorias": "/categorias",
            "productos": "/productos",
        },
    }


def main():
    """Función principal para ejecutar el servidor"""
    print("Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Recargar automáticamente en desarrollo
        log_level="info",
    )


if __name__ == "__main__":
    main()
