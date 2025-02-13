
class job_shop_model:
    
    #Método constructor donde definimos los atributos de nuestro modelo del problema job-shop
    def __init__(self,numero_de_trabajos:int,numero_de_maquinas:int,matriz_de_trabajos, matriz_de_tiempos):
        
        self.numero_de_maquinas = numero_de_maquinas
        self.numero_de_trebajos = numero_de_trabajos
        self.matriz_de_trabajos = matriz_de_trabajos
        self.matriz_de_tiempos = matriz_de_tiempos
        
        
        
        
    def get_time(self,job):
        pass
        
        
    def evaluate(solucion):
        pass
        
    