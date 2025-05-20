Definimos un tipo de objeto llamado `Individuo`, esto porque cada punto que le pasamos al algoritmo de soluciones no dominadas tiene en principio dos atributos importantes asociados:

1. Sus coordenadas en el **espacio de búsqueda** 
2. Sus coordenadas en el **espacio objetivo**

Y es más sencillo acceder a estos usando objetos; esto está en `individuo.py`

`comparacion_objetivos.py` tiene la funcionalidad de reducir el número de comparaciones, pero por el momento no lo estamos utilizando.

En `frente_de_pareto_cuadratico.py` obtenemos al conjunto de soluciones no-dominadas de un conjunto de puntos; para esto usamos el método `.domina_a()` de `Individuo`.

En `main.py` está el script de ejecución donde definimos un ejemplar de prueba (`dtlz1`) y lo necesario para la visualización en 2D y 3D.

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
