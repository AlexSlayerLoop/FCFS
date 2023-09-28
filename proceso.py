from random import choice, randint

class Process:
    
    def __init__(self, n_veces = 1):
        # constructor
        self.id = 0
        self.procesos = {
            "id": [],
            "tiempo_max": [],
            "operador": [],
            "num1": [],
            "num2": [],
            "resultado": []
        }
        
        for _ in range(n_veces):
            self.agregar_proceso()
    
    def agregar_proceso(self):
        # generar datos de procesos aleatoriamente
        tiempo_maximo = randint(6, 18)
        operador = choice(('+', '-', '*', '/', '%'))
        num1 = randint(1, 100)
        num2 = randint(1, 100)
        resultado = round(self.hacer_operacion(operador, num1, num2), 2)
        
        # insertarlos de el diccionarios de procesos 
        self.procesos["id"].append(self.id)
        self.procesos["tiempo_max"].append(tiempo_maximo)
        self.procesos["operador"].append(operador)
        self.procesos["num1"].append(num1)
        self.procesos["num2"].append(num2)
        self.procesos["resultado"].append(resultado)
        
        # incrementar id 
        self.id += 1
    
    def hacer_operacion(self, operador: str, num1: int, num2: int):
        return (
            num1 + num2 if operador == '+' else
            num1 - num2 if operador == '-' else
            num1 * num2 if operador == '*' else
            num1 / num2 if operador == '/' else
            num1 % num2 if operador == '%' else None
        )
    
    def numero_de_procesos(self) -> int:
        # retorna el numero de procesos
        return len(self.procesos["id"])
    
    