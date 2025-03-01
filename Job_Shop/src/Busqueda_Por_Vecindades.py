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
            if vecindad != []:
                # Caso normal.
                vecino = random.choice (vecindad)
            else:
                
                # Caso donde la solucion actual no tiene vecinos.
                temp =Solution_Management.generar_solucion(self.numero_de_maquinas,self.numero_de_trabajos,self.lista_de_vertices)
                eval_temp ,r,q,t,d,info = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas,self.numero_de_trabajos,self.lista_de_vertices,temp)
                vecindad, m = Generadora_de_vecinos.construir_vecindad(temp,eval_temp,r,q,info)
                
            # Evaluamos al vecino.
            eval_vecino, r2,q2,t2,d2,info2 = Evaluador_Makespan.calculadora_makespan(self.numero_de_maquinas,self.numero_de_trabajos,
                                                                                   self.lista_de_vertices,vecino)
            
            
            
            # Comparamos la solucion actual vs la solución del vecino.
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
    def recocido_simulado(self,no_de_evaluaciones:int,temp_inicial = 10000,factor_de_enfriamiento =.95):
        
        # Inicializamos las variables temporales que vamos a utilizar.
        mejor_sol = None
        mejor_eval = None
        comparaciones_actuales =0
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
            vecino = random.choice (vecindad)
            
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
    



    
    def busqueda_generacional(tamaño_generacion, numero_de_evaluaciones,operador_selector_de_padres,operador_mutacion,operador_cruza):
        pass
        