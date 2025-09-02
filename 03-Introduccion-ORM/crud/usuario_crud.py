"""
Operaciones CRUD para Usuario
=============================

Este módulo contiene todas las operaciones de base de datos
para la entidad Usuario.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..entities.usuario import Usuario, UsuarioCreate, UsuarioUpdate
from ..database.database import get_session_context

class UsuarioCRUD:
    """Clase para operaciones CRUD de Usuario"""
    
    @staticmethod
    def crear_usuario(usuario_data: UsuarioCreate) -> Usuario:
        """
        Crea un nuevo usuario
        
        Args:
            usuario_data: Datos del usuario a crear
            
        Returns:
            Usuario: Usuario creado
            
        Raises:
            ValueError: Si el email ya existe
        """
        with get_session_context() as session:
            # Verificar si el email ya existe
            if UsuarioCRUD.obtener_por_email(session, usuario_data.email):
                raise ValueError(f"El email {usuario_data.email} ya está registrado")
            
            # Crear el usuario
            usuario = Usuario(
                nombre=usuario_data.nombre,
                email=usuario_data.email,
                telefono=usuario_data.telefono,
                activo=usuario_data.activo
            )
            
            session.add(usuario)
            session.flush()  # Para obtener el ID
            session.refresh(usuario)
            
            return usuario
    
    @staticmethod
    def obtener_por_id(session: Session, usuario_id: int) -> Optional[Usuario]:
        """
        Obtiene un usuario por su ID
        
        Args:
            session: Sesión de base de datos
            usuario_id: ID del usuario
            
        Returns:
            Usuario o None si no existe
        """
        return session.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    @staticmethod
    def obtener_por_email(session: Session, email: str) -> Optional[Usuario]:
        """
        Obtiene un usuario por su email
        
        Args:
            session: Sesión de base de datos
            email: Email del usuario
            
        Returns:
            Usuario o None si no existe
        """
        return session.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def obtener_todos(
        session: Session,
        skip: int = 0,
        limit: int = 100,
        activo: Optional[bool] = None
    ) -> List[Usuario]:
        """
        Obtiene todos los usuarios con paginación
        
        Args:
            session: Sesión de base de datos
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            activo: Filtrar por estado activo/inactivo
            
        Returns:
            Lista de usuarios
        """
        query = session.query(Usuario)
        
        if activo is not None:
            query = query.filter(Usuario.activo == activo)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def buscar_usuarios(
        session: Session,
        termino_busqueda: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Usuario]:
        """
        Busca usuarios por nombre o email
        
        Args:
            session: Sesión de base de datos
            termino_busqueda: Término a buscar
            skip: Número de registros a saltar
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de usuarios que coinciden
        """
        termino = f"%{termino_busqueda}%"
        return session.query(Usuario).filter(
            or_(
                Usuario.nombre.ilike(termino),
                Usuario.email.ilike(termino)
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def actualizar_usuario(usuario_id: int, usuario_data: UsuarioUpdate) -> Optional[Usuario]:
        """
        Actualiza un usuario existente
        
        Args:
            usuario_id: ID del usuario a actualizar
            usuario_data: Datos a actualizar
            
        Returns:
            Usuario actualizado o None si no existe
            
        Raises:
            ValueError: Si el email ya existe en otro usuario
        """
        with get_session_context() as session:
            usuario = UsuarioCRUD.obtener_por_id(session, usuario_id)
            
            if not usuario:
                return None
            
            # Verificar si el email ya existe en otro usuario
            if usuario_data.email and usuario_data.email != usuario.email:
                usuario_existente = UsuarioCRUD.obtener_por_email(session, usuario_data.email)
                if usuario_existente:
                    raise ValueError(f"El email {usuario_data.email} ya está registrado")
            
            # Actualizar campos
            update_data = usuario_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(usuario, field, value)
            
            usuario.fecha_actualizacion = datetime.now()
            session.flush()
            session.refresh(usuario)
            
            return usuario
    
    @staticmethod
    def eliminar_usuario(usuario_id: int) -> bool:
        """
        Elimina un usuario (soft delete - lo marca como inactivo)
        
        Args:
            usuario_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            usuario = UsuarioCRUD.obtener_por_id(session, usuario_id)
            
            if not usuario:
                return False
            
            usuario.activo = False
            usuario.fecha_actualizacion = datetime.now()
            
            return True
    
    @staticmethod
    def eliminar_usuario_permanente(usuario_id: int) -> bool:
        """
        Elimina permanentemente un usuario de la base de datos
        
        Args:
            usuario_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó correctamente, False si no existe
        """
        with get_session_context() as session:
            usuario = UsuarioCRUD.obtener_por_id(session, usuario_id)
            
            if not usuario:
                return False
            
            session.delete(usuario)
            return True
    
    @staticmethod
    def contar_usuarios(session: Session, activo: Optional[bool] = None) -> int:
        """
        Cuenta el total de usuarios
        
        Args:
            session: Sesión de base de datos
            activo: Filtrar por estado activo/inactivo
            
        Returns:
            Número total de usuarios
        """
        query = session.query(Usuario)
        
        if activo is not None:
            query = query.filter(Usuario.activo == activo)
        
        return query.count()
    
    @staticmethod
    def obtener_estadisticas(session: Session) -> Dict[str, Any]:
        """
        Obtiene estadísticas de usuarios
        
        Args:
            session: Sesión de base de datos
            
        Returns:
            Diccionario con estadísticas
        """
        total = UsuarioCRUD.contar_usuarios(session)
        activos = UsuarioCRUD.contar_usuarios(session, activo=True)
        inactivos = UsuarioCRUD.contar_usuarios(session, activo=False)
        
        return {
            'total_usuarios': total,
            'usuarios_activos': activos,
            'usuarios_inactivos': inactivos,
            'porcentaje_activos': (activos / total * 100) if total > 0 else 0
        }
