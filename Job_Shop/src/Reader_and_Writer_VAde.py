# Basado (casi calca) fuertemente en 'Reader_and_Writer.py'

from Vertice_VAde import *

class Reader_and_Writer_VAde:
    @staticmethod
    def read(documento):
        # Leemos el archivo txt y generamos un string que será el contenido del texto.
        with open(documento, "r") as archivo:
            contenido = archivo.read()

        lineas = contenido.splitlines()

        linea0 = lineas[0].split()

        numero_de_trabajos = int(linea0[0])
        numero_de_maquinas = int(linea0[1])

        # Creamos una lista para almacenar los vértices
        lista_de_vertices = []

        # Vértice dummy inicial (id = 0)
        vertice_inicial = Vertice(id=0)
        lista_de_vertices.append(vertice_inicial)

        id = 1  # Empezamos a contar desde 1 para las operaciones
        for i in range(1, numero_de_trabajos + 1):
            linea_actual = lineas[i].split()
            numeros = [int(x) for x in linea_actual]

            # Creamos índices para iterar la lista de números
            maquina = 0
            tiempo = 1
            for _ in range(int(len(numeros) / 2)):
                vertice = Vertice(id, i, numeros[maquina], numeros[tiempo])
                lista_de_vertices.append(vertice)
                maquina += 2
                tiempo += 2
                id += 1

        # Vértice dummy final (id = N + 1)
        vertice_final = Vertice(id=id)
        lista_de_vertices.append(vertice_final)

        return numero_de_maquinas, numero_de_trabajos, lista_de_vertices
    
    
    
    @staticmethod 
    def write (documento):
        
        pass