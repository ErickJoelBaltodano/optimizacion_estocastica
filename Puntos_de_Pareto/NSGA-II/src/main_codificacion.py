from codificacion import *

def main():
    # Configuración
    x_original = [3.5, 2.0, 9.0, 12]
    limites = [(0, 10), (-5, 5), (0, 20), (0, 15)]
    n_bits = 10

    # Codificar
    genotipo = Codificacion.vector_real_a_binario(x_original, limites, n_bits)
    print(f"\nGenotipo ({len(genotipo)} bits): {genotipo}")

    # Decodificar
    x_reconstruido = Codificacion.binario_a_vector_real(genotipo, limites, n_bits)
    print(f"\nVector reconstruido: {x_reconstruido}")

    print(f"\nVector original: {x_original}")

if __name__ == "__main__":
    main()