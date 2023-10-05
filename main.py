from tabulate import tabulate
from time import sleep
import os
import keyboard
from proceso import Process
from tiempo import Contador
from getpass import getpass

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
            # registrar momento en que cada proceso llega a memoria (cola de listos)
            if len(procesos.dict_estadisticas["llegada_memoria"]) < cantidadProcesos:
                tiempo_actual = contador_general.obtener_tiempo_actual()
                procesos.dict_estadisticas["llegada_memoria"].append(tiempo_actual)

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
          
        # registrar el momento en que cada proceso termina 
        tiempo_finalizacion = contador_general.obtener_tiempo_actual()
        id_pos = procesos.dict_terminados["id"][-1] # obtener el id del proceso que finalizo
        procesos.dict_estadisticas["finalizacion"][id_pos] = tiempo_finalizacion

# asignar botones para eventos
keyboard.add_hotkey('p', on_p_pressed) 
keyboard.add_hotkey('c', on_c_pressed)
keyboard.add_hotkey('i', on_i_pressed)
keyboard.add_hotkey('e', on_e_pressed)

# --------- configuracion inicial --------------
os.system("cls") # para borrar la ruta del archivo al comenzar
contador_general = Contador()

while True:
    try:
        cantidadProcesos = int(input("Ingresa el numero de procesos: "))
        break
    except ValueError:
        print("Error, ingrese un numero entero")
procesos = Process(cantidadProcesos=cantidadProcesos)
 
# llenar la cola de LISTOS para ejecutar
while len(procesos.dict_listos["id"]) < 5 and len(procesos.dict_nuevos["id"]) > 0:
    # pasa un proceso de la cola de nuevos a la cola de listos 
    for key in procesos.dict_nuevos.keys():
        p = procesos.dict_nuevos[key].pop(0)
        procesos.dict_listos[key].append(p)
           
    # registrar el momento en que entra un proceso a la memoria del procesador (cola listos)
    procesos.dict_estadisticas["llegada_memoria"].append(contador_general.obtener_tiempo_actual()) # el tiempo sera cero porque entran de golpe varios procesos
# ----------------------------------------------

while True: # Bucle principal 
    if not pausado:
        os.system("cls")
        memoria_procesador = len(procesos.dict_listos["id"]) + len(procesos.dict_bloqueados["id"]) + len(procesos.dict_ejecucion["id"]) # listos + bloqueados + en ejecucion
        
        # si aun hay espacio en memoria de procesos y aun hay procesos Nuevos, entonces agrega uno a la cola de listos
        if memoria_procesador < 5 and len(procesos.dict_nuevos["id"]) > 0:
            for key in procesos.dict_nuevos.keys():
                p = procesos.dict_nuevos[key].pop(0)
                procesos.dict_listos[key].append(p)
            
            # registrar el momento en que entra un proceso a la memoria del procesador (cola listos)
            if len(procesos.dict_estadisticas["llegada_memoria"]) < cantidadProcesos:
                tiempo_actual = contador_general.obtener_tiempo_actual()
                procesos.dict_estadisticas["llegada_memoria"].append(tiempo_actual)
        
        # si aun no hay proceso en ejecucion y hay un procesos en la cola de listos, agraga uno a ejecucion
        if len(procesos.dict_ejecucion["id"]) == 0 and len(procesos.dict_listos["id"]) > 0:
            # agregar proceso a ejecucion
            for key in procesos.dict_listos.keys():
                p = procesos.dict_listos[key].pop(0)
                procesos.dict_ejecucion[key].append(p)
              
            # Registrar el momento en que entra un proceso a ejecucion por primera vez
            if len(procesos.dict_estadisticas["llegada_ejecucion"]) < cantidadProcesos:
                tiempo_actual = contador_general.obtener_tiempo_actual()
                procesos.dict_estadisticas["llegada_ejecucion"].append(tiempo_actual)
                          
        # obtener que se mostrara de cada tabla 
        listos = {key: value for key, value in procesos.dict_listos.items() if key == "id" or key == "tiempo_max" or key == "tiempo_restante"}
        enEjecucion = {key: value for key, value in procesos.dict_ejecucion.items() if key != "resultado"}
        bloqueados = {key: value for key, value in procesos.dict_bloqueados.items() if key == "id" or key == "trans_en_bloq"}
        terminados = {key: value for key, value in procesos.dict_terminados.items() if key == "id" or key == "num1" or key == "operador" or key == "num2" or key == "resultado"}
        
        # imprimir tablas 
        tabla_procesos_nuevos = [["# procesos nuevos"], [procesos.num_procesos_nuevos()]]
        print(tabulate(tabla_procesos_nuevos, headers="firstrow", tablefmt="simple_outline"), flush=True)
        
        tabla_listos = tabulate(listos, headers="keys", tablefmt="simple_outline")
        print("\nCola de Listos" + '\n' + tabla_listos, flush=True) 
        
        tabla_ejecucion_actual = tabulate(enEjecucion, headers="keys", tablefmt="simple_outline") 
        print("\nProceso en Ejecucion" + '\n' + tabla_ejecucion_actual, flush=True) 
        
        tabla_bloqueados = tabulate(bloqueados, headers="keys", tablefmt="simple_outline")
        print("\nCola de Bloqueados" + '\n' + tabla_bloqueados, flush=True)
        
        tabla_terminados = tabulate(terminados, headers="keys", tablefmt="simple_outline")
        print("\nCola de Terminados" + '\n' + tabla_terminados + '\n', flush=True)
        
        print(contador_general.actualizar_tiempo(), flush=True)
        
        if len(procesos.dict_ejecucion['id']) == 1:
            # actualizar los tiempos en ejecucion
            procesos.dict_ejecucion["tiempo_transcurrido"][0] += 1
            procesos.dict_ejecucion["tiempo_restante"][0] -= 1
            
            if procesos.dict_ejecucion["tiempo_restante"][0] == 0: # cuando tiempo restante llega a cero, enviar a termanidos 
                for key in procesos.dict_ejecucion.keys():
                    p = procesos.dict_ejecucion[key].pop()
                    procesos.dict_terminados[key].append(p)
                # registrar el momento en que cada proceso termina
                tiempo_finalizacion = contador_general.obtener_tiempo_actual()
                id_pos = procesos.dict_terminados["id"][-1] # obtener el id del proceso que finalizo
                procesos.dict_estadisticas["finalizacion"][id_pos] = tiempo_finalizacion
        
        # aumentar el tiempo trasncurrido en bloqueado para todos los procesos bloqueados
        if len(procesos.dict_bloqueados["id"]) > 0:
            procesos.dict_bloqueados["trans_en_bloq"] = [num + 1 for num in  procesos.dict_bloqueados["trans_en_bloq"]]
        
        # regresar a la cola de listos una vez pasados 8 segundos en bloqueados
        if len(procesos.dict_bloqueados["trans_en_bloq"]) > 0: # si existen procesos en la cola de bloquados
            if (procesos.dict_bloqueados["trans_en_bloq"][0] % 8) == 0: # si algun proceso ya cumplio 8 segundos ahi
                  for key in procesos.dict_bloqueados.keys(): # tranfierelo a la cola de listos
                        p = procesos.dict_bloqueados[key].pop(0)
                        procesos.dict_listos[key].append(p)
                    
        # si ya no hay procesos en la memoria, termina el bucle
        if memoria_procesador == 0:
            break
        sleep(1) 

