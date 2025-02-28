from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Generadora_de_vecinos import *
import random
import math
import sys
class Busqueda_Por_Vecindades:
    
    # Método Constructor de la Clase Busqueda por Vecindades
    def __init__(self,numero_de_maquinas,numero_de_trabajos,lista_de_vertices):
        self.numero_de_maquinas = numero_de_maquinas
        self.numero_de_trabajos = numero_de_trabajos
        self.lista_de_vertices = lista_de_vertices
    
    def random( self,no_de_iteraciones):
        #Generamos una primera solución inicial.
        mejor_sol = Solution_Management.generar_solucion(self.numero_de_maquinas,self.numero_de_trabajos,self.lista_de_vertices)
        mejor_eval = None
        
        
        for _ in range(no_de_iteraciones):
            mejor_eval, r1, q1, t1, d1, info1 = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas, self.numero_de_trabajos, 
                                                                             self.lista_de_vertices, mejor_sol)
            
            vecindad, m = Generadora_de_vecinos.construir_vecindad(mejor_sol, mejor_eval, r1, q1, info1)
            
            # Escogemos un vecino de la vecindad actual
            vecino = random.choice (vecindad)
            eval_vecino, r2,q2,t2,d2,info2 = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas,self.numero_de_trabajos,
                                                                                   self.lista_de_vertices,vecino)
            
            
            if eval_vecino < mejor_eval:
                
                mejor_sol = vecino
                mejor_eval = eval_vecino         
            
            
            
            
            
            
        return mejor_sol,mejor_eval
        
            

    def tabu (no_de_comparaciones:int,documento_de_entrada:str,documento_de_salida:str):
        mejor_sol = None
        mejor_eval = None
        #Generamos una solucion inicial.
        #Exploramos la vecindad.
        #Baneamos los elementos ya explorados.
        
        #Regresamos el mejor resultado encontrado.
        
        '''Mejor no, está muy dificil :´v '''
        
        return mejor_sol,mejor_eval

    #Método donde aproximamos una mejor solución para el problema job-shop con el método de recocido simulado 
    def recocido_simulado(self,no_de_evaluaciones:int,temp_inicial = 1000,factor_de_enfriamiento =.95):
        #Generamos una primera solución inicial.
        mejor_sol = Solution_Management.generar_solucion(self.numero_de_maquinas,self.numero_de_trabajos,self.lista_de_vertices)
        mejor_eval = None
        comparaciones_actuales =0
        sol_actual = mejor_sol
        eval_actual = None
        temperatura = temp_inicial
        vecino = None
        eval_vecino = None
        
        while temperatura > 0 or comparaciones_actuales < no_de_evaluaciones:
            #Calculamos el makespan, las q, las r, etc.
            makespan1, r1, q1, t1, d1, info1 = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas, self.numero_de_trabajos, 
                                                                             self.lista_de_vertices, mejor_sol)
            mejor_eval = makespan1
            eval_actual = makespan1
            #Calculamos la vecindad dada una solución actual.
            vecindad, m = Generadora_de_vecinos.construir_vecindad(mejor_sol, makespan1, r1, q1, info1)
            
            # Escogemos un vecino de la vecindad actual
            vecino = random.choice (vecindad)
            
            makespan2, r2,q2,t2,d2,info2 = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas,self.numero_de_trabajos,
                                                                                   self.lista_de_vertices,vecino)
            eval_vecino = makespan2
            
            delta_E = eval_vecino - mejor_eval
            
            if delta_E < 0:
                mejor_eval = eval_vecino
                mejor_sol = vecino
                sol_actual = mejor_sol
                eval_actual = mejor_eval
                
                print ("-------------------------------------------------------------")
                print (eval_actual)
                print (sol_actual)
                        
                print ("-------------------------------------------------------------")
                
            else :
                if random.random() < math.exp(-delta_E / temperatura):
                    
                    sol_actual = vecino
                    eval_actual = eval_vecino
            
            temperatura *= factor_de_enfriamiento
                    
       
        return mejor_sol,mejor_eval



    
    def busqueda_generacional(tamaño_generacion, numero_de_evaluaciones,operador_selector_de_padres,operador_mutacion,operador_cruza):
        pass
        