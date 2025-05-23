# src/main_nsga2.py
import pandas as pd
from problema_dtlz import ProblemaDTLZ
from nsga2 import NSGA2
from plot import plot_comparacion
import numpy as np
import os


if __name__ == "__main__":
    #Preguntamos al usuario el nombre del ejemplar
    ejemplar = input ("Ingresa el nombre del ejemplar (dtlz1,dtlz2,dtlz3,dtlz4 o dltz5)\n")   
    
     
    # 1) Definir problema DTLZ2 con 12 variables y 3 objetivos
    problema = ProblemaDTLZ(ejemplar, n_var=12, n_obj=3)

    # 2) Crear y ejecutar NSGA-II
    algoritmo = NSGA2(problema,
                      pop_size=100,
                      n_bits=10,
                      cx_prob=0.9,
                      mut_prob=1/(12*10), # 1/(n_var*n_bits)... La verdad es que no sé si esto es correcto,
                                          # pero se usa algo de este estilo en el paper de NSGA-II.
                      n_gen=200)

    # Mostrar parámetros en tabla
    params = {
        "Parámetro": ["Problema", "n_var", "n_obj", "pop_size", "n_bits", "cx_prob", "mut_prob", "n_gen"],
        "Valor":     [ejemplar,      12,      3,      100,        10,       0.9,       f"{1/(12*10):.4f}",  200]
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
    
    
    
        
        # Guardamos frente_aprox si el usuario lo desea
    if frente_aprox:
        print(f"Soluciones no dominadas finales: {len(frente_aprox)}")
        for i, f in enumerate(frente_aprox):
            print(f"Individuo {i+1}: {np.round(f, 4).tolist()}")

        guardar_bool = input("¿Deseas guardar esta solución? (S/N)\n")

        if guardar_bool.lower() == "s":
            # Ruta base del proyecto (dos niveles arriba de src/)
            ruta_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

            # Ruta de resultados para este ejemplar
            carpeta_resultados = os.path.join(ruta_base, "Results", "NSGA-II", ejemplar)
            os.makedirs(carpeta_resultados, exist_ok=True)

            # Nombre del archivo de salida
            nombre = input("Ingresa el nombre con el cual deseas guardar esta solución.\n")
            fichero = os.path.join(carpeta_resultados, f"{nombre}.txt")

            # Guardamos el frente de Pareto
            with open(fichero, 'w') as f:
                f.write(f"Soluciones no dominadas del ejemplar: {ejemplar}\n\n")
                for i, objetivos in enumerate(frente_aprox):
                    f.write(f"Individuo {i+1}:\n")
                    f.write(f"  Objetivos: {np.round(objetivos, 4).tolist()}\n\n")

            print(f"Frente de Pareto guardado en: {fichero}")
