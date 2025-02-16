
import random
from Vertice import *
class Solution_Generator:
    
    
    @staticmethod
    def random_permutation(numero_de_maquinas,numero_de_trabajos):
        resultado = []
        
        
        #Generamos una lista de trabajos planificables
        lista_de_espera = []
        x = 0
        for _ in range (numero_de_maquinas):
            lista_de_espera.append(x)
            x += numero_de_trabajos
        
            
        while (len(lista_de_espera) != 0):
            print (lista_de_espera)
            
            # Generamos un Indice aleatorio en el cual escogemos uno de los trabajos planificables.
            indice_aleatorio =random.randint(0,len(lista_de_espera)-1)
            
            #Planificamos el trabajo
            resultado.append (lista_de_espera[indice_aleatorio])
            
            #Agregamos es sucesor del trabajo en caso de ser necesario.
            if ((lista_de_espera[indice_aleatorio]+1)% numero_de_trabajos != 0):
                lista_de_espera.append(lista_de_espera[indice_aleatorio]+1)
            
            # Eliminamos el trabajo de la lista de espera.
            del lista_de_espera[indice_aleatorio]
            
            
        return resultado
    
    def random_chromosome(numero_de_maquinas:int,numero_de_trabajos:int, lista_de_vertices: [Vertice]):
        lista = Solution_Generator.random_permutation(numero_de_maquinas,numero_de_trabajos)
        resultado = [lista_de_vertices[x].get_maquina()for x in lista]
        return resultado
    
    def random_solution(numero_de_maquinas, numero_de_trabajos, lista_de_vertices):
        lista = Solution_Generator.random_permutation(numero_de_maquinas,numero_de_trabajos)
        resultado = [ [] for _ in range(numero_de_maquinas)]
        for l in lista:
            m = lista_de_vertices[l].get_maquina() -1
            j = lista_de_vertices[l].get_trabajo() -1
            resultado [m].append(j)
            
        return resultado
            
            
            
            
            

            
        
            
            
        
        