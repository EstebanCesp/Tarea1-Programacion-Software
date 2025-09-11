"""
Script para probar la conexión asíncrona con Neon PostgreSQL
Basado en el ejemplo de Neon
"""

import asyncio
import os
import re

from dotenv import load_dotenv
from entities.categoria import Categoria
from entities.producto import Producto
from entities.usuario import Usuario
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


async def async_main() -> None:
    """Función principal asíncrona para probar la conexión"""
    try:
        # Crear el motor asíncrono
        engine = create_async_engine(
            re.sub(r"^postgresql:", "postgresql+asyncpg:", os.getenv("DATABASE_URL")),
            echo=True,
        )

        # Probar conexión básica
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("✅ Conexión exitosa con Neon PostgreSQL!")
            print(f"Resultado de prueba: {result.fetchall()}")

        # Crear tablas
        print("\n📋 Creando tablas...")
        async with engine.begin() as conn:
            # Importar todas las entidades para crear las tablas
            from database.config import Base

            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas exitosamente!")

        # Probar inserción de datos
        print("\n📝 Probando inserción de datos...")
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False
        )

        async with async_session() as session:
            try:
                # Crear un usuario de prueba
                usuario_test = Usuario(
                    nombre="Usuario Test Async",
                    email="test-async@neon.com",
                    telefono="3001234567",
                )
                session.add(usuario_test)
                await session.commit()
                print(f"✅ Usuario creado: {usuario_test}")

                # Crear una categoría de prueba
                categoria_test = Categoria(
                    nombre="Test Category Async",
                    descripcion="Categoría de prueba asíncrona para Neon",
                )
                session.add(categoria_test)
                await session.commit()
                print(f"✅ Categoría creada: {categoria_test}")

                # Crear un producto de prueba
                producto_test = Producto(
                    nombre="Producto Test Async",
                    descripcion="Producto de prueba asíncrono para Neon",
                    precio=99.99,
                    stock=10,
                    categoria_id=categoria_test.id,
                    usuario_id=usuario_test.id,
                )
                session.add(producto_test)
                await session.commit()
                print(f"✅ Producto creado: {producto_test}")

                print("\n🎉 ¡Todas las pruebas asíncronas pasaron exitosamente!")
                print("Tu ORM asíncrono está listo para usar con Neon PostgreSQL")

            except Exception as e:
                print(f"❌ Error en las pruebas: {e}")
                await session.rollback()

        await engine.dispose()

    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        print("\n🔧 Verifica que:")
        print("1. Hayas creado el archivo .env con la URL de Neon")
        print("2. La URL de conexión sea correcta")
        print("3. Hayas instalado las dependencias: pip install -r requirements.txt")


if __name__ == "__main__":
    asyncio.run(async_main())
