"""
Ejemplo Básico de ORM con SQLAlchemy
=====================================

Este ejemplo muestra los conceptos fundamentales de ORM:
- Definición de modelos
- Creación de tablas
- Operaciones básicas de inserción y consulta
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Crear la base de datos en memoria (SQLite)
DATABASE_URL = "sqlite:///ejemplo_orm.db"
engine = create_engine(DATABASE_URL, echo=True)

# Crear la clase base para los modelos
Base = declarative_base()

class Usuario(Base):
    """
    Modelo de Usuario que representa la tabla 'usuarios'
    
    Atributos:
        id: Identificador único del usuario
        nombre: Nombre completo del usuario
        email: Correo electrónico del usuario
        fecha_registro: Fecha y hora de registro
    """
    
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        """Representación en string del objeto Usuario"""
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"
    
    def to_dict(self):
        """Convierte el objeto a un diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_registro': self.fecha_registro.isoformat()
        }

def crear_tablas():
    """Crea todas las tablas definidas en los modelos"""
    print("Creando tablas...")
    Base.metadata.create_all(engine)
    print("Tablas creadas exitosamente")

def crear_sesion():
    """Crea y retorna una sesión de base de datos"""
    Session = sessionmaker(bind=engine)
    return Session()

def ejemplo_crear_usuario():
    """Ejemplo de creación de un usuario"""
    print("\nCreando usuario...")
    
    session = crear_sesion()
    
    try:
        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            nombre="Juan Pérez",
            email="juan.perez@email.com"
        )
        
        # Agregar a la sesión
        session.add(nuevo_usuario)
        
        # Confirmar cambios
        session.commit()
        
        print(f"Usuario creado: {nuevo_usuario}")
        
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        session.rollback()
    finally:
        session.close()

def ejemplo_consultar_usuarios():
    """Ejemplo de consulta de usuarios"""
    print("\nConsultando usuarios...")
    
    session = crear_sesion()
    
    try:
        # Consultar todos los usuarios
        usuarios = session.query(Usuario).all()
        
        if usuarios:
            print(f"Se encontraron {len(usuarios)} usuarios:")
            for usuario in usuarios:
                print(f"   - {usuario}")
        else:
            print("No se encontraron usuarios")
            
    except Exception as e:
        print(f"Error al consultar usuarios: {e}")
    finally:
        session.close()

def ejemplo_buscar_por_email():
    """Ejemplo de búsqueda específica"""
    print("\nBuscando usuario por email...")
    
    session = crear_sesion()
    
    try:
        # Buscar usuario por email
        usuario = session.query(Usuario).filter_by(email="juan.perez@email.com").first()
        
        if usuario:
            print(f"Usuario encontrado: {usuario}")
        else:
            print("Usuario no encontrado")
            
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
    finally:
        session.close()

def main():
    """Función principal que ejecuta todos los ejemplos"""
    print("INICIANDO EJEMPLO BÁSICO DE ORM")
    print("=" * 50)
    
    # Crear tablas
    crear_tablas()
    
    # Ejemplos de operaciones
    ejemplo_crear_usuario()
    ejemplo_consultar_usuarios()
    ejemplo_buscar_por_email()
    
    print("\n" + "=" * 50)
    print("EJEMPLO COMPLETADO")
    print("\nConceptos aprendidos:")
    print("   • Definición de modelos con SQLAlchemy")
    print("   • Creación de tablas automática")
    print("   • Operaciones CRUD básicas")
    print("   • Manejo de sesiones")
    print("   • Consultas simples")

if __name__ == "__main__":
    main()
