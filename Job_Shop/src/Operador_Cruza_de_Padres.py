import random

class Operador_Cruza_de_Padres:
    
    @staticmethod
    def cruza_por_cromosoma(solucion1,solucion2):
        maquinas = len(solucion1)
        
        #Generamos una lista random de booleanos.
        gen = [random.choice([True,False])    for _ in range(maquinas)]
        
        hijo1 = []
        hijo2 = []
        indice = 0
        
        while indice < maquinas:
            
            if gen[indice]:
                
                hijo1.append(solucion1[indice])
                hijo2.append(solucion2[indice])
                
            else:
                hijo1.append(solucion2[indice])
                hijo2.append(solucion1[indice])
            
            
            indice += 1
            
            
        return hijo1,hijo2
        
        