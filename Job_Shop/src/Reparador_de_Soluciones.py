from Operador_de_Listas import *
import random

class Reparador_de_Soluciones:
    
    
    @staticmethod 
    def reparar(intento_de_solucion, lista_de_vertices,info = False):
        
        numero_de_maquinas = len(intento_de_solucion)
        numero_de_trabajos = len(intento_de_solucion[0])
        
        orden_global = []
        
        
        sigue_en_job = [x*numero_de_trabajos+1 for x in range (numero_de_maquinas)] # Es la O_J del artículo.
        sigue_en_maquina = [intento_de_solucion[x][0]   for x in range(numero_de_maquinas)] # Es la O_M del artículo.
        if info:
            print ("sig maqu {}".format(sigue_en_maquina))
            
            print ("sig job {}".format(sigue_en_job))
        # `sigue_en_<algo>` es una lista donde se van guardando iteración a iteración
        # cuáles son las siguientes operaciones acorde al orden dado por los jobs o
        # las máquinas.

        planificables = [] # Lista de operaciones en la intersección de O_J y O_M

        etiquetadas = [] # Lista de operaciones que ya han pasado por el proceso de
                         # reparación i.e. ya han sido planificadas.

        # Lista de indices de los jobs que ya han sido planificados por máquina
        lista_de_indices_job = [0 for _ in range (numero_de_maquinas)] 
       
        
        while len (planificables  )< numero_de_maquinas*numero_de_trabajos:
            
            # Generamos la interseccion de operaciones que nos indica que jobs podemos planificar.
            planificables = Operador_de_Listas.interseccion(lista1=sigue_en_job,lista2=sigue_en_maquina)
            
            
            
            '''
            CASO CURSEADO DE REPARACION
            '''
            if not planificables:
                operacion_elegida_id = random.choice(sigue_en_job)
                
            
            if info:
                print ("Planificables .{}".format(planificables))
            
            
           
                
             #Planificamos un job 
            aleatorio = random.randint(0, len (planificables)-1)
            job_planificado = planificables.pop(aleatorio)
                        
            
            if info:
                
                print ("Job Planificado : {}".format(job_planificado))
                print ("Planificables {}".format(planificables))

            
            
            #Actualizamos las O_M y O_J 
            
            # O_J
            if job_planificado % numero_de_trabajos != 0:
                #Caso de sucesor
                sigue_en_job[job_planificado // numero_de_trabajos]+=1
            else:
                #Caso donde no hay sucesor
                sigue_en_job.pop(job_planificado // numero_de_trabajos)
                
                
            # O_M
            if lista_de_indices_job[lista_de_vertices[job_planificado].get_maquina()] <numero_de_trabajos:
                # Caso donde hay sucesor
                lista_de_indices_job [lista_de_vertices[job_planificado].get_maquina()]+=1
                sigue_en_maquina[lista_de_vertices[job_planificado].get_maquina()-1] =intento_de_solucion[lista_de_vertices[job_planificado].get_maquina()-1][lista_de_indices_job [lista_de_vertices[job_planificado].get_maquina()]]
                
                
            else:
                # Caso donde no hay sucesor
                sigue_en_maquina.pop(lista_de_vertices[job_planificado].get_maquina())
            
            if info:
                print ("------------------------------Actualizacion-------------------------------")
                
                
                print ("sig maqu {}".format(sigue_en_maquina))
                
                print ("sig job {}".format(sigue_en_job))
                print ("Job Planificado : {}".format(job_planificado))
                print ("Planificables {}".format(planificables))
            
            return 
            
            
        
            
