"""Solución de referencia para agente/reto_final.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agente import AgenteVentas, cargar_ventas


agente = AgenteVentas(cargar_ventas())
pregunta = "¿Qué producto tuvo la mayor cantidad vendida?"
respuesta = agente.preguntar(pregunta)

print(respuesta)
assert respuesta["valor"]["nombre"] == "B"
