

class Solution_Generator:
    
    
    #Clase donde generamos soluciones que son válidas para nuestra implementación del problema del Job Shop.
    @staticmethod
    def random (numero_de_maquinas,numero_de_trabajos):
        
        resultado = []
        
        #Generamos una lista de trabajos planificables
        lista_de_espera = []
        x = 1
        for _ in range (numero_de_maquinas):
            lista_de_espera.append(x)
            x += numero_de_trabajos
            
        return resultado
        
            
            
        
        