from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Generadora_de_vecinos import *
from Busqueda_Por_Vecindades import *
import sys

if (len(sys.argv) != 2):
    raise ValueError("ERROR: Número de parámetros INCORRECTO >:V")


# Lectura de Ejemplar
documento_de_entrada = "./Ejemplares/" + sys.argv[1]+".txt"

print ("Leyendo Documento : {}".format(documento_de_entrada))
print ("==========================================================================")


numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read(documento_de_entrada)

print ("Lectura Exitosa ")
print ("==========================================================================")



#Representacion de ejemplares
print ("Representación del ejemplar {}".format(documento_de_entrada))
for x in lista_de_vertices:
    print (x)
    
print ("==========================================================================")


b = Busqueda_Por_Vecindades(numero_de_maquinas,numero_de_trabajos,lista_de_vertices)
print ("Realizando Busqueda Aleatoria")

sol, val =b.random  (100)
print("============================================================================\n MEJOR SOLUCION : {} \n MAKESPAN : {}\n============================================================================".format(sol,val))