from Function import * 
from Transformador_Funcion import *
from Metodo_Numerico import *
from Random_Solution_Generator import *


dimension = 8
limites = [0 if x % 2 == 0 else 100 for x in range(dimension*2)]

valores =Random_Solution_Generator.random_real_list(dimension,limites)

funcion = Transformador_Funcion(Function.griewank)

f =funcion.inversa(valores)
h =Metodo_Numerico.hessiana(f,valores)

print("Solucion random: {}\n R ({})={} \n Hessiana ({})=\n {} ".format(valores,valores,f,valores,h))