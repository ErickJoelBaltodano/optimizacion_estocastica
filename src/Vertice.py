

class Vertice:
    
    
    def __init__(self,id:int,trabajo:int,maquina:int, tiempo:int):
        self.id = id
        self.trabajo = trabajo
        self.maquina = maquina
        self.tiempo = tiempo
        
        
    # Getters y Setters
    
    def get_trabajo(self):
        return self.trabajo
    
    def get_maquina (self):
        return self.maquina
    
    def get_tiempo(self):
        return self.tiempo
    
    
    def __repr__(self):
        return "Id: {} \n Trabajo: {} \n, Tiempo: {}\n Máquina: {}\n".format(self.id,self.trabajo,self.tiempo,self.maquina)