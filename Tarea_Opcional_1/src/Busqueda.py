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
                d = -np.linalg.solve(H, grad)  
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
    def busqueda_lineal(f, x_inicial, maximo_de_iteraciones=100, h=1e-5, alpha=1.0, beta=0.5, c=0.1):
       
        
        x_actual = np.copy(x_inicial)  
        grad = Metodo_Numerico.gradiente(f, x_actual, h)  
        for _ in range(maximo_de_iteraciones):
            #Calculamos nueva direccion
            direccion_descenso = -grad
            
            #Calculamos un nuevo punto
            x_nuevo = x_actual + alpha * direccion_descenso
            
            # Verificamos la condición de Armijo
            if f(x_nuevo) <= f(x_actual) + c * alpha * np.dot(grad, direccion_descenso):
                return x_nuevo  
            
            # Reducimos el tamaño de paso
            alpha *= beta
        # Si no se cumple la condición, devolvemos el último punto calculado
        return x_nuevo  