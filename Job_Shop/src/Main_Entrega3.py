from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Generadora_de_vecinos import *
from Busqueda_Por_Vecindades import *
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

print(f"Leyendo Documento: {documento_de_entrada}")
print("=" * 75)

# Lectura de datos
numero_de_maquinas, numero_de_trabajos, lista_de_vertices = Reader_and_Writer_VAde.read(documento_de_entrada)

print("Lectura Exitosa")
print("=" * 75)

# Representación de ejemplares
print(f"Representación del ejemplar {documento_de_entrada}")
for x in lista_de_vertices:
    print(x)
print("=" * 75)

# Configuración de la búsqueda
b = Busqueda_Por_Vecindades(numero_de_maquinas, numero_de_trabajos, lista_de_vertices)
print(f"Realizando Búsqueda Aleatoria con {iteraciones} iteraciones")

# Ejecución con el número de iteraciones especificado
sol, val= b.busqueda_generacional(iteraciones)

# Resultado final mejorado
resultado = f"""
============================================================================
 MEJOR SOLUCIÓN ENCONTRADA (después de {iteraciones} iteraciones):
 
{sol}

 MAKESPAN: {val}
============================================================================"""
print(resultado)

