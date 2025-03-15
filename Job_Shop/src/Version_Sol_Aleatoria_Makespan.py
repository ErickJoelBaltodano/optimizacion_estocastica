from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Solution_Generator_VAde import *
from Calculadora_makespan_VAde import *

numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read("./Ejemplares/prueba3.txt")

numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read(ejemplar)

#print(lista_de_vertices)

# Prueba de fuego:
sol = Solution_Management.generar_solucion(numero_de_maquinas, numero_de_trabajos, lista_de_vertices)

print("\nLa solución generada es:", sol)

#print("\nEran ",len(sol), " máquinas.")

# Prueba de fuego 2:

makespan, r, q, info = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, sol)

#print("\nEl makespan: ", makespan)