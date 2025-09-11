"""
Operaciones CRUD para Usuario
"""

from typing import List, Optional

from entities.usuario import Usuario
from sqlalchemy.orm import Session


class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_usuario(
        self, nombre: str, email: str, telefono: str = None, es_admin: bool = False
    ) -> Usuario:
        """Crear un nuevo usuario"""
        usuario = Usuario(
            nombre=nombre, email=email, telefono=telefono, es_admin=es_admin
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, usuario_id: int) -> Optional[Usuario]:
        """Obtener un usuario por ID"""
        return self.db.query(Usuario).filter(Usuario.id_usuario == usuario_id).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """Obtener un usuario por email"""
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Obtener lista de usuarios con paginación"""
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def actualizar_usuario(self, usuario_id: int, **kwargs) -> Optional[Usuario]:
        """Actualizar un usuario"""
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            for key, value in kwargs.items():
                if hasattr(usuario, key):
                    setattr(usuario, key, value)
            self.db.commit()
            self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: int) -> bool:
        """Eliminar un usuario"""
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def desactivar_usuario(self, usuario_id: int) -> Optional[Usuario]:
        """Desactivar un usuario (soft delete)"""
        return self.actualizar_usuario(usuario_id, activo=False)

    def obtener_usuarios_admin(self) -> List[Usuario]:
        """Obtener todos los usuarios administradores"""
        return self.db.query(Usuario).filter(Usuario.es_admin == True).all()

    def es_admin(self, usuario_id: int) -> bool:
        """Verificar si un usuario es administrador"""
        usuario = self.obtener_usuario(usuario_id)
        return usuario.es_admin if usuario else False

    def obtener_admin_por_defecto(self) -> Optional[Usuario]:
        """Obtener el usuario administrador por defecto"""
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == "admin@system.com", Usuario.es_admin == True)
            .first()
        )