getpass("\n\nPresiona <Enter> para ver las estadisticas...")
os.system("cls")
# obtener listas del diccionario Estadisticas para hacer calculos
lista_llegada = procesos.dict_estadisticas["llegada_memoria"]    
lista_finalizacion = procesos.dict_estadisticas["finalizacion"]
lista_llegada_ejecucion = procesos.dict_estadisticas["llegada_ejecucion"] # lista con proposito de debugeo
lista_retorno = [x - y for x, y in zip(lista_finalizacion, lista_llegada)]
lista_respuesta = [x - y for x, y in zip(lista_llegada_ejecucion, lista_llegada)] # tiempo que dura en listos hasta que llega a ejecucion por primera vez

# calcular el tiempo de retorno: finalizacion - llegada
procesos.dict_estadisticas["retorno"] = lista_retorno

# calcular tiempo respuesta: llegada_ejecucion - llegada
procesos.dict_estadisticas["respuesta"] = lista_respuesta

# calcular tiempo de servicio (tiempo que el proceso ha estado dentro del procesador)
for i in range(len(procesos.dict_terminados["id"])):
    pos = procesos.dict_terminados["id"][i] # obtener la posicion donde insertar
    if procesos.dict_terminados["resultado"][i] == "Error":
        procesos.dict_estadisticas["servicio"][pos] = procesos.dict_terminados["tiempo_transcurrido"][i]
        
    elif procesos.dict_terminados["trans_en_bloq"][i] > 0:
        procesos.dict_estadisticas["servicio"][pos] = procesos.dict_terminados["tiempo_transcurrido"][i] \
                                                    + procesos.dict_terminados["trans_en_bloq"][i]
    else:
        procesos.dict_estadisticas["servicio"][pos] = procesos.dict_terminados["tiempo_max"][i]

# calcular tiempo espera
procesos.dict_estadisticas["espera"] = [x - y for x, y in zip(lista_finalizacion, procesos.dict_estadisticas["servicio"])]

# imprimir procesos terminados 
tabla_terminados = tabulate(procesos.dict_terminados, headers="keys", tablefmt="simple_outline") # no se debe mostrar
print("\nTabla de Terminados (con proposito de debugeo)" + '\n' + tabla_terminados)

# imprimir estadisticas 
estadisticas = {key: value for key, value in procesos.dict_estadisticas.items() if key != "llegada_ejecucion"}

tabla_estadisticas = tabulate(estadisticas, headers="keys", tablefmt="simple_outline")
print("\nTabla Estadisticas" + '\n' + tabla_estadisticas)
        