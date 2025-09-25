from datetime import datetime
from typing import Dict, List

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models import (
    Producto,
    ProductoCreate,
    ProductoUpdate,
    Usuario,
    UsuarioCreate,
    UsuarioUpdate,
)

app = FastAPI(
    title="API de Ejemplo - CRUD con FastAPI",
    description="Una API de ejemplo que demuestra operaciones CRUD básicas",
    version="1.0.0",
)

usuarios_db: Dict[int, Usuario] = {}
productos_db: Dict[int, Producto] = {}

usuario_id_counter = 1
producto_id_counter = 1


@app.get("/", response_model=Dict[str, str])
async def root():
    """Endpoint raíz que devuelve información básica de la API."""
    return {
        "mensaje": "Bienvenido a la API de ejemplo",
        "version": "1.0.0",
        "documentacion": "/docs",
    }


@app.get("/usuarios", response_model=List[Usuario])
async def obtener_usuarios():
    """Obtener todos los usuarios."""
    return list(usuarios_db.values())


@app.get("/usuarios/{usuario_id}", response_model=Usuario)
async def obtener_usuario(usuario_id: int):
    """Obtener un usuario específico por ID."""
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )
    return usuarios_db[usuario_id]


@app.post("/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCreate):
    """Crear un nuevo usuario."""
    global usuario_id_counter

    for existing_user in usuarios_db.values():
        if existing_user.email == usuario.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con este email",
            )

    nuevo_usuario = Usuario(
        id=usuario_id_counter,
        nombre=usuario.nombre,
        email=usuario.email,
        edad=usuario.edad,
        fecha_creacion=datetime.now(),
    )

    usuarios_db[usuario_id_counter] = nuevo_usuario
    usuario_id_counter += 1

    return nuevo_usuario


@app.put("/usuarios/{usuario_id}", response_model=Usuario)
async def actualizar_usuario(usuario_id: int, usuario_update: UsuarioUpdate):
    """Actualizar un usuario existente."""
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )

    usuario_actual = usuarios_db[usuario_id]
    update_data = usuario_update.dict(exclude_unset=True)

    if "email" in update_data:
        for existing_user in usuarios_db.values():
            if (
                existing_user.id != usuario_id
                and existing_user.email == update_data["email"]
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un usuario con este email",
                )

    usuario_actualizado = Usuario(
        id=usuario_actual.id,
        nombre=update_data.get("nombre", usuario_actual.nombre),
        email=update_data.get("email", usuario_actual.email),
        edad=update_data.get("edad", usuario_actual.edad),
        fecha_creacion=usuario_actual.fecha_creacion,
    )

    usuarios_db[usuario_id] = usuario_actualizado
    return usuario_actualizado


@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(usuario_id: int):
    """Eliminar un usuario."""
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado",
        )

    del usuarios_db[usuario_id]


@app.get("/productos", response_model=List[Producto])
async def obtener_productos():
    """Obtener todos los productos."""
    return list(productos_db.values())


@app.get("/productos/{producto_id}", response_model=Producto)
async def obtener_producto(producto_id: int):
    """Obtener un producto específico por ID."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado",
        )
    return productos_db[producto_id]


@app.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate):
    """Crear un nuevo producto."""
    global producto_id_counter

    nuevo_producto = Producto(
        id=producto_id_counter,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        stock=producto.stock,
        fecha_creacion=datetime.now(),
    )

    productos_db[producto_id_counter] = nuevo_producto
    producto_id_counter += 1

    return nuevo_producto


@app.put("/productos/{producto_id}", response_model=Producto)
async def actualizar_producto(producto_id: int, producto_update: ProductoUpdate):
    """Actualizar un producto existente."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado",
        )

    producto_actual = productos_db[producto_id]
    update_data = producto_update.dict(exclude_unset=True)

    producto_actualizado = Producto(
        id=producto_actual.id,
        nombre=update_data.get("nombre", producto_actual.nombre),
        descripcion=update_data.get("descripcion", producto_actual.descripcion),
        precio=update_data.get("precio", producto_actual.precio),
        stock=update_data.get("stock", producto_actual.stock),
        fecha_creacion=producto_actual.fecha_creacion,
    )

    productos_db[producto_id] = producto_actualizado
    return producto_actualizado


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(producto_id: int):
    """Eliminar un producto."""
    if producto_id not in productos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado",
        )

    del productos_db[producto_id]


@app.get("/estadisticas")
async def obtener_estadisticas():
    """Obtener estadísticas generales de la API."""
    return {
        "total_usuarios": len(usuarios_db),
        "total_productos": len(productos_db),
        "fecha_consulta": datetime.now().isoformat(),
    }


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Manejar errores de validación."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Error de validación", "detalle": str(exc)},
    )


if __name__ == "__main__":
    print("Iniciando servidor FastAPI...")
    print("Documentación disponible en: http://localhost:8000/docs")
    print("Interfaz alternativa en: http://localhost:8000/redoc")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
