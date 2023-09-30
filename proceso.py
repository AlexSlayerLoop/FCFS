from random import choice, randint

class Process:
    def __init__(self, cantidadProcesos = 1):
        # constructor
        self.id = 0
        self.estadistica_tiempos = {"id": [], "llegada": [], "finalizacion": [], "retorno": [], "respuesta": [], "espera": [], "servicio": []}
        
        self.dict_nuevos     = {"id": [], "tiempo_max": [], "operador": [], "num1": [], "num2": [], "resultado": [], "tiempo_transcurrido": [], "tiempo_restante": [], "trans_en_bloq": []}
        self.dict_listos     = {"id": [], "tiempo_max": [], "operador": [], "num1": [], "num2": [], "resultado": [], "tiempo_transcurrido": [], "tiempo_restante": [], "trans_en_bloq": []}
        self.dict_ejecucion  = {"id": [], "tiempo_max": [], "operador": [], "num1": [], "num2": [], "resultado": [], "tiempo_transcurrido": [], "tiempo_restante": [], "trans_en_bloq": []}
        self.dict_bloqueados = {"id": [], "tiempo_max": [], "operador": [], "num1": [], "num2": [], "resultado": [], "tiempo_transcurrido": [], "tiempo_restante": [], "trans_en_bloq": []}
        self.dict_terminados = {"id": [], "tiempo_max": [], "num1": [], "operador": [], "num2": [], "resultado": [], "tiempo_transcurrido": [], "tiempo_restante": [], "trans_en_bloq": []}
        
        for _ in range(cantidadProcesos):
            self.agregar_nuevo_proceso()
    
    def agregar_nuevo_proceso(self):
        # generar datos de procesos aleatoriamente
        tiempo_maximo = randint(6, 18)
        operador = choice(('+', '-', '*', '/', '%'))
        num1 = randint(1, 100)
        num2 = randint(1, 100)
        resultado = round(self.hacer_operacion(operador, num1, num2), 2)
        
        # insertarlos de el diccionarios de procesos 
        self.dict_nuevos["id"].append(self.id)
        self.dict_nuevos["tiempo_max"].append(tiempo_maximo)
        self.dict_nuevos["operador"].append(operador)
        self.dict_nuevos["num1"].append(num1)
        self.dict_nuevos["num2"].append(num2)
        self.dict_nuevos["resultado"].append(resultado)
        self.dict_nuevos["tiempo_restante"].append(tiempo_maximo)
        self.dict_nuevos["tiempo_transcurrido"].append(0)
        self.dict_nuevos["trans_en_bloq"].append(0)
        
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
    
    def num_procesos_nuevos(self) -> int:
        # retorna el numero de procesos
        return len(self.dict_nuevos["id"])
    
    