Se hace la implementación del algoritmo RWGA. 


El algoritmo se encuentra implementado dentro de la clase `RWGA` y utiliza otras clases auxiliares como `Individuo`, `Version_cuadratica` (para el cálculo del frente de Pareto), y `comparar_objetivos`.

Clases y Archivos Importados:
- `Individuo`: Representa una solución del problema.
- `Version_cuadratica`: Contiene el método para calcular el frente de Pareto de manera cuadrática.

Componentes Principales del Algoritmo: 
1. **Inicialización**
   - Se genera una población inicial aleatoria dentro del espacio de búsqueda [0,1]^n_var.
   - Cada individuo es evaluado con funciones objetivo proporcionadas por `func_generator`.
   - Se obtienen los no dominados de la población. 

2. **Cruzamiento Ponderado**
   - Se utiliza un operador de cruza basado en combinaciones lineales ponderadas aleatoriamente:
     `y1 = w_ia + (1-w_i)b`, `y2 = w_ib + (1-w_i)a`.

3. **Mutación**
   - Se aplica una mutación gaussiana por componente con probabilidad `pm`, manteniéndose dentro del rango [0,1].

4. **Selección y Descendencia**
   - Se generan vectores de pesos aleatorios para guiar la selección de padres.
   - La aptitud se calcula como el inverso del valor agregado `w·f` de cada individuo.
   - Se seleccionan padres por muestreo ponderado y se crean hijos mediante cruzamiento y mutación.

5. **Élite**
   - Se hace la selección de los n_elite de la población. Posteriormente se unen esos n_elite a los hijos mejorados. 

6. **Búsqueda Local**
   - Se aplica una búsqueda local tipo Hill Climbing sobre cada individuo de los del paso anterior, guiada por un vector de pesos aleatorios.

7. **Iteración**
   - El proceso se repite por `n_gen` generaciones.

Parámetros del Algoritmo: 
- `n_pop`: Tamaño de la población.
- `n_var`: Número de variables de decisión.
- `n_obj`: Número de objetivos.
- `n_elite`: Número de soluciones élite a preservar en cada generación.
- `pc`: Probabilidad de cruzamiento (no utilizada directamente pues la cruza siempre ocurre con un vector de pesos).
- `pm`: Probabilidad de mutación por componente.


