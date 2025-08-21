"""
Ejemplos prácticos de Pydantic para el curso de Programación de Software
"""

from pydantic import BaseModel, validator, Field, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
import json

# ============================================================================
# EJEMPLO 1: Modelo básico de Usuario
# ============================================================================

class Usuario(BaseModel):
    """Modelo básico para representar un usuario"""
    id: int
    nombre: str
    email: str
    edad: Optional[int] = None
    activo: bool = True
    
    @validator('nombre')
    def validar_nombre(cls, v):
        """Valida que el nombre tenga al menos 2 caracteres"""
        if len(v.strip()) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.strip().title()
    
    @validator('edad')
    def validar_edad(cls, v):
        """Valida que la edad sea razonable"""
        if v is not None:
            if v < 0 or v > 120:
                raise ValueError('La edad debe estar entre 0 y 120 años')
        return v

# ============================================================================
# EJEMPLO 2: Modelo de Producto con validaciones avanzadas
# ============================================================================

class Producto(BaseModel):
    """Modelo para representar un producto en una tienda"""
    id: int
    nombre: str
    precio: float
    categoria: str
    stock: int = 0
    descripcion: Optional[str] = None
    
    @validator('precio')
    def validar_precio(cls, v):
        """Valida que el precio sea positivo"""
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return round(v, 2)
    
    @validator('stock')
    def validar_stock(cls, v):
        """Valida que el stock no sea negativo"""
        if v < 0:
            raise ValueError('El stock no puede ser negativo')
        return v
    
    @validator('categoria')
    def validar_categoria(cls, v):
        """Valida que la categoría sea válida"""
        categorias_validas = ['electronica', 'ropa', 'libros', 'hogar', 'deportes']
        if v.lower() not in categorias_validas:
            raise ValueError(f'Categoría debe ser una de: {categorias_validas}')
        return v.lower()

# ============================================================================
# EJEMPLO 3: Modelo de Orden con relaciones
# ============================================================================

class ItemOrden(BaseModel):
    """Modelo para un item en una orden"""
    producto_id: int
    cantidad: int
    precio_unitario: float
    
    @validator('cantidad')
    def validar_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v
    
    @property
    def total(self) -> float:
        """Calcula el total del item"""
        return self.cantidad * self.precio_unitario

class Orden(BaseModel):
    """Modelo para representar una orden de compra"""
    id: int
    usuario_id: int
    items: List[ItemOrden]
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    estado: str = "pendiente"
    
    @validator('estado')
    def validar_estado(cls, v):
        estados_validos = ['pendiente', 'confirmada', 'enviada', 'entregada', 'cancelada']
        if v not in estados_validos:
            raise ValueError(f'Estado debe ser uno de: {estados_validos}')
        return v
    
    @property
    def total_orden(self) -> float:
        """Calcula el total de la orden"""
        return sum(item.total for item in self.items)

# ============================================================================
# EJEMPLO 4: Configuración de aplicación
# ============================================================================

