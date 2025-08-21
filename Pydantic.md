# Pydantic: Validación de Datos en Python

## ¿Qué es Pydantic?

Pydantic es una biblioteca de Python que proporciona validación de datos usando anotaciones de tipo de Python. Es especialmente útil para:

- **Validación de datos**: Asegurar que los datos cumplan con las especificaciones esperadas
- **Serialización**: Convertir objetos Python a JSON y viceversa
- **Configuración**: Manejar configuraciones de aplicaciones de forma segura
- **Documentación automática**: Generar documentación para APIs automáticamente

## Instalación

```bash
pip install pydantic
```

## Conceptos Básicos

### 1. Modelos Base (BaseModel)

Los modelos de Pydantic heredan de `BaseModel` y definen la estructura de los datos:

```python
from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    id: int
    nombre: str
    email: str
    edad: Optional[int] = None
    activo: bool = True
```

### 2. Validación Automática

Pydantic valida automáticamente los tipos de datos:

```python
# ✅ Correcto
usuario = Usuario(id=1, nombre="Ana", email="ana@ejemplo.com")

# ❌ Error - el ID debe ser un entero
# usuario = Usuario(id="uno", nombre="Ana", email="ana@ejemplo.com")
```

### 3. Valores por Defecto

Puedes definir valores por defecto para campos opcionales:

```python
class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    disponible: bool = True
    descripcion: Optional[str] = None
```

## Tipos de Datos Soportados

### Tipos Básicos
```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

class Ejemplo(BaseModel):
    texto: str
    numero: int
    decimal: float
    booleano: bool
    fecha: datetime
    lista: List[str]
    diccionario: Dict[str, int]
    opcional: Optional[str] = None
```

### Tipos Avanzados
```python
from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Union

class UsuarioAvanzado(BaseModel):
    email: EmailStr  # Valida formato de email
    sitio_web: HttpUrl  # Valida URL
    edad: Union[int, None] = None  # Puede ser int o None
```

## Validadores Personalizados

Pydantic permite crear validadores personalizados:

```python
from pydantic import BaseModel, validator

class Usuario(BaseModel):
    nombre: str
    edad: int
    
    @validator('edad')
    def validar_edad(cls, v):
        if v < 0:
            raise ValueError('La edad no puede ser negativa')
        if v > 120:
            raise ValueError('La edad no puede ser mayor a 120')
        return v
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if len(v) < 2:
            raise ValueError('El nombre debe tener al menos 2 caracteres')
        return v.title()  # Capitaliza el nombre
```

## Serialización

### Convertir a JSON
```python
usuario = Usuario(id=1, nombre="Carlos", email="carlos@ejemplo.com")
json_data = usuario.json()
print(json_data)
# {"id": 1, "nombre": "Carlos", "email": "carlos@ejemplo.com", "edad": null, "activo": true}
```

### Convertir desde JSON
```python
json_data = '{"id": 2, "nombre": "María", "email": "maria@ejemplo.com"}'
usuario = Usuario.parse_raw(json_data)
```

## Configuración de Modelos

Pydantic permite configurar el comportamiento de los modelos:

```python
from pydantic import BaseModel, Field

class Configuracion(BaseModel):
    class Config:
        # Permitir campos extra
        extra = "allow"
        # Validar asignaciones
        validate_assignment = True
        # Usar alias para campos
        fields = {
            'nombre': {'alias': 'user_name'},
            'email': {'alias': 'user_email'}
        }

class UsuarioConAlias(BaseModel):
    nombre: str = Field(alias="user_name")
    email: str = Field(alias="user_email")
    
    class Config:
        allow_population_by_field_name = True
```

## Casos de Uso Comunes

### 1. APIs con FastAPI
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    nombre: str
    precio: float
    disponible: bool

@app.post("/items/")
async def crear_item(item: Item):
    return {"mensaje": f"Item {item.nombre} creado", "precio": item.precio}
```

### 2. Configuración de Aplicación
```python
from pydantic import BaseSettings

class ConfiguracionApp(BaseSettings):
    nombre_app: str = "Mi Aplicación"
    puerto: int = 8000
    debug: bool = False
    base_datos_url: str
    
    class Config:
        env_file = ".env"

config = ConfiguracionApp()
```

### 3. Validación de Formularios
```python
from pydantic import BaseModel, validator

class FormularioRegistro(BaseModel):
    usuario: str
    email: str
    password: str
    confirmar_password: str
    
    @validator('password')
    def validar_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v
    
    @validator('confirmar_password')
    def validar_confirmacion(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Las contraseñas no coinciden')
        return v
```

## Ventajas de Pydantic

1. **Validación automática**: Reduce errores en tiempo de ejecución
2. **Documentación automática**: Ideal para APIs
3. **Type hints**: Mejora la experiencia de desarrollo
4. **Flexibilidad**: Fácil de extender y personalizar
5. **Performance**: Validación rápida y eficiente

## Mejores Prácticas

1. **Usa tipos específicos**: En lugar de `Any`, usa tipos específicos
2. **Valida datos de entrada**: Siempre valida datos que vienen del usuario
3. **Usa validadores personalizados**: Para lógica de negocio compleja
4. **Documenta tus modelos**: Usa docstrings para explicar el propósito
5. **Maneja errores**: Captura y maneja las excepciones de validación

## Ejercicios Prácticos

### Ejercicio 1: Crear un modelo de Libro
```python
# Crea un modelo para representar un libro con:
# - título (str, requerido)
# - autor (str, requerido)
# - año_publicacion (int, opcional)
# - isbn (str, opcional)
# - precio (float, debe ser positivo)
# - genero (lista de strings)
```

### Ejercicio 2: Validar una API de Usuarios
```python
# Crea endpoints para:
# - Crear usuario (validar email único, edad >= 18)
# - Actualizar usuario (validar que existe)
# - Obtener usuario por ID
```

## Recursos Adicionales

- [Documentación oficial de Pydantic](https://pydantic-docs.helpmanual.io/)
- [FastAPI con Pydantic](https://fastapi.tiangolo.com/tutorial/body/)
- [Ejemplos avanzados](https://github.com/pydantic/pydantic/tree/master/examples)

---

*Este documento es parte del curso de Programación de Software*
