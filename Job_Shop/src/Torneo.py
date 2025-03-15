from Calculadora_makespan_VAde import *


class Torneo:
    #No retornamos nada porque los cambios son en la memoria
    
    @staticmethod
    def hijos_vs_poblacion (poblacion,hijo1, hijo2,numero_de_maquinas,numero_de_trabajos,lista_de_vertices):
        # Generar el primer número
        numero1 = random.randint(0, len(poblacion)-1)

        # Generar el segundo número diferente al primero
        while True:
            numero2 = random.randint(0, len(poblacion)-1)
            if numero2 != numero1:
                break
         
        '''
        
        888                                                                        888                                                                        
        888                                                                        888
        888                                                                        888
        888888 .d88b. 888  888888d88888888b.  8888b. 88888b.d88b.  .d88b. 88888b.  888888
        888   d88""88b888  888888P"  888 "88b    "88b888 "888 "88bd8P  Y8b888 "88b 888
        888   888  888888  888888    888  888.d888888888  888  88888888888888  888 888
        Y88b. Y88..88PY88b 888888    888  888888  888888  888  888Y8b.    888  888 y88b
        "Y888 "Y88P"  "Y88888888    888  888"Y888888888  888  888 "Y8888 888  888  "Y888 
        
        
                          !                         !
               !          |>>>                      |>>>        !
               |>>>       |>>>                      |>>>        | >>>
               |          |>>>                      |>>>        |
              .|.         |_________________________|          .|.
            /     \       |WWWWWWWWWWWWWWWWWWWWWWWWW|        /     \     
          /         \     |    )~~~~~~~~~~~~~~~(    |      /         \               
        /             \   |   (                 )   |    /             \    
      /                 \ |   )                 (   |  /                 \    
     #################### |  (                   )  | WWWWWWWWWWWWWWWWWWWW
     |[ ] [ ] [] [ ] [ ]| |  )                   (  | |/\/\/\/\/\/\/\/\/\|
     | |   |  /\  |   | | | (                     ) | | |   |  /\  |   | | 
     | |   | /  \ |   | | |=<_____________________>=| | |   | /  \ |   | |
     | |   ||    ||   | | | )                     ( | | |   ||    ||   | |
     | |   ||    ||   | | |(!!!!!!!!!!!!!!!!!!!!!!!)| | |   ||    ||   | |
     | |   ||____||   | | |)_| |___| |___| |___| |_(| | |   ||____||   | |
     |_|___||    ||___|_| |(_| |___| |___| |___| |_)| |_|___||    ||___|_|    
                          |)_|_|___|_|___|_|___|_|_(|
                            
        
        
        ''' 
        contendiente1, r1, q1, t1, d1, info1 = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, 
                                                                             lista_de_vertices, poblacion[numero1])
        
        contendiente2, r2, q2, t2, d2, info2 = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, 
                                                                             lista_de_vertices, poblacion[hijo1])
        
       
        
        if (contendiente1 > contendiente2):
            self.poblacion[numero1]= hijo1
            
        contendiente1, r1, q1, t1, d1, info1 = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, 
                                                                             lista_de_vertices, poblacion[numero2])
        
        contendiente2, r2, q2, t2, d2, info2 = Evaluador_Makespan.calculadora_makespan(numero_de_maquinas, numero_de_trabajos, 
                                                                             lista_de_vertices, poblacion[hijo2])
        
       
        
        if (contendiente1 > contendiente2):
            self.poblacion[numero2]= hijo2
            
        
            
        