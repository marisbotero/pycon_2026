"""Agente didáctico: pregunta -> decisión JSON -> herramienta -> respuesta."""

import json
from dataclasses import asdict, dataclass
from typing import Any, Callable, Optional

import pandas as pd


@dataclass
class Decision:
    operacion: str
    columna: str = "ventas"
    agrupar_por: Optional[str] = None
    orden: str = "desc"
    limite: int = 1


ESQUEMA_DECISION = {
    "type": "object",
    "properties": {
        "operacion": {"type": "string", "enum": ["promedio", "suma", "ranking"]},
        "columna": {"type": "string", "enum": ["ventas", "cantidad"]},
        "agrupar_por": {
            "anyOf": [
                {"type": "string", "enum": ["region", "vendedor", "producto"]},
                {"type": "null"},
            ]
        },
        "orden": {"type": "string", "enum": ["asc", "desc"]},
        "limite": {"type": "integer", "minimum": 1, "maximum": 10},
    },
    "required": ["operacion", "columna", "agrupar_por", "orden", "limite"],
}


def aplicar_reglas(pregunta: str, contexto: str, decision: Decision) -> Decision:
    """Normaliza la propuesta del LLM con reglas explícitas del sistema."""
    texto = pregunta.lower()
    agrupacion = next(
        (campo for campo in ("region", "vendedor", "producto") if campo in texto),
        decision.agrupar_por,
    )
    if agrupacion is None and "segundo" in texto:
        agrupacion = next(
            (campo for campo in ("region", "vendedor", "producto") if campo in contexto.lower()),
            None,
        )
    if any(palabra in texto for palabra in ("más", "mayor", "menos", "menor", "segundo")):
        decision.operacion = "ranking"
    if any(palabra in texto for palabra in ("menos", "menor")):
        decision.orden = "asc"
    elif any(palabra in texto for palabra in ("más", "mayor", "segundo")):
        decision.orden = "desc"
    decision.limite = 2 if "segundo" in texto else 1
    decision.columna = "cantidad" if "cantidad" in texto else decision.columna
    decision.agrupar_por = agrupacion
    return decision


def crear_planificador_ollama(modelo: str = "gemma2:2b") -> Callable[[str, str], Decision]:
    """Crea el planificador real del taller usando Ollama local."""
    from ollama import chat

    def planificar(pregunta: str, contexto: str) -> Decision:
        prompt = f"""
Eres el planificador de un agente que analiza un dataset de ventas.
Convierte la pregunta en una decisión JSON. No calcules la respuesta.

Columnas numéricas: ventas, cantidad.
Agrupaciones permitidas: region, vendedor, producto.
Reglas:
- "más", "mayor", "menos", "menor" y "segundo" siempre usan ranking.
- "total de todas las ventas" usa suma sin agrupación.
- "ventas por región" usa suma agrupada.
- "promedio" usa promedio.
Usa orden="asc" para menor y orden="desc" para mayor.
Para "segundo lugar", usa limite=2 y conserva la agrupación del contexto.

Ejemplos:
"¿Cuál región tuvo más ventas?" -> ranking, ventas, region, desc, 1
"¿Cuál vendedor tuvo menos ventas?" -> ranking, ventas, vendedor, asc, 1
"¿Cuál es el promedio de ventas?" -> promedio, ventas, null, desc, 1

Contexto reciente:
{contexto}

Pregunta:
{pregunta}
"""
        respuesta = chat(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
            format=ESQUEMA_DECISION,
            options={"temperature": 0},
        )
        datos = json.loads(respuesta.message.content)
        return aplicar_reglas(pregunta, contexto, Decision(**datos))

    return planificar


def planificador_demo(pregunta: str, contexto: str) -> Decision:
    """Planificador determinista para poder trabajar incluso sin internet."""
    texto = pregunta.lower()
    agrupar = next((c for c in ("region", "vendedor", "producto") if c in texto), None)
    if agrupar is None and "segundo" in texto:
        agrupar = next((c for c in ("region", "vendedor", "producto") if c in contexto.lower()), None)
    columna = "cantidad" if "cantidad" in texto else "ventas"

    if "promedio" in texto or "media" in texto:
        return Decision("promedio", columna, agrupar)
    if "total" in texto or "suma" in texto:
        return Decision("suma", columna, agrupar)
    if "menos" in texto or "menor" in texto or "mínim" in texto:
        return Decision("ranking", columna, agrupar, "asc", 1)
    if "segundo" in texto:
        return Decision("ranking", columna, agrupar, "desc", 2)
    return Decision("ranking", columna, agrupar, "desc", 1)


