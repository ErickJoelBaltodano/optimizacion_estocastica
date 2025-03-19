from Metodo_Numerico import *
import numpy as np
class Busqueda:
    
    @staticmethod
    def metodo_newton(f, x_inicial, tol=1e-6, max_iter=100, h=1e-5):
    
        x = np.copy(x_inicial)
        for _ in range(max_iter):
            # Calcular gradiente y Hessiana
            grad = Metodo_Numerico.gradiente(f, x, h)
            H = Metodo_Numerico.hessiana(f, x, h)
            
            # Calcular la dirección de Newton
            try:
                d = -np.linalg.solve(H, grad)  # Resuelve H * d = -grad
            except np.linalg.LinAlgError:
                print("Hessiana singular. No se puede invertir.")
                break
            
            # Actualizar el punto
            x_nuevo = x + d
            
            # Verificar convergencia
            if np.linalg.norm(x_nuevo - x) < tol:
                break
            
            x = x_nuevo
        
        return x
    
    @staticmethod
    def busqueda_lineal(f, x_inicial, tol=1e-6, max_iter=100, h=1e-5, alpha_inicial=1.0, beta=0.5, c=0.1):
        x = np.copy(x_inicial)
        
        for _ in range(max_iter):
            # Calcular gradiente
            grad = Metodo_Numerico.gradiente(f, x, h)
            
            # Calcular la dirección de descenso
            d = -grad
            
            # Búsqueda de tamaño de paso (backtracking line search)
            alpha = alpha_inicial
            for _ in range(max_iter):
                if f(x + alpha * d) <= f(x) + c * alpha * np.dot(grad, d):
                    break
                alpha *= beta
            
            # Actualizar el punto
            x_nuevo = x + alpha * d
            
            # Verificar convergencia
            if np.linalg.norm(x_nuevo - x) < tol:
                break
            
            x = x_nuevo
        
        return x
