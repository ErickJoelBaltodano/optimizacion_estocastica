# problema_dtlz.py

import numpy as np
from pymoo.problems import get_problem

class ProblemaDTLZ:
    def __init__(self, nombre: str, n_var: int, n_obj: int):
        self.prob = get_problem(nombre, n_var=n_var, n_obj=n_obj)
        self.limites = list(zip(self.prob.xl, self.prob.xu))

        # Creamos lambdas que convierten x en array 2D antes de evaluar
        self.funciones = [
            (lambda idx: 
                lambda x: self._eval_objetivo(idx, x)
            )(i)
            for i in range(n_obj)
        ]

    def _eval_objetivo(self, idx: int, x: list[float]) -> float:
        """
        Evalúa un solo individuo x (1D list) para el objetivo idx,
        convirtiéndolo en un array 2D de NumPy.
        """
        X = np.array([x], dtype=float)               # shape (1, n_var)
        F = self.prob.evaluate(X, 
                               return_as_dictionary=False
                              ).flatten()           # shape (n_obj,)
        return float(F[idx])

    def evaluar(self, x_real: list[float]) -> list[float]:
        """
        Evalúa el vector x_real devolviendo la lista de sus M objetivos.
        """
        X = np.array([x_real], dtype=float)
        return self.prob.evaluate(X,
                                  return_as_dictionary=False
                                 ).flatten().tolist()
