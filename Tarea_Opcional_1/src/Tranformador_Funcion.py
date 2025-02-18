from Function import *

class Transformador_Funcion:
    #Definimos dentro de nuestros parametros que funcion queremos transformar.
    def __init__(self,funcion):
        self.funcion = funcion

    #Transformación para buscar valores por minimización
    def null(self,dimension:int,valores:list[float]):
        return self.funcion(dimension,valores)

    #Transformamos la funcion a la inversa de la función
    def inversa(self,dimension:int,valores:list[float]):
        return 1/self.funcion(dimension,valores)

    #Transformamos la funcion a la negativa de la función
    def negative(self,dimension:int,valores:list[float]):
        return -self.funcion(dimension,valores)        