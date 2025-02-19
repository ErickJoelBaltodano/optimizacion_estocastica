from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
import sys


def tabu (no_de_comparaciones:int,documento_de_entrada:str,documento_de_salida:str):
    mejor_sol = None
    mejor_eval = None
    #Generamos una solucion inicial.
    #Exploramos la vecindad.
    #Baneamos los elementos ya explorados.
    #Regresamos el mejor resultado encontrado.
    
    return mejor_sol,mejor_eval


def recocido_simulado(no_de_comparaciones:int):
    '''En caso de cambiar de idea.'''
    pass


if (len(sys.argv) != 2):
    raise ValueError("ERROR: Número de parámetros INCORRECTO >:V")

documento_de_entrada = "./Ejemplares/" + sys.argv[1]+".txt"


    
print (documento_de_entrada)
numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read(documento_de_entrada)

print(lista_de_vertices)

# Prueba de fuego:
sol = Solution_Management.generar_solucion(numero_de_maquinas, numero_de_trabajos, lista_de_vertices)

print("\nLa solución generada es:", sol)

print("\nEran ",len(sol), " máquinas.")

# Prueba de fuego 2:

makespan, r, q, orden_global, info = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, 
                                                                             lista_de_vertices, sol)

print("\nEl makespan: ", makespan)