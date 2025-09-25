from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UsuarioBase(BaseModel):
    """Modelo base para un usuario."""

    nombre: str
    email: str
    edad: Optional[int] = None


class UsuarioCreate(UsuarioBase):
    """Modelo para crear un usuario (sin ID)."""

    pass


class UsuarioUpdate(BaseModel):
    """Modelo para actualizar un usuario (todos los campos opcionales)."""

    nombre: Optional[str] = None
    email: Optional[str] = None
    edad: Optional[int] = None


class Usuario(UsuarioBase):
    """Modelo para respuesta de usuario (con ID y fecha de creación)."""

    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class ProductoBase(BaseModel):
    """Modelo base para un producto."""

    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int


class ProductoCreate(ProductoBase):
    """Modelo para crear un producto."""

    pass


class ProductoUpdate(BaseModel):
    """Modelo para actualizar un producto."""

    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None


class Producto(ProductoBase):
    """Modelo para respuesta de producto."""

    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Modelo para respuesta de error."""

    error: str
    detalle: Optional[str] = None
