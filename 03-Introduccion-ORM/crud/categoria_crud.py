"""
Operaciones CRUD para Categoría
"""

from typing import List, Optional
from uuid import UUID

from entities.categoria import Categoria
from sqlalchemy.orm import Session


class CategoriaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_categoria(
        self, nombre: str, descripcion: str = None, id_usuario_crea: UUID = None
    ) -> Categoria:
        """
        Crear una nueva categoría con validaciones

        Args:
            nombre: Nombre de la categoría (único, máximo 100 caracteres)
            descripcion: Descripción opcional
            id_usuario_crea: UUID del usuario que crea la categoría

        Returns:
            Categoría creada

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre de la categoría es obligatorio")

        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if self.obtener_categoria_por_nombre(nombre):
            raise ValueError("Ya existe una categoría con ese nombre")

        if id_usuario_crea is None:
            from entities.usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear la categoría"
                )
            id_usuario_crea = admin.id_usuario

        categoria = Categoria(
            nombre=nombre.strip(),
            descripcion=descripcion.strip() if descripcion else None,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def obtener_categoria(self, categoria_id: UUID) -> Optional[Categoria]:
        """
        Obtener una categoría por ID

        Args:
            categoria_id: UUID de la categoría

        Returns:
            Categoría encontrada o None
        """
        return (
            self.db.query(Categoria)
            .filter(Categoria.id_categoria == categoria_id)
            .first()
        )

    def obtener_categoria_por_nombre(self, nombre: str) -> Optional[Categoria]:
        """
        Obtener una categoría por nombre

        Args:
            nombre: Nombre de la categoría

        Returns:
            Categoría encontrada o None
        """
        return (
            self.db.query(Categoria).filter(Categoria.nombre == nombre.strip()).first()
        )

    def obtener_categorias(self, skip: int = 0, limit: int = 100) -> List[Categoria]:
        """
        Obtener lista de categorías con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de categorías
        """
        return self.db.query(Categoria).offset(skip).limit(limit).all()

    def actualizar_categoria(
        self, categoria_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Categoria]:
        """
        Actualizar una categoría con validaciones

        Args:
            categoria_id: UUID de la categoría
            id_usuario_edita: UUID del usuario que edita
            **kwargs: Campos a actualizar

        Returns:
            Categoría actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        categoria = self.obtener_categoria(categoria_id)
        if not categoria:
            return None

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre de la categoría es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            if (
                self.obtener_categoria_por_nombre(nombre)
                and self.obtener_categoria_por_nombre(nombre).id_categoria
                != categoria_id
            ):
                raise ValueError("Ya existe una categoría con ese nombre")
            kwargs["nombre"] = nombre.strip()

        if "descripcion" in kwargs and kwargs["descripcion"]:
            kwargs["descripcion"] = kwargs["descripcion"].strip()

        if id_usuario_edita is None:
            from entities.usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar la categoría"
                )
            id_usuario_edita = admin.id_usuario

        categoria.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(categoria, key):
                setattr(categoria, key, value)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def eliminar_categoria(self, categoria_id: UUID) -> bool:
        """
        Eliminar una categoría

        Args:
            categoria_id: UUID de la categoría

        Returns:
            True si se eliminó, False si no existe
        """
        categoria = self.obtener_categoria(categoria_id)
        if categoria:
            self.db.delete(categoria)
            self.db.commit()
            return True
        return False
