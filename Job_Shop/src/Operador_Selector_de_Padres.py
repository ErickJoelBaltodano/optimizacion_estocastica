import random
class Operador_Selector_de_Padres:
    
    @staticmethod
    def random(poblacion):
        # Generar el primer número
        numero1 = random.randint(0, len(poblacion)-1)

        # Generar el segundo número diferente al primero
        while True:
            numero2 = random.randint(0, len(poblacion)-1)
            if numero2 != numero1:
                break
            
        return numero1,numero2