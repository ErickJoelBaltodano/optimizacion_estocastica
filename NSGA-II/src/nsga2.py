import random
from typing import List, Dict
from individuo import *
from frente_de_pareto import *
from codificacion import vector_real_a_binario, binario_a_vector_real
from operadores_cruza import *
from mutacion import *
from problema_dtlz import *

def fast_nondominated_sort(pob: List[Individuo]) -> List[List[Individuo]]:
    """
    Ordenamiento no dominado rápido aplicado a tu clase Individuo.
    Devuelve lista de frentes: [F1, F2, ...], donde cada Fi es lista de Individuo.
    """
    S: Dict[Individuo, List[Individuo]] = {p: [] for p in pob}
    n: Dict[Individuo, int] = {p: 0 for p in pob}
    fronts: List[List[Individuo]] = [[]]

    # Relacionamos cada p con los q que domina, y contamos cuántos lo dominan
    for p in pob:
        for q in pob:
            if p.domina_a(q):
                S[p].append(q)
            elif q.domina_a(p):
                n[p] += 1
        if n[p] == 0:
            fronts[0].append(p)

    # Extraemos sucesivos frentes
    i = 0
    while fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in S[p]:
                n[q] -= 1
                if n[q] == 0:
                    next_front.append(q)
        i += 1
        fronts.append(next_front)

    return fronts[:-1]


def crowding_distance(front: List[Individuo]) -> Dict[Individuo, float]:
    """
    Calcula la distancia de hacinamiento de un frente dado (lista de Individuo).
    """
    distances = {p: 0.0 for p in front}
    M = len(front[0].f)  # número de objetivos

    for m in range(M):
        # ordenar por valor del objetivo m
        front.sort(key=lambda ind: ind.f[m])
        distances[front[0]] = distances[front[-1]] = float('inf')
        f_min, f_max = front[0].f[m], front[-1].f[m]

        for i in range(1, len(front)-1):
            prev_f = front[i-1].f[m]
            next_f = front[i+1].f[m]
            if f_max > f_min:  # evitar división por cero
                distances[front[i]] += (next_f - prev_f) / (f_max - f_min)

    return distances


class NSGA2:
    def __init__(self,
                 problema: ProblemaDTLZ,
                 pop_size: int = 100,
                 n_bits: int = 10,
                 cx_prob: float = 0.9,
                 mut_prob: float = 0.01,
                 n_gen: int = 200):
        self.prob = problema
        self.N = pop_size
        self.n_bits = n_bits
        self.cx_prob = cx_prob
        self.mut_prob = mut_prob
        self.n_gen = n_gen
        self.pobl: List[Individuo] = []
        self.pobl_bits: List[str] = []

    def inicializar(self):
        """Genera población inicial en binario, la decodifica y evalúa."""
        self.pobl.clear()
        self.pobl_bits.clear()
        for _ in range(self.N):
            # vector real aleatorio
            x_real = [lo + random.random()*(hi-lo) for lo,hi in self.prob.limites]
            bits = vector_real_a_binario(x_real, self.prob.limites, self.n_bits)
            self.pobl_bits.append(bits)

            x_dec = binario_a_vector_real(bits, self.prob.limites, self.n_bits)
            ind = Individuo(x_dec, funciones_objetivo=self.prob.funciones)
            self.pobl.append(ind)

    def evolucionar(self):
        """Bucle principal NSGA-II con elitismo y operadores binarios."""
        for gen in range(self.n_gen):
            # 1) Ordenamiento no dominado
            fronts = fast_nondominated_sort(self.pobl)

            # 2) Distancia de hacinamiento
            crowd_dist = {}
            for fr in fronts:
                crowd_dist.update(crowding_distance(fr))

            # 3) Crear hijos Q
            hijos_bits = []
            while len(hijos_bits) < self.N:
                # torneo binario: elige dos, queda el mejor
                def torneo() -> int:
                    a, b = random.sample(range(self.N), 2)
                    # buscar su frente
                    for rank, fr in enumerate(fronts):
                        if self.pobl[a] in fr: rank_a = rank
                        if self.pobl[b] in fr: rank_b = rank
                    if rank_a < rank_b:
                        return a
                    if rank_b < rank_a:
                        return b
                    # si mismo frente, mayor crowding distance
                    return a if crowd_dist[self.pobl[a]] > crowd_dist[self.pobl[b]] else b

                p1, p2 = torneo(), torneo()
                b1, b2 = self.pobl_bits[p1], self.pobl_bits[p2]

                # cruce y mutación
                if random.random() < self.cx_prob:
                    c1, c2 = cruza_un_punto(b1, b2)
                else:
                    c1, c2 = b1, b2
                c1 = mutacion_bit_flip(c1, self.mut_prob)
                c2 = mutacion_bit_flip(c2, self.mut_prob)

                hijos_bits += [c1, c2]

            # 4) Evaluar hijos y combinar poblaciones
            hijos = []
            for bits in hijos_bits[:self.N]:
                x_dec = binario_a_vector_real(bits, self.prob.limites, self.n_bits)
                hijos.append(Individuo(x_dec, funciones_objetivo=self.prob.funciones))
            R = self.pobl + hijos

            # 5) Selección elitista
            new_pop = []
            fronts_R = fast_nondominated_sort(R)
            for fr in fronts_R:
                if len(new_pop) + len(fr) <= self.N:
                    new_pop.extend(fr)
                else:
                    cd = crowding_distance(fr)
                    # ordenar por distancia descendente
                    fr.sort(key=lambda ind: cd[ind], reverse=True)
                    needed = self.N - len(new_pop)
                    new_pop.extend(fr[:needed])
                    break

            # actualizamos población y genotipos
            self.pobl = new_pop
            self.pobl_bits = [
                vector_real_a_binario(ind.x, self.prob.limites, self.n_bits)
                for ind in self.pobl
            ]

    def get_frente(self) -> List[Individuo]:
        """Devuelve la última población (aprox. Pareto)."""
        return self.pobl