class AgenteVentas:
    """Coordina planificación, ejecución, respuesta estructurada y memoria."""

    def __init__(
        self,
        datos: pd.DataFrame,
        planificador: Callable[[str, str], Decision] = planificador_demo,
        max_memoria: int = 3,
    ):
        self.datos = datos.copy()
        self.planificador = planificador
        self.max_memoria = max_memoria
        self.memoria: list[dict[str, Any]] = []

    def contexto(self) -> str:
        if not self.memoria:
            return "Sin conversaciones anteriores."
        lineas = []
        for turno in self.memoria[-self.max_memoria :]:
            respuesta = turno["respuesta"]
            resumen = respuesta["valor"]
            if resumen is None:
                resumen = respuesta.get("mensaje", "Sin resultado")
            lineas.append(f"P: {turno['pregunta']}\nR: {resumen}")
        return "\n".join(lineas)

    def limpiar_memoria(self) -> None:
        """Elimina el historial de la conversación."""
        self.memoria.clear()

    def ejecutar(self, decision: Decision) -> Any:
        if decision.columna not in {"ventas", "cantidad"}:
            raise ValueError("Columna no permitida")
        if decision.agrupar_por not in {None, "region", "vendedor", "producto"}:
            raise ValueError("Agrupación no permitida")

        serie = self.datos[decision.columna]
        if decision.agrupar_por:
            serie = self.datos.groupby(decision.agrupar_por)[decision.columna].sum()

        if decision.operacion == "promedio":
            return round(float(serie.mean()), 2)
        if decision.operacion == "suma":
            return float(serie.sum())
        if decision.operacion == "ranking":
            ordenado = serie.sort_values(ascending=decision.orden == "asc")
            posicion = min(decision.limite, len(ordenado)) - 1
            if decision.agrupar_por:
                return {"nombre": str(ordenado.index[posicion]), "valor": float(ordenado.iloc[posicion])}
            return float(ordenado.iloc[posicion])
        raise ValueError(f"Operación no soportada: {decision.operacion}")

    def _limitacion_de_datos(self, pregunta: str) -> Optional[dict[str, Any]]:
        """Detecta preguntas que requieren información inexistente."""
        texto = pregunta.lower()
        palabras_temporales = {"mes", "mensual", "fecha", "año", "enero", "febrero",
                               "marzo", "abril", "mayo", "junio", "julio", "agosto",
                               "septiembre", "octubre", "noviembre", "diciembre"}
        columnas_temporales = {"fecha", "mes", "año"}

        requiere_tiempo = any(palabra in texto for palabra in palabras_temporales)
        tiene_tiempo = bool(columnas_temporales & set(self.datos.columns))
        if requiere_tiempo and not tiene_tiempo:
            mensaje = (
                "No puedo responder consultas mensuales porque el dataset "
                "no contiene una columna de fecha, mes o año."
            )
            return {
                "estado": "no_disponible",
                "valor": None,
                "explicacion": mensaje,
                "decision": None,
                "consistencia": None,
                "mensaje": mensaje,
            }
        return None

    def preguntar(self, pregunta: str) -> dict[str, Any]:
        limitacion = self._limitacion_de_datos(pregunta)
        if limitacion:
            self.memoria.append({"pregunta": pregunta, "respuesta": limitacion})
            return limitacion

        decision = self.planificador(pregunta, self.contexto())
        valor = self.ejecutar(decision)
        respuesta = {
            "estado": "listo",
            "valor": valor,
            "explicacion": f"El resultado calculado es {valor}.",
            "decision": asdict(decision),
            "consistencia": str(valor) in f"El resultado calculado es {valor}.",
            "mensaje": None,
        }
        self.memoria.append({"pregunta": pregunta, "respuesta": respuesta})
        return respuesta
