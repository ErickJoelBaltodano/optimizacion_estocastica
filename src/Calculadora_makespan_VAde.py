'''
Aquí y en el futuro, se va a usar una estructura auxiliar para poder hacer la evaluación del makespan de las 
soluciones.
'''



class Evaluador_Makespan: # No tengo la menor idea de si debe ser clase o no.

    # Estructura auxiliar:
    @staticmethod
    def construct_info(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion):
        '''
        Construye la estructura auxiliar 'info' para cada operación,
        identificando los pred y suc en job y en máquina.
        'solucion' es la lista de listas (por máquina) generada por el generador de 
        soluciones aleatorias o por algún otro método (ej.: Búsqueda Tabú).
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
                'suc_job': None,
                'pred_maquina': None,
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

    # HASTA AQUÍ: La estructura auxiliar (debería funcionar aún para soluciones no-iniciales).

    @staticmethod
    def agregar_a_planificables(op_id, info, planificables):
        '''
        Agrega una operación a planificables sólo si sus predecesoras en job y máquina están completadas.
        '''
        if op_id in planificables or info[op_id]['completada']: # Si la operación está en la lista de 
                                                                # planificables o ya fue completada.
            return

        # Verifica si la predecesora en el job está completada
        pred_job = info[op_id]['pred_job']
        if pred_job is not None and not info[pred_job]['completada']:
            print(f"Op {op_id} no se puede planificar: su predecesora en el job ({pred_job}) no está completada.")
            return

        # Verifica si la predecesora en la máquina está completada
        pred_maquina = info[op_id]['pred_maquina']
        if pred_maquina is not None and not info[pred_maquina]['completada']:
            print(f"Op {op_id} no se puede planificar: su predecesora en la máquina ({pred_maquina}) no está completada.")
            return

        # Si ambas predecesoras están completadas, agrega la operación a planificables
        planificables.append(op_id)
        print(f"Op {op_id} agregada a planificables.")
        

    def calculadora_makespan(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion):
        
        '''
        Evalúa la solución generada:
          - Realiza una pasada forward simulando la ejecución según la intersección
            de operaciones planificables (tal como en Huang et al.).
          - Calcula los tiempos de inicio (r_i) y finalización.
          - Realiza una pasada backward recursiva para calcular los q_i.
        Retorna: makespan, diccionario de r, diccionario de q, el orden global de programación, y la estructura 'info'.
        '''

        # --- PASADA FORWARD: Cálculo de r_i y tiempos de finalización ---
        # Inicializamos el “pool” de operaciones disponibles (planificables) con la primera operación de cada job.
        orden_global = []  # Orden global en que se planifican las operaciones
        planificables = [] # Lista de operaciones disponibles para planificarse.
        for j in range(1, numero_de_trabajos+1): # Sí contamos todos los jobs.
            # La primera operación de cada job tiene id = 1 + (j-1)*numero_de_maquinas
            op_id = 1 + (j-1)*numero_de_maquinas
            planificables.append(op_id)
            print(f"Op {op_id} (primera del job {j}) agregada inicialmente a planificables.")
        
        # Arreglos para llevar el tiempo en que cada máquina y cada job queda libre.
        tiempo_maquina = [0] * numero_de_maquinas  # índice: máquina - 1
                                                   # Al principio, cada máquina está libre en el tiempo 0.
        tiempo_job = [0] * numero_de_trabajos      # índice: job - 1
                                                   # Al principio, cada job está libre en el tiempo 0.
        
        r = {}  # r[i]: tiempo de inicio (release time) de la operación i
        f = {}  # f[i]: tiempo de finalización de la operación i

        # Construye la estructura auxiliar 'info'
        info = Evaluador_Makespan.construct_info(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion)

        # Simulamos la ejecución siguiendo el orden de selección de las planificables.
        # (En el generador original se elige al azar, pero aquí para la evaluación usaremos un FIFO,
        #  lo que respeta las restricciones de precedencia. FIFO = "First In, First Out", o en español 
        # "Primero en entrar, primero en salir".)
        while planificables:
            op_id = planificables.pop(0)  # Tomamos el primer elemento de la lista "planificables" y lo 
                                          # eliminamos al mismo tiempo (FIFO)
            orden_global.append(op_id)
            op = lista_de_vertices[op_id]
            m_index = op.maquina - 1  # índice de la máquina 
            j_index = op.trabajo - 1  # índice del job

            # El tiempo de inicio es el máximo entre:
            # - El tiempo en que la máquina queda libre.
            # - El tiempo en que el job está listo (tras finalizar la operación anterior en el job).
            start_time = max(tiempo_maquina[m_index], tiempo_job[j_index])
            finish_time = start_time + op.tiempo
            r[op_id] = start_time # Este es el r_i
            f[op_id] = finish_time # Este creo que en el artículo lo ponen como d_algo. Me gustó más la 'f'
            tiempo_maquina[m_index] = finish_time
            tiempo_job[j_index] = finish_time

            # Marca la operación como completada
            info[op_id]['completada'] = True
            print(f"\n--- Op {op_id} planificada ---")
            print(f"Tiempo de inicio: {start_time}, Tiempo de finalización: {finish_time}")
            print(f"Tiempo máquina {op.maquina}: {tiempo_maquina[m_index]}")
            print(f"Tiempo job {op.trabajo}: {tiempo_job[j_index]}")

            # Agrega sucesoras a planificables (si cumplen con las dependencias duales)
            suc_job = info[op_id]['suc_job']
            if suc_job is not None:
                Evaluador_Makespan.agregar_a_planificables(suc_job, info, planificables)

            suc_maquina = info[op_id]['suc_maquina']
            if suc_maquina is not None:
                Evaluador_Makespan.agregar_a_planificables(suc_maquina, info, planificables)
        
        makespan = max(f.values()) if f else 0 # El 'makespan' 
        print(f"\n--- Makespan calculado: {makespan} ---")

        # --- PASADA BACKWARD: Cálculo de q_i ---
        # Primero se construye la estructura de precedencias.
        info = Evaluador_Makespan.construct_info(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion)
        
        # Usamos memorización para evitar recálculos
        memo = {}
        def computa_q(op_id):
            if op_id in memo:
                return memo[op_id]
            # Si la operación no tiene sucesores ni en el job ni en la máquina, se asume q = 0.
            suc_job = info[op_id]['suc_job']
            suc_maquina = info[op_id]['suc_maquina']
            if suc_job is None and suc_maquina is None:
                memo[op_id] = 0
                return 0
            candidate = 0
            if suc_job is not None:
                candidate = max(candidate, computa_q(suc_job) + info[suc_job]['tiempo'])
            if suc_maquina is not None:
                candidate = max(candidate, computa_q(suc_maquina) + info[suc_maquina]['tiempo'])
            memo[op_id] = candidate
            return candidate
        
        q = {}
        # Calculamos q para cada operación programada en el orden global.
        for op_id in orden_global:
            q[op_id] = computa_q(op_id)

        print("\n--- Valores de q calculados ---")
        for op_id, q_val in q.items():
            print(f"Op {op_id}: q = {q_val}")
        
        return makespan, r, q, orden_global, info