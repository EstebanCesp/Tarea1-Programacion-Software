# Sistema de Gestión de Productos - API REST

Este proyecto ha sido refactorizado para usar FastAPI como API REST, eliminando la interfaz de consola y proporcionando endpoints para todas las operaciones.

## 🚀 Características

- **API REST** con FastAPI
- **Autenticación** de usuarios
- **Gestión de usuarios** (CRUD completo)
- **Gestión de categorías** (CRUD completo)
- **Gestión de productos** (CRUD completo)
- **Documentación automática** con Swagger UI
- **Base de datos PostgreSQL** con Neon
- **ORM SQLAlchemy** para operaciones de base de datos

## 📋 Requisitos

- Python 3.8+
- PostgreSQL (usando Neon)
- Variables de entorno configuradas

## 🛠️ Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar variables de entorno:**
Crear un archivo `.env` en la raíz del proyecto:
```env
DATABASE_URL=postgresql://usuario:contraseña@host:puerto/database
```

3. **Ejecutar el servidor:**
```bash
python main.py
```

El servidor se ejecutará en `http://localhost:8000`

## 📚 Documentación de la API

Una vez que el servidor esté ejecutándose, puedes acceder a:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔗 Endpoints Principales

### Autenticación (`/auth`)
- `POST /auth/login` - Iniciar sesión
- `POST /auth/crear-admin` - Crear usuario administrador
- `GET /auth/verificar/{usuario_id}` - Verificar usuario
- `GET /auth/estado` - Estado del sistema

### Usuarios (`/usuarios`)
- `GET /usuarios/` - Listar usuarios
- `GET /usuarios/{usuario_id}` - Obtener usuario por ID
- `GET /usuarios/email/{email}` - Obtener usuario por email
- `GET /usuarios/username/{nombre_usuario}` - Obtener usuario por nombre de usuario
- `POST /usuarios/` - Crear usuario
- `PUT /usuarios/{usuario_id}` - Actualizar usuario
- `DELETE /usuarios/{usuario_id}` - Eliminar usuario
- `PATCH /usuarios/{usuario_id}/desactivar` - Desactivar usuario
- `POST /usuarios/{usuario_id}/cambiar-contraseña` - Cambiar contraseña
- `GET /usuarios/admin/lista` - Listar administradores
- `GET /usuarios/{usuario_id}/es-admin` - Verificar si es admin

### Categorías (`/categorias`)
- `GET /categorias/` - Listar categorías
- `GET /categorias/{categoria_id}` - Obtener categoría por ID
- `GET /categorias/nombre/{nombre}` - Obtener categoría por nombre
- `POST /categorias/` - Crear categoría
- `PUT /categorias/{categoria_id}` - Actualizar categoría
- `DELETE /categorias/{categoria_id}` - Eliminar categoría

### Productos (`/productos`)
- `GET /productos/` - Listar productos
- `GET /productos/{producto_id}` - Obtener producto por ID
- `GET /productos/categoria/{categoria_id}` - Productos por categoría
- `GET /productos/usuario/{usuario_id}` - Productos por usuario
- `GET /productos/buscar/{nombre}` - Buscar productos por nombre
- `POST /productos/` - Crear producto
- `PUT /productos/{producto_id}` - Actualizar producto
- `PATCH /productos/{producto_id}/stock` - Actualizar stock
- `DELETE /productos/{producto_id}` - Eliminar producto

## 🔧 Uso Básico

### 1. Crear usuario administrador
```bash
curl -X POST "http://localhost:8000/auth/crear-admin"
```

### 2. Iniciar sesión
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre_usuario": "admin",
    "contraseña": "contraseña_temporal"
  }'
```

### 3. Crear un usuario
```bash
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "nombre_usuario": "juanperez",
    "email": "juan@ejemplo.com",
    "contraseña": "MiContraseña123!",
    "telefono": "+1234567890",
    "es_admin": false
  }'
```

### 4. Crear una categoría
```bash
curl -X POST "http://localhost:8000/categorias/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Electrónicos",
    "descripcion": "Dispositivos electrónicos y tecnología"
  }'
```

### 5. Crear un producto
```bash
curl -X POST "http://localhost:8000/productos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Smartphone Samsung",
    "descripcion": "Teléfono inteligente con Android",
    "precio": 599.99,
    "stock": 50,
    "categoria_id": "uuid-de-la-categoria",
    "usuario_id": "uuid-del-usuario"
  }'
```

## 🏗️ Estructura del Proyecto

```
03-Introduccion-ORM/
├── apis/                    # APIs REST
│   ├── __init__.py
│   ├── auth.py             # Autenticación
│   ├── usuario.py          # Gestión de usuarios
│   ├── categoria.py        # Gestión de categorías
│   └── producto.py         # Gestión de productos
├── auth/                   # Sistema de autenticación
│   └── security.py
├── crud/                   # Operaciones CRUD (sin cambios)
│   ├── usuario_crud.py
│   ├── categoria_crud.py
│   └── producto_crud.py
├── database/               # Configuración de base de datos
│   └── config.py
├── entities/               # Modelos de base de datos
│   ├── usuario.py
│   ├── categoria.py
│   └── producto.py
├── schemas.py              # Modelos Pydantic para la API
├── main.py                 # Aplicación FastAPI principal
├── requirements.txt        # Dependencias
└── README_API.md          # Esta documentación
```

## 🔒 Seguridad

- Las contraseñas se almacenan con hash seguro (PBKDF2)
- Validación de fortaleza de contraseñas
- Autenticación requerida para operaciones sensibles
- Validación de datos de entrada con Pydantic

## 📝 Notas Importantes

1. **Primera ejecución**: Usa `/auth/crear-admin` para crear el usuario administrador inicial
2. **Base de datos**: Las tablas se crean automáticamente al iniciar la aplicación
3. **Documentación**: Siempre consulta `/docs` para la documentación interactiva
4. **CORS**: Configurado para permitir todas las orígenes en desarrollo

## 🐛 Solución de Problemas

- **Error de conexión a BD**: Verifica la variable `DATABASE_URL`
- **Puerto ocupado**: Cambia el puerto en `main.py` (línea 67)
- **Dependencias faltantes**: Ejecuta `pip install -r requirements.txt`

## 🚀 Próximos Pasos

- Implementar autenticación JWT
- Agregar middleware de logging
- Implementar rate limiting
- Agregar tests unitarios
- Configurar CI/CD
