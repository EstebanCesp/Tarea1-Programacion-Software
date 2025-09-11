"""
Operaciones CRUD para Categoría
"""

from typing import List, Optional

from entities.categoria import Categoria
from sqlalchemy.orm import Session


class CategoriaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_categoria(
        self, nombre: str, descripcion: str = None, id_usuario_crea: int = None
    ) -> Categoria:
        """Crear una nueva categoría"""
        # Si no se proporciona usuario, buscar el admin por defecto
        if id_usuario_crea is None:
            from entities.usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            id_usuario_crea = admin.id_usuario if admin else 1

        categoria = Categoria(
            nombre=nombre, descripcion=descripcion, id_usuario_crea=id_usuario_crea
        )
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def obtener_categoria(self, categoria_id: int) -> Optional[Categoria]:
        """Obtener una categoría por ID"""
        return (
            self.db.query(Categoria)
            .filter(Categoria.id_categoria == categoria_id)
            .first()
        )

    def obtener_categoria_por_nombre(self, nombre: str) -> Optional[Categoria]:
        """Obtener una categoría por nombre"""
        return self.db.query(Categoria).filter(Categoria.nombre == nombre).first()

    def obtener_categorias(self, skip: int = 0, limit: int = 100) -> List[Categoria]:
        """Obtener lista de categorías con paginación"""
        return self.db.query(Categoria).offset(skip).limit(limit).all()

    def actualizar_categoria(
        self, categoria_id: int, id_usuario_edita: int = None, **kwargs
    ) -> Optional[Categoria]:
        """Actualizar una categoría"""
        categoria = self.obtener_categoria(categoria_id)
        if categoria:
            # Si no se proporciona usuario, buscar el admin por defecto
            if id_usuario_edita is None:
                from entities.usuario import Usuario

                admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
                id_usuario_edita = admin.id_usuario if admin else 1

            # Actualizar campos de auditoría
            categoria.id_usuario_edita = id_usuario_edita

            # Actualizar otros campos
            for key, value in kwargs.items():
                if hasattr(categoria, key):
                    setattr(categoria, key, value)
            self.db.commit()
            self.db.refresh(categoria)
        return categoria

    def eliminar_categoria(self, categoria_id: int) -> bool:
        """Eliminar una categoría"""
        categoria = self.obtener_categoria(categoria_id)
        if categoria:
            self.db.delete(categoria)
            self.db.commit()
            return True
        return False
