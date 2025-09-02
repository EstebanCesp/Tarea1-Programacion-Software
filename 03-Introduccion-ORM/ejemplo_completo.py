"""
Ejemplo Completo de ORM con Estructura Profesional
==================================================

Este ejemplo demuestra el uso completo de la estructura ORM organizada:
- Entidades con SQLAlchemy y Pydantic
- Operaciones CRUD separadas
- Configuración de base de datos modular
- Validaciones y manejo de errores
"""

import sys
import os
from datetime import datetime
from typing import List

# Agregar el directorio padre al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import create_tables, check_connection, get_session
from entities import (
    Usuario, UsuarioCreate, UsuarioUpdate, UsuarioResponse,
    Categoria, CategoriaCreate, CategoriaUpdate, CategoriaResponse,
    Producto, ProductoCreate, ProductoUpdate, ProductoResponse
)
from crud import UsuarioCRUD, CategoriaCRUD, ProductoCRUD

def mostrar_separador(titulo: str):
    """Muestra un separador con título"""
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")

def ejemplo_usuarios():
    """Ejemplo completo de operaciones con usuarios"""
    mostrar_separador("EJEMPLO DE USUARIOS")
    
    try:
        # Crear usuarios
        print("\n1. Creando usuarios...")
        
        usuarios_data = [
            UsuarioCreate(
                nombre="Juan Pérez",
                email="juan.perez@email.com",
                telefono="+57 300 123 4567",
                activo=True
            ),
            UsuarioCreate(
                nombre="María García",
                email="maria.garcia@email.com",
                telefono="+57 301 234 5678",
                activo=True
            ),
            UsuarioCreate(
                nombre="Carlos López",
                email="carlos.lopez@email.com",
                telefono="+57 302 345 6789",
                activo=False
            )
        ]
        
        usuarios_creados = []
        for usuario_data in usuarios_data:
            try:
                usuario = UsuarioCRUD.crear_usuario(usuario_data)
                usuarios_creados.append(usuario)
                print(f"   ✅ Usuario creado: {usuario.nombre} (ID: {usuario.id})")
            except ValueError as e:
                print(f"   ❌ Error al crear usuario {usuario_data.nombre}: {e}")
        
        # Consultar usuarios
        print("\n2. Consultando usuarios...")
        session = get_session()
        try:
            usuarios = UsuarioCRUD.obtener_todos(session, limit=10)
            print(f"   Total de usuarios encontrados: {len(usuarios)}")
            for usuario in usuarios:
                print(f"   - {usuario.nombre} ({usuario.email}) - Activo: {usuario.activo}")
        finally:
            session.close()
        
        # Buscar usuarios
        print("\n3. Buscando usuarios...")
        session = get_session()
        try:
            usuarios_encontrados = UsuarioCRUD.buscar_usuarios(session, "Juan")
            print(f"   Usuarios que contienen 'Juan': {len(usuarios_encontrados)}")
            for usuario in usuarios_encontrados:
                print(f"   - {usuario.nombre} ({usuario.email})")
        finally:
            session.close()
        
        # Actualizar usuario
        if usuarios_creados:
            print("\n4. Actualizando usuario...")
            usuario_id = usuarios_creados[0].id
            update_data = UsuarioUpdate(
                telefono="+57 300 999 9999",
                activo=True
            )
            usuario_actualizado = UsuarioCRUD.actualizar_usuario(usuario_id, update_data)
            if usuario_actualizado:
                print(f"   ✅ Usuario actualizado: {usuario_actualizado.nombre}")
                print(f"   📞 Nuevo teléfono: {usuario_actualizado.telefono}")
        
        # Estadísticas
        print("\n5. Estadísticas de usuarios...")
        session = get_session()
        try:
            stats = UsuarioCRUD.obtener_estadisticas(session)
            print(f"   📊 Total usuarios: {stats['total_usuarios']}")
            print(f"   ✅ Usuarios activos: {stats['usuarios_activos']}")
            print(f"   ❌ Usuarios inactivos: {stats['usuarios_inactivos']}")
            print(f"   📈 Porcentaje activos: {stats['porcentaje_activos']:.1f}%")
        finally:
            session.close()
            
        return usuarios_creados
        
    except Exception as e:
        print(f"❌ Error en ejemplo de usuarios: {e}")
        return []

