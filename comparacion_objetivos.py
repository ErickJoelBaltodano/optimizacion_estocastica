from individuo import *


def comparar_objetivos(a: Individuo, b: Individuo) -> int:
    """
    Retorna:
        1: a domina a b
        2: b domina a a
        0: Equivalentes
        -1: Incomparables
    """
    mejor_a = 0
    mejor_b = 0
    
    for f_a, f_b in zip(a.f, b.f):
        if f_a < f_b:
            mejor_a += 1
        elif f_b < f_a:
            mejor_b += 1
    
    if mejor_a == len(a.f) and mejor_b == len(b.f):
        return 0  # Caso especial (ojalá raro por diversidad)
    elif mejor_a == len(a.f):
        return 1
    elif mejor_b == len(b.f):
        return 2
    else:
        return -1