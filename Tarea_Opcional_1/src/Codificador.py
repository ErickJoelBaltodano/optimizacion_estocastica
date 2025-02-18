from typing import List

class Codificador:

    #Método donde recibimos como parámetro un entero  y lo regresaremos a una regresentación en bits.
    @staticmethod
    def codifica_natural(entero:int, numero_de_bits:int)->List[int]:
        lista = []
        x = entero

        for _ in range(numero_de_bits):
            y = x%2
            lista.append(y)
            x =int(x/2)
        lista.reverse()
        return lista


    #Método donde recibimos como parámetro una lista de bits y regresamos el número entero que representa.
    @staticmethod
    def decodifica_natural(binario:List[int])->int:
        numero = 2 ** (len(binario)-1)
        resultado = 0 
        for x in binario:
            if x == 1:
                resultado += numero
                numero = numero /2
            else :
                numero = numero /2

        return resultado

    #Método donde recibimos un real, límites superior e inferior, y regresamos su representación en binario.
    @staticmethod
    def codifica_real(real:float,limite_inferior:float, limite_superior:float ,numero_de_bits:int)->List[int]:
        numero_de_marcadores = 2 ** numero_de_bits
        distancia_ab = limite_superior - limite_inferior
        delta = distancia_ab / numero_de_marcadores
        distancia_areal = real - limite_inferior
        return Codificador.codifica_natural ((int (distancia_areal / delta)), numero_de_bits)



    #Método donde recibimos una representación binaria del número y los límites inferior y superior, y regresamos su el valor representado (con un cierto margen de error).
    @staticmethod
    def decodifica_real(binario:List[int],limite_inferior:float, limite_superior:float)->float:
        numero = Codificador.decodifica_natural(binario)
        distancia_ab = limite_superior - limite_inferior
        delta = distancia_ab / (2 **len(binario)-1)
        distancia_areal = numero * delta
        return limite_inferior + distancia_areal
        

    #Método donde recibimos una lista de reales dentro de un rango de números y los transformamos todos a binario.
    @staticmethod
    def codifica_lista(reales: List[float],limites:List[float],numero_de_bits:int)->List[int]:
        lista = []
        x = 0
        y = 1

        for real in reales:
            limite_inferior = limites[x]
            limite_superior = limites[y]
            binario =Codificador.codifica_real(real, limite_inferior,limite_superior,numero_de_bits)
            lista =lista + binario
            x +=2
            y +=2
            
        return lista




    #Transformamos la lista de binarios a lista de listas de binarios y luego iteramos sobre esta y la decodificamos.
    @staticmethod
    def decodifica_lista (lista:List[int],numero_de_bits:int,limites:List[int])->List[float]:
        lista_auxiliar = []
        binario = []
        lista.reverse()

        #Transformamos la lista de binarios a lista de listas de binarios (según su nḿmero de bits).
        while ((len (lista) != 0)):
            for _ in range(numero_de_bits):
                binario.append(lista.pop())
            lista_auxiliar.append(binario)
            binario = []
        
        #Transformamos cada elemento a reales según los límites dados.
        resultado = []
        x = 0
        y = 1
        for elemento in lista_auxiliar:
            limite_inferior = limites[x]
            limite_superior = limites[y]
            resultado.append (Codificador.decodifica_real(elemento,limite_inferior,limite_superior))
            x +=2
            y +=2   
        return resultado

        