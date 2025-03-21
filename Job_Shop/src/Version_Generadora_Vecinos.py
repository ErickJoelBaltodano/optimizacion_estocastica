from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Solution_Generator_VAde import *
from Calculadora_makespan_VAde import *
from Generadora_de_vecinos import *
import random
import sys 

#ejemplar = input("Escribe el nombre del ejemplar (no olvides el .txt):\t")
ejemplar = sys.argv[1] # Para evitar preguntarle al usuario el ejemplar.
random.seed(10)

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

'''# Imprimir detalles de las operaciones críticas
Generadora_de_vecinos.imprimir_nueva_info(nueva_info, makespan)'''

vecindad_de_movimientos = Generadora_de_vecinos.construir_vecindad(solucion, makespan, r, q, info)
#print(f"\n Los vecinos son: {vecindad_de_movimientos}")


idx_vecino = random.randint(0, len(vecindad_de_movimientos)-1) # El índice del vecino elegido.
solucion_vecina = Generadora_de_vecinos.decodificar_vecino(idx_vecino, vecindad_de_movimientos, solucion)
makespan_vecino = Generadora_de_vecinos.evaluar_vecino(solucion_vecina, numero_de_maquinas, numero_de_trabajos, lista_de_vertices)
