# Makefile
   
# --- Reglas principales ---
.PHONY: no_dominados

# Para probar la generadora de puntos no-dominados (ejemplar por defecto: DLTZ1)
no_dominados:
	@python3 src/main_cuadratico.py

# Para probar la codificadora-decodificadora de vectores de reales-bits
codificar-decodificar:
	@python3 NSGA-II/src/main_codificacion.py

# Un intento del NSGA-II 
nsga2:
	@python3 NSGA-II/src/main_nsga2.py

rwga:
	@python3 RWGA/src/main.py