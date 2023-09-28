from tabulate import tabulate
from time import sleep
import os
import keyboard
from proceso import Process

contador_general = 0

# id | tiempo maximo (6-18) | operador | numero1 | numero2 | resultado
procesos = Process(11).procesos

# mostrar un proceso en especifico
for k, v in procesos.items():
      print(k,  v[5])

# imprimir tabla de todos los procesos
table1 = tabulate(procesos, headers="keys", tablefmt="simple_outline")
print(table1)



while True:
      minutos = contador_general // 60
      segundos = contador_general % 60
      tiempo_formateado = f"{minutos:02}:{segundos:02}"
      tabla_reloj = [["      Reloj      "], [tiempo_formateado]]
      print(tabulate(tabla_reloj, headers="firstrow", tablefmt="simple_outline", stralign="center"))
      sleep(1)
      contador_general += 1
      # os.system("cls")
    