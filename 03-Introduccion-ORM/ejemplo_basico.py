"""
Ejemplo básico de uso del ORM SQLAlchemy con SQL Server
"""

from database.config import SessionLocal, create_tables
from entities.categoria import Categoria
from entities.producto import Producto
from entities.usuario import Usuario


def ejemplo_basico():
    """Ejemplo básico de operaciones con SQLAlchemy"""
    print("=== EJEMPLO BÁSICO ORM ===\n")

    # Crear tablas
    create_tables()
    print("✓ Tablas creadas")

    # Crear sesión
    db = SessionLocal()

    try:
        # 1. Crear un usuario
        print("\n1. Creando usuario...")
        usuario = Usuario(
            nombre="Ana López", email="ana.lopez@email.com", telefono="3009876543"
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        print(f"✓ Usuario creado con ID: {usuario.id}")

        # 2. Crear una categoría
        print("\n2. Creando categoría...")
        categoria = Categoria(
            nombre="Libros", descripcion="Libros y material educativo"
        )
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        print(f"✓ Categoría creada con ID: {categoria.id}")

        # 3. Crear un producto
        print("\n3. Creando producto...")
        producto = Producto(
            nombre="Python para Principiantes",
            descripcion="Libro introductorio de Python",
            precio=45.99,
            stock=25,
            categoria_id=categoria.id,
            usuario_id=usuario.id,
        )
        db.add(producto)
        db.commit()
        db.refresh(producto)
        print(f"✓ Producto creado con ID: {producto.id}")

        # 4. Consultar datos
        print("\n4. Consultando datos...")

        # Obtener todos los usuarios
        usuarios = db.query(Usuario).all()
        print(f"Total usuarios: {len(usuarios)}")

        # Obtener todos los productos
        productos = db.query(Producto).all()
        print(f"Total productos: {len(productos)}")

        # 5. Consulta con filtro
        print("\n5. Consulta con filtro...")
        productos_caros = db.query(Producto).filter(Producto.precio > 40).all()
        print(f"Productos con precio > $40: {len(productos_caros)}")

        # 6. Actualizar datos
        print("\n6. Actualizando datos...")
        producto.precio = 39.99
        db.commit()
        print("✓ Precio actualizado")

        # 7. Consulta con JOIN
        print("\n7. Consulta con relaciones...")
        producto_con_relaciones = (
            db.query(Producto).filter(Producto.id == producto.id).first()
        )

        if producto_con_relaciones:
            print(f"Producto: {producto_con_relaciones.nombre}")
            print(f"Categoría: {producto_con_relaciones.categoria.nombre}")
            print(f"Usuario: {producto_con_relaciones.usuario.nombre}")

        print("\n=== EJEMPLO COMPLETADO ===")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    ejemplo_basico()
