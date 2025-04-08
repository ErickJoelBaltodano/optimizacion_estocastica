from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Generadora_de_vecinos import *
from Busqueda_Por_Vecindades import *
from Job_Shop_Problem import *
import sys

# Validación de parámetros actualizada
if len(sys.argv) < 2 or len(sys.argv) > 3:
    raise ValueError("ERROR: Parámetros incorrectos. Uso: <documento> [iteraciones]")

# Lectura de parámetros
documento = sys.argv[1]
iteraciones = 100  # Valor por defecto

# Si se especifican iteraciones
if len(sys.argv) == 3:
    try:
        iteraciones = int(sys.argv[2])
    except ValueError:
        raise ValueError("El número de iteraciones debe ser un entero válido")

# Lectura de Ejemplar
documento_de_entrada = f"./Ejemplares/{documento}.txt"


# Lectura de datos
numero_de_maquinas, numero_de_trabajos, lista_de_vertices = Reader_and_Writer_VAde.read(documento_de_entrada)

jsp = Job_Shop_Problem(lista_de_vertices,numero_de_maquinas,numero_de_trabajos)

for x in jsp.vertices:
    print(x)
    

print ("Machs{} \n Jobs{}".format(numero_de_maquinas,numero_de_trabajos))


m,c =jsp.makespan()

print ("Camino Crítico {}\n Makespan {}".format(c,m))

print(jsp.makespan())
'''for x in jsp.solucion:
    print(x)

'''
jsp.generacional_con_recocido_simulado(100)

print (jsp.makespan())



'''for x in jsp.solucion:
    print(x)
'''