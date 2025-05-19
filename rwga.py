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
                vecino = Individuo(vecino_x.tolist(), s.funciones)
                vecino.evaluar()
                f_vecino = np.dot(w, vecino.f)

                if f_vecino < f_s:
                    s = vecino
                    f_s = f_vecino
                    mejorado = True
                    break
        return s

    def run(self, n_gen, func_generator):
        poblacion = []
        for _ in range(self.n_pop):
            x = np.random.rand(self.n_var).tolist()
            funcs = [lambda x, i=i: func_generator(x)[i] for i in range(self.n_obj)]
            poblacion.append(Individuo(x, funcs))

        for gen in range(n_gen):
            for ind in poblacion:
                ind.evaluar()
            no_dom = Version_cuadratica.frente_pareto(poblacion)

            offspring = []
            weight_list = []
            n_pairs = (self.n_pop - self.n_elite) // 2
            for _ in range(n_pairs):
                w = np.random.rand(self.n_obj)
                w /= w.sum()
                weight_list.append(w)

                agg = np.array([np.dot(w, ind.f) for ind in poblacion])
                fitness = 1.0 / (agg + 1e-8)
                probs = fitness / fitness.sum()
                padres = np.random.choice(poblacion, size=2, replace=False, p=probs)

                c1_x, c2_x = self.weighted_average_crossover(padres[0].x, padres[1].x)
                c1_x = self.mutate(c1_x)
                c2_x = self.mutate(c2_x)

                funcs = padres[0].funciones
                c1 = Individuo(c1_x, funcs); c2 = Individuo(c2_x, funcs)
                c1.evaluar(); c2.evaluar()
                offspring.extend([c1, c2])

            if len(no_dom) <= self.n_elite:
                elite_sel = no_dom.copy()
            else:
                elite_sel = list(np.random.choice(no_dom, size=self.n_elite, replace=False))

            improved = [self.local_search(ind, w) for ind, w in zip(offspring, weight_list * (len(offspring)//len(weight_list)))]
            poblacion = elite_sel + improved

        return poblacion
