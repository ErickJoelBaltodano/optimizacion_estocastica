# NSGA-II

**Flujo detallado del algoritmo**
1. Inicialización

Se genera aleatoriamente una población P0P0​ de tamaño NN, evaluando cada individuo en los MM objetivos
sci2s.ugr.es
.
2.2. Ordenamiento no dominado

    Fast Non-Dominated Sort: clasifica PtPt​ en frentes F1,F2,…F1​,F2​,… según niveles de dominancia
    sci2s.ugr.es
    .

    Asigna a cada individuo un rank igual al índice de su frente.

2.3. Cálculo de la distancia de hacinamiento

Para cada frente FiFi​:

    Ordena soluciones por cada objetivo.

    Calcula la distancia de hacinamiento como la suma de las distancias normalizadas a los vecinos inmediatos en cada objetivo
    cse.unr.edu
    .

2.4. Selección por torneo binario

Para generar la población de cría QtQt​:

    Repite NN veces un torneo entre dos individuos aleatorios.

    Compara primero rank; si hay empate elige el de mayor distancia de hacinamiento
    Pymoo
    .

2.5. Cruce y mutación

Aplica operadores como SBX (Simulated Binary Crossover) y mutación polinomial a los padres seleccionados para crear QtQt​
Medium
.
2.6. Selección de supervivencia

    Une las poblaciones Rt=Pt∪QtRt​=Pt​∪Qt​.

    Repite el ordenamiento no dominado y el cálculo de distancia en RtRt​.

    Llena Pt+1Pt+1​ con frentes completos hasta alcanzar NN.

    Si un frente no cabe entero, ordena sus soluciones por distancia de hacinamiento y selecciona las más dispersas para completar Pt+1Pt+1​
    ScienceDirect
    .

2.7. Criterio de parada

Detén después de un número GG de generaciones o un límite de evaluaciones 

## Sobre la representación de los individuos de la población y la generadora de individuos no-dominados.

Definimos un tipo de objeto llamado `Individuo`, esto porque cada punto que le pasamos al algoritmo de soluciones no dominadas tiene en principio dos atributos importantes asociados:

1. Sus coordenadas en el **espacio de búsqueda** 
2. Sus coordenadas en el **espacio objetivo**

Y es más sencillo acceder a estos usando objetos; esto está en `individuo.py`

`comparacion_objetivos.py` tiene la funcionalidad de reducir el número de comparaciones, pero por el momento no lo estamos utilizando.

En `frente_de_pareto_cuadratico.py` obtenemos al conjunto de soluciones no-dominadas de un conjunto de puntos; para esto usamos el método `.domina_a()` de `Individuo`.

En `main_cuadratico.py` está el script de ejecución donde definimos un ejemplar de prueba (`dtlz1`) y lo necesario para la visualización en 2D y 3D.

La configuración actual es:
```python
N_POBLACION = 100
N_VARIABLES = 7
N_OBJETIVOS = 2
```

De manera que por el momento la visualización es en 2D y nuestra población es de 100 puntos aleatorios.

Para ejecutar el script es necesario tener instalado `numpy` y `matplotlib`.

Para ejecutarlo usamos:
```python
python3 main.py
```
Desde terminal estando dentro de la carpeta `src`.

Un ejemplo de ejecución con la configuración actual:
![alt text](Imágenes/sols_no_dominadas.png)

## Sobre `fast_nondominated_sort` dentro de `nsga2.py`

El ordenamiento en este script (Fast Non-dominated Sort) tiene por objetivo:
clasificar toda la población en varios “frentes” de dominancia:

* Frente 1 ($F_1​$): individuos no dominados por ningún otro.

* Frente 2 ($F_2​$​): individuos dominados solo por los de $F_1​$​.

* Y así sucesivamente.
En cada par $(p,q)$, comparamos dos individuos:

    * $p$ es el actual “candidato” cuyo estado de dominancia estamos analizando.

    * $q$ recorre todos los demás individuos para ver si domina o es dominado por $p$.


Fuente de esto: https://www.geeksforgeeks.org/non-dominated-sorting-genetic-algorithm-2-nsga-ii/?utm_source=chatgpt.com


