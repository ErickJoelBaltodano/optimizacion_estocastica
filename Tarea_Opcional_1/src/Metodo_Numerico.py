from random import *
from Random_Solution_Generator import *


class Metodo_Numerico:
    
    @staticmethod
    def busqueda_en_linea(iteraciones,funcion,valores):
        
        dimension = int(len(valores)/2)
        
        #Generamos una primera solución inicial dentro del espacio de búsqueda.
        
        sol_inicial = Random_Solution_Generator.random_real_list(20,valores)
        f_x = funcion(dimension,sol_inicial)
        """sol_i = None
        
        for i in range(iteraciones):
            """"""
            sol_i = i
            """
        
        #Regresamos el valor obtenido
        return sol_inicial,f_x
        
        