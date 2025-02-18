from Function import *
from Metodo_Numerico import * 
from Random_Solution_Generator import *

#Obtenemos la dimensión sobre la que vamos a trabajar.
dimension =int(input ("Ingrese la dimension sobre la que realizaremos la búsqueda:  "  ))

#Obtenemos la funcion sobre la que vamos a trabajar.
funcion = Function.rastrigin

#Obtenemos el espacio de busqueda sobre el que vamos a trabajar
espacio_de_busqueda = []
for i in range (dimension):
    espacio_de_busqueda.append(int(input("Ingrese el límite inferior sobre la dimension {}:  ".format(i))))
    espacio_de_busqueda.append(int(input("Ingrese el límite superior sobre la dimension {}:  ".format(i))))
    
    
print (espacio_de_busqueda)
print (funcion(1,[50]))

x,y =Metodo_Numerico.busqueda_en_linea(5,funcion,[0,100,101,200,300,400])
print ("{}------{}".format(x,y))