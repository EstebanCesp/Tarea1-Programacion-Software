#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo 1: Ejercicios Prácticos de POO en Python
Docente: Alejandro Salgar Marín
ITM 2025-2
"""

from xxlimited import Str


print("EJERCICIOS PRÁCTICOS - MÓDULO 1: POO EN PYTHON")
print("=" * 60)

# ============================================================================
# EJERCICIO 1: CLASE ESTUDIANTE
# ============================================================================
print("\nEJERCICIO 1: CLASE ESTUDIANTE")
print("-" * 40)

class Estudiante:
    def __init__(self, nombre:Str, edad:int, carrera:Str):
        self.nombre = nombre
        self.edad = edad
        self.carrera = carrera
        self.promedio = 0.0
        self.materias_inscritas = []
    
    def presentarse(self) -> Str:
        return f"Hola, soy {self.nombre}, tengo {self.edad} años y estudio {self.carrera}."
    
    def inscribir_materia(self, materia:Str)->Str:
        if materia not in self.materias_inscritas:
            self.materias_inscritas.append(materia)
            return f"{self.nombre} se ha inscrito en {materia}"
        else:
            return f"{self.nombre} ya está inscrito en {materia}"
    
    def agregar_nota(self, materia:Str, nota:float)->Str:
        if materia in self.materias_inscritas and 0.0 <= nota <= 5.0:
            if self.promedio == 0.0:
                self.promedio = nota
            else:
                total_materias = len(self.materias_inscritas)
                suma_actual = self.promedio * (total_materias - 1)
                self.promedio = (suma_actual + nota) / total_materias
            return f"Nota {nota} agregada a {materia}. Nuevo promedio: {self.promedio:.2f}"
        else:
            return "Error: materia no inscrita o nota inválida"

# Probar clase Estudiante
estudiante1 = Estudiante("María González", 20, "Ingeniería de Sistemas")
print(estudiante1.presentarse())

print(estudiante1.inscribir_materia("Programación I"))
print(estudiante1.inscribir_materia("Matemáticas"))
print(estudiante1.agregar_nota("Programación I", 4.5))
print(estudiante1.agregar_nota("Matemáticas", 4.2))

# ============================================================================
# EJERCICIO 2: CLASE RECTÁNGULO
# ============================================================================
print("\nEJERCICIO 2: CLASE RECTÁNGULO")
print("-" * 40)

class Rectangulo:
    def __init__(self, base, altura):
        if base > 0 and altura > 0:
            self.base = base
            self.altura = altura
        else:
            raise ValueError("La base y altura deben ser valores positivos")
    
    def calcular_area(self):
        return self.base * self.altura
    
    def calcular_perimetro(self):
        return 2 * (self.base + self.altura)
    
    def es_cuadrado(self):
        return self.base == self.altura
    
    def mostrar_info(self):
        return f"""
INFORMACIÓN DEL RECTÁNGULO
   Base: {self.base} unidades
   Altura: {self.altura} unidades
   Área: {self.calcular_area():.2f} unidades²
   Perímetro: {self.calcular_perimetro():.2f} unidades
   ¿Es cuadrado?: {'Sí' if self.es_cuadrado() else 'No'}
        """

# Probar clase Rectangulo
try:
    rect1 = Rectangulo(5, 3)
    rect2 = Rectangulo(4, 4)
    
    print("Rectángulo 1:")
    print(rect1.mostrar_info())
    
    print("\nRectángulo 2:")
    print(rect2.mostrar_info())
    
except ValueError as e:
    print(f"❌ Error: {e}")

# ============================================================================
# EJERCICIO 3: CLASE CUENTA BANCARIA MEJORADA
# ============================================================================
print("\nEJERCICIO 3: CLASE CUENTA BANCARIA MEJORADA")
print("-" * 40)

class CuentaBancaria:
    def __init__(self, titular, saldo_inicial, tipo_cuenta="ahorros"):
        self.titular = titular
        self.__saldo = saldo_inicial
        self.tipo_cuenta = tipo_cuenta
        self.activa = True
    
    def depositar(self, cantidad):
        if not self.activa:
            return "La cuenta está inactiva"
        
        if cantidad > 0:
            self.__saldo += cantidad
            return f"Depósito exitoso de ${cantidad:,.2f}. Nuevo saldo: ${self.__saldo:,.2f}"
        else:
            return "La cantidad debe ser mayor a 0"
    
    def retirar(self, cantidad):
        if not self.activa:
            return "La cuenta está inactiva"
        
        if cantidad > 0 and cantidad <= self.__saldo:
            self.__saldo -= cantidad
            return f"Retiro exitoso de ${cantidad:,.2f}. Saldo restante: ${self.__saldo:,.2f}"
        else:
            return "Fondos insuficientes o cantidad inválida"
    
    def consultar_saldo(self):
        if self.activa:
            return f"Saldo actual: ${self.__saldo:,.2f}"
        else:
            return "La cuenta está inactiva"
    
    def obtener_resumen(self):
        return f"""
RESUMEN DE CUENTA BANCARIA
   Titular: {self.titular}
   Tipo de cuenta: {self.tipo_cuenta.title()}
   Estado: {'Activa' if self.activa else 'Inactiva'}
   Saldo actual: ${self.__saldo:,.2f}
        """

# Probar clase CuentaBancaria
cuenta1 = CuentaBancaria("Alejandro Salgar", 5000, "corriente")
cuenta2 = CuentaBancaria("María López", 2000, "ahorros")

print(cuenta1.obtener_resumen())
print(cuenta2.obtener_resumen())

print(f"\n{cuenta1.depositar(1500)}")
print(f"{cuenta1.retirar(800)}")
print(f"{cuenta1.consultar_saldo()}")

print(f"\n{cuenta2.depositar(300)}")
print(f"{cuenta2.consultar_saldo()}")

print(f"\n¡Todos los ejercicios completados exitosamente!")
print("=" * 60)
