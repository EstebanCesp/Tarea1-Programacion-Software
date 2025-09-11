"""
Script para probar la conexión con Neon PostgreSQL
"""

from database.config import SessionLocal, create_tables, engine
from entities.categoria import Categoria
from entities.producto import Producto
from entities.usuario import Usuario


def test_connection():
    """Probar la conexión con la base de datos"""
    try:
        # Probar conexión
        with engine.connect() as connection:
            from sqlalchemy import text

            result = connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa con Neon PostgreSQL!")
            print(f"Resultado de prueba: {result.fetchone()}")

        # Crear tablas
        print("\n📋 Creando tablas...")
        create_tables()
        print("✅ Tablas creadas exitosamente!")

        # Probar inserción de datos
        print("\n📝 Probando inserción de datos...")
        db = SessionLocal()

        try:
            # Crear un usuario de prueba
            usuario_test = Usuario(
                nombre="Usuario Test",
                email="test@neon.com",
                telefono="3001234567",
                es_admin=False,
            )
            db.add(usuario_test)
            db.commit()
            print(f"✅ Usuario creado: {usuario_test}")

            # Crear una categoría de prueba
            categoria_test = Categoria(
                nombre="Test Category",
                descripcion="Categoría de prueba para Neon",
                id_usuario_crea=usuario_test.id_usuario,
            )
            db.add(categoria_test)
            db.commit()
            print(f"✅ Categoría creada: {categoria_test}")

            # Crear un producto de prueba
            producto_test = Producto(
                nombre="Producto Test",
                descripcion="Producto de prueba para Neon",
                precio=99.99,
                stock=10,
                categoria_id=categoria_test.id_categoria,
                usuario_id=usuario_test.id_usuario,
                id_usuario_crea=usuario_test.id_usuario,
            )
            db.add(producto_test)
            db.commit()
            print(f"✅ Producto creado: {producto_test}")

            print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
            print("Tu ORM está listo para usar con Neon PostgreSQL")

        except Exception as e:
            print(f"❌ Error en las pruebas: {e}")
            db.rollback()
        finally:
            db.close()

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 Verifica que:")
        print("1. Hayas creado el archivo .env con la URL de Neon")
        print("2. La URL de conexión sea correcta")
        print("3. Hayas instalado las dependencias: pip install -r requirements.txt")


if __name__ == "__main__":
    test_connection()
