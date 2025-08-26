class Persona:
    def __init__(self, nombre:str, documento:str):
        self.nombre =  nombre
        self.documento = documento

    def __str__(self) -> str:
        return f"{self.nombre}, se creo esta persona con el documneto {self.documento}"
    
class CuentaBancaria:
    def __init__(self, titutar: Persona, saldo: int = 0):
        self.titutar = titutar
        self._saldo = saldo
    
    def saldo(self) -> int:
        return self._saldo
    
    def depositar(self, monto: float) -> None:
        if monto > 0:
            self._saldo += monto
            print(f"Se depósito un monto de {monto} y mi saldo actual {self._saldo}")
        else:
            print("El monto debe ser positivo")

    def retirar(self, monto: float) -> None:
        if monto <= self._saldo:
            self._saldo -= monto
            print(f"Se retira del saldo {self._saldo} el monto de {monto}")
        else:
            print(f"no se puede retirar un monto mayor al saldo de la cuenta")

        def __str__(self) -> str:
            return f"{self.nombre}, se creo esta persona con el documneto {self.documento}"
        
class CuentaAhorro(CuentaBancaria):
    def __init__(self, titular, saldo = 0, interes: float = 0.02):
        super().__init__(titular, saldo)
        self.interes = interes

    def calcular_interes(self):
        ganancia = self._saldo * self.interes
        self._saldo += ganancia
        print(f"interes aplicado y su nuevo saldo es {self._saldo}")


class CuentaCorriente(CuentaBancaria):
    def __init__(self, titular, saldo = 0, limite_de_sobregiro: float = 500):
        super().__init__(titular, saldo)
        self.limite_de_sobregiro = limite_de_sobregiro

    def retirar(self, monto: float):
        if monto <= self._saldo + self.limite_de_sobregiro:
            self._saldo -= monto 
            print(f"Se retira del saldo {self._saldo} el monto de {monto}")
        else:
            print(f"no se puede retirar un monto mayor al saldo de la cuenta")


class Banco:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.cuentas = []

    def crear_cuentar(self, titular, tipo="ahorros") -> list:
        if tipo == "ahorro":
            cuenta = CuentaAhorro(titular)
        else:
            cuenta = CuentaCorriente(titular)
        self.cuentas.append(cuenta)
        print(f"cuenta brancaria {self.nombre}")
        return cuenta
    
    def mostrar_cuentas(self):
        if not self.cuentas:
            print("No tengo cuentas registradas")
        else:
            for i, cuenta in enumerate(self.cuentas, 1):
                print(f"{i}. {cuenta}")



banco = Banco(nombre="Banco ITM")
while True:
    print("\n--- MENU ---")
    print("1. crear una persona y una cuenta")
    print("2. Depositar")
    print("3. Retirar")
    print("4. APlicar interes a una cuenta de ahorros")
    print("5. Mostrar cuentas")
    print("6. Salir")
    # continuar con las demas opciones
    
    
    #Consultar como validar que este input sea un numero del 1 al 6
    opcion = input("Elige una opcion: ")
    
    if opcion == "1":
        nombre = input("Ingrese el nombre de la persona ")
        documento = input("ingrese el documento de la persona ")
        persona = Persona(nombre=nombre,documento=documento)

        print("\nQue tipo de cuenta quiere crear")
        #Validar tipo de dato entre str ahorro o corriente
        tipo = input("Escriba ahorros o corriente ").lower()
        banco.crear_cuentar(persona,tipo)

    elif opcion == "5":
        banco.mostrar_cuentas()

    elif opcion == "6":
        print("Gracias por usar nuestra aplicacion")
        break

    else:
        print("Opcion no valida")


# terminar todas las opciones que son 2, 3, 4, ajustar la 5 para que imprima el objeto y no la referencia de memoria
# Validar que todos los input sean del valor deseado, mostrando errores por consola sin try catch