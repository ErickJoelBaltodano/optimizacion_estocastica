import numpy as np
import matplotlib.pyplot as plt
from individuo import *
from rwga import *
from frente_de_pareto_cuadratico import *
import os

def dtlz1(x: list, m: int = 3) -> list:
    """Función benchmark DTLZ1 para pruebas"""
    k = len(x) - m + 1
    g = 100 * (k + sum((xi - 0.5)**2 - np.cos(20 * np.pi * (xi - 0.5)) for xi in x[-k:]))
    objectives = [0.5 * (1 + g) * np.prod(x[:m-1])]
    for i in range(1, m-1):
        objectives.append(0.5 * (1 + g) * np.prod(x[:m-i-1]) * (1 - x[m-i-1]))
    objectives.append(0.5 * (1 - x[0]) * (1 + g))
    return objectives

def dtlz3(x: list, m: int = 3) -> list:
    """Función benchmark DTLZ3"""
    k = len(x) - m + 1
    g = 10 * k + sum((xi - 0.5)**2 - np.cos(20 * np.pi * (xi - 0.5)) for xi in x[-k:])
    
    objectives = []
    for i in range(m):
        f = 0.5 * (1 + g)
        for j in range(m - i - 1):
            f *= x[j]
        if i > 0:
            f *= (1 - x[m - i - 1])
        objectives.append(f)
    return objectives

def dtlz4(x: list, m: int = 3, alpha: int = 100) -> list:
    """Función benchmark DTLZ4 con sesgo en las variables (alpha típico = 100)"""
    x_mod = [xi**alpha for xi in x]  # deformación en los primeros m-1
    k = len(x_mod) - m + 1
    g = sum((xi - 0.5)**2 for xi in x_mod[-k:])
    
    objectives = []
    for i in range(m):
        f = 1 + g
        for j in range(m - i - 1):
            f *= np.cos(0.5 * np.pi * x_mod[j])
        if i > 0:
            f *= np.sin(0.5 * np.pi * x_mod[m - i - 1])
        objectives.append(f)
    return objectives

def dtlz5(x: list, m: int = 3) -> list:
    """
    Función benchmark DTLZ5 para pruebas.
    x: lista de n variables en [0,1]
    m: número de objetivos
    Devuelve lista de m valores [f1, f2, ..., fm]
    """
    # 1. Calculamos k y g
    k = len(x) - m + 1
    tail = x[-k:]                           # las últimas k variables
    g = sum((xi - 0.5)**2 for xi in tail)   # g(x_M)

    # 2. Calculamos los ángulos θ
    theta = [0.0] * m
    theta[0] = np.pi * x[0] / 2.0
    for i in range(1, m):
        theta[i] = (np.pi / (2 * (1 + 2 * g))) * (1 + 2 * g * x[i])

    # 3. Construimos los objetivos con cos y sin
    objectives = []
    for i in range(m):
        prod = 1 + g
        # producto de cosenos hasta θ[m−i−2]
        for j in range(m - i - 1):
            prod *= np.cos(theta[j])
        # si no es el primer objetivo, multiplicar también por sin(θ[m−i−1])
        if i > 0:
            prod *= np.sin(theta[m - i - 1])
        objectives.append(prod)

    return objectives

def dtlz2(x: list, m: int = 3) -> list:
    """
    Función benchmark DTLZ2 para pruebas.
    x: lista de n variables en [0,1]
    m: número de objetivos
    Devuelve lista de m valores [f1, f2, ..., fm]
    """
    k = len(x) - m + 1
    g = sum((xi - 0.5)**2 for xi in x[-k:])  # g(x_M)

    theta = [np.pi / 2 * xi for xi in x[:m-1]]  # ángulos θ

    objectives = []
    for i in range(m):
        prod = 1 + g
        for j in range(m - i - 1):
            prod *= np.cos(theta[j])
        if i > 0:
            prod *= np.sin(theta[m - i - 1])
        objectives.append(prod)

    return objectives


def generar_poblacion(n: int, n_variables: int, n_objetivos: int) -> list[Individuo]:
    """Genera población aleatoria para DTLZ1"""
    poblacion = []
    for _ in range(n):
        x = np.random.rand(n_variables).tolist()
        # Creamos una lambda por cada objetivo
        funciones = [lambda x, i=i: dtlz1(x, n_objetivos)[i] for i in range(n_objetivos)]
        poblacion.append(Individuo(x, funciones))
    return poblacion

