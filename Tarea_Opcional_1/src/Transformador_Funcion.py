class Transformador_Funcion:
    
    def __init__(self,funcion):
        self.funcion = funcion
        
        
    def inversa(self,valores):
        return lambda valores: 1 / self.funcion(valores)
        
    
    def none(self,valores):
        return lambda valores:  self.funcion(valores)
    
    