"""
Ejemplo de cliente para probar la API
Este archivo muestra cómo consumir la API desde Python
"""

import json
from datetime import datetime

import requests

BASE_URL = "http://localhost:8000"


def probar_api():
    """Función para probar todos los endpoints de la API"""

    print("Iniciando pruebas de la API...")
    print("=" * 50)

    print("\n1. Probando endpoint raíz...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Respuesta: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: No se puede conectar al servidor. ¿Está ejecutándose?")
        return

    print("\n2. Creando usuarios...")
    usuarios_prueba = [
        {"nombre": "Juan Pérez", "email": "juan@email.com", "edad": 25},
        {"nombre": "María García", "email": "maria@email.com", "edad": 30},
        {"nombre": "Carlos López", "email": "carlos@email.com", "edad": 28},
    ]

    usuarios_creados = []
    for usuario_data in usuarios_prueba:
        try:
            response = requests.post(f"{BASE_URL}/usuarios", json=usuario_data)
            if response.status_code == 201:
                usuario = response.json()
                usuarios_creados.append(usuario)
                print(f"Usuario creado: {usuario['nombre']} (ID: {usuario['id']})")
            else:
                print(f"Error creando usuario: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

    print("\n3. Obteniendo todos los usuarios...")
    try:
        response = requests.get(f"{BASE_URL}/usuarios")
        usuarios = response.json()
        print(f"Total de usuarios: {len(usuarios)}")
        for usuario in usuarios:
            print(f"   - {usuario['nombre']} ({usuario['email']})")
    except Exception as e:
        print(f"Error: {e}")

    if usuarios_creados:
        print("\n4. Obteniendo usuario específico...")
        usuario_id = usuarios_creados[0]["id"]
        try:
            response = requests.get(f"{BASE_URL}/usuarios/{usuario_id}")
            usuario = response.json()
            print(f"Usuario encontrado: {usuario['nombre']}")
        except Exception as e:
            print(f"Error: {e}")

    if usuarios_creados:
        print("\n5. Actualizando usuario...")
        usuario_id = usuarios_creados[0]["id"]
        datos_actualizacion = {"edad": 26, "nombre": "Juan Carlos Pérez"}
        try:
            response = requests.put(
                f"{BASE_URL}/usuarios/{usuario_id}", json=datos_actualizacion
            )
            if response.status_code == 200:
                usuario_actualizado = response.json()
                print(
                    f"Usuario actualizado: {usuario_actualizado['nombre']} (edad: {usuario_actualizado['edad']})"
                )
            else:
                print(f"Error actualizando usuario: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

    print("\n6. Creando productos...")
    productos_prueba = [
        {
            "nombre": "Laptop",
            "descripcion": "Laptop para desarrollo",
            "precio": 1500.00,
            "stock": 10,
        },
        {
            "nombre": "Mouse",
            "descripcion": "Mouse inalámbrico",
            "precio": 25.50,
            "stock": 50,
        },
        {
            "nombre": "Teclado",
            "descripcion": "Teclado mecánico",
            "precio": 80.00,
            "stock": 30,
        },
    ]

    productos_creados = []
    for producto_data in productos_prueba:
        try:
            response = requests.post(f"{BASE_URL}/productos", json=producto_data)
            if response.status_code == 201:
                producto = response.json()
                productos_creados.append(producto)
                print(f"Producto creado: {producto['nombre']} (ID: {producto['id']})")
            else:
                print(f"Error creando producto: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

    print("\n7. Obteniendo estadísticas...")
    try:
        response = requests.get(f"{BASE_URL}/estadisticas")
        stats = response.json()
        print(f"Estadísticas: {stats}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n8. Probando error 404...")
    try:
        response = requests.get(f"{BASE_URL}/usuarios/999")
        print(f"Status esperado 404, obtenido: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

    print("\n" + "=" * 50)
    print("Pruebas completadas!")


def probar_endpoints_individuales():
    """Función para probar endpoints específicos de forma interactiva"""

    print("\nPruebas interactivas de endpoints")
    print("=" * 40)

    while True:
        print("\nOpciones:")
        print("1. Crear usuario")
        print("2. Obtener usuarios")
        print("3. Crear producto")
        print("4. Obtener productos")
        print("5. Obtener estadísticas")
        print("0. Salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "0":
            break
        elif opcion == "1":
            nombre = input("Nombre: ")
            email = input("Email: ")
            edad = input("Edad (opcional): ")

            usuario_data = {"nombre": nombre, "email": email}
            if edad:
                usuario_data["edad"] = int(edad)

            try:
                response = requests.post(f"{BASE_URL}/usuarios", json=usuario_data)
                if response.status_code == 201:
                    print(f"Usuario creado: {response.json()}")
                else:
                    print(f"Error: {response.text}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "2":
            try:
                response = requests.get(f"{BASE_URL}/usuarios")
                usuarios = response.json()
                print(f"Usuarios encontrados: {len(usuarios)}")
                for usuario in usuarios:
                    print(f"   - {usuario['nombre']} ({usuario['email']})")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "3":
            nombre = input("Nombre del producto: ")
            descripcion = input("Descripción: ")
            precio = float(input("Precio: "))
            stock = int(input("Stock: "))

            producto_data = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
            }

            try:
                response = requests.post(f"{BASE_URL}/productos", json=producto_data)
                if response.status_code == 201:
                    print(f"Producto creado: {response.json()}")
                else:
                    print(f"Error: {response.text}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "4":
            try:
                response = requests.get(f"{BASE_URL}/productos")
                productos = response.json()
                print(f"Productos encontrados: {len(productos)}")
                for producto in productos:
                    print(f"   - {producto['nombre']} (${producto['precio']})")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "5":
            try:
                response = requests.get(f"{BASE_URL}/estadisticas")
                stats = response.json()
                print(f"Estadísticas: {stats}")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    print("Cliente de prueba para la API FastAPI")
    print("Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")

    try:
        import requests
    except ImportError:
        print("Error: El módulo 'requests' no está instalado.")
        print("Instálalo con: pip install requests")
        exit(1)

    probar_api()

    continuar = input("\n¿Quieres hacer pruebas interactivas? (s/n): ").lower()
    if continuar == "s":
        probar_endpoints_individuales()

    print("\n¡Hasta luego!")
