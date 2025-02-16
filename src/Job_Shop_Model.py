from Vertice import *

class Job_Shop_Model:
    
    #Método constructor donde definimos los atributos de nuestro modelo del problema job-shop
    def __init__(self,numero_de_trabajos:int,numero_de_maquinas:int,lista_de_vertices:[Vertice]):
        
        self.numero_de_trabajos = numero_de_trabajos
        self.numero_de_maquinas = numero_de_maquinas
        self.vertices = lista_de_vertices
        
        self.solution = None    
        self.job_sequence = []
        self.mach_sequence = []
    
        
       
        
        
        
    # Método en el que actualizamos la solucion.  
    def set_solution(self,solucion):
        self.solution = solucion
        '''Falta Actualizar las secuencias'''
    
    # Método en el que calculamos el índice del siguiente job.
    def get_next_job(self,actual_job:int):
        next_job = actual_job +1
        if (next_job % self.numero_de_maquinas == 1):
            return None 
        return next_job

    # Método en el que calculamos el índice de la siguiente máquinna.
    def get_next_mach(self,actual_mach:int):
        pass

    # Método en el que calculamos el índice del anterior job.
    def get_prev_job(self,actual_job:int):
        prev_job = actual_job -1
        if (next_job % self.numero_de_maquinas == 0):
            return None 
        return prev_job

    def get_prev_mach(self,actual_mach:int):
        pass
    
    def eval_current_solution(self):
        pass
    
    def makespan (self):
        pass