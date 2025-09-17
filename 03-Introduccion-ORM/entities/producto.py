"""
Modelo de Producto
"""

import uuid
from typing import Any

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # Claves foráneas
    categoria_id = Column(
        UUID(as_uuid=True), ForeignKey("categorias.id_categoria"), nullable=False
    )
    usuario_id = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )

    # Campos de auditoría
    id_usuario_crea = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    # Relaciones
    categoria = relationship("Categoria", back_populates="productos")
    usuario = relationship(
        "Usuario", back_populates="productos", foreign_keys=[usuario_id]
    )

    # Relaciones de auditoría
    usuario_crea = relationship(
        "Usuario",
        foreign_keys=[id_usuario_crea],
        overlaps="usuario,usuario_edita,productos",
    )
    usuario_edita = relationship(
        "Usuario",
        foreign_keys=[id_usuario_edita],
        overlaps="usuario,usuario_crea,productos",
    )

    def __repr__(self):
        return f"<Producto(id_producto={self.id_producto}, nombre='{self.nombre}', precio={self.precio})>"
