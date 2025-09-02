"""
Módulo de entidades
==================

Este módulo contiene todas las entidades del sistema usando SQLAlchemy
y sus esquemas de validación con Pydantic.
"""

from .usuario import Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse
from .categoria import Categoria, CategoriaCreate, CategoriaUpdate, CategoriaResponse
from .producto import Producto, ProductoCreate, ProductoUpdate, ProductoResponse

__all__ = [
    # Usuario
    'Usuario', 'UsuarioCreate', 'UsuarioUpdate', 'UsuarioResponse',
    # Categoria
    'Categoria', 'CategoriaCreate', 'CategoriaUpdate', 'CategoriaResponse',
    # Producto
    'Producto', 'ProductoCreate', 'ProductoUpdate', 'ProductoResponse'
]
