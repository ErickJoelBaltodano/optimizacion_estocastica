from Solution_Management import *
from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Generadora_de_vecinos import *
from Busqueda_Por_Vecindades import *
from Reparador_de_Soluciones import *
from Operador_Cruza_de_Padres import * 
from Job_Shop_Problem import *
from Reparador_de_Soluciones import *
import random
import sys

'''

PROBANDO LA FUNCION NEXT MACH DADA UNA SOLUCION

'''


documento_de_entrada = "./Ejemplares/" + "orb06"+".txt"


    
print (documento_de_entrada)
numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read(documento_de_entrada)


sol1 =Solution_Management.random_solution(numero_de_maquinas,numero_de_trabajos,lista_de_vertices)

sol2 = Solution_Management.random_solution(numero_de_maquinas,numero_de_trabajos,lista_de_vertices)

h1,h2 = Operador_Cruza_de_Padres.cruza_por_cromosoma(sol1,sol2)
print ("_________________________________________")
for x in sol1:
    print(x)
print ("_________________________________________")


jsp = Job_Shop_Problem(lista_de_vertices,numero_de_maquinas,numero_de_trabajos,solucion=h1)


for x in jsp.solucion:
    print("-")
    print (x)
    

numero_aleatorio = random.randint(1, 100)
print (numero_aleatorio)

print("next mach {}".format(jsp.get_next_mach(numero_aleatorio)))



for x in h1:
    for y in x:
        
        print ("next_mach({})= {}".format(y,jsp.get_next_mach(y)))
        