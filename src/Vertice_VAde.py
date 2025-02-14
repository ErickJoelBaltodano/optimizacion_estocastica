# Basado fuertemente (casi calca) en 'Vertice.py'

'''
Agregué un constructor alternativo para los vértices "dummy": el 0 y N+1.
Estos vértices no tendrán trabajo, máquina ni tiempo asociado, pero sí un id.
'''

class Vertice:
    # Cosas como 'trabajo: int = None' permite la creación de los dummies
    def __init__(self, id: int, trabajo: int = None, maquina: int = None, tiempo: int = None):
        self.id = id
        self.trabajo = trabajo
        self.maquina = maquina
        self.tiempo = tiempo

    # Getters y Setters
    def get_trabajo(self):
        return self.trabajo

    def get_maquina(self):
        return self.maquina

    def get_tiempo(self):
        return self.tiempo

    def __repr__(self):
        if self.trabajo is None:  # Para vértices dummy
            return f"Vértice Dummy (Id: {self.id})"
        return f"Id: {self.id}, Trabajo: {self.trabajo}, Máquina: {self.maquina}, Tiempo: {self.tiempo}"