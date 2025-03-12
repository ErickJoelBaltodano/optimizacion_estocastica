class Operador_de_Listas:

    @staticmethod
    def union(lista1, lista2):
        # Convertimos las listas a conjuntos y luego usamos el operador | para obtener la unión
        return list(set(lista1) | set(lista2))
    
    @staticmethod 
    def interseccion(lista1, lista2):
        # Convertimos las listas a conjuntos y usamos el operador & para obtener la intersección
        return list(set(lista1) & set(lista2))
