import random

class Cruzar:

    def cruza_un_punto(p1: str, p2: str) -> tuple[str, str]:
        if len(p1) != len(p2):
            raise ValueError("Padres de distinta longitud")
        punto = random.randint(1, len(p1)-1)
        h1 = p1[:punto] + p2[punto:]
        h2 = p2[:punto] + p1[punto:]
        return h1, h2

    # Este es el que vamos a usar porque promueve diversidad sin ser tan computacionalmente costoso
    def cruza_dos_puntos(p1: str, p2: str) -> tuple[str, str]:
        if len(p1) != len(p2):
            raise ValueError("Padres de distinta longitud")
        a, b = sorted(random.sample(range(1, len(p1)), 2))
        h1 = p1[:a] + p2[a:b] + p1[b:]
        h2 = p2[:a] + p1[a:b] + p2[b:]
        return h1, h2

    # Este probablemente sea "mejor" que el de dos puntos, pero es más costoso computacionalmente
    # y no creo que sea buena idea agregar complejidad computacional a lo loco.
    def cruza_uniforme(p1: str, p2: str, prob: float = 0.5) -> tuple[str, str]:
        if len(p1) != len(p2):
            raise ValueError("Padres de distinta longitud")
        h1_bits, h2_bits = [], []
        for b1, b2 in zip(p1, p2):
            if random.random() < prob:
                h1_bits.append(b2); h2_bits.append(b1)
            else:
                h1_bits.append(b1); h2_bits.append(b2)
        return ''.join(h1_bits), ''.join(h2_bits)
