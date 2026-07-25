"""Solución de referencia para agente/ejercicios.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agente import AgenteVentas, cargar_ventas


agente = AgenteVentas(cargar_ventas())

pregunta_1 = "¿Qué producto tuvo la mayor cantidad vendida?"
print(agente.preguntar(pregunta_1))

pregunta_2 = "¿Cuál vendedor tuvo menos ventas?"
print(agente.preguntar(pregunta_2))

print(agente.contexto())
