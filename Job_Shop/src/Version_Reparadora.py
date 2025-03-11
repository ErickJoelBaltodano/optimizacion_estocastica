from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Solution_Generator_VAde import *
from Calculadora_makespan_VAde import *
from Generadora_de_vecinos import *
from Reparadora_de_sols import *
import random

ejemplar = input("Escribe el nombre del ejemplar (no olvides el .txt):\t")

numero_de_maquinas, numero_de_trabajos, lista_de_vertices =Reader_and_Writer_VAde.read(ejemplar)

#print(lista_de_vertices)

# Prueba de fuego:
solucion = Solution_Generator.generador_solucion(numero_de_maquinas, numero_de_trabajos, lista_de_vertices)

print("\nLa solución generada es:", solucion)

#print("\nEran ",len(sol), " máquinas.")

# Prueba de fuego 2:

makespan, r, q, t, d, info = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion)

# Vamos a reordenar la primera máquina para que esté al azar y así probar la reparadora.
solucion_desordenada = [random.sample(maquina, len(maquina)) for maquina in solucion]

print("\nLa solución ojalá no factible es: ", solucion_desordenada)

solucion_reparada = Reparadora.reparacion(solucion_desordenada, numero_de_maquinas, numero_de_trabajos, lista_de_vertices)