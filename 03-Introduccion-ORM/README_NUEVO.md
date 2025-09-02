# Introducción a ORM con Estructura Profesional

Este módulo presenta una implementación completa y profesional de ORM (Object-Relational Mapping) usando SQLAlchemy y Pydantic, organizada en una estructura modular y escalable.

## Estructura del Proyecto

```
03-Introduccion-ORM/
├── database/                 # Configuración de base de datos
│   ├── __init__.py
│   ├── config.py            # Configuraciones de BD
│   └── database.py          # Conexión y sesiones
├── entities/                 # Entidades del sistema
│   ├── __init__.py
│   ├── usuario.py           # Entidad Usuario
│   ├── categoria.py         # Entidad Categoria
│   └── producto.py          # Entidad Producto
├── crud/                    # Operaciones CRUD
│   ├── __init__.py
│   ├── usuario_crud.py      # CRUD de Usuario
│   ├── categoria_crud.py    # CRUD de Categoria
│   └── producto_crud.py     # CRUD de Producto
├── ejemplo_completo.py      # Ejemplo principal
├── requirements.txt         # Dependencias
└── README_NUEVO.md         # Esta documentación
```

## Características Principales

### Entidades con Pydantic
- **Validación automática** de datos de entrada
- **Serialización** consistente de respuestas
- **Esquemas separados** para Create, Update y Response
- **Validadores personalizados** para reglas de negocio

### Operaciones CRUD Completas
- **Create**: Crear nuevos registros con validación
- **Read**: Consultas con filtros, paginación y búsqueda
- **Update**: Actualizaciones parciales y completas
- **Delete**: Soft delete y eliminación permanente

### Configuración de Base de Datos
- **Soporte múltiple**: SQLite, PostgreSQL, MySQL
- **Context managers** para manejo seguro de sesiones
- **Configuración por entorno** (desarrollo/producción)
- **Logging** integrado para debugging

## Entidades del Sistema

### Usuario
```python
class Usuario(Base):
    id: int (PK)
    nombre: str (100)
    email: str (120, unique)
    telefono: str (20, optional)
    activo: bool (default: True)
    fecha_registro: datetime
    fecha_actualizacion: datetime
```

### Categoria
```python
class Categoria(Base):
    id: int (PK)
    nombre: str (100, unique)
    descripcion: text (optional)
    activa: bool (default: True)
    fecha_creacion: datetime
    fecha_actualizacion: datetime
```

### Producto
```python
class Producto(Base):
    id: int (PK)
    nombre: str (200)
    descripcion: text (optional)
    precio: float
    stock: int (default: 0)
    activo: bool (default: True)
    categoria_id: int (FK -> Categoria)
    usuario_id: int (FK -> Usuario)
    fecha_creacion: datetime
    fecha_actualizacion: datetime
```

## Relaciones

- **Usuario** → **Producto** (1:N) - Un usuario puede tener muchos productos
- **Categoria** → **Producto** (1:N) - Una categoría puede tener muchos productos

## Instalación y Configuración

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Base de Datos
Editar `database/config.py` para cambiar la configuración:

```python
# Para SQLite (desarrollo)
DATABASE_URL = "sqlite:///./ejemplo_orm.db"

# Para PostgreSQL (producción)
DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Para MySQL
DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"
```

### 3. Ejecutar el Ejemplo
```bash
python ejemplo_completo.py
```

## Ejemplos de Uso

### Crear un Usuario
```python
from entities import UsuarioCreate
from crud import UsuarioCRUD

usuario_data = UsuarioCreate(
    nombre="Juan Pérez",
    email="juan@email.com",
    telefono="+57 300 123 4567"
)

usuario = UsuarioCRUD.crear_usuario(usuario_data)
print(f"Usuario creado: {usuario.nombre}")
```

