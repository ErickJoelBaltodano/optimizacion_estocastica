from Funcion import *
import numpy as np


class Individuo:
    
    def __init__(self, funciones: list, valores: list[list[int]], pesos: list[float] = None):
            self.funciones = funciones
            self.valores = valores
            
            if pesos is None:
                self.pesos = [1 / len(funciones) for _ in range(len(funciones))]
            else:
                self.pesos = pesos        
        
        
    
    def get(self, f: int = None):
        if f is None:  # Evaluar todas las funciones con sus respectivos valores
            imagen = []
            for func, val in zip(self.funciones, self.valores):
                transformed_func = func(val)
                if callable(transformed_func):
                    result = transformed_func(val)  # Pasar los valores aquí
                else:
                    result = transformed_func
                imagen.append(result)
            return self.valores, imagen
        elif 0 <= f < len(self.funciones):  # Evaluar una función específica
            transformed_func = self.funciones[f](self.valores[f])
            if callable(transformed_func):
                return self.valores[f], transformed_func(self.valores[f])  # Pasar valores aquí
            else:
                return self.valores[f], transformed_func
        else:
            raise IndexError(f"Índice {f} fuera de rango. Debe estar entre 0 y {len(self.funciones) - 1}.")