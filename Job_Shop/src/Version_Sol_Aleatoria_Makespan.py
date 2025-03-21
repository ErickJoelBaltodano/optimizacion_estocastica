from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Solution_Generator_VAde import *
from Calculadora_makespan_VAde import *
import sys 

#ejemplar = input("Escribe el nombre del ejemplar (no olvides el .txt):\t")
ejemplar = sys.argv[1] # Para evitar preguntarle al usuario el ejemplar.
random.seed(10)

numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read(ejemplar)

#print(lista_de_vertices)

# Prueba de fuego:
sol = Solution_Generator.generador_solucion(numero_de_maquinas, numero_de_trabajos, lista_de_vertices)

print("\nLa solución generada es:", sol)

#print("\nEran ",len(sol), " máquinas.")

# Prueba de fuego 2:

makespan, r, q, t, d, info = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, sol)

#print("\nEl makespan: ", makespan)