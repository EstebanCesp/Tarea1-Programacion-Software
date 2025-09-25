# 04 - Introducción a APIs con FastAPI

Este módulo introduce los conceptos básicos de APIs REST usando FastAPI, incluyendo un ejemplo completo de operaciones CRUD.

## ¿Qué son las APIs?

Una **API (Application Programming Interface)** es un conjunto de reglas y protocolos que permite que diferentes aplicaciones se comuniquen entre sí. En el contexto web, las APIs REST permiten que las aplicaciones intercambien datos usando HTTP.

### Características de las APIs REST:
- **Stateless**: Cada petición es independiente
- **Resource-based**: Los datos se organizan como recursos
- **HTTP Methods**: GET, POST, PUT, DELETE
- **JSON**: Formato estándar para intercambio de datos

## FastAPI

FastAPI es un framework moderno y rápido para construir APIs con Python, basado en estándares abiertos como OpenAPI y JSON Schema.

### Ventajas de FastAPI:
- **Rápido**: Uno de los frameworks más rápidos disponibles
- **Documentación automática**: Genera documentación interactiva
- **Validación automática**: Validación de datos con Pydantic
- **Python moderno**: Soporte completo para type hints
- **Fácil de usar**: Sintaxis simple e intuitiva

## Estructura del Proyecto

```
04-Introduccion-APIs/
├── main.py              # API principal con endpoints CRUD
├── models.py            # Modelos Pydantic para validación
├── ejemplo_cliente.py   # Cliente de prueba para la API
├── requirements.txt     # Dependencias del proyecto
└── README.md           # Este archivo
```

## Instalación y Configuración

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar el servidor
```bash
python main.py
```

### 3. Acceder a la documentación
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints Disponibles

### Usuarios
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/usuarios` | Obtener todos los usuarios |
| GET | `/usuarios/{id}` | Obtener usuario por ID |
| POST | `/usuarios` | Crear nuevo usuario |
| PUT | `/usuarios/{id}` | Actualizar usuario |
| DELETE | `/usuarios/{id}` | Eliminar usuario |

### Productos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/productos` | Obtener todos los productos |
| GET | `/productos/{id}` | Obtener producto por ID |
| POST | `/productos` | Crear nuevo producto |
| PUT | `/productos/{id}` | Actualizar producto |
| DELETE | `/productos/{id}` | Eliminar producto |

### Otros
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información básica de la API |
| GET | `/estadisticas` | Estadísticas generales |

## Conceptos Clave

### 1. Modelos Pydantic
Los modelos definen la estructura de los datos y proporcionan validación automática:

```python
class UsuarioBase(BaseModel):
    nombre: str
    email: str
    edad: Optional[int] = None
```

### 2. Decoradores de FastAPI
Los decoradores definen los endpoints:

```python
@app.get("/usuarios")
async def obtener_usuarios():
    return list(usuarios_db.values())
```

### 3. Códigos de Estado HTTP
- `200`: OK (éxito)
- `201`: Created (recurso creado)
- `400`: Bad Request (error en la petición)
- `404`: Not Found (recurso no encontrado)
- `204`: No Content (eliminación exitosa)

### 4. Validación Automática
FastAPI valida automáticamente los datos de entrada usando los modelos Pydantic.

## Pruebas de la API

### Usando el cliente de prueba
```bash
python ejemplo_cliente.py
```

### Usando curl (ejemplos)
```bash
# Obtener todos los usuarios
curl http://localhost:8000/usuarios

# Crear un usuario
curl -X POST http://localhost:8000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Juan Pérez", "email": "juan@email.com", "edad": 25}'

# Obtener un usuario específico
curl http://localhost:8000/usuarios/1
```

### Usando la documentación interactiva
1. Ve a http://localhost:8000/docs
2. Expande cualquier endpoint
3. Haz clic en "Try it out"
4. Completa los datos y ejecuta

## Ejemplos de Uso

### Crear un usuario
```json
POST /usuarios
{
  "nombre": "Ana García",
  "email": "ana@email.com",
  "edad": 28
}
```

### Actualizar un usuario
```json
PUT /usuarios/1
{
  "edad": 29
}
```

### Crear un producto
```json
POST /productos
{
  "nombre": "Laptop",
  "descripcion": "Laptop para desarrollo",
  "precio": 1500.00,
  "stock": 10
}
```

## Manejo de Errores

La API incluye manejo de errores con códigos de estado apropiados:

- **400 Bad Request**: Datos inválidos o email duplicado
- **404 Not Found**: Recurso no encontrado
- **422 Unprocessable Entity**: Error de validación de datos

## Características Avanzadas

### 1. Documentación Automática
FastAPI genera automáticamente documentación interactiva basada en los modelos y endpoints.

### 2. Validación de Tipos
Los type hints de Python se usan para validación automática y documentación.

### 3. Respuestas Estructuradas
Todas las respuestas siguen un formato consistente con códigos de estado apropiados.

### 4. Base de Datos en Memoria
Este ejemplo usa una base de datos simulada en memoria para simplicidad.

## Próximos Pasos

Para proyectos más avanzados, considera:

1. **Base de datos real**: SQLAlchemy con PostgreSQL/MySQL
2. **Autenticación**: JWT tokens, OAuth2
3. **Middleware**: CORS, logging, rate limiting
4. **Testing**: pytest con FastAPI TestClient
5. **Deployment**: Docker, cloud platforms
6. **Caching**: Redis para mejorar rendimiento

## Recursos Adicionales

- [Documentación oficial de FastAPI](https://fastapi.tiangolo.com/)
- [Tutorial de Pydantic](https://pydantic-docs.helpmanual.io/)
- [Guía de APIs REST](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)

## Contribuir

Este es un proyecto educativo. Si encuentras errores o tienes sugerencias, ¡no dudes en contribuir!

---

**¡Disfruta aprendiendo sobre APIs con FastAPI!**