from typing import List, Tuple

'''
Para representar una variable real x_i∈[a_i,b_i], mapeamos los 10 bits a ese intervalo.
Usamos 10 porque en algún momento del semestre pasado se dijo que ese era un buen número de bits.
'''
def real_a_binario(valor, minimo, maximo, n_bits=10):
    """Convierte un número real a su representación binaria."""
    
    escala = (valor - minimo) / (maximo - minimo) # `escala`∈[0, 1] (si `valor` está dentro del intervalo).
    
    entero = round(escala * (2**n_bits - 1)) # mapea `escala` al rango [0, 2**n_bits - 1] (`round` hace el
                                                # redondeo al entero más cercano dentro de ese rango).
    
    return format(entero, f'0{n_bits}b') # Devuelve un string de bits de longitud `n_bits` (rellena con 
                                            # ceros a la izquierda si es necesario).


def binario_a_real(bits, minimo, maximo):
    """Convierte un string de bits a su número real correspondiente."""
    
    n_bits = len(bits)
    
    entero = int(bits, 2) # Convierte el string binario (base 2) a un entero decimal.
    
    escala = entero / (2**n_bits - 1) # Normaliza el entero al rango [0, 1]
    
    return minimo + escala * (maximo - minimo) # Desnormaliza el valor al rango [minimo, maximo]



"""
Funciones para codificar y decodificar un vector de variables reales a su representación binaria
y viceversa. Se usa la función `real_a_binario` para codificar cada variable y la función `binario_a_real`
"""
def vector_real_a_binario(x: List[float],
                        limites: List[Tuple[float,float]],
                        n_bits: int = 10) -> str:
    """
    Convierte un vector real x en su genotipo binario.
    - x: [x1, x2, ..., xn]
    - limites: [(min1,max1), ..., (minn,maxn)]
    - n_bits: bits por variable
    Retorna: string de n*n_bits caracteres '0'/'1'
    """
    if len(x) != len(limites):
        raise ValueError("longitud de x y limites debe coincidir")
    bits = []
    for valor, (lo, hi) in zip(x, limites):
        # usamos la función real_a_binario ya definida
        bits.append(real_a_binario(valor, lo, hi, n_bits))
    return ''.join(bits)


def binario_a_vector_real(bits: str,
                        limites: List[Tuple[float,float]],
                        n_bits: int = 10) -> List[float]:
    """
    Reconstruye el vector real a partir del genotipo binario.
    - bits: string de longitud n*n_bits
    - limites: [(min1,max1), ..., (minn,maxn)]
    - n_bits: bits por variable
    Devuelve: [x1, x2, ..., xn]
    """
    n = len(limites)
    if len(bits) != n * n_bits:
        raise ValueError(f"bits debe tener longitud {n*n_bits}")
    x = []
    for i, (lo, hi) in enumerate(limites):
        chunk = bits[i*n_bits:(i+1)*n_bits]
        x.append(binario_a_real(chunk, lo, hi))
    return x