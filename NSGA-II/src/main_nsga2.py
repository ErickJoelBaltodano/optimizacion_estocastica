# src/main_nsga2.py
import pandas as pd
from problema_dtlz import ProblemaDTLZ
from nsga2 import NSGA2
from plot import plot_comparacion


if __name__ == "__main__":
    # 1) Definir problema DTLZ2 con 12 variables y 3 objetivos
    problema = ProblemaDTLZ("dtlz4", n_var=12, n_obj=3)

    # 2) Crear y ejecutar NSGA-II
    algoritmo = NSGA2(problema,
                      pop_size=100,
                      n_bits=10,
                      cx_prob=0.9,
                      mut_prob=1/(12*10),
                      n_gen=200)

    # Mostrar parámetros en tabla
    params = {
        "Parámetro": ["Problema", "n_var", "n_obj", "pop_size", "n_bits", "cx_prob", "mut_prob", "n_gen"],
        "Valor":     ["dtlz4",      12,      3,      100,        10,       0.9,       f"{1/(12*10):.4f}",  200]
    }
    df = pd.DataFrame(params)
    print("\nParámetros del experimento:\n")
    print(df.to_string(index=False))
    algoritmo.inicializar()
    algoritmo.evolucionar()

    # 3) Extraer frente aproximado
    frente_aprox = [ind.f for ind in algoritmo.get_frente()]

    # 4) Extraer frente teórico
    fr_opt = problema.prob.pareto_front()

    # 5) Graficar tablas y frentes
    plot_comparacion(frente_aprox, fr_opt)