### Consultar Productos con Relaciones
```python
from crud import ProductoCRUD
from database import get_session

session = get_session()
try:
    productos = ProductoCRUD.obtener_todos(
        session, 
        incluir_relaciones=True,
        limit=10
    )
    
    for producto in productos:
        print(f"{producto.nombre} - {producto.categoria.nombre}")
finally:
    session.close()
```

### Buscar con Filtros
```python
# Buscar productos por rango de precio
productos = ProductoCRUD.buscar_por_rango_precio(
    session, 
    precio_min=100000, 
    precio_max=500000
)

# Buscar usuarios por nombre o email
usuarios = UsuarioCRUD.buscar_usuarios(
    session, 
    termino_busqueda="Juan"
)
```

### Actualizar con Validación
```python
from entities import UsuarioUpdate

update_data = UsuarioUpdate(
    telefono="+57 300 999 9999",
    activo=True
)

usuario_actualizado = UsuarioCRUD.actualizar_usuario(
    usuario_id, 
    update_data
)
```

## Validaciones Implementadas

### Usuario
- Nombre: mínimo 2 caracteres, máximo 100
- Email: formato válido y único
- Teléfono: formato numérico con caracteres especiales
- Normalización automática de nombres

### Producto
- Precio: debe ser mayor a 0
- Stock: no puede ser negativo
- Categoría y Usuario: deben existir en la BD
- Redondeo automático de precios a 2 decimales

### Categoria
- Nombre: único en el sistema
- Descripción: opcional pero validada

## Funcionalidades Avanzadas

### Estadísticas
```python
# Estadísticas de usuarios
stats = UsuarioCRUD.obtener_estadisticas(session)
print(f"Total: {stats['total_usuarios']}")
print(f"Activos: {stats['usuarios_activos']}")

# Estadísticas de productos
stats = ProductoCRUD.obtener_estadisticas(session)
print(f"Precio promedio: ${stats['precio_promedio']:,.2f}")
```

### Productos con Stock Bajo
```python
productos_bajo_stock = ProductoCRUD.obtener_productos_bajo_stock(
    session, 
    stock_minimo=10
)
```

### Soft Delete
```python
# Marcar como inactivo (soft delete)
UsuarioCRUD.eliminar_usuario(usuario_id)

# Eliminación permanente
UsuarioCRUD.eliminar_usuario_permanente(usuario_id)
```

## Beneficios de esta Estructura

### **Modularidad**
- Cada entidad en su propio archivo
- CRUD separado por entidad
- Configuración centralizada

### **Seguridad**
- Validación automática con Pydantic
- Manejo seguro de sesiones
- Prevención de inyección SQL

### **Escalabilidad**
- Fácil agregar nuevas entidades
- Patrones consistentes
- Reutilización de código

### **Mantenibilidad**
- Código bien documentado
- Separación de responsabilidades
- Fácil testing

### **Performance**
- Consultas optimizadas
- Lazy loading de relaciones
- Paginación integrada

## Configuración Avanzada

### Variables de Entorno
```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/db
DB_ECHO=True
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
```

### Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Conceptos Aprendidos

1. **ORM con SQLAlchemy**: Mapeo objeto-relacional
2. **Validación con Pydantic**: Esquemas de datos
3. **Patrón Repository**: Separación de lógica de datos
4. **Context Managers**: Manejo seguro de recursos
5. **Relaciones**: Foreign keys y joins
6. **Consultas Avanzadas**: Filtros, paginación, búsqueda
7. **Manejo de Errores**: Validaciones y excepciones
8. **Estructura Modular**: Organización profesional

## Próximos Pasos

- [ ] Implementar autenticación y autorización
- [ ] Agregar tests unitarios
- [ ] Implementar cache con Redis
- [ ] Crear API REST con FastAPI
- [ ] Agregar migraciones con Alembic
- [ ] Implementar logging avanzado
- [ ] Agregar documentación automática

---

**¡Esta estructura te proporciona una base sólida para proyectos profesionales con ORM!**