class ConfiguracionApp(BaseModel):
    """Modelo para la configuración de la aplicación"""
    nombre_app: str = "Mi Tienda Online"
    puerto: int = 8000
    debug: bool = False
    base_datos_url: str
    max_conexiones: int = 100
    
    @validator('puerto')
    def validar_puerto(cls, v):
        if v < 1024 or v > 65535:
            raise ValueError('El puerto debe estar entre 1024 y 65535')
        return v
    
    @validator('max_conexiones')
    def validar_conexiones(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('Las conexiones deben estar entre 1 y 1000')
        return v

# ============================================================================
# FUNCIONES DE DEMOSTRACIÓN
# ============================================================================

def demostrar_usuario():
    """Demuestra el uso del modelo Usuario"""
    print("=== DEMOSTRACIÓN: Modelo Usuario ===")
    
    # Crear usuario válido
    try:
        usuario1 = Usuario(
            id=1,
            nombre="  juan carlos  ",  # Se limpiará y capitalizará
            email="juan@ejemplo.com",
            edad=25
        )
        print(f"✅ Usuario creado: {usuario1}")
        print(f"   JSON: {usuario1.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Intentar crear usuario inválido
    try:
        usuario2 = Usuario(
            id=2,
            nombre="a",  # Muy corto
            email="maria@ejemplo.com",
            edad=150  # Edad inválida
        )
    except Exception as e:
        print(f"❌ Error esperado: {e}")

def demostrar_producto():
    """Demuestra el uso del modelo Producto"""
    print("\n=== DEMOSTRACIÓN: Modelo Producto ===")
    
    # Crear producto válido
    try:
        producto1 = Producto(
            id=1,
            nombre="Laptop Gaming",
            precio=1299.99,
            categoria="electronica",
            stock=10,
            descripcion="Laptop para gaming de alto rendimiento"
        )
        print(f"✅ Producto creado: {producto1}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Intentar crear producto inválido
    try:
        producto2 = Producto(
            id=2,
            nombre="Producto Inválido",
            precio=-50.0,  # Precio negativo
            categoria="categoria_invalida",  # Categoría inválida
            stock=-5  # Stock negativo
        )
    except Exception as e:
        print(f"❌ Error esperado: {e}")

def demostrar_orden():
    """Demuestra el uso del modelo Orden"""
    print("\n=== DEMOSTRACIÓN: Modelo Orden ===")
    
    # Crear items válidos
    item1 = ItemOrden(producto_id=1, cantidad=2, precio_unitario=29.99)
    item2 = ItemOrden(producto_id=2, cantidad=1, precio_unitario=99.99)
    
    # Crear orden
    try:
        orden = Orden(
            id=1,
            usuario_id=1,
            items=[item1, item2],
            estado="confirmada"
        )
        print(f"✅ Orden creada: {orden}")
        print(f"   Total de la orden: ${orden.total_orden:.2f}")
        print(f"   JSON: {orden.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def demostrar_configuracion():
    """Demuestra el uso del modelo ConfiguracionApp"""
    print("\n=== DEMOSTRACIÓN: Configuración de App ===")
    
    try:
        config = ConfiguracionApp(
            base_datos_url="postgresql://usuario:password@localhost/db",
            puerto=8080,
            debug=True
        )
        print(f"✅ Configuración creada: {config}")
        print(f"   JSON: {config.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")

def demostrar_serializacion():
    """Demuestra la serialización y deserialización"""
    print("\n=== DEMOSTRACIÓN: Serialización ===")
    
    # Crear objeto
    usuario = Usuario(id=1, nombre="Ana", email="ana@ejemplo.com", edad=30)
    
    # Serializar a JSON
    json_data = usuario.json()
    print(f"✅ JSON generado: {json_data}")
    
    # Deserializar desde JSON
    usuario_recuperado = Usuario.parse_raw(json_data)
    print(f"✅ Objeto recuperado: {usuario_recuperado}")
    
    # Verificar que son iguales
    print(f"   ¿Son iguales? {usuario == usuario_recuperado}")

# ============================================================================
# EJECUCIÓN DE DEMOSTRACIONES
# ============================================================================

if __name__ == "__main__":
    print("🚀 INICIANDO DEMOSTRACIONES DE PYDANTIC")
    print("=" * 50)
    
    # Ejecutar todas las demostraciones
    demostrar_usuario()
    demostrar_producto()
    demostrar_orden()
    demostrar_configuracion()
    demostrar_serializacion()
    
    print("\n" + "=" * 50)
    print("✅ TODAS LAS DEMOSTRACIONES COMPLETADAS")
    print("\n💡 Consejos:")
    print("   - Ejecuta este archivo para ver los ejemplos en acción")
    print("   - Modifica los valores para probar diferentes validaciones")
    print("   - Experimenta creando tus propios modelos")