from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Solution_Generator_VAde import *

numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read("prueba3.txt")

print(lista_de_vertices)

# Prueba de fuego:
sol = Solution_Generator.generador_solucion(numero_de_maquinas, numero_de_trabajos, lista_de_vertices)

print("\nLa solución generada es:", sol)

print("\nEran ",len(sol), " máquinas.")