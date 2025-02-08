from Vertice import *

class Reader_and_Writer:
    
    
    #Método donde leemos un archivo txt y regresamos una representación del modelo job-shop.
    @staticmethod
    def read(documento):
        
        #Leemos el archivo txt y generamos un string que será el contenido del texto.
        with open(documento, "r") as archivo:
            contenido = archivo.read()

        
        lineas = contenido.splitlines()
        
        linea0= lineas[0].split()
        
        numero_de_trabajos =int(linea0[0])
        numero_de_maquinas = int(linea0[1])
        
        lista_de_vertices = []
        i = 1
        id = 0
        for i in range( numero_de_trabajos):
            linea_actual = lineas[i].split()
            numeros = [int (x) for x in linea_actual]
            maquina = 0
            tiempo = 1
            for _ in range (int (len(numeros)/2)):
                vertice = Vertice(id,i,numeros[maquina],numeros[tiempo])
                lista_de_vertices.append(vertice)
                maquina += 2
                tiempo +=2
                id +=1
            
            
        
        
        
        return numero_de_maquinas , numero_de_trabajos,lista_de_vertices
        
        