"""
Operaciones CRUD para Producto
==============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Producto.
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

from ..entities.producto import Producto, ProductoCreate, ProductoUpdate
from ..database.database import get_session_context

class ProductoCRUD:
    """Clase para operaciones CRUD de Producto"""
    
    @staticmethod
    def crear_producto(producto_data: ProductoCreate) -> Producto:
        """
        Crea un nuevo producto
        
        Args:
            producto_data: Datos del producto a crear
            
        Returns:
            Producto: Producto creado
            
        Raises:
            ValueError: Si la categoría o usuario no existen
        """
        with get_session_context() as session:
            # Verificar que la categoría existe
            from .categoria_crud import CategoriaCRUD
            from .usuario_crud import UsuarioCRUD
            
            categoria = CategoriaCRUD.obtener_por_id(session, producto_data.categoria_id)
            if not categoria:
                raise ValueError(f"La categoría con ID {producto_data.categoria_id} no existe")
            
            usuario = UsuarioCRUD.obtener_por_id(session, producto_data.usuario_id)
            if not usuario:
                raise ValueError(f"El usuario con ID {producto_data.usuario_id} no existe")
            
            # Crear el producto
            producto = Producto(
                nombre=producto_data.nombre,
                descripcion=producto_data.descripcion,
                precio=producto_data.precio,
                stock=producto_data.stock,
                activo=producto_data.activo,
                categoria_id=producto_data.categoria_id,
                usuario_id=producto_data.usuario_id
            )
            
            session.add(producto)
            session.flush()  # Para obtener el ID
            session.refresh(producto)
            
            return producto
    
    @staticmethod
    def obtener_por_id(session: Session, producto_id: int, incluir_relaciones: bool = False) -> Optional[Producto]:
        """
        Obtiene un producto por su ID
        
        Args:
            session: Sesión de base de datos
            producto_id: ID del producto
            incluir_relaciones: Si incluir categoría y usuario
            
        Returns:
            Producto o None si no existe
        """
        query = session.query(Producto).filter(Producto.id == producto_id)
        
        if incluir_relaciones:
            query = query.options(
                joinedload(Producto.categoria),
                joinedload(Producto.usuario)
            )
        
        return query.first()
    
    @staticmethod
    def obtener_todos(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        activo: Optional[bool] = None,
        categoria_id: Optional[int] = None,
        usuario_id: Optional[int] = None,
        incluir_relaciones: bool = False
    ) -> List[Producto]:
        """
        Obtiene todos los productos con paginación y filtros
        
        Args:
            session: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            activo: Filtrar por estado activo/inactivo
            categoria_id: Filtrar por categoría
            usuario_id: Filtrar por usuario
            incluir_relaciones: Si incluir categoría y usuario
            
        Returns:
            Lista de productos
        """
        query = session.query(Producto)
        
        if activo is not None:
            query = query.filter(Producto.activo == activo)
        
        if categoria_id is not None:
            query = query.filter(Producto.categoria_id == categoria_id)
        
        if usuario_id is not None:
            query = query.filter(Producto.usuario_id == usuario_id)
        
        if incluir_relaciones:
            query = query.options(
                joinedload(Producto.categoria),
                joinedload(Producto.usuario)
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def buscar_productos(
        session: Session,
        termino_busqueda: str,
        skip: int = 0,
        limit: int = 100,
        incluir_relaciones: bool = False
    ) -> List[Producto]:
        """
        Busca productos por nombre o descripción
        
        Args:
            session: Sesión de base de datos
            termino_busqueda: Término a buscar
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            incluir_relaciones: Si incluir categoría y usuario
            
        Returns:
            Lista de productos que coinciden
        """
        termino = f"%{termino_busqueda}%"
        query = session.query(Producto).filter(
            or_(
                Producto.nombre.ilike(termino),
                Producto.descripcion.ilike(termino)
            )
        )
        
        if incluir_relaciones:
            query = query.options(
                joinedload(Producto.categoria),
                joinedload(Producto.usuario)
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def buscar_por_rango_precio(
        session: Session,
        precio_min: float,
        precio_max: float,
        skip: int = 0,
        limit: int = 100
    ) -> List[Producto]:
        """
        Busca productos por rango de precio
        
        Args:
            session: Sesión de base de datos
            precio_min: Precio mínimo
            precio_max: Precio máximo
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de productos en el rango de precio
        """
        return session.query(Producto).filter(
            and_(
                Producto.precio >= precio_min,
                Producto.precio <= precio_max
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def actualizar_producto(producto_id: int, producto_data: ProductoUpdate) -> Optional[Producto]:
        """
        Actualiza un producto existente
        
        Args:
            producto_id: ID del producto a actualizar
            producto_data: Datos a actualizar
            
        Returns:
            Producto actualizado o None si no existe
            
        Raises:
            ValueError: Si la categoría o usuario no existen
        """
        with get_session_context() as session:
            producto = ProductoCRUD.obtener_por_id(session, producto_id)
            
            if not producto:
                return None
            
            # Verificar que la categoría existe si se está actualizando
            if producto_data.categoria_id and producto_data.categoria_id != producto.categoria_id:
                from .categoria_crud import CategoriaCRUD
                categoria = CategoriaCRUD.obtener_por_id(session, producto_data.categoria_id)
                if not categoria:
                    raise ValueError(f"La categoría con ID {producto_data.categoria_id} no existe")
            
            # Verificar que el usuario existe si se está actualizando
            if producto_data.usuario_id and producto_data.usuario_id != producto.usuario_id:
                from .usuario_crud import UsuarioCRUD
                usuario = UsuarioCRUD.obtener_por_id(session, producto_data.usuario_id)
                if not usuario:
                    raise ValueError(f"El usuario con ID {producto_data.usuario_id} no existe")
            
            # Actualizar campos
            update_data = producto_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(producto, field, value)
            
            producto.fecha_actualizacion = datetime.now()
            session.flush()
            session.refresh(producto)
            
            return producto
    
    @staticmethod
    def actualizar_stock(producto_id: int, nueva_cantidad: int) -> Optional[Producto]:
        """
        Actualiza el stock de un producto
        
        Args:
            producto_id: ID del producto
            nueva_cantidad: Nueva cantidad en stock
            
        Returns:
            Producto actualizado o None si no existe
        """
        with get_session_context() as session:
            producto = ProductoCRUD.obtener_por_id(session, producto_id)
            
            if not producto:
                return None
            
            producto.stock = nueva_cantidad
            producto.fecha_actualizacion = datetime.now()
            session.flush()
            session.refresh(producto)
            
            return producto
    
    @staticmethod
    def eliminar_producto(producto_id: int) -> bool:
        """
        Elimina un producto (soft delete - lo marca como inactivo)
        
        Args:
            producto_id: ID del producto a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            producto = ProductoCRUD.obtener_por_id(session, producto_id)
            
            if not producto:
                return False
            
            producto.activo = False
            producto.fecha_actualizacion = datetime.now()
            
            return True
    
    @staticmethod
    def eliminar_producto_permanente(producto_id: int) -> bool:
        """
        Elimina permanentemente un producto de la base de datos
        
        Args:
            producto_id: ID del producto a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            producto = ProductoCRUD.obtener_por_id(session, producto_id)
            
            if not producto:
                return False
            
            session.delete(producto)
            return True
    
    @staticmethod
    def contar_productos(
        session: Session,
        activo: Optional[bool] = None,
        categoria_id: Optional[int] = None,
        usuario_id: Optional[int] = None
    ) -> int:
        """
        Cuenta el total de productos
        
        Args:
            session: Sesión de base de datos
            activo: Filtrar por estado activo/inactivo
            categoria_id: Filtrar por categoría
            usuario_id: Filtrar por usuario
            
        Returns:
            Número total de productos
        """
        query = session.query(Producto)
        
        if activo is not None:
            query = query.filter(Producto.activo == activo)
        
        if categoria_id is not None:
            query = query.filter(Producto.categoria_id == categoria_id)
        
        if usuario_id is not None:
            query = query.filter(Producto.usuario_id == usuario_id)
        
        return query.count()
    
    @staticmethod
    def obtener_productos_bajo_stock(session: Session, stock_minimo: int = 10) -> List[Producto]:
        """
        Obtiene productos con stock bajo
        
        Args:
            session: Sesión de base de datos
            stock_minimo: Stock mínimo considerado como bajo
            
        Returns:
            Lista de productos con stock bajo
        """
        return session.query(Producto).filter(
            and_(
                Producto.stock <= stock_minimo,
                Producto.activo == True
            )
        ).all()
    
    @staticmethod
    def obtener_estadisticas(session: Session) -> Dict[str, Any]:
        """
        Obtiene estadísticas de productos
        
        Args:
            session: Sesión de base de datos
            
        Returns:
            Diccionario con estadísticas
        """
        total = ProductoCRUD.contar_productos(session)
        activos = ProductoCRUD.contar_productos(session, activo=True)
        inactivos = ProductoCRUD.contar_productos(session, activo=False)
        bajo_stock = len(ProductoCRUD.obtener_productos_bajo_stock(session))
        
        # Estadísticas de precios
        precio_stats = session.query(
            func.min(Producto.precio).label('precio_min'),
            func.max(Producto.precio).label('precio_max'),
            func.avg(Producto.precio).label('precio_promedio')
        ).filter(Producto.activo == True).first()
        
        return {
            'total_productos': total,
            'productos_activos': activos,
            'productos_inactivos': inactivos,
            'productos_bajo_stock': bajo_stock,
            'precio_minimo': float(precio_stats.precio_min) if precio_stats.precio_min else 0,
            'precio_maximo': float(precio_stats.precio_max) if precio_stats.precio_max else 0,
            'precio_promedio': float(precio_stats.precio_promedio) if precio_stats.precio_promedio else 0,
            'porcentaje_activos': (activos / total * 100) if total > 0 else 0
        }