def visualizar_frente(poblacion: list[Individuo], frente: list[Individuo]):
    """Visualización 2D/3D de la población y del frente de Pareto"""
    # Extraemos valores de objetivos
    obj_pob = [ind.f for ind in poblacion]
    obj_frt = [ind.f for ind in frente]
    
    dim = len(obj_pob[0])
    if dim == 2:
        # Plot de toda la población en azul
        plt.scatter(*zip(*obj_pob), label='Población', alpha=0.4)
        # Plot del frente en rojo
        plt.scatter(*zip(*obj_frt), color='red', label='Soluciones no-dominadas')
        plt.xlabel('f1')
        plt.ylabel('f2')
        plt.title('Conjunto de soluciones no-dominadas 2D')
        plt.grid()
        plt.legend()
        plt.show()

    elif dim == 3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # Población
        ax.scatter(*zip(*obj_pob), label='Población', alpha=0.4)
        # Frente
        ax.scatter(*zip(*obj_frt), color='red', label='Soluciones no-dominadas')
        ax.set_xlabel('f1')
        ax.set_ylabel('f2')
        ax.set_zlabel('f3')
        plt.title('Conjunto de soluciones no-dominadas 3D')
        ax.grid()
        ax.legend()
        plt.show()

    else:
        print("Visualización solo disponible para 2 o 3 objetivos")

if __name__ == "__main__":
    
    #Preguntamos al usuario el nombre del ejemplar
    ejemplar = input ("Ingresa el nombre del ejemplar (dtlz1,dtlz2,dtlz3,dtlz4 o dltz5)\n")
    
    #Inicializamos nuestros parametros del algoritmo.
    rwga = RWGA(n_pop=200, n_var=7, n_obj=3, n_elite=60)
    final_pop = None
    
    match(ejemplar):
        case "dtlz1":
            final_pop = rwga.run(n_gen=150, func_generator=lambda x: dtlz1(x, 3))
        
        case "dtlz2":
            final_pop = rwga.run(n_gen=150, func_generator=lambda x: dtlz2(x, 3))
            
        case "dtlz3":
            final_pop = rwga.run(n_gen=150, func_generator=lambda x: dtlz3(x, 3))
        
        case "dtlz4":
            final_pop = rwga.run(n_gen=150, func_generator=lambda x: dtlz4(x, 3))
            
        case "dtlz5":
            final_pop = rwga.run(n_gen=150, func_generator=lambda x: dtlz5(x, 3))
        
        case _:
            print ("Ejemplar no Válido")
            
    
    if final_pop != None:
        
        for ind in final_pop:
            ind.evaluar()
        frente = Version_cuadratica.frente_pareto(final_pop)
        print(f"Soluciones no dominadas finales: {len(frente)}")
        for sol in frente:
            print(sol)
        visualizar_frente(final_pop, final_pop)
        
        guardar_bool = input("Deseas guardar esta solución S/N\n")
        
        
        #Guardamos la población final de los ejemplares en el fichero correspondiente.
        if guardar_bool is "S" or guardar_bool is "s":
            
            # Obtenemos la ruta base del proyecto (dos niveles arriba del actual)
            ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

            # Ruta final donde guardar resultados
            carpeta_resultados = os.path.join(ruta_base, "Results", "RWGA", ejemplar)
            os.makedirs(carpeta_resultados, exist_ok=True)

            # Nombre del archivo de salida
            nombre = input("Ingresa el nombre con el cual desea guardar esta solución.\n")
            fichero = os.path.join(carpeta_resultados, f"{nombre}.txt")

            # Guardamos los resultados
            with open(fichero, 'w') as f:
                f.write(f"Soluciones no dominadas del ejemplar: {ejemplar}\n\n")
                for i, ind in enumerate(frente):
                    f.write(f"Individuo {i+1}:\n")
                    f.write(f"  Variables: {np.round(ind.x, 4).tolist()}\n")
                    f.write(f"  Objetivos: {np.round(ind.f, 4).tolist()}\n\n")

            print(f"Frente de Pareto guardado en: {fichero}")