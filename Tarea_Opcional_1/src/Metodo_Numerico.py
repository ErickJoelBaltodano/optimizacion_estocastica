from random import *
from Random_Solution_Generator import *
import numpy as np

class Metodo_Numerico:
    
    @staticmethod
    def hessiana(f, x, h=1e-5):
  
        n = len(x)
        H = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    # Segundas derivadas puras
                    x_plus = np.copy(x)
                    x_minus = np.copy(x)
                    x_plus[i] += h
                    x_minus[i] -= h
                    H[i, j] = (f(x_plus) - 2 * f(x) + f(x_minus)) / (h**2)
                else:
                    # Segundas derivadas mixtas
                    x_pp = np.copy(x)
                    x_pm = np.copy(x)
                    x_mp = np.copy(x)
                    x_mm = np.copy(x)
                    x_pp[i] += h
                    x_pp[j] += h
                    x_pm[i] += h
                    x_pm[j] -= h
                    x_mp[i] -= h
                    x_mp[j] += h
                    x_mm[i] -= h
                    x_mm[j] -= h
                    H[i, j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4 * h**2)
        
        return H