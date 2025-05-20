import numpy as np
from individuo import Individuo
from frente_de_pareto_cuadratico import Version_cuadratica
from comparacion_objetivos import comparar_objetivos

# Definimos una clase para el algoritmo RWGA
class RWGA:
    def __init__(self, n_pop, n_var, n_obj, n_elite, pc=1.0, pm=0.1):
        #Inicializamos los parametros del algoritmo
        self.n_var = n_var #Este es el numero de variables de decision 
        self.n_pop = n_pop #Este es el tamaño de la población 
        self.n_obj = n_obj #Este es el numero de objetivos a optimizar
        self.n_elite = n_elite #Estas son las mejores soluciones a preservar
        self.pm = pm #Esta es la probabilidad de mutacion que se usa en el algoritmo 

    def weighted_average_crossover(self, x1, x2):
        #Este es nuestro operador de cruza. Da un vector de pesos uniformente aleatorios w y considera las siguientes combinaciones lineales como hijos: wa+(1-w)b y wb+(1-w)b
        w = np.random.rand()
        y1 = [(w * a + (1 - w) * b) for a, b in zip(x1, x2)]
        y2 = [(w * b + (1 - w) * a) for a, b in zip(x1, x2)]
        return y1, y2

    def mutate(self, x):
        y = x.copy()
        #Este es el operador de mutación. Funciona dando una probabilidad pm. 
        for i in range(len(y)):
            if np.random.rand() < self.pm: #Damos un numero uniformemente aleatorio por cada entrada de la solucion y_i
                y[i] += np.random.normal(0, 0.1) #Si ese numero es menor que pm, entonces a y_i le sumamos un numero aleatorio sacado de una variable aleatoria normal
                y[i] = np.clip(y[i], 0, 1) #Si el numero se sale del espacio de busqueda, hacemos una correccion. 
        return y

    def local_search(self, ind: Individuo, w: np.ndarray, step=0.05, n_vecinos=20):
        #Esta es una busqueda local hil climbing guiada por un vetor de pesos w
        s = Individuo(ind.x.copy(), ind.funciones) #Creamos una copia de la solucion actual 
        s.f = ind.f.copy()
        f_s = np.dot(w, s.f) #Calculamos la evaluacion de la solucion mediante el producto punto wf

        mejorado = True #Nos indica si se ha encontrado una mejora
        while mejorado:
            mejorado = False
            for _ in range(n_vecinos): #generamos n_vecinos en cada iteracion
                vecino_x = s.x + np.random.uniform(-step, step, len(s.x)) # np.random.uniform(-step, step, len(s.x)) genera un vector alatorio de tamaño len(s.x). Cada entrada del vector 
                #tiene valores en el rango [-step,step] (por defecto tomamos a step=0.05). A la respectiva solucion le sumamos la solucion actual y asi obtenemos a un vecino 
                vecino_x = np.clip(vecino_x, 0, 1) #Nos asegura que los vecinos se queden dentro del espacio de busqueda. 
                vecino = Individuo(vecino_x.tolist(), s.funciones) #Creamos un nuevo individuo con el vecino
                vecino.evaluar() #Evaluamos al nuevo individuo (vecino)
                f_vecino = np.dot(w, vecino.f) #Calculamos la evaluacion del nuevo individuo (vecino) mediante el producto punto wf
                if f_vecino < f_s: #Si el nuevo individuo (vecino) es mejor que la solucion actual, entonces lo guardamos
                    s = vecino 
                    f_s = f_vecino
                    mejorado = True
                    break #Si el nuevo individuo (vecino) es mejor que la solucion actual, entonces lo guardamos y reiniciamos el ciclo
        return s # Devolvemos la mejor solucion encontrada en la busqueda local

    def run(self, n_gen, func_generator): # Este es el rwga.
        poblacion = [] #Generamos la poblacion inicial de tamaño n_pop.
        for _ in range(self.n_pop): 
            x = np.random.rand(self.n_var).tolist() #Cada individuo de la poblacion tiene entradas con valores entre 0 y 1.
            funcs = [lambda x, i=i: func_generator(x)[i] for i in range(self.n_obj)] 
            poblacion.append(Individuo(x, funcs))  

        for gen in range(n_gen): #Iteramos n_gen veces
            for ind in poblacion:#Evaluamos a cada individuo de la poblacion actual
                ind.evaluar()
            no_dom = Version_cuadratica.frente_pareto(poblacion) #Calculamos el frente de pareto de usando el metodo de la version cuadratica.

            offspring = [] #Inicializamos la lista de descendientes 
            weight_list = [] #Inicializamos una lista de pesos 
            n_pairs = (self.n_pop - self.n_elite) // 2  #Calculamos el numero de pares de padres que vamos a usar para generar descendientes. 
            for _ in range(n_pairs): 
                w = np.random.rand(self.n_obj) #se crean n_pairs de  vectores de pesos aleatorios.
                w /= w.sum() # Normalizamos el vector de pesos para que la suma de sus entradas sea igual a 1.
                weight_list.append(w) #Guardaos esos vectores de pesos en la lista de pesos anteriormente inicializada.
                agg = np.array([np.dot(w, ind.f) for ind in poblacion]) #Dado un w, generamos un vector de evaluaciones de la poblacion.
                fitness = 1.0 / (agg + 1e-8) #Tomamos el inverso de las evaluaciones para obtener el fitness de cada individuo. Sumamos un epsilon para evitar la division por cero.
                probs = fitness / fitness.sum() #Para ese w generamos un vector de probabilidades para seleccionar a los padres.
                padres = np.random.choice(poblacion, size=2, replace=False, p=probs) #Elegimos a los padres de la poblacion usando el vector de probabilidades.

                c1_x, c2_x = self.weighted_average_crossover(padres[0].x, padres[1].x) #Generamos los hijos usando el operador de cruza definido anteriormente con el respectivo w
                c1_x = self.mutate(c1_x) #Aplicamos el operador de mutacion a los hijos generados
                c2_x = self.mutate(c2_x)

                funcs = padres[0].funciones
                c1 = Individuo(c1_x, funcs); c2 = Individuo(c2_x, funcs) #Crea dos nuevos individuos hijos con las mismas funciones objetivo.
                c1.evaluar(); c2.evaluar()
                offspring.extend([c1, c2]) #Se evaluan los nuevos individuos  y se agregan a la lista de descendientes.
                
            if len(no_dom) <= self.n_elite: #Tomamos a los n_elites. Si el numero de individuos no dominados es menor o igual a n_elite, entonces tomamos a todos los individuos no dominados.
                elites = no_dom.copy()
            else: #Si el numero de individuos no dominados es mayor a n_elite, entonces tomamos n_elites de manera aleatoria.
                elites = list(np.random.choice(no_dom, size=self.n_elite, replace=False))

            combinada = elites + offspring #Combinamos a los elites con los descendientes generados.

           
            nueva_pob = [] #inicializa la nueva poblacion
            for ind in combinada:
                # Para cada individuo, generar nuevo peso y buscar mejora
                w_ls = np.random.rand(self.n_obj)
                w_ls /= w_ls.sum()
                mejor = self.local_search(ind, w_ls)
                nueva_pob.append(mejor)

          
            poblacion = nueva_pob #Actualizamos la poblacion con la nueva poblacion generada

        return poblacion

