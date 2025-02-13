
import random
class Solution_Generator:
    
    
    #Clase donde generamos soluciones que son válidas para nuestra implementación del problema del Job Shop.
    @staticmethod
    def random (numero_de_maquinas,numero_de_trabajos,lista_de_vertices):
        
        resultado = []
        
        for _ in range (numero_de_maquinas):
            resultado.append ([])
        
        
        #Generamos una lista de trabajos planificables
        lista_de_espera = []
        x = 1
        for _ in range (numero_de_maquinas):
            lista_de_espera.append(x)
            x += numero_de_trabajos
                  
        
        for i in range(numero_de_maquinas):"""Pendiente"""
            # Generamos un Indice aleatorio en el cual escogemos uno de los trabajos planificables.
            indice_aleatorio =random.randint(0,len(lista_de_espera)-1)
            
            
            # Agregamos el planificable escogido creo
            resultado[lista_de_vertices[indice_aleatorio].get_maquina()].append(lista_de_vertices[indice_aleatorio].get_trabajo())
            
            lista_de_espera.pop(indice_aleatorio-1)
            if (lista_de_vertices[indice_aleatorio].get_maquina()):
                lista_de_espera.push(lista_de_vertices[indice_aleatorio].get_id()) # +1-1
            
            
        return resultado
        
            
            
        
        