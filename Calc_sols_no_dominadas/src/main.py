import numpy as np
import matplotlib.pyplot as plt
from individuo import *
from frente_de_pareto_cuadratico import *

def dtlz1(x: list, m: int = 3) -> list:
    """Función benchmark DTLZ1 para pruebas"""
    k = len(x) - m + 1
    g = 100 * (k + sum((xi - 0.5)**2 - np.cos(20 * np.pi * (xi - 0.5)) for xi in x[-k:]))
    objectives = [0.5 * (1 + g) * np.prod(x[:m-1])]
    for i in range(1, m-1):
        objectives.append(0.5 * (1 + g) * np.prod(x[:m-i-1]) * (1 - x[m-i-1]))
    objectives.append(0.5 * (1 - x[0]) * (1 + g))
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
        plt.title('Frente de Pareto 2D')
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
        plt.title('Frente de Pareto 3D')
        ax.legend()
        plt.show()

    else:
        print("Visualización solo disponible para 2 o 3 objetivos")

if __name__ == "__main__":
    # Configuración
    N_POBLACION = 100
    N_VARIABLES = 7
    N_OBJETIVOS = 2
    
    # Generar y evaluar población
    poblacion = generar_poblacion(N_POBLACION, N_VARIABLES, N_OBJETIVOS)
    for ind in poblacion:
        ind.evaluar()
    
    # Calcular frente de Pareto
    frente = Version_cuadratica.frente_pareto(poblacion)
    
    # Resultados
    print(f"\nPoblación inicial: {len(poblacion)} individuos")
    print(f"\n{len(frente)} soluciones no dominadas")
    print("\nEjemplos de soluciones en el frente:")
    for sol in frente[:3]:
        print(f" - {sol}")
    
    # Visualización de población + frente
    visualizar_frente(poblacion, frente)
