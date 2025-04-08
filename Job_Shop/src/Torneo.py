from Calculadora_makespan_VAde import *


class Torneo:
    #No retornamos nada porque los cambios son en la memoria
    @staticmethod
    def hijos_vs_poblacion (poblacion,makespans,hijo1,hijo2,makespan_hijo1,makespan_hijo2):
        # Generar el primer número
        numero1 = random.randint(0, len(poblacion)-1)

        # Generar el segundo número diferente al primero
        while True:
            numero2 = random.randint(0, len(poblacion)-1)
            if numero2 != numero1:
                break
            
        '''Torneo 1'''
        if makespan_hijo1 < makespans[numero1]:
            poblacion[numero1]= hijo1
            makespans[numero1]= makespan_hijo1
        
        '''Torneo 2'''
        if makespan_hijo2 < makespans[numero2]:
            poblacion[numero2]= hijo2
            makespans[numero2]= makespan_hijo2
        