def ejemplo_categorias():
    """Ejemplo completo de operaciones con categorías"""
    mostrar_separador("EJEMPLO DE CATEGORÍAS")
    
    try:
        # Crear categorías
        print("\n1. Creando categorías...")
        
        categorias_data = [
            CategoriaCreate(
                nombre="Electrónicos",
                descripcion="Dispositivos electrónicos y tecnología",
                activa=True
            ),
            CategoriaCreate(
                nombre="Ropa",
                descripcion="Vestimenta y accesorios",
                activa=True
            ),
            CategoriaCreate(
                nombre="Hogar",
                descripcion="Artículos para el hogar",
                activa=True
            )
        ]
        
        categorias_creadas = []
        for categoria_data in categorias_data:
            try:
                categoria = CategoriaCRUD.crear_categoria(categoria_data)
                categorias_creadas.append(categoria)
                print(f"   ✅ Categoría creada: {categoria.nombre} (ID: {categoria.id})")
            except ValueError as e:
                print(f"   ❌ Error al crear categoría {categoria_data.nombre}: {e}")
        
        # Consultar categorías
        print("\n2. Consultando categorías...")
        session = get_session()
        try:
            categorias = CategoriaCRUD.obtener_todas(session, limit=10)
            print(f"   Total de categorías encontradas: {len(categorias)}")
            for categoria in categorias:
                print(f"   - {categoria.nombre}: {categoria.descripcion}")
        finally:
            session.close()
        
        # Actualizar categoría
        if categorias_creadas:
            print("\n3. Actualizando categoría...")
            categoria_id = categorias_creadas[0].id
            update_data = CategoriaUpdate(
                descripcion="Dispositivos electrónicos, computadoras y tecnología avanzada"
            )
            categoria_actualizada = CategoriaCRUD.actualizar_categoria(categoria_id, update_data)
            if categoria_actualizada:
                print(f"   ✅ Categoría actualizada: {categoria_actualizada.nombre}")
                print(f"   📝 Nueva descripción: {categoria_actualizada.descripcion}")
        
        # Estadísticas
        print("\n4. Estadísticas de categorías...")
        session = get_session()
        try:
            stats = CategoriaCRUD.obtener_estadisticas(session)
            print(f"   📊 Total categorías: {stats['total_categorias']}")
            print(f"   ✅ Categorías activas: {stats['categorias_activas']}")
            print(f"   📦 Categorías con productos: {stats['categorias_con_productos']}")
        finally:
            session.close()
            
        return categorias_creadas
        
    except Exception as e:
        print(f"❌ Error en ejemplo de categorías: {e}")
        return []

