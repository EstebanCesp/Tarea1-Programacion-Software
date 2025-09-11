"""
Operaciones CRUD para Producto
"""

from typing import List, Optional

from entities.producto import Producto
from sqlalchemy.orm import Session


class ProductoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_producto(
        self,
        nombre: str,
        descripcion: str,
        precio: float,
        stock: int,
        categoria_id: int,
        usuario_id: int,
        id_usuario_crea: int = None,
    ) -> Producto:
        """Crear un nuevo producto"""
        # Si no se proporciona usuario creador, usar el mismo usuario_id
        if id_usuario_crea is None:
            id_usuario_crea = usuario_id

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            categoria_id=categoria_id,
            usuario_id=usuario_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        """Obtener un producto por ID"""
        return (
            self.db.query(Producto).filter(Producto.id_producto == producto_id).first()
        )

    def obtener_productos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        """Obtener lista de productos con paginación"""
        return self.db.query(Producto).offset(skip).limit(limit).all()

    def obtener_productos_por_categoria(self, categoria_id: int) -> List[Producto]:
        """Obtener productos por categoría"""
        return (
            self.db.query(Producto).filter(Producto.categoria_id == categoria_id).all()
        )

    def obtener_productos_por_usuario(self, usuario_id: int) -> List[Producto]:
        """Obtener productos por usuario"""
        return self.db.query(Producto).filter(Producto.usuario_id == usuario_id).all()

    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """Buscar productos por nombre (búsqueda parcial)"""
        return self.db.query(Producto).filter(Producto.nombre.contains(nombre)).all()

    def actualizar_producto(
        self, producto_id: int, id_usuario_edita: int = None, **kwargs
    ) -> Optional[Producto]:
        """Actualizar un producto"""
        producto = self.obtener_producto(producto_id)
        if producto:
            # Si no se proporciona usuario, usar el admin por defecto
            if id_usuario_edita is None:
                from entities.usuario import Usuario

                admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
                id_usuario_edita = admin.id_usuario if admin else 1

            # Actualizar campos de auditoría
            producto.id_usuario_edita = id_usuario_edita

            # Actualizar otros campos
            for key, value in kwargs.items():
                if hasattr(producto, key):
                    setattr(producto, key, value)
            self.db.commit()
            self.db.refresh(producto)
        return producto

    def actualizar_stock(
        self, producto_id: int, nuevo_stock: int
    ) -> Optional[Producto]:
        """Actualizar el stock de un producto"""
        return self.actualizar_producto(producto_id, stock=nuevo_stock)

    def eliminar_producto(self, producto_id: int) -> bool:
        """Eliminar un producto"""
        producto = self.obtener_producto(producto_id)
        if producto:
            self.db.delete(producto)
            self.db.commit()
            return True
        return False
