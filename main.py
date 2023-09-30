from tabulate import tabulate
from time import sleep
import os
import keyboard
from proceso import Process
from tiempo import Contador

pausado = False

# funciones para eventos
def on_p_pressed():
    global pausado
    pausado = True

def on_c_pressed():
    global pausado
    pausado = False
    
def on_i_pressed():
      # sacar que proceso en ejecucion actual
      for key in procesos.dict_ejecucion.keys():
            try:
                  p = procesos.dict_ejecucion[key].pop(0)
            except IndexError:
                  pass
            else:
                  procesos.dict_bloqueados[key].append(p)

def on_e_pressed():
      try: 
            # marcar Error en el proceso en ejecucion
            procesos.dict_ejecucion["resultado"][0] = "Error" 
      except IndexError:
            pass
      else:
            # mandar a la cola de terminados
            for key in procesos.dict_ejecucion.keys():
                  p = procesos.dict_ejecucion[key].pop(0)
                  procesos.dict_terminados[key].append(p)

# asignar botones para eventos
keyboard.add_hotkey('p', on_p_pressed) 
keyboard.add_hotkey('c', on_c_pressed)
keyboard.add_hotkey('i', on_i_pressed)
keyboard.add_hotkey('e', on_e_pressed)


# --------- configuracion inicial --------------

os.system("cls") # para borrar la ruta del archivo al comenzar
contador_general = Contador()
n = int(input("Ingrsa el numero de procesos: "))
procesos = Process(cantidadProcesos=n)

# llenar la cola de LISTOS para ejecutar
while len(procesos.dict_listos["id"]) < 5 and len(procesos.dict_nuevos["id"]) > 0:
      for key in procesos.dict_nuevos.keys():
            p = procesos.dict_nuevos[key].pop(0)
            procesos.dict_listos[key].append(p)

# ----------------------------------------------
while True:
      if not pausado:
            os.system("cls")
            memoria_procesador = len(procesos.dict_listos["id"]) + len(procesos.dict_bloqueados["id"]) + len(procesos.dict_ejecucion["id"])

            # si aun hay espacio en memoria de procesos y aun hay procesos Nuevos, entonces agrega uno a la cola de listos
            if memoria_procesador < 5 and len(procesos.dict_nuevos["id"]) > 0:
                  for key in procesos.dict_nuevos.keys():
                        p = procesos.dict_nuevos[key].pop(0)
                        procesos.dict_listos[key].append(p)

            # si aun no hay proceso en ejecucion y hay un procesos en la cola de listos, agraga uno a ejecucion
            if len(procesos.dict_ejecucion["id"]) == 0 and len(procesos.dict_listos["id"]) > 0:
                  # agregar proceso a ejecucion
                  for key in procesos.dict_listos.keys():
                        p = procesos.dict_listos[key].pop(0)
                        procesos.dict_ejecucion[key].append(p)
                  
            # obtener que se mostrara de cada tabla (no todas las tablas lo requieren)
            listos = {key: value for key, value in procesos.dict_listos.items() if key == "id" or key == "tiempo_max" or key == "tiempo_restante"}
            enEjecucion = {key: value for key, value in procesos.dict_ejecucion.items() if key != "resultado"}
            bloqueados = {key: value for key, value in procesos.dict_bloqueados.items() if key == "id" or key == "trans_en_bloq"}
            terminados = {key: value for key, value in procesos.dict_terminados.items() if key == "id" or key == "num1" or key == "operador" or key == "num2" or key == "resultado"}

            # imprimir tablas 
            tabla_nuevos = tabulate(procesos.dict_nuevos, headers="keys", tablefmt="simple_outline") # no se debe mostrar
            print("\nCola de Nuevos (con proposito de debugeo)" + '\n' + tabla_nuevos)

            tabla_procesos_nuevos = [["# procesos nuevos"], [procesos.num_procesos_nuevos()]]
            print(tabulate(tabla_procesos_nuevos, headers="firstrow", tablefmt="simple_outline"), flush=True)

            tabla_listos = tabulate(listos, headers="keys", tablefmt="simple_outline")
            print("\nCola de Listos" + '\n' + tabla_listos) 

            tabla_ejecucion_actual = tabulate(enEjecucion, headers="keys", tablefmt="simple_outline") 
            print("\nProceso en Ejecucion" + '\n' + tabla_ejecucion_actual) 

            tabla_bloqueados = tabulate(bloqueados, headers="keys", tablefmt="simple_outline")
            print("\nCola de Bloqueados" + '\n' + tabla_bloqueados)

            tabla_terminados = tabulate(terminados, headers="keys", tablefmt="simple_outline")
            print("\nCola de Terminados" + '\n' + tabla_terminados + '\n')

            print(contador_general.actualizar_tiempo())

            if len(procesos.dict_ejecucion['id']) == 1:
                  # actualizar los tiempos en ejecucion
                  procesos.dict_ejecucion["tiempo_transcurrido"][0] += 1
                  procesos.dict_ejecucion["tiempo_restante"][0] -= 1

                  if procesos.dict_ejecucion["tiempo_restante"][0] == 0:
                        for key in procesos.dict_ejecucion.keys():
                              p = procesos.dict_ejecucion[key].pop()
                              procesos.dict_terminados[key].append(p)

            # aumentar el tiempo trasncurrido en bloqueado para los procesos bloqueados
            if len(procesos.dict_bloqueados["id"]) > 0:
                  procesos.dict_bloqueados["trans_en_bloq"] = [num + 1 for num in  procesos.dict_bloqueados["trans_en_bloq"]]
            
            # regresar a la cola de listos una vez pasados 8 segundos en bloqueados
            if len(procesos.dict_bloqueados["trans_en_bloq"]) > 0: # si existen procesos en la cola de bloquados
                  if procesos.dict_bloqueados["trans_en_bloq"][0] == 8: # si algun proceso ya cumplio 8 segundos
                        for key in procesos.dict_bloqueados.keys(): # tranfierelo a la cola de listos
                              p = procesos.dict_bloqueados[key].pop(0)
                              procesos.dict_listos[key].append(p)

            # si ya no hay procesos en la memoria, termina el bucle
            if memoria_procesador == 0:
                  break

            sleep(1) 

print("memoria del procesador:", memoria_procesador)


      

# TODO calcular los siguientes tiempos  

# a. Tiempo de Llegada: Hora en la que el proceso entra al sistema. 

# b. Tiempo de Finalización: Hora en la que el proceso termino. 

# c. Tiempo de Retorno: Tiempo total desde que el proceso llega hasta que termina. 

# d. Tiempo de Respuesta: Tiempo transcurrido desde que llega hasta que es atendido por primera vez. 

# e. Tiempo de Espera: Tiempo que el proceso ha estado esperando para usar el procesador. 

# f. Tiempo de Servicio: Tiempo que el proceso ha estado dentro del procesador. 
# (Si el proceso termino su ejecución normal es el TME, de no ser así es el tiempo transcurrido)


