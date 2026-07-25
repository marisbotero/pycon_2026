"""Reto final: completa una pregunta nueva sin cambiar la arquitectura."""

from agente import AgenteVentas
from datos import cargar_ventas


agente = AgenteVentas(cargar_ventas())

# TODO: cambia esta pregunta por una que use producto y cantidad.
pregunta = "¿Qué producto tuvo la mayor cantidad vendida?"

respuesta = agente.preguntar(pregunta)
print(respuesta)

# TODO: escribe una comprobación para el resultado esperado.
# assert respuesta["valor"]["nombre"] == "..."
