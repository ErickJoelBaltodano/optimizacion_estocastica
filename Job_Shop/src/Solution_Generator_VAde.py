'''Aquí estoy suponiendo que ya se han creado los vértices "dummy"
que corresponden al 0 y al N+1 y por tanto que los índices en la 
lista de vértices son los mismos que los id's que le corresponden 
a los vértices como objeto.'''

import random
from Calculadora_makespan_VAde import *

class Solution_Management:
    
    # Clase donde generamos soluciones que son válidas para nuestra implementación del problema del Job Shop.
    @staticmethod
    def generar_solucion(numero_de_maquinas,numero_de_trabajos,lista_de_vertices):

        solucion = [] # Solución que corresponde al orden en que entran las operaciones en las máquinas
                      # es una lista de listas, con tantas listas como máquinas.
        
        for _ in range (numero_de_maquinas):
            solucion.append([]) # Tantas listas como máquinas.

        
        # Para la construcción de la solución, necesitamos una lista de planificables, esta lista tiene 
        # tantos elementos como Jobs (numero_de_trabajos).
        planificables = []

        # Paso 1: Metemos en la lista de planificables a todas las operaciones iniciales de cada Job.
        x = 1 # Garantizamos iniciar con el vértice de Id = 1
        for _ in range(numero_de_trabajos): # |planificables| = num_de_trabajos
            planificables.append(x) # Agregamos a cada paso la primer operación de cada Job.
            x += numero_de_maquinas # Si tengo 3 máquinas y 4 jobs, la primer operación del Job1 es 1,
                                    # la primer operación del Job2 es 1+3=4, la primer operación de Job3
                                    # es 4+3=7, la primer operación de Job4 es 7+3=10.

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

        while (len(planificables) != 0):
            operacion_elegida = random.choice(planificables) 
        
            maquina_del_elegido = lista_de_vertices[operacion_elegida].get_maquina()
        
            solucion[maquina_del_elegido-1].append(operacion_elegida)  

            planificables.remove(operacion_elegida)

            if (operacion_elegida % numero_de_maquinas != 0): 
                planificables.append(operacion_elegida+1)

        return solucion
    
    
    #Método donde dada una solución generamos una vecindad de soluciones válidas.
    @staticmethod
    def generar_vecindad(solucion):
        vecindad = []
        '''
        Inserte aquí el método, por favor
        '''
        
        return vecindad
        
        