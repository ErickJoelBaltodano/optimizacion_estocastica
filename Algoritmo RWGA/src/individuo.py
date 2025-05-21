class Individuo:
    def __init__(self, variables_decision: list, funciones_objetivo: list = None):
        self.x = variables_decision.copy()  # Espacio de búsqueda
        self.funciones = funciones_objetivo if funciones_objetivo else []
        self.f = None  # Espacio objetivo
        
        if self.funciones:
            self.evaluar()

    def evaluar(self):
        """Ejecuta todas las funciones objetivo."""
        if not self.funciones:
            raise ValueError("Funciones objetivo no definidas")
        self.f = [f(self.x) for f in self.funciones]

    def domina_a(self, otro: 'Individuo') -> bool:
        """Comparación de dominancia (suponemos minimización)."""
        if not self.f or not otro.f:
            raise ValueError("Individuos no evaluados")
        
        mejor_en_todo = all(a <= b for a, b in zip(self.f, otro.f))
        mejor_en_algo = any(a < b for a, b in zip(self.f, otro.f))
        return mejor_en_todo and mejor_en_algo

    def __repr__(self):
        return f"Individuo(x={self.x}, f={self.f})"

    