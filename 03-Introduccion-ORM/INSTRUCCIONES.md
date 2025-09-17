# Sistema de Gestión de Productos con ORM SQLAlchemy y Neon PostgreSQL

##  Configuración Inicial

### 1. Configurar variables de entorno
Copia el archivo `env.example` a `.env` y configura tu conexión a Neon:

```bash
cp env.example .env
```

Edita el archivo `.env` con tus credenciales de Neon:
```
DATABASE_URL=postgresql://usuario:password@ep-xxxxx.us-east-1.aws.neon.tech/nombre_db?sslmode=require
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Crear migraciones (opcional)
```bash
# Generar migración inicial
alembic revision --autogenerate -m "Initial migration"

# Aplicar migraciones
alembic upgrade head
```

##  Ejecutar el Sistema

### Ejecutar la aplicación principal
```bash
python main.py
```

##  Funcionalidades del Sistema

### 1. Gestión de Usuarios
- - Crear usuarios con validaciones (email, teléfono)
- - Listar todos los usuarios
- - Buscar usuario por email
- - Actualizar información de usuarios
- - Eliminar usuarios
- - Crear usuario administrador por defecto

### 2. Gestión de Categorías
- - Crear categorías con validaciones
- - Listar todas las categorías
- - Buscar categoría por nombre
- - Actualizar categorías
- - Eliminar categorías

### 3. Gestión de Productos
- - Crear productos con validaciones completas
- - Listar todos los productos
- - Buscar productos por nombre
- - Actualizar productos
- - Actualizar stock específicamente
- - Eliminar productos
- - Ver productos por categoría
- - Ver productos por usuario

### 4. Consultas y Reportes
- - Resumen general del sistema
- - Productos con bajo stock
- - Productos por rango de precio
- - Listar usuarios administradores
- - Estadísticas generales

##  Características Técnicas

### Modelos con UUID
- Todos los IDs son UUIDs únicos
- Generación automática con `uuid.uuid4()`
- Compatible con PostgreSQL

### Validaciones Robustas
- **Usuarios**: Email válido, teléfono opcional, nombres únicos
- **Categorías**: Nombres únicos, descripciones opcionales
- **Productos**: Precios positivos, stock no negativo, relaciones válidas

### Auditoría
- Campos de creación y edición automáticos
- Seguimiento de usuarios que crean/editan registros
- Timestamps con zona horaria

### Manejo de Errores
- Validaciones en tiempo real
- Mensajes de error descriptivos
- Rollback automático en caso de errores

##  Estructura de Base de Datos

### Tabla `usuarios`
- `id_usuario` (UUID, PK)
- `nombre` (String, 100 chars)
- `nombre_usuario` (String, 50 chars, único)
- `email` (String, 150 chars, único)
- `contraseña_hash` (String, 255 chars)
- `telefono` (String, 20 chars, opcional)
- `activo` (Boolean, default True)
- `es_admin` (Boolean, default False)
- `fecha_creacion` (DateTime)
- `fecha_edicion` (DateTime)

### Tabla `categorias`
- `id_categoria` (UUID, PK)
- `nombre` (String, 100 chars, único)
- `descripcion` (Text, opcional)
- `fecha_creacion` (DateTime)
- `fecha_edicion` (DateTime)
- `id_usuario_crea` (UUID, FK)
- `id_usuario_edita` (UUID, FK, opcional)

### Tabla `productos`
- `id_producto` (UUID, PK)
- `nombre` (String, 200 chars)
- `descripcion` (Text)
- `precio` (Numeric, 10,2)
- `stock` (Integer, default 0)
- `fecha_creacion` (DateTime)
- `fecha_edicion` (DateTime)
- `categoria_id` (UUID, FK)
- `usuario_id` (UUID, FK)
- `id_usuario_crea` (UUID, FK)
- `id_usuario_edita` (UUID, FK, opcional)

##  Uso del Sistema

1. **Primera ejecución**: El sistema creará automáticamente las tablas
2. **Crear administrador**: Usa la opción 7 en Gestión de Usuarios
3. **Iniciar sesión**: Con las credenciales creadas
4. **Crear categorías**: Necesarias antes de crear productos
5. **Crear usuarios**: Para asignar productos
6. **Crear productos**: Selecciona categoría y usuario existentes

##  **Sistema de Autenticación**

### **Primera configuración:**
1. Al ejecutar por primera vez, crea un usuario administrador
2. El sistema generará una contraseña temporal segura
3. Inicia sesión con las credenciales proporcionadas
4. Cambia la contraseña en "Mi Perfil" → "Cambiar Contraseña"

### **Características de seguridad:**
- - Contraseñas hasheadas con PBKDF2 y salt
- - Validación de fortaleza de contraseñas
- - Máximo 3 intentos de login
- - Sesión persistente durante la ejecución
- - Opción de cerrar sesión y volver a autenticarse

##  Ejemplos de Uso

### Crear un usuario administrador
```
1. Gestión de Usuarios
2. Crear Usuario Administrador
```

### Crear una categoría
```
1. Gestión de Categorías
2. Crear Categoría
3. Ingresar: "Electrónicos"
4. Descripción: "Dispositivos electrónicos"
```

### Crear un producto
```
1. Gestión de Productos
2. Crear Producto
3. Seleccionar categoría y usuario
4. Ingresar datos del producto
```

##  Solución de Problemas

### Error de conexión a Neon
- Verifica que la URL en `.env` sea correcta
- Asegúrate de que la base de datos esté activa en Neon
- Verifica que el SSL esté habilitado

### Error de validación
- Revisa que los emails sean válidos
- Los precios deben ser números positivos
- Los nombres no pueden estar vacíos

### Error de relaciones
- Asegúrate de crear categorías antes que productos
- Crea usuarios antes de asignar productos
