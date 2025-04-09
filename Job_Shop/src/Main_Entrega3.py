from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Generadora_de_vecinos import *
from Busqueda_Por_Vecindades import *
from Job_Shop_Problem import *
import sys

# Validación de parámetros actualizada
if len(sys.argv) < 2 or len(sys.argv) > 3:
    raise ValueError("ERROR: Parámetros incorrectos. Uso: <documento> [evaluaciones]")

# Lectura de parámetros
documento = sys.argv[1]
iteraciones = 100  # Valor por defecto

# Si se especifican iteraciones
if len(sys.argv) == 3:
    try:
        iteraciones = int(sys.argv[2])
    except ValueError:
        raise ValueError("El número de evaluaciones debe ser un entero válido")

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


# Configuración de busqueda
jsp = Job_Shop_Problem(lista_de_vertices,numero_de_maquinas,numero_de_trabajos)
print(f"Realizando Búsqueda con Algoritmo Memético con {iteraciones} iteraciones")

# Realizando busqueda por recocido simulado
sol,val,p=jsp.generacional_con_recocido_simulado(iteraciones)


# Resultado final mejorado
resultado = f"""
============================================================================
 MEJOR SOLUCIÓN ENCONTRADA (después de {iteraciones} iteraciones):
 
{sol}

 MAKESPAN: {val}
============================================================================"""
print(resultado)
print(val)

print (p)
