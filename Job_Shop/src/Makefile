.PHONY: generar_sol_aleatoria_y_makespan info Entrega1 Entrega2 clean-results

# Información de uso
info:
	@echo "USO DEL PROGRAMA:"
	@echo "------------------------------------------------------------"
	@echo "Para ejecutar la búsqueda con un ejemplar específico:"
	@echo "  make Entrega1 DOCUMENTO=<nombre> [ITER=<iteraciones>]"
	@echo ""
	@echo "Donde:"
	@echo "  <nombre>       = Nombre del archivo SIN extensión (.txt)"
	@echo "                   (Debe estar en la carpeta 'Ejemplares')"
	@echo "  <iteraciones>  = Número de iteraciones (opcional)"
	@echo "                   Valor por defecto: 100"
	@echo ""
	@echo "Ejemplos:"
	@echo "  make Entrega1 DOCUMENTO=swv10        # 100 iteraciones"
	@echo "  make Entrega1 DOCUMENTO=mi_ejemplo ITER=500"
	@echo "------------------------------------------------------------\n"

# Ejecutar la búsqueda con parámetros
Entrega1:
	@python3 Main_Entrega1.py $(DOCUMENTO) $(ITER)

# Otras reglas (mantenidas sin cambios)
Entrega2:
	@python3 Main_Entrega2.py $(DOCUMENTO)

clean-results:
	@cd Resultados
	@rm *