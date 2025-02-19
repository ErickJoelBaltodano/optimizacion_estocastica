# Este usa: Reader_and_Writer_VAde, Vertice_VAde, e Intento_Solution_Generator.
# Con el prueba3.txt.
# Generar solución aleatoria y calcular el makespan
generar_sol_aleatoria_y_makespan: 
	@python3 Version_Ade.py

# Información de uso
info:
	@echo "Para ejecutar el programa, usa:"
	@echo "make job-shop DOCUMENTO=nombre_del_ejemplar"
	@echo "El ejemplar debe estar en la carpeta 'Ejemplares'"
	@echo "Ejemplo:"
	@echo "make job-shop DOCUMENTO=swv10"



# Ejecutar la búsqueda por vecindades con un ejemplar específico
job-shop:
	@python3 Busqueda_Por_Vecindades.py $(DOCUMENTO)
