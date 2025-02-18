from typing import List
from Codificador import *
import random

class Random_Solution_Generator:

    #Método estático mediante el cual generamos soluciones aleatorias binarias de una determinada longitud.(Al ser un método estático no hay que crear instancias de RandomSolutionGenerator solo hay que nombrar la clase).
    @staticmethod
    def Binary_List(length):

        #random randint crea enteros entre los parámetros recibidos, y los agregamos en una lista.
        return [random.randint(0, 1) for _ in range(length)]



    #Método donde usamos nuestro generador de binarios aleatorios y lo codificamos dado un rango para generar un número real
    @staticmethod
    def random_real_generate(length,limite_inferior:int,limite_superior:int):
        r = Random_Solution_Generator.Binary_List(length)
        c =Codificador.decodifica_real(r,limite_inferior,limite_superior)
        return c

    
    #Método donde generamos una lista de reales.
    @staticmethod
    def random_real_list(lenght,limites):
        inferior= 0
        superior= 1
        lista_final = []
        dimension = int (len(limites)/2)
        for _ in range(dimension):
            
            lista_final.append(Random_Solution_Generator.random_real_generate(lenght,limites[inferior],limites[superior]))
            inferior += 2
            superior += 2
        return lista_final
    
    @staticmethod
    def n_puntos(n,longitud_total):
       
        

        lista = []
        for _ in range (n):
            lista.append(True)
        for _ in range (longitud_total-n):
            lista.append(False)
        
        
        # Mezclar la lista para distribuir los True de forma aleatoria
        random.shuffle(lista)
        
        return lista

   