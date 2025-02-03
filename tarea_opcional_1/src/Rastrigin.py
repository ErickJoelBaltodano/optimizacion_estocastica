from Function import *

dimension =int(input ("Ingrese la dimension sobre la que realizaremos la búsqueda:  "  ))
espacio_de_busqueda = []
funcion = Function.rastrigin

for i in range (dimension):
    espacio_de_busqueda.append(int(input("Ingrese el límite inferior sobre la dimension {}:  ".format(i))))
    espacio_de_busqueda.append(int(input("Ingrese el límite superior sobre la dimension {}:  ".format(i))))
    
    
print (espacio_de_busqueda)
print (funcion(1,[50]))