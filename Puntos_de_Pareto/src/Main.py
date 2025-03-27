from Individuo import *
from Transformacion import *
from Random_Solution_Generator import *


f1 = Transformacion(Funcion.rastrigin)

f2 = Transformacion(Funcion.ackley)

dimension = 5
limites = [0 if x % 2 == 0 else 100 for x in range(dimension*2)]

funciones =[f1.inversa,f2.none]

valores1 = Random_Solution_Generator.random_real_list(5,limites)
valores2 = Random_Solution_Generator.random_real_list(5,limites)

valores= [valores1,valores2]

print(valores)

i =Individuo(funciones,valores)

print(i.get())

print (i.get(1))
print (i.get(0))

