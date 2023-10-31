from tabulate import tabulate 

class Contador:
    def __init__(self):
        self.contador_general = 0
        
    def actualizar_tiempo(self, seg: int = 1): 
        # Actualizar la tabla que lleva el tiempo
        minutos = self.contador_general // 60
        segundos = self.contador_general % 60
        tiempo_formateado = f"{minutos:02}:{segundos:02}"
        tabla_reloj = [
            ["     Reloj     "], 
            [tiempo_formateado]
        ]
        self.contador_general += seg
        return tabulate(tabla_reloj, headers="firstrow", stralign="center")
    
    def obtener_tiempo_actual(self):
        return self.contador_general
    