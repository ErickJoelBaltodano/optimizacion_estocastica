from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Generadora_de_vecinos import *
from Busqueda_Por_Vecindades import *
import sys

if (len(sys.argv) != 2):
    raise ValueError("ERROR: Número de parámetros INCORRECTO >:V")

documento_de_entrada = "./Ejemplares/" + sys.argv[1]+".txt"


    
print (documento_de_entrada)
numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read(documento_de_entrada)

print(lista_de_vertices)

b = Busqueda_Por_Vecindades(numero_de_maquinas,numero_de_trabajos,lista_de_vertices)

b.recocido_simulado(10)