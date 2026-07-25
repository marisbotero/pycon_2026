"""Ejercicios cortos en modo demo. Busca TODO y completa una línea."""

from agente import AgenteVentas
from datos import cargar_ventas


agente = AgenteVentas(cargar_ventas())

# Ejercicio 1: cambia la pregunta para consultar el producto con más cantidad.
pregunta_1 = "TODO"
print(agente.preguntar(pregunta_1))

# Ejercicio 2: pregunta por el vendedor con menos ventas.
pregunta_2 = "TODO"
print(agente.preguntar(pregunta_2))

# Ejercicio 3: inspecciona la memoria después de las dos preguntas.
# Pista: usa agente.contexto()
print("TODO")
