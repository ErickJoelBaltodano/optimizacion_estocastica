from Calculadora_makespan_VAde import *


class Torneo:
    #No retornamos nada porque los cambios son en la memoria
    
    @staticmethod
    def hijos_vs_poblacion (poblacion,hijo1, hijo2,numero_de_maquinas,numero_de_trabajos,lista_de_vertices):
        # Generar el primer número
        numero1 = random.randint(0, len(poblacion)-1)

        # Generar el segundo número diferente al primero
        while True:
            numero2 = random.randint(0, len(poblacion)-1)
            if numero2 != numero1:
                break
         
        contendiente1, r1, q1,  info1 = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, 
                                                                             lista_de_vertices, poblacion[numero1])
        
        contendiente2, r2, q2,  info2 = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, 
                                                                             lista_de_vertices, poblacion[hijo1])
        
       
        
        if (contendiente1 > contendiente2):
            self.poblacion[numero1]= hijo1
            
        contendiente1, r1, q1,  info1 = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, 
                                                                             lista_de_vertices, poblacion[numero2])
        
        contendiente2, r2, q2, info2 = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, 
                                                                             lista_de_vertices, poblacion[hijo2])
        
       
        
        if (contendiente1 > contendiente2):
            self.poblacion[numero2]= hijo2
            
        return 
        
            
        

