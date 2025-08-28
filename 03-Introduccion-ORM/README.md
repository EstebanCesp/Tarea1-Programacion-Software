# Introducción a ORM (Object-Relational Mapping)

## ¿Qué es ORM?

ORM (Object-Relational Mapping) es una técnica de programación que permite convertir datos entre sistemas de tipos incompatibles en lenguajes de programación orientados a objetos. En términos simples, **ORM nos permite trabajar con bases de datos usando objetos de Python en lugar de escribir SQL directamente**.

### ¿Por qué usar ORM?

Antes de ORM, los desarrolladores tenían que escribir consultas SQL manualmente, lo que presentaba varios problemas:

- **Código repetitivo**: Escribir las mismas consultas SQL una y otra vez
- **Dependencia de la base de datos**: El código SQL era específico para cada motor de base de datos
- **Vulnerabilidades de seguridad**: Riesgo de inyecciones SQL
- **Mantenimiento complejo**: Cambios en la estructura de la base requerían modificar múltiples archivos
- **Falta de tipado**: No había validación de tipos en tiempo de compilación

## Ventajas del ORM

- **Productividad**: Menos código repetitivo y más tiempo enfocado en la lógica de negocio
- **Mantenibilidad**: Código más limpio, organizado y fácil de mantener
- **Portabilidad**: Funciona con diferentes bases de datos (SQLite, PostgreSQL, MySQL, etc.)
- **Seguridad**: Previene inyecciones SQL automáticamente
- **Tipado**: Mejor control de tipos de datos y validaciones
- **Abstracción**: No necesitas conocer SQL avanzado para operaciones complejas
- **Consistencia**: Patrones uniformes para todas las operaciones de base de datos

## Conceptos Clave

### 1. **Modelo (Model)**
Representa una tabla de la base de datos como una clase de Python. Cada instancia de la clase representa una fila en la tabla, y cada atributo de la clase representa una columna.

```python
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    email = Column(String(120))
```

### 2. **Sesión (Session)**
Maneja la conexión y transacciones con la base de datos. Es como un "carrito de compras" que acumula cambios antes de enviarlos a la base de datos.

```python
session = Session()
session.add(nuevo_usuario)  # Agregar a la sesión
session.commit()             # Confirmar cambios
session.rollback()           # Deshacer cambios
```

### 3. **Query (Consulta)**
Permite realizar consultas a la base de datos usando métodos de Python en lugar de SQL. SQLAlchemy traduce estas consultas a SQL optimizado.

```python
# En lugar de: SELECT * FROM usuarios WHERE email = 'juan@email.com'
usuarios = session.query(Usuario).filter_by(email='juan@email.com').all()
```

### 4. **Migración**
Proceso de actualizar la estructura de la base de datos cuando cambias los modelos. Herramientas como Alembic automatizan este proceso.

### 5. **Relaciones**
ORM permite definir relaciones entre modelos de forma declarativa:

- **One-to-One**: Un usuario tiene un perfil
- **One-to-Many**: Una categoría tiene muchos productos
- **Many-to-Many**: Un producto puede estar en múltiples categorías

## Ejemplos Incluidos

- `ejemplo_basico.py`: Conceptos fundamentales de ORM
- `ejemplo_avanzado.py`: Relaciones entre modelos y consultas complejas
- `requirements.txt`: Dependencias necesarias

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python ejemplo_basico.py
python ejemplo_avanzado.py
```

## Recursos Adicionales

- [Documentación oficial de SQLAlchemy](https://docs.sqlalchemy.org/)
- [Tutorial de ORM con Python](https://realpython.com/python-sqlite-sqlalchemy/)
- [Patrones de diseño en ORM](https://martinfowler.com/eaaCatalog/)
