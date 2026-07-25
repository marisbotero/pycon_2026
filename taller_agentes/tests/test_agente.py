from agente.agente import AgenteVentas, Decision, aplicar_reglas
from agente.datos import cargar_ventas


def test_region_con_mas_ventas():
    respuesta = AgenteVentas(cargar_ventas()).preguntar("¿Cuál region tuvo más ventas?")
    assert respuesta["valor"] == {"nombre": "Sur", "valor": 4300.0}
    assert respuesta["consistencia"] is True


def test_memoria_conserva_ultimos_turnos():
    agente = AgenteVentas(cargar_ventas(), max_memoria=1)
    agente.preguntar("¿Cuál es el promedio de ventas?")
    agente.preguntar("¿Cuál vendedor tuvo menos ventas?")
    assert "vendedor" in agente.contexto().lower()
    assert "promedio" not in agente.contexto().lower()


def test_memoria_resuelve_pregunta_de_seguimiento():
    agente = AgenteVentas(cargar_ventas())
    agente.preguntar("¿Cuál region tuvo más ventas?")
    respuesta = agente.preguntar("¿Y cuál quedó en segundo lugar?")
    assert respuesta["valor"] == {"nombre": "Centro", "valor": 4200.0}


def test_reglas_corrigen_una_decision_inconsistente():
    propuesta = Decision("suma", "ventas", "vendedor", "desc", 2)
    decision = aplicar_reglas("¿Cuál vendedor tuvo menos ventas?", "", propuesta)
    assert decision == Decision("ranking", "ventas", "vendedor", "asc", 1)


def test_clear_elimina_la_memoria():
    agente = AgenteVentas(cargar_ventas())
    agente.preguntar("¿Cuál es el promedio de ventas?")
    agente.limpiar_memoria()
    assert agente.contexto() == "Sin conversaciones anteriores."


def test_consulta_mensual_sin_fecha_no_inventa_resultado():
    agente = AgenteVentas(cargar_ventas())
    respuesta = agente.preguntar("¿Cuáles fueron las ventas del mes?")
    assert respuesta["estado"] == "no_disponible"
    assert respuesta["valor"] is None
    assert respuesta["decision"] is None
    assert "fecha" in respuesta["mensaje"].lower()
    assert "no contiene" in agente.contexto().lower()
