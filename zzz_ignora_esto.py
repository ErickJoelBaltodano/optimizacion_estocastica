import numpy as np
from individuo import Individuo
from frente_de_pareto_cuadratico import Version_cuadratica
from comparacion_objetivos import comparar_objetivos


def weighted_average_crossover(x1, x2):
    """Cruza usando combinación ponderada aleatoria de los genes."""
    w = np.random.rand()
    y1 = [(w * a + (1 - w) * b) for a, b in zip(x1, x2)]
    y2 = [(w * b + (1 - w) * a) for a, b in zip(x1, x2)]
    return y1, y2


def mutate(x, pm):
    """Mutación gaussiana en cada gen con probabilidad pm."""
    y = x.copy()
    for i in range(len(y)):
        if np.random.rand() < pm:
            y[i] += np.random.normal(0, 0.1)
            y[i] = np.clip(y[i], 0, 1)
    return y


def local_search(ind: Individuo, w: np.ndarray, step=0.05, n_vecinos=20):
    s = Individuo(ind.x.copy(), ind.funciones)
    s.f = ind.f.copy()
    f_s = np.dot(w, s.f)

    mejorado = True
    while mejorado:
        mejorado = False
        for _ in range(n_vecinos):
            vecino_x = s.x + np.random.uniform(-step, step, len(s.x))
            vecino_x = np.clip(vecino_x, 0, 1)
            vecino = Individuo(vecino_x.tolist(), s.funciones)
            vecino.evaluar()
            f_vecino = np.dot(w, vecino.f)

            if f_vecino < f_s:
                s = vecino
                f_s = f_vecino
                mejorado = True
                break  # toma el primer mejor
    return s


class RWGA:
    def __init__(self, n_pop, n_var, n_obj, n_elite, pc=1.0, pm=0.1):
        self.n_pop = n_pop
        self.n_var = n_var
        self.n_obj = n_obj
        self.n_elite = n_elite
        self.pm = pm

    def run(self, n_gen, func_generator):
        # 1. Inicialización
        poblacion = []
        for _ in range(self.n_pop):
            x = np.random.rand(self.n_var).tolist()
            funcs = [lambda x, i=i: func_generator(x)[i] for i in range(self.n_obj)]
            poblacion.append(Individuo(x, funcs))

        for gen in range(n_gen):
            # 2. Evaluación y frente de Pareto
            for ind in poblacion:
                ind.evaluar()
            no_dom = Version_cuadratica.frente_pareto(poblacion)

            # 3. Selección de padres y generación de descendencia
            offspring = []
            weight_list = []
            n_pairs = (self.n_pop - self.n_elite) // 2
            for _ in range(n_pairs):
                # generar vector de pesos
                w = np.random.rand(self.n_obj)
                w /= w.sum()
                weight_list.append(w)

                # selección proporcional
                agg = np.array([np.dot(w, ind.f) for ind in poblacion])
                fitness = 1.0 / (agg + 1e-8)
                probs = fitness / fitness.sum()
                padres = np.random.choice(poblacion, size=2, replace=False, p=probs)

                # Reproducción: cruza ponderada
                c1_x, c2_x = weighted_average_crossover(padres[0].x, padres[1].x)
                c1_x = mutate(c1_x, self.pm)
                c2_x = mutate(c2_x, self.pm)

                # hijos
                funcs = padres[0].funciones
                c1 = Individuo(c1_x, funcs); c2 = Individuo(c2_x, funcs)
                c1.evaluar(); c2.evaluar()
                offspring.extend([c1, c2])

            # 5. Elitismo
            if len(no_dom) <= self.n_elite:
                elite_sel = no_dom.copy()
            else:
                elite_sel = list(np.random.choice(no_dom, size=self.n_elite, replace=False))

            # 6. Mejora local (búsqueda por escalada)
            improved = [local_search(ind, w) for ind, w in zip(offspring, weight_list * (len(offspring)//len(weight_list)))]

            # 7. Reemplazo
            poblacion = elite_sel + improved

        return poblacion


