"""
Archivo principal para probar la funcionalidad del ORM con SQL Server
"""

from crud.categoria_crud import CategoriaCRUD
from crud.producto_crud import ProductoCRUD
from crud.usuario_crud import UsuarioCRUD
from database.config import SessionLocal, create_tables
from entities.categoria import Categoria
from entities.producto import Producto
from entities.usuario import Usuario


def main():
    """Función principal para demostrar el uso del ORM"""
    print("=== DEMO ORM SQLAlchemy con SQL Server ===\n")

    # Crear las tablas si no existen
    print("1. Creando tablas en la base de datos...")
    create_tables()
    print("✓ Tablas creadas exitosamente\n")

    # Crear sesión de base de datos
    db = SessionLocal()

    try:
        # Inicializar CRUDs
        usuario_crud = UsuarioCRUD(db)
        categoria_crud = CategoriaCRUD(db)
        producto_crud = ProductoCRUD(db)

        print("2. Creando usuarios...")
        # Crear usuarios
        usuario1 = usuario_crud.crear_usuario(
            nombre="Juan Pérez", email="juan.perez@email.com", telefono="3001234567"
        )
        print(f"✓ Usuario creado: {usuario1}")

        usuario2 = usuario_crud.crear_usuario(
            nombre="María García", email="maria.garcia@email.com", telefono="3007654321"
        )
        print(f"✓ Usuario creado: {usuario2}\n")

        print("3. Creando categorías...")
        # Crear categorías
        categoria1 = categoria_crud.crear_categoria(
            nombre="Electrónicos", descripcion="Dispositivos electrónicos y tecnología"
        )
        print(f"✓ Categoría creada: {categoria1}")

        categoria2 = categoria_crud.crear_categoria(
            nombre="Ropa", descripcion="Vestimenta y accesorios"
        )
        print(f"✓ Categoría creada: {categoria2}\n")

        print("4. Creando productos...")
        # Crear productos
        producto1 = producto_crud.crear_producto(
            nombre="Smartphone Samsung",
            descripcion="Teléfono inteligente con cámara de 64MP",
            precio=899.99,
            stock=50,
            categoria_id=categoria1.id,
            usuario_id=usuario1.id,
        )
        print(f"✓ Producto creado: {producto1}")

        producto2 = producto_crud.crear_producto(
            nombre="Camiseta Nike",
            descripcion="Camiseta deportiva de algodón",
            precio=29.99,
            stock=100,
            categoria_id=categoria2.id,
            usuario_id=usuario2.id,
        )
        print(f"✓ Producto creado: {producto2}\n")

        print("5. Consultando datos...")
        # Consultar usuarios
        usuarios = usuario_crud.obtener_usuarios()
        print(f"✓ Total de usuarios: {len(usuarios)}")
        for usuario in usuarios:
            print(f"  - {usuario.nombre} ({usuario.email})")

        # Consultar categorías
        categorias = categoria_crud.obtener_categorias()
        print(f"\n✓ Total de categorías: {len(categorias)}")
        for categoria in categorias:
            print(f"  - {categoria.nombre}: {categoria.descripcion}")

        # Consultar productos
        productos = producto_crud.obtener_productos()
        print(f"\n✓ Total de productos: {len(productos)}")
        for producto in productos:
            print(
                f"  - {producto.nombre}: ${producto.precio} (Stock: {producto.stock})"
            )

        print("\n6. Probando actualizaciones...")
        # Actualizar un producto
        producto_actualizado = producto_crud.actualizar_producto(
            producto1.id, precio=799.99, stock=45
        )
        print(f"✓ Producto actualizado: {producto_actualizado}")

        # Actualizar stock
        producto_crud.actualizar_stock(producto2.id, 95)
        print("✓ Stock actualizado")

        print("\n7. Probando búsquedas...")
        # Buscar productos por nombre
        productos_samsung = producto_crud.buscar_productos_por_nombre("Samsung")
        print(f"✓ Productos encontrados con 'Samsung': {len(productos_samsung)}")

        # Obtener productos por categoría
        productos_electronicos = producto_crud.obtener_productos_por_categoria(
            categoria1.id
        )
        print(f"✓ Productos en categoría 'Electrónicos': {len(productos_electronicos)}")

        print("\n8. Probando relaciones...")
        # Obtener un producto con sus relaciones
        producto_con_relaciones = (
            db.query(Producto).filter(Producto.id == producto1.id).first()
        )
        if producto_con_relaciones:
            print(f"✓ Producto: {producto_con_relaciones.nombre}")
            print(f"  - Categoría: {producto_con_relaciones.categoria.nombre}")
            print(f"  - Usuario: {producto_con_relaciones.usuario.nombre}")

        print("\n=== DEMO COMPLETADO EXITOSAMENTE ===")

    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        db.rollback()
    finally:
        db.close()


def demo_consultas_avanzadas():
    """Demostración de consultas más avanzadas"""
    print("\n=== CONSULTAS AVANZADAS ===\n")

    db = SessionLocal()
    try:
        # Consulta con JOIN
        print("1. Productos con información de categoría y usuario:")
        productos_completos = (
            db.query(Producto, Categoria, Usuario)
            .join(Categoria, Producto.categoria_id == Categoria.id)
            .join(Usuario, Producto.usuario_id == Usuario.id)
            .all()
        )

        for producto, categoria, usuario in productos_completos:
            print(
                f"  - {producto.nombre} | Categoría: {categoria.nombre} | Usuario: {usuario.nombre}"
            )

        # Consulta con filtros
        print("\n2. Productos con precio mayor a $50:")
        productos_caros = db.query(Producto).filter(Producto.precio > 50).all()
        for producto in productos_caros:
            print(f"  - {producto.nombre}: ${producto.precio}")

        # Consulta con ordenamiento
        print("\n3. Productos ordenados por precio (descendente):")
        productos_ordenados = db.query(Producto).order_by(Producto.precio.desc()).all()
        for producto in productos_ordenados:
            print(f"  - {producto.nombre}: ${producto.precio}")

    except Exception as e:
        print(f"❌ Error en consultas avanzadas: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
    demo_consultas_avanzadas()

