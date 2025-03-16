class Solution_Management:
    
    @staticmethod
    def random_solution(numero_de_maquinas,numero_de_trabajos,lista_de_vertices):
        solucion = [] # Solución que corresponde al orden en que entran las operaciones en las máquinas
                      # es una lista de listas, con tantas listas como máquinas.
        
        for _ in range (numero_de_maquinas):
            solucion.append([]) # Tantas listas como máquinas.

        
        # Para la construcción de la solución, necesitamos una lista de planificables, esta lista tiene 
        # tantos elementos como Jobs (numero_de_trabajos).
        planificables = []

        # Paso 1: Metemos en la lista de planificables a todas las operaciones iniciales de cada Job.
        op_id = 1 # Garantizamos iniciar con el vértice de Id = 1

        for j in range(1, numero_de_trabajos+1): # Sí contamos todos los jobs.
            # La primera operación de cada job tiene id = 1 + (j-1)*numero_de_maquinas
            op_id = 1 + (j-1)*numero_de_maquinas
            planificables.append(op_id)

        ''' Lo que sigue es iterativo, por eso viene repetido dentro del while.

        # De las planificables, se elije una al azar:
        operacion_elegida = random.choice(planificables) # Este número está en correspondencia con el Id
                                                         # del vértice al que corresponde.
        
        # Para poder planificar esta primera elección, es necesario obtener la máquina que le corresponde
        # al vértice elegido.
        maquina_del_elegido = lista_de_vertices[operacion_elegida].get_maquina()

        # Planificamos la operación:
        solucion[maquina_del_elegido-1].append(operacion_elegida) # En la máquina correspondiente (restamos un 1
                                                                  # porque las listas en Python cuentan desde 0),
                                                                  # agregamos a la operación elegida.

        # Quitamos la operación de la lista de planificables:
        planificables.remove(operacion_elegida)

        # Si la operación elegida no era la operación final dentro del mismo Job, agregamos la operación que sigue.
        if (operacion_elegida % numero_de_maquinas != 0): # Las operaciones finales dentro de un Job son divisibles
                                                          # entre el número de máquinas.
            planificables.append(operacion_elegida+1)

        # Esto se repite hasta que |planificables| != 0
        '''

        while planificables:
            operacion_elegida = random.choice(planificables) 
        
            maquina_del_elegido = lista_de_vertices[operacion_elegida].get_maquina()
        
            solucion[maquina_del_elegido-1].append(operacion_elegida)  

            planificables.remove(operacion_elegida)

            if (operacion_elegida % numero_de_maquinas != 0): 
                planificables.append(operacion_elegida+1)

        return solucion
    
    @staticmethod
    def get_makespan(solucion):
        pass
    

    @staticmethod
    def get_vecino(solucion):
        pass
