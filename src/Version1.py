from Reader_and_Writer import *
from Vertice import *
from Solution_Generator import *

numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer.read("prueba3.txt")

print (lista_de_vertices)


l =Solution_Generator.random_permutation(numero_de_maquinas,numero_de_trabajos,lista_de_vertices)


print (l)

print (len(l))

