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
            nueva_info[op_id] = {
                **datos,  # Copiamos igualito lo que ya estaba
                'r': r.get(op_id, 0),  # Usamos 0 como valor por defecto si la clave no existe
                'q': q.get(op_id, 0),  # Usamos 0 como valor por defecto si la clave no existe
                'critica': (r.get(op_id, 0) + q.get(op_id, 0)) == makespan
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
        print("\n=== Estructura 'nueva_info' (operaciones críticas) ===")
        for op_id, datos in nueva_info.items():
            critica = datos['r'] + datos['q'] == makespan
            print(f"Op {op_id}: r={datos['r']}, q={datos['q']}, r+q={datos['r'] + datos['q']} | ¿Crítica? {critica}")
    
    @staticmethod
    def construir_vecindad(solucion, makespan, r, q, info):

        # Construye la estructura auxiliar `nueva_info`:
        nueva_info = Generadora_de_vecinos.construir_nueva_info(makespan, r, q, info)

        vecindad = [] # Lista de vecinos (elegí esto porque como a priori no sabemos
                      # exactamente cuántos vecinos hay no consideré adecuado un 
                      # np.array; pero se puede elegir un np.array de tamaño igual a
                      # la cota superior de los vecinos que es:
                      # numero_maquinas*(numero_jobs - 1) creo).
        
        movimientos = [] # Por si posteriormente queremos implementar búsqueda tabú
                         # (o por si sirve de algo) aquí se guarda el movimiento que
                         # dio lugar a cada vecino.

        print("\n=== Inicio de generación de vecinos ===")

        # Iteramos por cada máquina en la solución:
        for maquina_idx, secuencia in enumerate(solucion):
            print(f"\n--- Máquina {maquina_idx + 1} (secuencia: {secuencia}) ---")

            # Verificamos pares consecutivos en la máquina (para la permutación de 
            # operaciones):
            for i in range(len(secuencia)-1):
                op_actual = secuencia[i]
                op_siguiente = secuencia[i+1]
                print(f"  Verificando par: Op {op_actual} (crítica: {nueva_info[op_actual]['critica']}) y Op {op_siguiente} (crítica: {nueva_info[op_siguiente]['critica']})")

                # Si tenemos dos operaciones críticas consecutivas generamos un vecino
                # con sólo esas dos operaciones permutadas:
                if nueva_info[op_actual]['critica'] and nueva_info[op_siguiente]['critica']:
                    # Creamos una copia de la solución original
                    vecino = [list(m) for m in solucion]
                    # Intercambiamos las operaciones
                    vecino[maquina_idx][i], vecino[maquina_idx][i+1] = vecino[maquina_idx][i+1], vecino[maquina_idx][i]

                    # Registramos el movimiento
                    movimiento = {
                        'maquina': maquina_idx + 1,
                        'operaciones_intercambiadas': (op_actual, op_siguiente),
                        'posiciones': (i, i+1)
                    }

                    vecindad.append(vecino)
                    movimientos.append(movimiento)
                    print(f"  -> Vecino generado: {vecino[maquina_idx]}")
                
                else:
                    print("  -> No se intercambian (al menos una no es crítica)")

        print("\n=== Fin de generación de vecinos ===")
        return vecindad, movimientos # Retornamos dos listas: la vecindad y los movimientos.