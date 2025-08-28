"""
Ejemplo Avanzado de ORM con SQLAlchemy
======================================

Este ejemplo muestra conceptos avanzados de ORM:
- Relaciones entre modelos (One-to-Many, Many-to-Many)
- Consultas complejas
- Lazy loading vs Eager loading
- Transacciones
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from datetime import datetime
import os

# Crear la base de datos
DATABASE_URL = "sqlite:///ejemplo_orm_avanzado.db"
engine = create_engine(DATABASE_URL, echo=True)

# Clase base para los modelos
Base = declarative_base()

# Tabla de asociación para relación Many-to-Many
categoria_producto = Table(
    'categoria_producto',
    Base.metadata,
    Column('categoria_id', Integer, ForeignKey('categorias.id')),
    Column('producto_id', Integer, ForeignKey('productos.id'))
)

class Categoria(Base):
    """Modelo de Categoría"""
    
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    # Relación One-to-Many con Producto
    productos = relationship("Producto", back_populates="categoria")
    
    # Relación Many-to-Many con Producto (a través de la tabla de asociación)
    productos_many = relationship("Producto", secondary=categoria_producto, back_populates="categorias_many")
    
    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre='{self.nombre}')>"

class Producto(Base):
    """Modelo de Producto"""
    
    __tablename__ = 'productos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)  # Precio en centavos
    stock = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    fecha_creacion = Column(DateTime, default=datetime.now)
    
    # Relación Many-to-One con Categoria
    categoria = relationship("Categoria", back_populates="productos")
    
    # Relación Many-to-Many con Categoria
    categorias_many = relationship("Categoria", secondary=categoria_producto, back_populates="productos_many")
    
    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio=${self.precio/100:.2f})>"
    
    @property
    def precio_formateado(self):
        """Retorna el precio formateado como string"""
        return f"${self.precio/100:.2f}"

class Venta(Base):
    """Modelo de Venta"""
    
    __tablename__ = 'ventas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Integer, nullable=False)
    fecha_venta = Column(DateTime, default=datetime.now)
    
    # Relación con Producto
    producto = relationship("Producto")
    
    def __repr__(self):
        return f"<Venta(id={self.id}, producto_id={self.producto_id}, cantidad={self.cantidad})>"
    
    @property
    def total(self):
        """Calcula el total de la venta"""
        return self.cantidad * self.precio_unitario

def crear_tablas():
    """Crea todas las tablas"""
    print("Creando tablas avanzadas...")
    Base.metadata.create_all(engine)
    print("Tablas creadas exitosamente")

def crear_sesion():
    """Crea y retorna una sesión"""
    Session = sessionmaker(bind=engine)
    return Session()

def poblar_datos_ejemplo():
    """Pobla la base de datos con datos de ejemplo"""
    print("\nPoblando base de datos con datos de ejemplo...")
    
    session = crear_sesion()
    
    try:
        # Crear categorías
        categoria1 = Categoria(nombre="Electrónicos", descripcion="Productos electrónicos y tecnología")
        categoria2 = Categoria(nombre="Ropa", descripcion="Vestimenta y accesorios")
        categoria3 = Categoria(nombre="Hogar", descripcion="Artículos para el hogar")
        
        session.add_all([categoria1, categoria2, categoria3])
        session.commit()
        
        # Crear productos
        producto1 = Producto(nombre="Laptop", precio=150000, stock=10, categoria=categoria1)
        producto2 = Producto(nombre="Smartphone", precio=80000, stock=15, categoria=categoria1)
        producto3 = Producto(nombre="Camiseta", precio=2500, stock=50, categoria=categoria2)
        producto4 = Producto(nombre="Sofá", precio=50000, stock=5, categoria=categoria3)
        
        # Asignar múltiples categorías a algunos productos
        producto1.categorias_many.extend([categoria1, categoria3])  # Laptop es electrónico y hogar
        
        session.add_all([producto1, producto2, producto3, producto4])
        session.commit()
        
        print("Datos de ejemplo creados exitosamente")
        
    except Exception as e:
        print(f"Error al poblar datos: {e}")
        session.rollback()
    finally:
        session.close()

def ejemplo_relaciones():
    """Ejemplo de consultas con relaciones"""
    print("\nEjemplos de relaciones entre modelos...")
    
    session = crear_sesion()
    
    try:
        # Consulta con JOIN (Eager Loading)
        print("\nProductos con sus categorías (Eager Loading):")
        productos = session.query(Producto).options(joinedload(Producto.categoria)).all()
        
        for producto in productos:
            print(f"   - {producto.nombre} | Categoría: {producto.categoria.nombre}")
        
        # Consulta con filtros en relaciones
        print("\nProductos de la categoría 'Electrónicos':")
        productos_electronicos = session.query(Producto).join(Producto.categoria).filter(
            Categoria.nombre == "Electrónicos"
        ).all()
        
        for producto in productos_electronicos:
            print(f"   - {producto.nombre} | Precio: {producto.precio_formateado}")
        
        # Consulta con relaciones Many-to-Many
        print("\nProductos con múltiples categorías:")
        productos_multiples = session.query(Producto).filter(
            Producto.categorias_many.any()
        ).all()
        
        for producto in productos_multiples:
            categorias = [cat.nombre for cat in producto.categorias_many]
            print(f"   - {producto.nombre} | Categorías: {', '.join(categorias)}")
            
    except Exception as e:
        print(f"Error en consultas de relaciones: {e}")
    finally:
        session.close()

def ejemplo_consultas_complejas():
    """Ejemplo de consultas complejas"""
    print("\nConsultas complejas y agregaciones...")
    
    session = crear_sesion()
    
    try:
        # Productos con stock bajo
        print("\nProductos con stock bajo (< 10):")
        productos_stock_bajo = session.query(Producto).filter(Producto.stock < 10).all()
        
        for producto in productos_stock_bajo:
            print(f"   - {producto.nombre} | Stock: {producto.stock}")
        
        # Categorías con más productos
        print("\nCategorías ordenadas por cantidad de productos:")
        categorias_ordenadas = session.query(
            Categoria.nombre,
            Categoria.id
        ).join(Categoria.productos).group_by(Categoria.id).order_by(
            Categoria.id
        ).all()
        
        for categoria in categorias_ordenadas:
            print(f"   - {categoria.nombre}")
        
        # Búsqueda por texto
        print("\nBúsqueda de productos que contengan 'phone':")
        productos_busqueda = session.query(Producto).filter(
            Producto.nombre.ilike('%phone%')
        ).all()
        
        for producto in productos_busqueda:
            print(f"   - {producto.nombre}")
            
    except Exception as e:
        print(f"Error en consultas complejas: {e}")
    finally:
        session.close()

def ejemplo_transacciones():
    """Ejemplo de transacciones"""
    print("\nEjemplo de transacciones...")
    
    session = crear_sesion()
    
    try:
        # Simular una venta
        print("\nProcesando venta...")
        
        # Buscar producto
        producto = session.query(Producto).filter_by(nombre="Laptop").first()
        
        if producto and producto.stock > 0:
            # Crear venta
            venta = Venta(
                producto_id=producto.id,
                cantidad=1,
                precio_unitario=producto.precio
            )
            
            # Actualizar stock
            producto.stock -= 1
            
            # Agregar venta
            session.add(venta)
            
            # Commit de la transacción
            session.commit()
            
            print(f"Venta procesada: {venta.producto.nombre} por {venta.total/100:.2f}")
            print(f"   Stock restante: {producto.stock}")
        else:
            print("Producto no disponible")
            
    except Exception as e:
        print(f"Error en transacción: {e}")
        session.rollback()
    finally:
        session.close()

def main():
    """Función principal"""
    print("INICIANDO EJEMPLO AVANZADO DE ORM")
    print("=" * 60)
    
    # Crear tablas
    crear_tablas()
    
    # Poblar con datos de ejemplo
    poblar_datos_ejemplo()
    
    # Ejemplos avanzados
    ejemplo_relaciones()
    ejemplo_consultas_complejas()
    ejemplo_transacciones()
    
    print("\n" + "=" * 60)
    print("EJEMPLO AVANZADO COMPLETADO")
    print("\nConceptos avanzados aprendidos:")
    print("   • Relaciones One-to-Many y Many-to-Many")
    print("   • Eager Loading vs Lazy Loading")
    print("   • Consultas complejas con JOINs")
    print("   • Transacciones y rollback")
    print("   • Filtros y búsquedas avanzadas")

if __name__ == "__main__":
    main()
