from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Solution_Generator_VAde import *
from Calculadora_makespan_VAde import *
from Generadora_de_vecinos import *

ejemplar = input("Escribe el nombre del ejemplar (no olvides el .txt):\t")

numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read(ejemplar)

#print(lista_de_vertices)

# Prueba de fuego:
solucion = Solution_Generator.generador_solucion(numero_de_maquinas, numero_de_trabajos, lista_de_vertices)

print("\nLa solución generada es:", solucion)

#print("\nEran ",len(sol), " máquinas.")

# Prueba de fuego 2:

makespan, r, q, t, d, info = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion)

#print("\nEl makespan: ", makespan)



# Ahora la generadora de vecinos:

# Construir nueva_info
nueva_info = Generadora_de_vecinos.construir_nueva_info(makespan, r, q, info)

# Imprimir detalles de las operaciones críticas
Generadora_de_vecinos.imprimir_nueva_info(nueva_info, makespan)

vecindad, movimientos = Generadora_de_vecinos.construir_vecindad(solucion, makespan, r, q, info)
print(f"\n Los vecinos son: {vecindad}")

