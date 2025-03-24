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
        while (planificables or (sigue_en_job or sigue_en_maquina)):   

            # Lista de las operaciones planificables; sus elementos están en O_J y O_M
            planificables = list(set(sigue_en_job) & set(sigue_en_maquina))

            # Algunos prints para ver cómo va la cosa:
            print('\ncompletadas', completadas)
            print('\nsigue_en_job', sigue_en_job)
            print('\nsigue_en_maquina', sigue_en_maquina) 
            print('\nplanificables', planificables)
            print(f"\nLa solución (en reparación) es: {solucion}")  

            '''# Imprimir el estado de `info` en cada iteración
            print("Estado de info en esta iteración:")
            for op_id, datos in info.items():
                print(f"Operación {op_id}: {datos}")'''

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
            if not planificables: # Si `planificables` es vacío (pero aún hay operaciones en
                                  # máquinas y/o jobs que falten por planificar).

                print("\nEstamos en el caso feo...\n")                

                operacion_elegida_id = random.choice(sigue_en_job) # Elegimos alguna operación al azar
                                                                   # de aquellas que nos falte planificar
                                                                   # en la lista de los jobs.
                
                # Vamos a la máquina que corresponde a la operación que elegimos:
                maquina_op_elegida_idx = info[operacion_elegida_id]['maquina']   
                # `solucion[m-1]` es la lista que corresponde a la máquina m - 1 

                print(f"La máquina de la operación elegida ({operacion_elegida_id}) es {info[operacion_elegida_id]['maquina'] + 1}")

                maquina_elegida = solucion[maquina_op_elegida_idx] # Lista de operaciones en la máquina
                                                                   # elegida. Ej.: [1, 4, 8]

                print(f"La máquina elegida es {maquina_elegida}")
                
                # Índice de la operación elegida.
                op_elegida_idx = maquina_elegida.index(operacion_elegida_id)

                # Vamos a reordenar a la solución mandando a la `operacion_elegida_id` en la primera
                # posición disponible después de la última operación ya planificada.
                for operacion_idx, op_id in enumerate(maquina_elegida):
                    if info[op_id]['completada']: 
                        continue    # Si la operación en la que vamos ya fue planificada i.e. su 
                                    # flag está como `completada` == True, nos vamos con la que sigue.

                    print(f"La lista de las que siguen en máquina es {sigue_en_maquina}")
                    print(f"La operación con la que haremos el cambio es {op_id}")

                    # Para hacer el procedimiento descrito en 'INSTRUCCIONES':
                    op_elegida = operacion_elegida_id
                    op_cambio = op_id 
                    
                    pred_maq_op_elegida = info[op_elegida]['pred_maquina']
                    suc_maq_op_elegida = info[op_elegida]['suc_maquina']
                    pred_maq_op_cambio = info[op_cambio]['pred_maquina']
                    suc_maq_op_cambio = info[op_cambio]['suc_maquina']

                    # 1. Actualizar predecesor de op_elegida (nuevo predecesor: pred_maq_op_cambio)
                    info[op_elegida]['pred_maquina'] = pred_maq_op_cambio
                    if pred_maq_op_cambio is not None:
                        info[pred_maq_op_cambio]['suc_maquina'] = op_elegida  # Antes apuntaba a op_cambio

                    # 2. Actualizar sucesor de op_elegida (nuevo sucesor: suc_maq_op_cambio)
                    info[op_elegida]['suc_maquina'] = suc_maq_op_cambio
                    if suc_maq_op_cambio is not None:
                        info[suc_maq_op_cambio]['pred_maquina'] = op_elegida  # Antes apuntaba a op_cambio

                    # 3. Actualizar predecesor de op_cambio (nuevo predecesor: pred_maq_op_elegida)
                    info[op_cambio]['pred_maquina'] = pred_maq_op_elegida
                    if pred_maq_op_elegida is not None:
                        info[pred_maq_op_elegida]['suc_maquina'] = op_cambio  # Antes apuntaba a op_elegida

                    # 4. Actualizar sucesor de op_cambio (nuevo sucesor: suc_maq_op_elegida)
                    info[op_cambio]['suc_maquina'] = suc_maq_op_elegida
                    if suc_maq_op_elegida is not None:
                        info[suc_maq_op_elegida]['pred_maquina'] = op_cambio  # Antes apuntaba a op_elegida

                    # Hacemos el cambio a nivel solución (lista de máquinas):
                    maquina_elegida[op_elegida_idx], maquina_elegida[operacion_idx] = \
                    maquina_elegida[operacion_idx], maquina_elegida[op_elegida_idx]

                    # Modificamos O_M
                    sigue_en_maquina.remove(op_cambio)
                    sigue_en_maquina.append(op_elegida)

                    print("Modificación dentro del caso feo de O_M: ", sigue_en_maquina)

                    # Imprimir el estado de `info` en cada iteración del caso feo.
                    print("\nEstado de info en esta iteración:\n")
                    for op_id, datos in info.items():
                        print(f"Operación {op_id}: {datos}")

                    # Para este momento, O_J *intersección* O_J ya no es el vacío.
                    planificables = list(set(sigue_en_job) & set(sigue_en_maquina))
                    # Pero esto se va a cotejar hasta la siguiente iteración porque aquí termina este bloque.

                    break # # Salimos del `for`

                # En teoría, de aquí salimos del `while planificables == False` porque `operacion_elegida` ya
                # está ahí. 


        print("La nueva solución es: ", solucion)
        
        return solucion # Quiero que regrese la solución ya reparada.