

class Vertice:
    
    
    def __init__(self,id:int,trabajo:int,maquina:int, tiempo:int):
        self.id = id
        self.trabajo = trabajo
        self.maquina = maquina
        self.tiempo = tiempo
        self.trabajo_siguiente =None
        self.trabajo_anterior= None
        self.maquina_siguiente =None
        self.maquina_anterior= None
        
    # Getters y Setters
    
    def get_trabajo(self):
        return self.trabajo
    
    def get_maquina (self):
        return self.maquina
    
    def get_tiempo(self):
        return self.tiempo
    
    def get_trabajo_siguiente(self):
        return self.trabajo_siguiente
    
    def get_trabajo_anterior(self):
        return self.trabajo_anterior
    
    def get_maquina_siguiente(self):
        return self.maquina_siguiente
    
    def get_maquina_anterior(self):
        return self.maquina_anterior
    
    
    def set_maquina_anterior(self,vertice:"Vertice"):
        pass
    
    def set_maquina_siguiente(self,vertice:"Vertice"):
        pass
    
    @staticmethod
    def conectar(vertice_inicio:"Vertice",vertice_final:"Vertice"):
        vertice_inicio.set_maquina_siguiente(vertice_final)
        vertice_final.set_maquina_anterior(vertice_inicio)
        
    
    
    def __repr__(self):
        return "Id: {} \n Trabajo: {} \n, Tiempo: {}\n Máquina: {}\n".format(self.id,self.trabajo,self.tiempo,self.maquina)