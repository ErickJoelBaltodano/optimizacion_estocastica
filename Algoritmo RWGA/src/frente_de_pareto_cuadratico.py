from individuo import *

class Version_cuadratica:
    def frente_pareto(poblacion: list[Individuo]) -> list[Individuo]:
        frente = []
        for candidato in poblacion:
            dominado = False
            # Modificamos la lista durante el ciclo
            for solucion in list(frente):
                if solucion.domina_a(candidato):
                    dominado = True
                    break
                if candidato.domina_a(solucion):
                    frente.remove(solucion)
            if not dominado:
                frente.append(candidato)
        return frente