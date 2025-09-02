"""
Entidad Producto
================

Modelo de Producto con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List

from ..database.database import Base

class Producto(Base):
    """
    Modelo de Producto que representa la tabla 'productos'
    
    Atributos:
        id: Identificador único del producto
        nombre: Nombre del producto
        descripcion: Descripción detallada del producto
        precio: Precio del producto
        stock: Cantidad en stock
        activo: Estado del producto (activo/inactivo)
        categoria_id: ID de la categoría a la que pertenece
        usuario_id: ID del usuario que creó el producto
        fecha_creacion: Fecha y hora de creación
        fecha_actualizacion: Fecha y hora de última actualización
    """
    
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False, index=True)
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    categoria = relationship("Categoria", back_populates="productos")
    usuario = relationship("Usuario", back_populates="productos")
    
    def __repr__(self):
        """Representación en string del objeto Producto"""
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'stock': self.stock,
            'activo': self.activo,
            'categoria_id': self.categoria_id,
            'usuario_id': self.usuario_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

# Esquemas de Pydantic para validación y serialización

class ProductoBase(BaseModel):
    """Esquema base para Producto"""
    nombre: str = Field(..., min_length=2, max_length=200, description="Nombre del producto")
    descripcion: Optional[str] = Field(None, description="Descripción del producto")
    precio: float = Field(..., gt=0, description="Precio del producto (debe ser mayor a 0)")
    stock: int = Field(0, ge=0, description="Cantidad en stock (no puede ser negativo)")
    activo: bool = Field(True, description="Estado del producto")
    categoria_id: int = Field(..., description="ID de la categoría")
    usuario_id: int = Field(..., description="ID del usuario")
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()
    
    @validator('descripcion')
    def validar_descripcion(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('precio')
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return round(v, 2)

class ProductoCreate(ProductoBase):
    """Esquema para crear un nuevo producto"""
    pass

class ProductoUpdate(BaseModel):
    """Esquema para actualizar un producto existente"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=200)
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    activo: Optional[bool] = None
    categoria_id: Optional[int] = None
    usuario_id: Optional[int] = None
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip() if v else v
    
    @validator('descripcion')
    def validar_descripcion(cls, v):
        if v is not None:
            return v.strip() if v.strip() else None
        return v
    
    @validator('precio')
    def validar_precio(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return round(v, 2) if v is not None else v

class ProductoResponse(ProductoBase):
    """Esquema para respuesta de producto"""
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ProductoConRelaciones(ProductoResponse):
    """Esquema para producto con relaciones"""
    categoria: Optional['CategoriaResponse'] = None
    usuario: Optional['UsuarioResponse'] = None
    
    class Config:
        from_attributes = True

class ProductoListResponse(BaseModel):
    """Esquema para lista de productos"""
    productos: List[ProductoResponse]
    total: int
    pagina: int
    por_pagina: int
    
    class Config:
        from_attributes = True