def ejemplo_productos(usuarios: List[Usuario], categorias: List[Categoria]):
    """Ejemplo completo de operaciones con productos"""
    mostrar_separador("EJEMPLO DE PRODUCTOS")
    
    if not usuarios or not categorias:
        print("❌ No se pueden crear productos sin usuarios y categorías")
        return []
    
    try:
        # Crear productos
        print("\n1. Creando productos...")
        
        productos_data = [
            ProductoCreate(
                nombre="Laptop HP Pavilion",
                descripcion="Laptop para trabajo y entretenimiento",
                precio=2500000.00,
                stock=15,
                activo=True,
                categoria_id=categorias[0].id,  # Electrónicos
                usuario_id=usuarios[0].id
            ),
            ProductoCreate(
                nombre="Camiseta Algodón",
                descripcion="Camiseta 100% algodón, varios colores",
                precio=45000.00,
                stock=50,
                activo=True,
                categoria_id=categorias[1].id,  # Ropa
                usuario_id=usuarios[1].id
            ),
            ProductoCreate(
                nombre="Sofá 3 Puestos",
                descripcion="Sofá cómodo para sala",
                precio=1800000.00,
                stock=3,
                activo=True,
                categoria_id=categorias[2].id,  # Hogar
                usuario_id=usuarios[0].id
            )
        ]
        
        productos_creados = []
        for producto_data in productos_data:
            try:
                producto = ProductoCRUD.crear_producto(producto_data)
                productos_creados.append(producto)
                print(f"   ✅ Producto creado: {producto.nombre} (ID: {producto.id})")
                print(f"      💰 Precio: ${producto.precio:,.2f} | 📦 Stock: {producto.stock}")
            except ValueError as e:
                print(f"   ❌ Error al crear producto {producto_data.nombre}: {e}")
        
        # Consultar productos
        print("\n2. Consultando productos...")
        session = get_session()
        try:
            productos = ProductoCRUD.obtener_todos(session, limit=10, incluir_relaciones=True)
            print(f"   Total de productos encontrados: {len(productos)}")
            for producto in productos:
                print(f"   - {producto.nombre}")
                print(f"     💰 ${producto.precio:,.2f} | 📦 {producto.stock} | 📂 {producto.categoria.nombre}")
        finally:
            session.close()
        
        # Buscar productos por precio
        print("\n3. Buscando productos por rango de precio...")
        session = get_session()
        try:
            productos_rango = ProductoCRUD.buscar_por_rango_precio(session, 40000, 50000)
            print(f"   Productos entre $40,000 y $50,000: {len(productos_rango)}")
            for producto in productos_rango:
                print(f"   - {producto.nombre}: ${producto.precio:,.2f}")
        finally:
            session.close()
        
        # Actualizar stock
        if productos_creados:
            print("\n4. Actualizando stock de producto...")
            producto_id = productos_creados[0].id
            producto_actualizado = ProductoCRUD.actualizar_stock(producto_id, 20)
            if producto_actualizado:
                print(f"   ✅ Stock actualizado: {producto_actualizado.nombre}")
                print(f"   📦 Nuevo stock: {producto_actualizado.stock}")
        
        # Productos con stock bajo
        print("\n5. Productos con stock bajo...")
        session = get_session()
        try:
            productos_bajo_stock = ProductoCRUD.obtener_productos_bajo_stock(session, stock_minimo=10)
            print(f"   Productos con stock ≤ 10: {len(productos_bajo_stock)}")
            for producto in productos_bajo_stock:
                print(f"   ⚠️  {producto.nombre}: {producto.stock} unidades")
        finally:
            session.close()
        
        # Estadísticas
        print("\n6. Estadísticas de productos...")
        session = get_session()
        try:
            stats = ProductoCRUD.obtener_estadisticas(session)
            print(f"   📊 Total productos: {stats['total_productos']}")
            print(f"   ✅ Productos activos: {stats['productos_activos']}")
            print(f"   ⚠️  Productos bajo stock: {stats['productos_bajo_stock']}")
            print(f"   💰 Precio mínimo: ${stats['precio_minimo']:,.2f}")
            print(f"   💰 Precio máximo: ${stats['precio_maximo']:,.2f}")
            print(f"   💰 Precio promedio: ${stats['precio_promedio']:,.2f}")
        finally:
            session.close()
            
        return productos_creados
        
    except Exception as e:
        print(f"❌ Error en ejemplo de productos: {e}")
        return []

