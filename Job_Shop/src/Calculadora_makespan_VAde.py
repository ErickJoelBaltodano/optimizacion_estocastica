class Evaluador_Makespan: 

    # Estructura auxiliar:
    @staticmethod
    def construct_info(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion):
        '''
        Construye la estructura auxiliar 'info' para cada operación,
        identificando los pred y suc en job y en máquina.
        'solucion' es la lista de listas (por máquina) generada por el generador de 
        soluciones aleatorias o por algún otro método.
        Se asume que la lista_de_vertices tiene los dummies en la posición 0 y N+1.
        '''
        # Inicializamos la info para cada vértice (operación)
        # Usamos el id (que coincide con el índice en lista_de_vertices) como clave.
        info = {}
        for op in range(1, len(lista_de_vertices)-1): # Ignoramos los dummys 0 y N+1
            vert = lista_de_vertices[op]
            info[op] = {
                'tiempo': vert.tiempo, 
                'maquina': vert.maquina,
                'job': vert.trabajo,
                'pred_job': None,
                'suc_job': None, # Hasta aquí, datos de entrada.

                'pred_maquina': None, # Aquí empiezan datos de solución.
                'suc_maquina': None,
                'completada': False  # Nuevo campo, creo que va a servir.
            }


        # Precedencia en el job:
        # En nuestro formato, las operaciones de cada job se generan consecutivamente.
        # La primera operación de un job es aquella cuyo id es 1 + (job-1)*numero_de_maquinas.
        for op in range(1, len(lista_de_vertices)-1):  # Se ignoran los dummies
            if info[op]['job'] is not None: # Según yo esta condición siempre se cumple (porque
                                            # quité los dummys, pero lo dejo por si acaso).
                # Si la operación anterior pertenece al mismo job, es su predecesora
                if op - 1 >= 1 and info[op-1]['job'] == info[op]['job']:
                    info[op]['pred_job'] = op - 1
                    info[op-1]['suc_job'] = op
        
        
        # Precedencia en la máquina:
        # 'solucion' es una lista de listas; cada lista contiene los id's de las operaciones
        # en el orden en que se procesan en esa máquina.
        for m in range(numero_de_maquinas):
            operaciones_maquina = solucion[m] # 'solucion' es una lista de listas donde se guardan
                                              # (en cada lista) las operaciones de cada máquina.
                                              # solucion[m] es la lista (ordenada) de operaciones que
                                              # se ejecutan en la máquina m+1
            for i, op in enumerate(operaciones_maquina): 
                if i > 0: # Si i==0, estamos en la primera operación que se ejecuta en la máquina.
                    info[op]['pred_maquina'] = operaciones_maquina[i-1]
                    info[operaciones_maquina[i-1]]['suc_maquina'] = op
        
        print("\n--- Estructura 'info' construida ---")
        for op, datos in info.items():
            print(f"Op {op}: {datos}")
        
        return info

    # Ahora para la pasada forward, construimos nuestra función auxiliar para agregar a planificables.
    @staticmethod
    def agregar_a_planificables(op_id, info, planificables):
        '''
        Agrega una operación a planificables sólo si sus predecesoras en job y máquina están completadas.
        '''
        if op_id in planificables or info[op_id]['completada']: # Si la operación está en la lista de 
                                                                # planificables o ya fue completada.
            return # No hacemos nada.

        # Verifica si la predecesora en el job (si existe) está completada
        pred_job = info[op_id]['pred_job']
        if pred_job is not None and not info[pred_job]['completada']:
            #print(f"Op {op_id} no se puede planificar: su predecesora en el job ({pred_job}) no está completada.")
            return

        # Verifica si la predecesora en la máquina (si existe) está completada  
        pred_maquina = info[op_id]['pred_maquina']
        if pred_maquina is not None and not info[pred_maquina]['completada']:
            #print(f"Op {op_id} no se puede planificar: su predecesora en la máquina ({pred_maquina}) no está completada.")
            return

        # Si ambas predecesoras están completadas, agrega la operación a planificables
        planificables.append(op_id)
        #print(f"Op {op_id} agregada a planificables.")


    # Para la pasada backward, hacemos nuestra función auxiliar para planificar operaciones.
    @staticmethod
    def agregar_a_planificables_backward(op_id, info, planificables_backward):
        '''
        Agrega una operación a planificables (backward) sólo si sus sucesoras en job y máquina están completadas.
        (Se oye raro que así sea, pero es que estamos recorriendo el grafo al revés).
        '''

        if op_id in planificables_backward or info[op_id]['completada']: # Si la operación está en la lista de 
                                                                         # planificables o ya fue completada.
            return

        # Verifica si la sucesora en el job está completada
        suc_job = info[op_id]['suc_job']
        if suc_job is not None and not info[suc_job]['completada']:
            #print(f"Op {op_id} no se puede planificar: su sucesora en el job ({suc_job}) no está completada.")
            return

        # Verifica si la sucesora en la máquina está completada  
        suc_maquina = info[op_id]['suc_maquina']
        if suc_maquina is not None and not info[suc_maquina]['completada']:
            #print(f"Op {op_id} no se puede planificar: su sucesora en la máquina ({suc_maquina}) no está completada.")
            return

        # Si ambas sucesoras están completadas, agrega la operación a planificables
        planificables_backward.append(op_id)
        #print(f"Op {op_id} agregada a planificables (pasada backward).")

    
    def calculadora_makespan(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion):

        # Construye la estructura auxiliar 'info'
        info = Evaluador_Makespan.construct_info(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion)
        
        '''
        Evalúa la solución generada:
          - Realiza una pasada forward simulando la ejecución según la intersección
            de operaciones planificables (tal como en Huang et al.).
          - Calcula los tiempos de inicio (r_i) y finalización.
          - Realiza una pasada backward recursiva para calcular los q_i.
        Retorna: makespan, diccionario de r, diccionario de q y la estructura 'info'.
        '''

        # --- PASADA FORWARD: Cálculo de r_i y tiempos de finalización ---
        # Inicializamos el “pool” de operaciones disponibles (planificables) con la primera operación de cada job.
        # orden_global = []  # Orden global en que se planifican las operaciones
        planificables = [] # Lista de operaciones disponibles para planificarse.
        for op_id, datos in info.items():
            # Solo es planificable si no tiene predecesora en el job y en la máquina
            if datos['pred_job'] is None and datos['pred_maquina'] is None:
                planificables.append(op_id)
                #print(f"Op {op_id} agregada inicialmente a planificables.")
        
        # Arreglos para llevar el tiempo en que cada máquina y cada job queda libre.
        tiempo_maquina = [0] * numero_de_maquinas  # índice: máquina - 1
                                                   # Al principio, cada máquina está libre en el tiempo 0.
                                                   # Si numero_de_maquinas=3, tempo_maquina = [0, 0, 0]
        tiempo_job = [0] * numero_de_trabajos      # índice: job - 1
                                                   # Al principio, cada job está libre en el tiempo 0.
        
        r = {}  # r[i]: tiempo de inicio (release time) de la operación i
        f = {}  # f[i]: tiempo de finalización de la operación i

        # Simulamos la ejecución siguiendo el orden de selección de las planificables.
        # (En el generador original se elige al azar, pero aquí para la evaluación usaremos un FIFO,
        #  lo que respeta las restricciones de precedencia. FIFO = "First In, First Out", o en español 
        # "Primero en entrar, primero en salir".)
        while planificables:
            op_id = planificables.pop(0)  # Tomamos el primer elemento de la lista "planificables" y lo 
                                          # eliminamos al mismo tiempo (FIFO)
            # orden_global.append(op_id) # Creo que el 'orden global' en realidad no sirve de mucho.
            op = lista_de_vertices[op_id]
            m_index = op.maquina - 1  # índice de la máquina 
            j_index = op.trabajo - 1  # índice del job


            # El tiempo de inicio es el máximo entre:
            # - El tiempo en que la máquina queda libre.
            # - El tiempo en que el job está listo (tras finalizar la operación anterior en el job).
            start_time = max(tiempo_maquina[m_index], tiempo_job[j_index])
            finish_time = start_time + op.tiempo # Tiempo en el que puede iniciar + tiempo en que se procesa.
            r[op_id] = start_time # Este es el r_i
            f[op_id] = finish_time # Este creo que en el artículo lo ponen como d_algo. Me gustó más la 'f'
            tiempo_maquina[m_index] = finish_time
            tiempo_job[j_index] = finish_time

            # Marca la operación como completada
            info[op_id]['completada'] = True
            '''print(f"\n--- Op {op_id} planificada ---")
            print(f"Tiempo de inicio: {start_time}, Tiempo de finalización: {finish_time}")
            print(f"Tiempo máquina {op.maquina}: {tiempo_maquina[m_index]}")
            print(f"Tiempo job {op.trabajo}: {tiempo_job[j_index]}")'''

            # Agrega sucesoras a planificables (si cumplen con las dependencias duales)
            suc_job = info[op_id]['suc_job']
            if suc_job is not None:
                Evaluador_Makespan.agregar_a_planificables(suc_job, info, planificables)

            suc_maquina = info[op_id]['suc_maquina']
            if suc_maquina is not None:
                Evaluador_Makespan.agregar_a_planificables(suc_maquina, info, planificables)
        
        makespan = max(f.values()) # El 'makespan' 
        print(f"\n--- Makespan (forward) calculado: {makespan} ---\n")

        # Como vamos a recorrer el grafo al revés, necesitamos resetear las flags:
        for op_id in info:
            info[op_id]['completada'] = False

        # --- PASADA BACKWARD: Cálculo de q_i ---
        # Esto es casi un Ctrl C + Ctrl V de lo de arriba.
        planificables_backward = [] # Lista de operaciones disponibles para planificarse.
        for op_id, datos in info.items():
            # Solo es planificable si no tiene sucesora en el job y en la máquina
            if datos['suc_job'] is None and datos['suc_maquina'] is None:
                planificables_backward.append(op_id)
                #print(f"Op {op_id} agregada inicialmente a planificables_backward.")

        # Arreglos para llevar el tiempo en que cada máquina y cada job queda libre.
        tiempo_maquina = [0] * numero_de_maquinas  # índice: máquina - 1
                                                   # Al principio, cada máquina está libre en el tiempo 0.
                                                   # Si numero_de_maquinas=3, tiempo_maquina = [0, 0, 0]
        tiempo_job = [0] * numero_de_trabajos      # índice: job - 1
                                                   # Al principio, cada job está libre en el tiempo 0.
        q = {} # Diccionario donde se van a guardar las qi's. Para cada operación i, q_i = t_i + d_i. Donde
               # t_i es el tiempo más largo en el que llegamos de la operación i (suponiendo que ya la 
               # terminamos) al final del proceso y d_i es el tiempo en el que es procesada la operación i

        t = {}
        d = {}

        # Al igual que en la pasada forward, vamos a simular la ejecución. Sólo que ahora estamos recorriendo
        # el grafo al revés.
        while planificables_backward:
            op_id = planificables_backward.pop(0)  # Tomamos el primer elemento de la lista "planificables" y lo 
                                                   # eliminamos al mismo tiempo (FIFO)

            op = lista_de_vertices[op_id]
            m_index = op.maquina - 1  # índice de la máquina 
            j_index = op.trabajo - 1  # índice del job

            # El t_i es el máximo entre.
            # - El q_SMi (El q del sucesor en máquina)
            # - El q_SJi (El q del sucesor en job)
            t[op_id] = max(tiempo_maquina[m_index], tiempo_job[j_index])
            d[op_id] = op.tiempo # Tiempo en el que puede iniciar + tiempo en que se procesa.
            q[op_id] = t[op_id] + d[op_id]
            tiempo_maquina[m_index] = q[op_id]
            tiempo_job[j_index] = q[op_id]

            # Marca la operación como completada
            info[op_id]['completada'] = True
            '''print(f"\n--- Op {op_id} planificada ---")
            print(f"Tiempo de cola: {t[op_id]}, Tiempo de duración: {d[op_id]}")
            print(f"Tiempo máquina {op.maquina}: {tiempo_maquina[m_index]}")
            print(f"Tiempo job {op.trabajo}: {tiempo_job[j_index]}")'''

            # Agrega predecesoras a planificables_backward (si cumplen con las dependencias duales)
            pred_job = info[op_id]['pred_job']
            if pred_job is not None:
                Evaluador_Makespan.agregar_a_planificables_backward(pred_job, info, planificables_backward)

            pred_maquina = info[op_id]['pred_maquina']
            if pred_maquina is not None:
                Evaluador_Makespan.agregar_a_planificables_backward(pred_maquina, info, planificables_backward)
        
        makespan_reverso = max(q.values()) # El 'makespan' del recorrido al revés
        print(f"\n--- Makespan (reverso) calculado: {makespan_reverso} ---")

        return makespan, r, q, t, d, info # Por si en algún momento de la vida sirve, le pedí también que retornara los
                                          # diccionarios con las t's y d's (como recordatorio: q = t + d)

