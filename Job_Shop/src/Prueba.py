from Solution_Management import *
from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Generadora_de_vecinos import *
from Busqueda_Por_Vecindades import *
from Reparador_de_Soluciones import *
from Operador_Cruza_de_Padres import * 
import sys



documento_de_entrada = "./Ejemplares/" + "orb06"+".txt"


    
print (documento_de_entrada)
numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read(documento_de_entrada)


sol1 =Solution_Management.generar_solucion(numero_de_maquinas,numero_de_trabajos,lista_de_vertices)

sol2 = Solution_Management.generar_solucion(numero_de_maquinas,numero_de_trabajos,lista_de_vertices)

print ("_________________________________________")
for x in sol1:
    print(x)
    
print ("_________________________________________")
for x in sol2:
    print(x)

h1,h2 = Operador_Cruza_de_Padres.cruza_por_cromosoma(sol1,sol2)

print ("_________________________________________")
for x in h1:
    print(x)
    
print ("\n")
Reparador_de_Soluciones.reparar(h1,lista_de_vertices,info=True)