def ejemplo_validaciones():
    """Ejemplo de validaciones con Pydantic"""
    mostrar_separador("EJEMPLO DE VALIDACIONES")
    
    print("\n1. Probando validaciones de Usuario...")
    
    # Datos válidos
    try:
        usuario_valido = UsuarioCreate(
            nombre="Ana María",
            email="ana.maria@email.com",
            telefono="+57 300 123 4567"
        )
        print(f"   ✅ Usuario válido: {usuario_valido.nombre}")
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
    
    # Datos inválidos
    casos_invalidos = [
        {"nombre": "", "email": "test@email.com", "error": "Nombre vacío"},
        {"nombre": "A", "email": "test@email.com", "error": "Nombre muy corto"},
        {"nombre": "Test", "email": "email-invalido", "error": "Email inválido"},
        {"nombre": "Test", "email": "test@email.com", "telefono": "abc123", "error": "Teléfono inválido"}
    ]
    
    for caso in casos_invalidos:
        try:
            UsuarioCreate(**{k: v for k, v in caso.items() if k != "error"})
            print(f"   ❌ Debería haber fallado: {caso['error']}")
        except Exception as e:
            print(f"   ✅ Validación correcta para {caso['error']}: {str(e)[:50]}...")
    
    print("\n2. Probando validaciones de Producto...")
    
    # Datos válidos
    try:
        producto_valido = ProductoCreate(
            nombre="Producto Test",
            precio=100000.00,
            stock=10,
            categoria_id=1,
            usuario_id=1
        )
        print(f"   ✅ Producto válido: {producto_valido.nombre}")
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
    
    # Datos inválidos
    casos_invalidos_producto = [
        {"nombre": "Test", "precio": -100, "stock": 10, "categoria_id": 1, "usuario_id": 1, "error": "Precio negativo"},
        {"nombre": "Test", "precio": 100, "stock": -5, "categoria_id": 1, "usuario_id": 1, "error": "Stock negativo"},
        {"nombre": "", "precio": 100, "stock": 10, "categoria_id": 1, "usuario_id": 1, "error": "Nombre vacío"}
    ]
    
    for caso in casos_invalidos_producto:
        try:
            ProductoCreate(**{k: v for k, v in caso.items() if k != "error"})
            print(f"   ❌ Debería haber fallado: {caso['error']}")
        except Exception as e:
            print(f"   ✅ Validación correcta para {caso['error']}: {str(e)[:50]}...")

def main():
    """Función principal que ejecuta todos los ejemplos"""
    print("🚀 INICIANDO EJEMPLO COMPLETO DE ORM PROFESIONAL")
    print("=" * 60)
    
    # Verificar conexión a la base de datos
    print("\n1. Verificando conexión a la base de datos...")
    if not check_connection():
        print("❌ No se pudo conectar a la base de datos")
        return
    
    print("✅ Conexión a la base de datos exitosa")
    
    # Crear tablas
    print("\n2. Creando tablas...")
    try:
        create_tables()
        print("✅ Tablas creadas exitosamente")
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return
    
    # Ejecutar ejemplos
    try:
        # Ejemplo de validaciones
        ejemplo_validaciones()
        
        # Ejemplo de usuarios
        usuarios = ejemplo_usuarios()
        
        # Ejemplo de categorías
        categorias = ejemplo_categorias()
        
        # Ejemplo de productos
        productos = ejemplo_productos(usuarios, categorias)
        
        # Resumen final
        mostrar_separador("RESUMEN FINAL")
        print(f"📊 Usuarios creados: {len(usuarios)}")
        print(f"📂 Categorías creadas: {len(categorias)}")
        print(f"📦 Productos creados: {len(productos)}")
        
        print("\n🎉 ¡Ejemplo completado exitosamente!")
        print("\nConceptos demostrados:")
        print("   • Estructura modular de ORM")
        print("   • Entidades con SQLAlchemy y Pydantic")
        print("   • Operaciones CRUD separadas")
        print("   • Validaciones de datos")
        print("   • Manejo de relaciones")
        print("   • Consultas avanzadas")
        print("   • Manejo de errores")
        print("   • Configuración de base de datos")
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
