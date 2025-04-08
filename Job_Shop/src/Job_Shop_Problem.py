from Solution_Generator_VAde import *
from Vertice_VAde import *
from Reparadora_de_Soluciones import *
from Operador_Cruza_de_Padres import *
from Operador_Selector_de_Padres import *
from Operador_de_Listas import *
import random
import math


class Job_Shop_Problem:
    
    
    def __init__(self,lista_de_vertices:list[Vertice],numero_de_maquinas:int,numero_de_trabajos:int ,solucion = None):
        self.vertices = lista_de_vertices
        self.numero_de_maquinas = numero_de_maquinas
        self.numero_de_trabajos = numero_de_trabajos
        self.solucion = None
        if solucion is None:
            self.solucion =Solution_Generator.generador_solucion(numero_de_maquinas,numero_de_trabajos,lista_de_vertices)
        else:
            self.solucion = solucion
        
    # Algoritmo mediante el cual generamos una vecindad
    def get_neightborhood(self):
        vecinos = []
        _, camino_critico = self.makespan()

        for i in range(len(camino_critico) - 1):
            u = camino_critico[i]
            v = camino_critico[i + 1]

            maquina = self.vertices[u].get_maquina()
            if self.vertices[v].get_maquina() != maquina:
                continue  # Solo consideramos intercambios en la misma máquina

            # Obtener la posición de u y v en la máquina
            posicion_u = self.solucion[maquina].index(u)
            posicion_v = self.solucion[maquina].index(v)

            if abs(posicion_u - posicion_v) == 1:
                # Crear una copia de la solución
                nueva_solucion = [list(m) for m in self.solucion]
                # Intercambiar u y v
                nueva_solucion[maquina][posicion_u], nueva_solucion[maquina][posicion_v] = \
                    nueva_solucion[maquina][posicion_v], nueva_solucion[maquina][posicion_u]
                vecinos.append(nueva_solucion)

        return vecinos   
    
    # Método donde iteramos aleatoriamente sobre las vecindades
    def busqueda_aleatoria(self,numero_de_iteraciones,solucion = None):
        
        if solucion != None:
            self.set_solution(solucion)
            
            
        mejor_eval = self.makespan()
        
        for _ in range(numero_de_iteraciones):
            vecino = random.choice(self.get_neightborhood())
            eval_vecino = self.makespan(solution=vecino)
            
            if (eval_vecino < mejor_eval):
                self.set_solution(vecino)
                mejor_eval = eval_vecino
                
        return mejor_eval,self.solucion
                
                
                

    
    #Algoritmo de busqueda con recocido simulado
    def recocido_simulado(self,no_de_evaluaciones:int,temp_inicial = 10000,factor_de_enfriamiento =.95, sol_actual = None):
        if sol_actual != None :
            self.solucion = sol_actual
            
        mejor_eval,_ = self.makespan()
        evaluaciones_actuales =1
        temperatura = temp_inicial


            
        while  evaluaciones_actuales < no_de_evaluaciones and temperatura > 1:
            
            vecino = random.choice(self.get_neightborhood())
            eval_vecino,_= self.makespan(solution=vecino)
            evaluaciones_actuales +=1
            
            if (mejor_eval > eval_vecino):
                
                self.set_solution(vecino)
                mejor_eval = eval_vecino
            
            else:
                # Si no generamos una probabilidad de mover nuestra solución actual en caso contrario no hacemos NADOTA :D
                if random.random() < math.exp(-(eval_vecino-mejor_eval) / temperatura):    
                        
        
                    self.set_solution(vecino)
                    mejor_eval = eval_vecino
        
        
        
            # Actualizamos la temperatura
            temperatura *= factor_de_enfriamiento
        return self.solucion,mejor_eval

    
    #Algoritmo Memético.
    def generacional_con_recocido_simulado(self,
                                           evaluaciones_totales:int,
                                           operador_cruza_padres = Operador_Cruza_de_Padres.cruza_por_cromosoma
                                           ,operador_selector_de_padres = Operador_Selector_de_Padres.random,
                                           tamaño_generacional= 30,
                                           evaluaciones_recocido = 250,
                                           temp_inicial = 10000,
                                           factor_de_enfriamiento =.95):
        
        
        # Generamos una vecindad inicial
        poblacion = [Solution_Generator.generador_solucion(self.numero_de_maquinas,self.numero_de_trabajos,self.vertices) for _ in range(tamaño_generacional)]
        makespans = [None  for _ in poblacion] # Dado que las soluciones son aleatorias,no vale la pena evaluarlas ahorita
        
        evaluaciones_actuales = 0
        
        
        while (evaluaciones_actuales < evaluaciones_totales):
            
            #Mejoramos con recocido simulado la población.    
            i = 0
            while i  < len(poblacion):
                poblacion[i]= self.recocido_simulado(evaluaciones_recocido,temp_inicial,factor_de_enfriamiento)
                for x in poblacion [i]:
                    print (x)
                k,j = self.makespan(poblacion[i])
            
            # Dado que evaluamos n individuos hay que incrementar el contador
            evaluaciones_actuales += tamaño_generacional
            
            #Seleccionamos a los padres
            indice_padre_1,indice_padre_2 = operador_selector_de_padres(poblacion)
            
            #Cruzamos y generamos hijos
            hijo1, hijo2 = operador_cruza_padres(poblacion[indice_padre_1],poblacion[indice_padre_2])
            
            
            #Reparamos los hijos
            hijo1 = Reparadora.reparacion(hijo1,self.numero_de_maquinas,self.numero_de_trabajos,self.vertices)
            hijo2 = Reparadora.reparacion(hijo2,self.numero_de_maquinas,self.numero_de_trabajos,self.vertices)
            
            
            
            #Reemplazamos a los padres de la poblacion
            poblacion[indice_padre_1]= hijo1
            poblacion[indice_padre_2]= hijo2
            
            # Recalculamos los makespans
            makespans[indice_padre_1] = self.makespan(hijo1)
            makespans[indice_padre_2] = self.makespan(hijo2)
            
            evaluaciones_actuales+=2
            
                  
        return poblacion,makespans
        
        
        
   
    
    # Regresa el siguiente job dado un id 
    def get_next_job(self,id_actual:int):
        if id_actual > self.numero_de_maquinas*self.numero_de_trabajos:
            raise ValueError("Fuera de Rango >:v")
        if id_actual % self.numero_de_trabajos == 0:
            return self.numero_de_maquinas*self.numero_de_trabajos
        return id_actual + 1
    
    #Regresa el job anterior dado un id
    def get_previous_job(self,id_actual:int):
        if id_actual > self.numero_de_maquinas*self.numero_de_trabajos:
            raise ValueError("Fuera de Rango >:v")
        if id_actual % self.numero_de_trabajos == 1:
            return 0
        return id_actual -1
     
     
        
    #Regresa el tiempo dado un id
    def get_time(self,id_actual:int):
        if id_actual > self.numero_de_maquinas*self.numero_de_trabajos:
            raise ValueError("Fuera de Rango >:v")
        return self.vertices[id_actual].get_tiempo()
     
     
        
    # Regresa un vértice dado un indice 
    '''Warning: Dado que regresa el vértice este puede ser modificado'''
    def get_vertice(self,indice):
        if indice > self.numero_de_maquinas*self.numero_de_trabajos:
            raise ValueError("Fuera de Rango >:v")
        return self.vertices[indice]
    
    
    
    
    def get_previous_mach(self,id_actual:int):
        if id_actual > self.numero_de_maquinas*self.numero_de_trabajos:
            raise ValueError("Fuera de Rango >:v")
        
        
               # Caso donde calculamos la siguiente maquina de dado un id de un vértice sin lista de índices O(numero de jobs)
        maquina = self.vertices[id_actual].get_maquina()
        contador = 0
        while contador < len (self.solucion[maquina]):
            if self.solucion[maquina][contador] == id_actual :
                if  contador == 0:
                    # Caso donde es el ultimo planificado dentro de su máquina
                    return 0
                # Caso promedio
                return self.solucion[maquina][contador -1]    
            else:
                # Iteramos
                contador +=1

            

    
    def get_next_mach(self,id_actual:int,lista_de_indices:list[int]= None):
        if id_actual > self.numero_de_maquinas*self.numero_de_trabajos:
            raise ValueError("Fuera de Rango >:v")
        

        '''----------------------------------------------------------------------------------------------------'''
        # Caso donde calculamos la siguiente maquina de dado un id de un vértice sin lista de índices O(numero de jobs)
        if lista_de_indices == None:# O(numero de jobs)
            maquina = self.vertices[id_actual].get_maquina()
            contador = 0
            while contador < len (self.solucion[maquina]):
                if self.solucion[maquina][contador] == id_actual :
                    if  contador >= self.numero_de_trabajos-1:
                        # Caso donde es el ultimo planificado dentro de su máquina
                        return self.numero_de_maquinas*self.numero_de_trabajos
                    # Caso promedio
                    return self.solucion[maquina][contador +1]    
                else:
                    # Iteramos
                    contador +=1
            '''-----------------------------------------------------------------------------------------------'''
        else :# O(1)
            maquina = self.vertices[id_actual].get_maquina()
            indice = lista_de_indices[maquina-1]
            if  indice >= self.numero_de_trabajos-1:
                # Caso donde es el ultimo planificado dentro de su máquina
                lista_de_indices[maquina-1] = None
                return self.numero_de_maquinas*self.numero_de_trabajos
            # Caso promedio
            lista_de_indices[maquina-1]+=1
            return self.solucion[maquina][indice +1]
                
    

   
  
    def set_solution(self,solution):
        self.solucion = solution
        
         
        

    #Método donde calculamos el makespan de cada elemento de cada operación y calculamos el camino crítico.
    def makespan(self, solution=None):
        # Inicializar arrays de resultados
        num_ops = self.numero_de_maquinas * self.numero_de_trabajos
        resultado = [None] * (num_ops + 2)  # Tiempos de finalización
        resultado[0] = 0  # Tiempo inicial
        
        # Para rastrear el camino crítico
        predecesores = [None] * (num_ops + 2)  # Guarda de dónde viene cada operación
        
        # Usar solución temporal si se proporciona
        original_solution = self.solucion
        if solution is not None:
            self.solucion = solution
        
        # Inicializar listas de planificables
        planificables_job = [1 + (j * self.numero_de_maquinas) for j in range(self.numero_de_trabajos)]
        indices_maquinas = [0 for _ in range(self.numero_de_maquinas)]
        planificables_mach = [self.solucion[m][0] for m in range(self.numero_de_maquinas) if len(self.solucion[m]) > 0]
        
        planificados = 0
        
        while planificados < num_ops:
            planificables = Operador_de_Listas.interseccion(planificables_job, planificables_mach)
            
            if not planificables:
                raise ValueError("No hay operaciones planificables - solución inválida")
            
            for operacion in planificables:
                maquina = self.vertices[operacion].get_maquina()
                
                # Calcular tiempos previos
                prev_job = self.get_previous_job(operacion)
                prev_mach = self.get_previous_mach(operacion)
                
                tiempo_prev_job = resultado[prev_job] if prev_job is not None else 0
                tiempo_prev_mach = resultado[prev_mach] if prev_mach is not None else 0
                
                # Determinar qué precedente fue el restrictivo
                if tiempo_prev_job > tiempo_prev_mach:
                    predecesores[operacion] = prev_job
                else:
                    predecesores[operacion] = prev_mach
                
                tiempo_inicio = max(tiempo_prev_job, tiempo_prev_mach)
                resultado[operacion] = tiempo_inicio + self.vertices[operacion].get_tiempo()
                
                planificados += 1
                
                # Actualizar planificables_job
                if operacion % self.numero_de_maquinas != 0:
                    siguiente_job = operacion + 1
                    idx = planificables_job.index(operacion)
                    planificables_job[idx] = siguiente_job
                else:
                    planificables_job.remove(operacion)
                
                # Actualizar planificables_mach
                indice = indices_maquinas[maquina]
                if indice + 1 < len(self.solucion[maquina]):
                    siguiente_mach = self.solucion[maquina][indice + 1]
                    idx = planificables_mach.index(operacion)
                    planificables_mach[idx] = siguiente_mach
                    indices_maquinas[maquina] += 1
                else:
                    planificables_mach.remove(operacion)
        
        # Encontrar la operación que termina última (makespan)
        makespan_val = max(resultado[1:-1])
        ultima_op = resultado.index(makespan_val)
        
        # Reconstruir camino crítico hacia atrás
        camino_critico = []
        op_actual = ultima_op
        while op_actual is not None and op_actual != 0:
            camino_critico.append(op_actual)
            op_actual = predecesores[op_actual]
        camino_critico.reverse()  # Para tenerlo en orden cronológico
        
        # Restaurar solución original si era temporal
        if solution is not None:
            self.solucion = original_solution
        
        return makespan_val, camino_critico