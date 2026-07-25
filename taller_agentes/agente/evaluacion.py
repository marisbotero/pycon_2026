"""Evaluación mínima del agente: contrato, consistencia y errores."""

from agente import AgenteVentas
from datos import cargar_ventas


def ejecutar_evaluacion() -> None:
    agente = AgenteVentas(cargar_ventas())
    casos = [
        ("¿Cuál region tuvo más ventas?", "Sur"),
        ("¿Cuál vendedor tuvo menos ventas?", "Pedro"),
        ("¿Cuál es el promedio de ventas?", 1500.0),
    ]

    aprobados = 0
    for pregunta, esperado in casos:
        respuesta = agente.preguntar(pregunta)
        valor = respuesta["valor"]
        valor_simple = valor.get("nombre") if isinstance(valor, dict) else valor
        contrato_ok = {"valor", "explicacion", "decision", "consistencia"} <= respuesta.keys()
        resultado_ok = valor_simple == esperado
        ok = contrato_ok and resultado_ok and respuesta["consistencia"]
        aprobados += int(ok)
        print(f"{'✅' if ok else '❌'} {pregunta}")

    print(f"\nResultado: {aprobados}/{len(casos)} casos aprobados")

    mensual = agente.preguntar("¿Cuáles fueron las ventas del mes?")
    limitacion_ok = (
        mensual["estado"] == "no_disponible"
        and mensual["valor"] is None
        and "fecha" in mensual["mensaje"].lower()
    )
    print(f"{'✅' if limitacion_ok else '❌'} Consulta mensual sin datos temporales")


if __name__ == "__main__":
    ejecutar_evaluacion()
