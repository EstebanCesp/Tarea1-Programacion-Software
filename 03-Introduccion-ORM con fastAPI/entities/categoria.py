import uuid

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    # Campos de auditoría
    id_usuario_crea = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    # Relación con productos (una categoría puede tener muchos productos)
    productos = relationship("Producto", back_populates="categoria")

    # Relaciones de auditoría
    usuario_crea = relationship(
        "Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita,productos"
    )
    usuario_edita = relationship(
        "Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea,productos"
    )

    def __repr__(self):
        return f"<Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre}')>"
