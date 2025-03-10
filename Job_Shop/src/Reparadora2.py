import random 
from Calculadora_makespan_VAde import *

class Reparadora:

    '''
    El proceso de reparación sirve simultáneamente para raparar una solución no
    factible y para verificar factibilidad.
    '''

    # Método para actualizar las listas en el proceso de reparación una vez obtenida una 
    # operación en la lista de `planificables`.
    @staticmethod
    def actualizacion_de_listas(op_id, info, etiquetadas, sigue_en_job, sigue_en_maquina):
        
        etiquetadas.append(op_id) # Agregamos la operación planificable a la lista de
                                  # operaciones etiquetadas.
                
        info[op_id]['completada'] = True # Marcamos a la operación como completada

        # Si ya la completamos, independientemente de si tiene sucesores en máquina o job,
        # la tenemos que quitar de las operaciones por planificar.
        sigue_en_job.remove(op_id) 
        sigue_en_maquina.remove(op_id)

        if info[op_id]['suc_job'] is None:
            pass    # Si la operación no tiene un sucesor en job no hacemos
                    # nada y nos vamos a preguntarle a la operación si tiene un sucesor
                    # en máquina.
        else:
            # Si la operación sí tiene un sucesor en job:
            op_id_suc_job = info[op_id]['suc_job'] 
            #sigue_en_job.remove(op_id) 
            sigue_en_job.append(op_id_suc_job)
            # Actualizamos la lista de las que siguen por planificarse en job de acuerdo al orden dado
            # por los jobs (quitamos la ya etiquetada y ponemos a su sucesora).

        if info[op_id]['suc_maquina'] is None:
            pass    # Si la operación no tiene un sucesor en máquina, nos saltamos el siguiente
                    # bloque del `else`

        else:
            # Si la operación sí tiene un sucesor en máquina:
            op_id_suc_maquina = info[op_id]['suc_maquina'] 
            #sigue_en_maquina.remove(op_id) 
            sigue_en_maquina.append(op_id_suc_maquina)
            # Actualizamos la lista de las que siguen por planificarse en máquina de acuerdo al orden dado
            # por las máquinas (quitamos la ya etiquetada y ponemos a su sucesora).

        return # Se puede quitar, no está haciendo nada (lo dejo por costumbre).

    @staticmethod
    def reparacion(solucion, lista_de_vertices):

        numero_de_maquinas = len(solucion)
        numero_de_trabajos = len(solucion[0])
        info = Evaluador_Makespan.construct_info(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion)

        print(info)
        
        sigue_en_job = [] # Es la O_J del artículo.
        sigue_en_maquina = [] # Es la O_M del artículo.
        # `sigue_en_<algo>` es una lista donde se van guardando iteración a iteración
        # cuáles son las siguientes operaciones acorde al orden dado por los jobs o
        # las máquinas.

        planificables = [] # Lista de operaciones en la intersección de O_J y O_M

        etiquetadas = [] # Lista de operaciones que ya han pasado por el proceso de
                         # reparación i.e. ya han sido planificadas.

        
        # Agregamos las primeras operaciones en los jobs a `sigue_en_job` (dados por
        # el problema) y las primeras operaciones en las máquinas a `sigue_en_maquina`
        # (dadas por la solución a reparar).
        for op_id, datos in info.items():
            if datos['pred_job'] is None: # Si la op no tiene predecesor en Job, es la
                                          # primera en el Job.
                sigue_en_job.append(op_id)

            if datos['pred_maquina'] is None: # Análogo a lo de arriba, pero para máquina.
                sigue_en_maquina.append(op_id)
            
            # NOTA: Van dos `if`s en vez de un `if` y un `elif` porque puede ocurrir que
            # una op sea la primera en Job y Maq simultáneamente y necesito que esté en 
            # las dos listas en ese caso (con `elif` sólo se guardaría en la primera).


        # Sabemos que una solución ha sido reparada si y sólo si se cumple que `planificables`
        # es una lista vacía y ya no hay operaciones que sigan en los jobs o máquinas que nos
        # falte por planificar.
        # Así que vamos a repetir el algoritmo de reparación mientras se cumpla la negación de
        # lo anterior.
        while (planificables or (sigue_en_job or sigue_en_maquina)): 

            # Lista de las operaciones planificables; sus elementos están en O_J y O_M
            planificables = list(set(sigue_en_job) & set(sigue_en_maquina))

            # Imprimir el estado de `info` en cada iteración
            print("Estado de info en esta iteración:")
            for op_id, datos in info.items():
                print(f"Operación {op_id}: {datos}")

            # Caso donde `planificables` no es una lista vacía.
            for operacion_idx, op_id in enumerate(planificables):
                Reparadora.actualizacion_de_listas(op_id, info, etiquetadas, sigue_en_job, sigue_en_maquina)
                                

            while planificables == False: # Si `planificables` es vacío (pero aún hay operaciones en
                                          # máquinas y/o jobs que falten por planificar).

                operacion_elegida_id = random.choice(sigue_en_job) # Elegimos alguna operación al azar
                                                                   # de aquellas que nos falte planificar
                                                                   # en la lista de los jobs.
                
                # Vamos a la máquina que corresponde a la operación que elegimos:
                maquina_op_elegida_idx = info[operacion_elegida_id]['maquina'] - 1 
                # `solucion[m-1]` es la lista que corresponde a la máquina m

                maquina_elegida = solucion[maquina_op_elegida_idx] # Lista de operaciones en la máquina
                                                                   # elegida. Ej.: [1, 4, 8]
                
                # Índice de la operación elegida.
                op_elegida_idx = maquina_elegida.index(operacion_elegida_id)

                # Vamos a reordenar a la solución mandando a la `operacion_elegida_id` en la primera
                # posición disponible después de la última operación ya planificada.
                for operacion_idx, op_id in enumerate(maquina_elegida):
                    if info[op_id]['completada']: 
                        continue    # Si la operación en la que vamos ya está en `etiquetadas`, i.e. su 
                                    # flag está como `completada` == True, nos vamos con la que sigue.

                    maquina_elegida[operacion_idx], maquina_elegida[op_elegida_idx] = \
                    maquina_elegida[op_elegida_idx], maquina_elegida[operacion_idx]

                    # Cambiamos en `info` lo referente a sucesores y predecesores en máquina de las 
                    # operaciones intercambiadas.
                    info[operacion_elegida_id]['pred_maquina'], info[operacion_elegida_id]['suc_maquina'], \
                    info[op_id]['pred_maquina'], info[op_id]['suc_maquina'] = \
                    info[op_id]['pred_maquina'], info[op_id]['suc_maquina'], \
                    info[operacion_elegida_id]['pred_maquina'], info[operacion_elegida_id]['suc_maquina']

                    # Agregamos a la lista de operaciones planificables por máquina a la operación elegida.
                    sigue_en_maquina.append(op_elegida_id)

                    planificables = list(set(sigue_en_job) & set(sigue_en_maquina))

                    # Hasta aquí (si todo salió bien) se supone que la intersección de O_J y O_M ya no es 
                    # vacía (y tiene como único elemento a `op_elegida_id`)
                    # Pero esto se va a cotejar hasta la siguiente iteración porque aquí termina este bloque.

                    break # Salimos del `for`
                         


            # Algunos prints para ver cómo va la cosa:
            print('planificables', planificables)
            print('etiquetadas', etiquetadas)
            print('sigue_en_job', sigue_en_job)
            print('sigue_en_maquina', sigue_en_maquina)
        
        return etiquetadas