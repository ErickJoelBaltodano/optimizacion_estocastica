from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Operador_Selector_de_Padres import *
from Operador_Cruza_de_Padres import *
from Generadora_de_vecinos import *
from Torneo import *
import random
import math
import sys
class Busqueda_Por_Vecindades:
    
    # Método Constructor de la Clase Busqueda por Vecindades
    def __init__(self,numero_de_maquinas,numero_de_trabajos,lista_de_vertices):
        self.numero_de_maquinas = numero_de_maquinas
        self.numero_de_trabajos = numero_de_trabajos
        self.lista_de_vertices = lista_de_vertices
        
    def random (self,no_de_iteraciones):
        mejor_sol = None
        mejor_eval = None
        for _ in range(no_de_iteraciones):
            sol_temporal = Solution_Generator.generador_solucion(self.numero_de_maquinas,self.numero_de_trabajos,self.lista_de_vertices)
            eval_temporal ,_, _, _,_,_ = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas, self.numero_de_trabajos, self.lista_de_vertices, sol_temporal)
            
            if mejor_sol is None or mejor_eval > eval_temporal:
                mejor_sol =sol_temporal
                mejor_eval = eval_temporal
                
        return mejor_sol,mejor_eval
            
        
        
        
    
    def random2( self,no_de_iteraciones):
        #Generamos una primera solución inicial.
        mejor_sol = Solution_Management.generar_solucion(self.numero_de_maquinas,self.numero_de_trabajos,self.lista_de_vertices)
        mejor_eval = None
        
        
        for _ in range(no_de_iteraciones):
            mejor_eval, r, q, _,_,info = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas, self.numero_de_trabajos, self.lista_de_vertices, mejor_sol)
            
            print ("++++++++++++++++++++++++++++++++++++++++++")
            print ("Sol {}".format(mejor_sol))
            vecindad = Generadora_de_vecinos.construir_vecindad(mejor_sol, mejor_eval, r, q, info)
            
            # Escogemos un vecino de la vecindad actual
            if vecindad != []:
                # Caso normal.
                vecino = Generadora_de_vecinos.decodificar_vecino(random.randint(0, len (vecindad)-1), vecindad, mejor_sol)
                
            else:
                
                raise(ValueError("ERROR : Esta mal en algo, EN ALGO (la vecindad del vecino {} es vacía.)".format(mejor_sol)) )
                
            # Evaluamos al vecino.
            eval_vecino, r_1, q_1,_,_,info_1 = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas, self.numero_de_trabajos, self.lista_de_vertices, vecino)
            
            
            
            # Comparamos la solucion actual vs la solución del vecino.
            if eval_vecino < mejor_eval:
                
                mejor_sol = vecino
                mejor_eval = eval_vecino         
 
        return mejor_sol,mejor_eval
        
            

    #Método donde aproximamos una mejor solución para el problema job-shop con el método de recocido simulado 
    def recocido_simulado(self,no_de_evaluaciones:int,temp_inicial = 10000,factor_de_enfriamiento =.95, sol_actual = None):
        
        # Inicializamos las variables temporales que vamos a utilizar.
        mejor_sol = None
        mejor_eval = None
        comparaciones_actuales =0
        if sol_actual is None:
            sol_actual = Solution_Management.generar_solucion(self.numero_de_maquinas,self.numero_de_trabajos,self.lista_de_vertices)
        mejor_sol = None
        eval_actual = None
        temperatura = temp_inicial
        vecino = None
        eval_vecino = None
        
        while  comparaciones_actuales < no_de_evaluaciones and temperatura > 1:
            # Evaluamos nuestra solución actual.
           
            eval_actual, r1, q1, t1, d1, info1 = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas, self.numero_de_trabajos, 
                                                                             self.lista_de_vertices, sol_actual)
            
            # Iteramos nuestro contador.
            comparaciones_actuales +=1
            #Calculamos la vecindad dada una solución actual.
            vecindad, m = Generadora_de_vecinos.construir_vecindad(sol_actual, eval_actual, r1, q1, info1)
            
            # Escogemos un vecino de la vecindad actual
            vecino = random.choice (vecindad)  # PENDIENTE
            
            eval_vecino, r2,q2,t2,d2,info2 = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas,self.numero_de_trabajos,
                                                                                   self.lista_de_vertices,vecino)
            # Iteramos nuestro contador.
            comparaciones_actuales +=1            

            # Si es mejor la reemplazamos.

            if mejor_eval is None or eval_actual < mejor_eval:
                
                mejor_eval = eval_actual
                mejor_sol = sol_actual
                
            else :
                
                # Si no generamos una probabilidad de mover nuestra solución actual en caso contrario no hacemos NADOTA :D
                if random.random() < math.exp(-(eval_vecino-mejor_eval) / temperatura):
                    sol_actual = vecino
                    eval_actual = eval_vecino
            
            # Actualizamos la temperatura
            temperatura *= factor_de_enfriamiento
        
        return mejor_sol,mejor_eval
    
    
    
    
    



    
    def busqueda_generacional(tamaño_generacion = 30, numero_de_evaluaciones= 15000, evaluaciones_recocido = 250 ):
        
        # Inicializamos la poblacion
        poblacion = [Solution_Management.generar_solucion(self.numero_de_maquinas,self.numero_de_trabajos,self.lista_de_vertices) for _ in range(tamaño_generacion)]
        
        evaluaciones_actuales = 0
        while (evaluaciones_actuales < numero_de_evaluaciones):
            # La mejoramos tantito con pocas iteraciones de recocido simulado        
            for individuo in poblacion:
                individuo, _ = self.recocido_simulado(evaluaciones_recocido, sol_actual = individuo)
                
            # Evaluaciones de recocido x numero de individuos = no de evaluaciones actuales (tal vez    )
            evaluaciones_actuales += numero_de_evaluaciones * evaluaciones_recocido 
            
            # Seleccionamos padres
            padre1, padre2 = Operador_Selector_de_Padres.random(poblacion=poblacion)
            
            # Cruzamos y mutamos
            hijo1, hijo2 =Operador_Cruza_de_Padres.cruza_por_cromosoma(padre1,padre2) # 4 evaluaciones 
            
            #Torneo (los cambios quedan en la memoria)
            Torneo.hijos_vs_poblacion(poblacion,hijo1=hijo1,hijo2=hijo2)
            
            evaluaciones_actuales += 4 #tal vez
            
            
        return poblacion
            
        
        
        
        '''
        [[1,2,3]   [[3,1,2
        [2,1,3]     [3,1,2]
        3,1,2]      [3,1,2]]
        
        '''