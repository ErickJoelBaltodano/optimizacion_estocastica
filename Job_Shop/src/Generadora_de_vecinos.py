import copy
from Calculadora_makespan_VAde import *

class Generadora_de_vecinos:

    '''
    Recibiendo parte del output de `Calculadora_makespan_VAde` se debe:

        1. Generar una estructura auxiliar parecida a `info` que guarde
           también las ri's y qi's que le corresponden al vértice.
        2. Por el artículo (sepa cuál), sabemos que un vértice está en 
           la ruta crítica sii ri + qi = makespan. Así que en la creación
           de la estructura auxiliar me gustaría tener una bandera que me
           indique si el vértice cumple la condición. (Algo así como
           'crítica' = True si lo está y False en otro caso).
    '''

  
    @staticmethod
    def construir_nueva_info(makespan, r, q, info):
        nueva_info = {}

        for op_id, datos in info.items():
            if op_id not in r or op_id not in q:
                print(f"Advertencia: Falta la clave {op_id} en r o q. Se omitirá esta operación.")
                continue  # Omitir esta operación

            nueva_info[op_id] = {
                **datos,  # Copiar los datos existentes
                'r': r[op_id],  # El ri
                'q': q[op_id],  # El qi
                'critica': (r[op_id] + q[op_id]) == makespan  # Bandera de ruta crítica
            }

        return nueva_info            
    '''
    Teniendo la info_auxiliar ahora podemos generar a los vecinos:
        1. Dada una solución, digamos: [[1, 8, 5], [4, 9, 2], [7, 3, 6]]
           sus vecinas son soluciones del estilo:
           * [[8, 1, 5], [4, 9, 2], [7, 3, 6]]
           * [[1, 5, 8], [4, 9, 2], [7, 3, 6]]
           * [[1, 8, 5], [4, 9, 2], [3, 7, 6]]
           Es decir, permutan **exactamente dos** operaciones consecutivas
           en una misma máquina dejando todo lo demás igual a la solución
           original. Esta permutación sólo se puede hacer si las dos operaciones
           candidatas cumplen la restricción: ri + qi = makespan
        2. Idealmente todos los vecinos deberían generarse en una sola pasada, 
           para que la cosa sea eficiente.
        3. Me gustaría generar otra estructura aparte donde pudiera guardar los
           movimientos que se hicieron para pasar de una operación a su vecina,
           algo así como: 
           Si solucion == [[1, 8, 5], [4, 9, 2], [7, 3, 6]], y uno de sus vecinos
           es vecino == [[1, 8, 5], [4, 9, 2], [3, 7, 6]], entonces para pasar de
           `solucion` a `vecino` se hizo el movimiento:
           movimiento = {'maquina': 3, 'nuevo_predecesor': 3, 'nuevo_sucesor': 7}
           Porque se hizo la permutación en la máquina 3 (de índice python 2) y el
           cambio quedó de manera en que ahora la operación 3 va antes que la 7.
    '''

    @staticmethod
    def imprimir_nueva_info(nueva_info, makespan):
        #print("\n=== Estructura 'nueva_info' (operaciones críticas) ===")
        for op_id, datos in nueva_info.items():
            critica = datos['r'] + datos['q'] == makespan
            #print(f"Op {op_id}: r={datos['r']}, q={datos['q']}, r+q={datos['r'] + datos['q']} | ¿Crítica? {critica}")
    
    @staticmethod
    def construir_vecindad(solucion, makespan, r, q, info):

        # Construye la estructura auxiliar `nueva_info`:
        nueva_info = Generadora_de_vecinos.construir_nueva_info(makespan, r, q, info)

        #vecindad = [] # Lista de vecinos (elegí esto porque como a priori no sabemos
                      # exactamente cuántos vecinos hay no consideré adecuado un 
                      # np.array; pero se puede elegir un np.array de tamaño igual a
                      # la cota superior de los vecinos que es:
                      # numero_maquinas*(numero_jobs - 1) creo).
        
        vecindad_de_movimientos = [] # Se genera una lista donde los vecinos de la solución dada
                                     # se guardan como el movimiento que se hizo para generarlos.

        #print("\n=== Inicio de generación de vecinos ===")

        # Iteramos por cada máquina en la solución:
        for maquina_idx, secuencia in enumerate(solucion):
            #print(f"\n--- Máquina {maquina_idx + 1} (secuencia: {secuencia}) ---")

            # Verificamos pares consecutivos en la máquina (para la permutación de 
            # operaciones):
            for i in range(len(secuencia)-1):
                op_actual = secuencia[i]
                op_siguiente = secuencia[i+1]
                #print(f"  Verificando par: Op {op_actual} (crítica: {nueva_info[op_actual]['critica']}) y Op {op_siguiente} (crítica: {nueva_info[op_siguiente]['critica']})")

                # Si tenemos dos operaciones críticas consecutivas generamos un vecino
                # con sólo esas dos operaciones permutadas:
                if nueva_info[op_actual]['critica'] and nueva_info[op_siguiente]['critica']:
                    # Creamos una copia de la solución original
                    # vecino = [list(m) for m in solucion]
                    # Intercambiamos las operaciones
                    # vecino[maquina_idx][i], vecino[maquina_idx][i+1] = vecino[maquina_idx][i+1], vecino[maquina_idx][i]

                    # Registramos el movimiento
                    movimiento = {
                        'maquina': maquina_idx + 1,
                        'operaciones_intercambiadas': (op_actual, op_siguiente),
                        'posiciones': (i, i+1)
                    }

                    # vecindad.append(vecino)
                    vecindad_de_movimientos.append(movimiento)
                    # print(f"  -> Vecino generado: {vecino[maquina_idx]}")
                
                '''else:
                    print("  -> No se intercambian (al menos una no es crítica)")'''

                
                #print(f"\n=== La solución sigue siendo {solucion} ===")
        print(f"\n=== Se generaron {len(vecindad_de_movimientos)} vecinos ===")

        #print("\n=== Fin de generación de vecinos ===")
        # return vecindad, movimientos # Retornamos dos listas: la vecindad y los movimientos.
        return vecindad_de_movimientos

    
    '''
    Tenemos una cierta vecindad_de_movimientos, para el Recocido Simulado (y tal vez para otras
    aplicaciones), nos interesa que una vez elegido uno de los índices de la vecindad_de_movimientos,
    podamos decodificar al vecino en cuestión para tener una nueva solución que podamos evaluar.
    '''

    @staticmethod 
    def decodificar_vecino(idx_vecino, vecindad_de_movimientos, solucion):
        
        if idx_vecino >= len(vecindad_de_movimientos):
            print("\n=== La elección de vecino está fuera de rango. ===")

        # Fijamos el movimiento seleccionado:
        # Ej.: {'maquina': 1, 'operaciones_intercambiadas': (17, 92), 'posiciones': (7, 8)}
        movimiento_seleccionado = vecindad_de_movimientos[idx_vecino]

        print(f"\n=== El movimiento seleccionado es: {movimiento_seleccionado} ===")

        solucion_vecina = copy.deepcopy(solucion) # Hacemos una copia profunda de la `solucion`
                                                  # que modificaremos para crear a su vecino (una
                                                  # copia superficial no basta porque necesitamos
                                                  # que la solución también se quede como estaba).

        # Extraemos la información del movimiento
        maquina = movimiento_seleccionado['maquina']  # OJO: Es 1-based (ej. 1,2,3...)
        pos_i, pos_j = movimiento_seleccionado['posiciones']

        maquina_idx = maquina - 1 # Lo pasamos como índice (0-based para Python)

        # Intercambiamos las posiciones en la máquina correspondiente
        solucion_vecina[maquina_idx][pos_i], solucion_vecina[maquina_idx][pos_j] = \
        solucion_vecina[maquina_idx][pos_j], solucion_vecina[maquina_idx][pos_i]

        # Verificamos que todo esté bien:
        print(f"\n=== La solución sigue siendo {solucion} ===")
        print(f"\n=== La solución vecina es {solucion_vecina} ===")
        if (solucion != solucion_vecina):
            print(f"\n=== El vecino sí es distinto ===")


        return solucion_vecina

    
    @staticmethod
    def evaluar_vecino(solucion_vecina, numero_de_maquinas, numero_de_trabajos, lista_de_vertices):

        # Sólo nos interesa el makespan de la solución vecina.
        makespan_vecino, _, _, _, _, _ = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, lista_de_vertices, solucion_vecina)

        print(f"\n === El makespan del vecino es: {makespan_vecino}")
        return makespan_vecino  