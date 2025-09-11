"""
Modelo de Usuario
"""

from database.config import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True)
    es_admin = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con productos (un usuario puede tener muchos productos)
    productos = relationship("Producto", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(id_usuario={self.id_usuario}, nombre='{self.nombre}', email='{self.email}')>"
        """Representación en string del objeto Usuario"""
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'activo': self.activo,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None
        }

# Esquemas de Pydantic para validación y serialización

class UsuarioBase(BaseModel):
    """Esquema base para Usuario"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    telefono: Optional[str] = Field(None, max_length=20, description="Número de teléfono")
    activo: bool = Field(True, description="Estado del usuario")
    
    @validator('nombre')   
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().title()
    
    @validator('telefono')
    def validar_telefono(cls, v):
        if v is not None:
            # Remover caracteres no numéricos excepto + al inicio
            v = v.strip()
            if v and not v.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
                raise ValueError('Formato de teléfono inválido')
        return v

class UsuarioCreate(UsuarioBase):
    """Esquema para crear un nuevo usuario"""
    pass

class UsuarioUpdate(BaseModel):
    """Esquema para actualizar un usuario existente"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if v is not None and not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().title() if v else v
    
    @validator('telefono')
    def validar_telefono(cls, v):
        if v is not None:
            v = v.strip()
            if v and not v.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
                raise ValueError('Formato de teléfono inválido')
        return v

class UsuarioResponse(UsuarioBase):
    """Esquema para respuesta de usuario"""
    id: int
    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UsuarioListResponse(BaseModel):
    """Esquema para lista de usuarios"""
    usuarios: List[UsuarioResponse]
    total: int
    pagina: int
    por_pagina: int
    
    class Config:
        from_attributes = True
