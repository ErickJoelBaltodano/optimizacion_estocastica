import random 
from Calculadora_makespan_VAde import *

class Reparadora:

    '''
    El proceso de reparación sirve simultáneamente para raparar una solución no
    factible y para verificar factibilidad.
    '''


    @staticmethod
    def reparacion(solucion, numero_de_maquinas, numero_de_trabajos, lista_de_vertices):

        info = Evaluador_Makespan.construct_info(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion)

        print(info)

        completadas = [] # ESTO ES SÓLO PARA EL DEBUGGING
        
        sigue_en_job = [] # Es la O_J del artículo.
        sigue_en_maquina = [] # Es la O_M del artículo.
        # `sigue_en_<algo>` es una lista donde se van guardando iteración a iteración
        # cuáles son las siguientes operaciones acorde al orden dado por los jobs o
        # las máquinas.

        planificables = [] # Lista de operaciones en la intersección de O_J y O_M

        
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
        # Esta triple validación se hace en 3 pasos.
        while len(sigue_en_job) > 0 or len(sigue_en_maquina) > 0:  # Condición modificada 

            # Lista de las operaciones planificables; sus elementos están en O_J y O_M
            planificables = list(set(sigue_en_job) & set(sigue_en_maquina))

            # Algunos prints para ver cómo va la cosa:
            print('\ncompletadas', completadas)
            print('\nsigue_en_job', sigue_en_job)
            print('\nsigue_en_maquina', sigue_en_maquina) 
            print('\nplanificables', planificables)
            print(f"\nLa solución (en reparación) es: {solucion}")  

            # Caso donde `planificables` no es una lista vacía.
            for operacion_idx, op_id in enumerate(planificables):

                # Se tiene que quitar a la operación de O_J y O_M:
                sigue_en_job.remove(op_id) # Se quita de O_J
                sigue_en_maquina.remove(op_id) # Se quita de O_M

                # Marcamos a la operación como completada
                info[op_id]['completada'] = True 
                completadas.append(op_id)

                # Luego, se le pregunta a la op_id si tiene sucesores en job y máquina.

                if info[op_id]['suc_job'] is None:
                    pass    # Si la operación no tiene un sucesor en job no hacemos
                            # nada y nos vamos a preguntarle a la operación si tiene un sucesor
                            # en máquina.
                else:
                    # Si la operación sí tiene un sucesor en job:
                    op_id_suc_job = info[op_id]['suc_job'] 
                    sigue_en_job.append(op_id_suc_job)
                    # Actualizamos la lista de las que siguen por planificarse en job de acuerdo al orden dado
                    # por los jobs (quitamos la ya etiquetada y ponemos a su sucesora).

                if info[op_id]['suc_maquina'] is None:
                    pass    # Si la operación no tiene un sucesor en máquina, nos saltamos el siguiente
                            # bloque del `else`

                else:
                    # Si la operación sí tiene un sucesor en máquina:
                    op_id_suc_maquina = info[op_id]['suc_maquina'] 
                    sigue_en_maquina.append(op_id_suc_maquina)
                    # Actualizamos la lista de las que siguen por planificarse en máquina de acuerdo al orden dado
                    # por las máquinas (quitamos la ya etiquetada y ponemos a su sucesora).                
                                
            # Caso feo:
            if not planificables:

                if not sigue_en_job:  # Validación añadida
                    break

                print("\nEstamos en el caso feo...\n")                

                operacion_elegida_id = random.choice(sigue_en_job)
                
                # Obtener la máquina (índice 0-based)
                maquina_op_elegida_idx = info[operacion_elegida_id]['maquina']
                maquina_elegida = solucion[maquina_op_elegida_idx]
                
                print(f"Máquina de la operación elegida {operacion_elegida_id}: {maquina_op_elegida_idx}")
                print(f"La máquina elegida es: {maquina_elegida}")

                # Encontrar la primera operación no completada para intercambiar
                op_cambio_idx = None
                for idx, op_id in enumerate(maquina_elegida):
                    if not info[op_id]['completada']:
                        op_cambio_idx = idx
                        break
                
                if op_cambio_idx is not None:
                    # Intercambiar posiciones
                    op_elegida_idx = maquina_elegida.index(operacion_elegida_id)
                    maquina_elegida[op_elegida_idx], maquina_elegida[op_cambio_idx] = \
                        maquina_elegida[op_cambio_idx], maquina_elegida[op_elegida_idx]

                    # Reconstruir relaciones de TODA la máquina
                    for i in range(len(maquina_elegida)):
                        current_op = maquina_elegida[i]
                        info[current_op]['pred_maquina'] = maquina_elegida[i-1] if i > 0 else None
                        info[current_op]['suc_maquina'] = maquina_elegida[i+1] if i < len(maquina_elegida)-1 else None

                    # Actualizar sigue_en_maquina
                    sigue_en_maquina = [op for op in sigue_en_maquina if op not in maquina_elegida]
                    for op in maquina_elegida:
                        if not info[op]['completada']:
                            if op not in sigue_en_maquina:
                                sigue_en_maquina.append(op)
                            break

                    print(f"Modificación dentro del caso feo de O_M: {sigue_en_maquina}")

                    # Forzar continuidad del bucle principal
                    planificables = list(set(sigue_en_job) & set(sigue_en_maquina))


        # Imprimir el estado de `info` al final
            print("\nEstado de info al finalizar el proceso:")
            for op_id, datos in info.items():
                print(f"Operación {op_id}: {datos}")

        
        print("\nLa nueva solución es: ", solucion)
        
        return solucion # Quiero que regrese la solución ya reparada.