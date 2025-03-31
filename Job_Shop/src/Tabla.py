from Solution_Generator_VAde import *
from Reader_and_Writer_VAde import *
from Vertice_VAde import *
from Generadora_de_vecinos import *
from Busqueda_Por_Vecindades import *
import sys
import os
import traceback
from tabulate import tabulate

# Validación de parámetros
if len(sys.argv) > 2:
    raise ValueError("ERROR: Parámetros incorrectos. Uso: [iteraciones]")

iteraciones = 100  # Valor por defecto

# Si se especifican iteraciones
if len(sys.argv) == 2:
    try:
        iteraciones = int(sys.argv[1])
        if iteraciones <= 0:
            raise ValueError("El número de iteraciones debe ser positivo")
    except ValueError:
        raise ValueError("El número de iteraciones debe ser un entero válido")

# Procesar todos los archivos de la carpeta Ejemplares
ejemplares_path = "./Ejemplares/"
if not os.path.exists(ejemplares_path):
    raise FileNotFoundError(f"La carpeta {ejemplares_path} no existe")

# Obtener lista de archivos .txt ordenados
archivos = sorted([f for f in os.listdir(ejemplares_path) if f.endswith('.txt')])

if not archivos:
    raise ValueError("No se ha encontrado ningún archivo")

# Estructuras para guardar resultados
resultados = {
    'ejemplares': [],
    'maquinas': [],
    'trabajos': [],
    'vertices': [],
    'mejor_makespan': [],
    'eval_promedio': [],
    'soluciones': [],
    'busqueda': []
}

# Contadores para estadísticas
archivos_procesados = 0
archivos_con_error = 0

print("\n" + "=" * 75)
print(f"INICIANDO PROCESAMIENTO DE {len(archivos)} ARCHIVOS CON {iteraciones} ITERACIONES CADA UNO")
print("=" * 75)

# Procesar cada archivo
for archivo in archivos:
    documento_de_entrada = os.path.join(ejemplares_path, archivo)
    
    print("\n" + "=" * 75)
    print(f"PROCESANDO ARCHIVO: {archivo}")
    print("=" * 75)
    
    try:
        # Lectura de datos
        print(f"\nLeyendo Documento: {documento_de_entrada}")
        numero_de_maquinas, numero_de_trabajos, lista_de_vertices = Reader_and_Writer_VAde.read(documento_de_entrada)
        print("Lectura Exitosa")
        print(f"Máquinas: {numero_de_maquinas}, Trabajos: {numero_de_trabajos}, Vértices: {len(lista_de_vertices)}")
        print("-" * 50)
        
        # Configuración de la búsqueda
        b = Busqueda_Por_Vecindades(numero_de_maquinas, numero_de_trabajos, lista_de_vertices)
        print(f"\nRealizando Búsqueda Aleatoria con {iteraciones} iteraciones")
        
        # Ejecución con el número de iteraciones especificado
        sol, val, lista_valores, lista_eval = b.random(iteraciones)
        promedio_eval = sum(lista_valores)/len(lista_eval)
        
        # Guardar resultados
        resultados['ejemplares'].append(archivo)
        resultados['maquinas'].append(numero_de_maquinas)
        resultados['trabajos'].append(numero_de_trabajos)
        resultados['vertices'].append(len(lista_de_vertices))
        resultados['mejor_makespan'].append(val)
        resultados['eval_promedio'].append(round(promedio_eval, 2))
        resultados['soluciones'].append(sol)
        resultados['busqueda'].append("Aleatoria")
        
        # Actualizar contadores
        archivos_procesados += 1
        
        # Resultado parcial
        resultado = f"""
============================================================================
 ARCHIVO: {archivo}
 
 MEJOR SOLUCIÓN ENCONTRADA (después de {iteraciones} iteraciones):
 
{sol}

 MAKESPAN: {val}
 EVALUACIÓN PROMEDIO: {promedio_eval:.2f}
============================================================================"""
        print(resultado)
        
    except Exception as e:
        archivos_con_error += 1
        print(f"\nERROR al procesar {archivo}:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje: {str(e)}")
        print("\nTraceback (últimos llamados):")
        traceback.print_exc(limit=1)
        print("-" * 50)
        continue

# Resumen final
print("\n" + "=" * 75)
print("RESUMEN FINAL")
print("=" * 75)
print(f"Archivos procesados correctamente: {archivos_procesados}")
print(f"Archivos con errores: {archivos_con_error}")

# Mostrar tabla resumen
if archivos_procesados > 0:
    # Preparar datos para la tabla
    tabla_resumen = []
    for i in range(len(resultados['ejemplares'])):
        fila = [
            resultados['ejemplares'][i],
            resultados['maquinas'][i],
            resultados['trabajos'][i],
            resultados['vertices'][i],
            resultados['mejor_makespan'][i],
            resultados['eval_promedio'][i],
            resultados['busqueda'][i]
        ]
        tabla_resumen.append(fila)
    
    # Encabezados de la tabla
    headers = [
        "Ejemplar", 
        "Máquinas", 
        "Trabajos", 
        "Vértices", 
        "Mejor Makespan", 
        "Eval. Promedio", 
        "Tipo Búsqueda"
    ]
    
    print("\nRESULTADOS:")
    print(tabulate(tabla_resumen, headers=headers, tablefmt="grid"))
  