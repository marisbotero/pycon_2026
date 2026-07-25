"""Genera el notebook del taller desde una fuente fácil de mantener."""

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
nb = nbf.v4.new_notebook()
cells = []


def md(text: str) -> None:
    cells.append(nbf.v4.new_markdown_cell(text.strip()))


def code(text: str) -> None:
    cells.append(nbf.v4.new_code_cell(text.strip()))


md(
    """
# ✨ De prompts a agentes con Python y Ollama

## Construyamos a Astra, un pequeño oráculo de datos

Una pregunta entra. Una decisión estructurada sale. Python aplica reglas,
pandas actúa y el sistema recuerda lo necesario para la siguiente pregunta.

**Duración:** 2 horas · **Nivel:** Python básico · **Motor:** Ollama local
**Meta:** terminar con un agente propio, comprensible y reutilizable.

> Los prompts son solo el inicio. Lo importante es diseñar el sistema que hay
> alrededor del modelo.
"""
)

md(
    """
## 🗺️ Nuestra ruta

| Hora | Momento | Lo que vas a hacer |
|---|---|---|
| 10:30–10:40 | Bienvenida | Preparar el proyecto y ejecutar una prueba |
| 10:40–10:55 | De instrucción a prompt | Añadir objetivo, contexto y restricciones |
| 10:55–11:10 | Contrato JSON | Convertir texto libre en una decisión confiable |
| 11:10–11:30 | Primer agente | Conectar entrada, modelo, reglas y respuesta |
| 11:30–11:35 | Pausa | Respirar ☕ |
| 11:35–11:50 | Herramientas | Usar pandas para actuar sobre datos reales |
| 11:50–12:05 | Contexto y memoria | Probar seguimiento, `/memoria` y `/clear` |
| 12:05–12:20 | Evaluación | Probar contrato, resultados y errores |
| 12:20–12:27 | Reto final | Enseñarle una pregunta nueva a Astra |
| 12:27–12:30 | Cierre | Síntesis y siguientes pasos |
"""
)

md(
    """
## 📁 El mapa del proyecto

Este notebook explica **por qué** hacemos cada cosa. La carpeta `agente/`
contiene lo que ejecutamos y modificamos.

```text
taller_agentes/
├── Workshop_Agentes.ipynb    ← estás aquí: teoría + recorrido
├── agente/
│   ├── datos.py              ← dataset pequeño
│   ├── agente.py             ← decisión, Ollama, reglas, acción y memoria
│   ├── main.py               ← conversación y comandos
│   ├── ejercicios.py         ← práctica guiada
│   ├── evaluacion.py         ← pruebas de calidad
│   └── reto_final.py         ← desafío de cierre
├── respuestas/               ← soluciones y guía rápida
└── tests/                    ← pruebas automatizadas
```

Durante el taller busca el marcador **✋ Tu turno**. Ahí debes escribir,
ejecutar o modificar algo.
"""
)

md(
    """
# 1. Bienvenida y preparación · 10 minutos

## El pacto del taller

- Ollama ejecuta `gemma2:2b` localmente.
- No usamos API keys.
- El notebook funciona como guía; el agente vive en archivos `.py`.
- El modo `--demo` nos permite continuar si un equipo tiene problemas con el modelo.

En una terminal:

```bash
ollama pull gemma2:2b
ollama serve
```

En otra:

```bash
python -m pip install -r requirements.txt
cd agente
python main.py --demo
```
"""
)

code(
    """
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
if not (ROOT / "agente").exists():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from agente import AgenteVentas, cargar_ventas
from agente.agente import Decision, planificador_demo

df = cargar_ventas()
print(f"✅ Preparación lista: {len(df)} filas, {len(df.columns)} columnas")
df.head()
"""
)

md(
    """
# 2. De instrucción a prompt · 15 minutos

Una instrucción aislada suele ser ambigua:

> “Analiza las ventas”

Un prompt útil funciona como una ficha de trabajo:

1. **Rol:** quién debe actuar.
2. **Objetivo:** qué decisión debe tomar.
3. **Contexto:** con qué datos e historial.
4. **Restricciones:** qué puede y qué no puede hacer.
5. **Formato:** cómo debe entregar el resultado.

La claridad no garantiza que el modelo tenga razón, pero hace que su
comportamiento sea más observable y evaluable.
"""
)

code(
    """
prompt_simple = "Analiza las ventas"

prompt_estructurado = f'''
ROL: Eres el planificador de un agente de ventas.
OBJETIVO: Convierte una pregunta en una operación de análisis.
CONTEXTO: Columnas disponibles: {", ".join(df.columns)}.
RESTRICCIONES:
- Operaciones: promedio, suma o ranking.
- No inventes columnas.
- No calcules todavía el resultado.
FORMATO: Devuelve únicamente una decisión JSON.
'''

print(prompt_estructurado)
"""
)

md(
    """
### ✋ Tu turno — mejorar una instrucción

Transforma `“¿Quién vendió mejor?”` en un prompt con:

- objetivo concreto;
- columnas disponibles;
- al menos dos restricciones;
- formato esperado.

La solución de referencia está en `respuestas/02_prompt_estructurado.md`.
"""
)

code(
    """
# Escribe aquí tu versión.
mi_prompt = '''
TODO
'''
print(mi_prompt)
"""
)

md(
    """
# 3. El contrato JSON · 15 minutos

Texto libre:

> “Creo que deberías agrupar por región y buscar el valor más alto.”

Decisión estructurada:

```json
{
  "operacion": "ranking",
  "columna": "ventas",
  "agrupar_por": "region",
  "orden": "desc",
  "limite": 1
}
```

El JSON es un **contrato** entre el modelo y Python. Podemos validar sus campos
antes de ejecutar cualquier acción.
"""
)

code(
    """
decision = Decision(
    operacion="ranking",
    columna="ventas",
    agrupar_por="region",
    orden="desc",
    limite=1,
)

print(json.dumps(decision.__dict__, ensure_ascii=False, indent=2))
"""
)

md(
    """
## ¿Qué protege el contrato?

- Las operaciones forman una lista cerrada.
- Las columnas numéricas permitidas son `ventas` y `cantidad`.
- Solo agrupamos por `region`, `vendedor` o `producto`.
- `orden` solo puede ser ascendente o descendente.
- Una salida inválida se rechaza antes de tocar los datos.

Mira `ESQUEMA_DECISION` y `aplicar_reglas()` en `agente/agente.py`.
"""
)

code(
    """
from agente.agente import ESQUEMA_DECISION

print(json.dumps(ESQUEMA_DECISION, ensure_ascii=False, indent=2))
"""
)

md(
    """
# 4. Primer agente · 20 minutos

Un agente no es solamente un prompt. Es un ciclo:

```text
pregunta
   ↓ percepción
Ollama propone una decisión JSON
   ↓ reglas
Python valida y normaliza
   ↓ herramienta
pandas calcula sobre datos reales
   ↓ respuesta
JSON final + memoria
```

Astra es el “director de orquesta”: no hace todos los trabajos; coordina
componentes con responsabilidades claras.
"""
)

code(
    """
# Primero observamos el ciclo sin depender de Ollama.
agente_demo = AgenteVentas(df, planificador=planificador_demo)
respuesta = agente_demo.preguntar("¿Cuál region tuvo más ventas?")
print(json.dumps(respuesta, ensure_ascii=False, indent=2))
"""
)

md(
    """
## ¿Dónde entra Ollama?

`crear_planificador_ollama()` envía a `gemma2:2b`:

- la pregunta;
- el contexto reciente;
- reglas y ejemplos;
- el esquema JSON.

Ollama propone la decisión. Después, `aplicar_reglas()` la normaliza. Esta
combinación es importante: **el modelo interpreta; el sistema gobierna**.

Para probar el agente real:

```bash
cd agente
python main.py
```
"""
)

md(
    """
# ☕ Pausa corta · 5 minutos

Checkpoint:

- [ ] Puedo explicar por qué un prompt no es un agente.
- [ ] Entiendo para qué sirve el contrato JSON.
- [ ] Identifico modelo, reglas, herramienta y respuesta.
- [ ] Ya ejecuté una pregunta en modo demo o con Ollama.
"""
)

md(
    """
# 5. Herramientas y acciones · 15 minutos

El modelo **no calcula las ventas**. Solo propone qué hacer. La herramienta
pandas trabaja con el dataset real.

Esto separa dos responsabilidades:

- Ollama interpreta lenguaje natural.
- Python ejecuta una operación verificable.

En este taller no ejecutamos código arbitrario producido por el modelo.
`AgenteVentas.ejecutar()` acepta únicamente decisiones previamente permitidas.
"""
)

code(
    """
preguntas = [
    "¿Cuál vendedor tuvo menos ventas?",
    "¿Qué producto tuvo la mayor cantidad vendida?",
    "¿Cuál es el promedio de ventas?",
]

for pregunta in preguntas:
    respuesta = agente_demo.preguntar(pregunta)
    print(f"\\n{pregunta}\\n→ {respuesta['valor']}")
"""
)

md(
    """
### ✋ Tu turno — seguir el dato

Abre `agente/agente.py` y encuentra:

1. dónde se valida la columna;
2. dónde se aplica `groupby`;
3. dónde se selecciona una posición del ranking;
4. dónde se construye la respuesta final.

Después completa los `TODO` de `agente/ejercicios.py`.

Soluciones: `respuestas/03_herramienta_pandas.md` y
`respuestas/04_ejercicios_solucion.py`.
"""
)

md(
    """
# 6. Contexto y memoria · 15 minutos

Sin memoria:

> “¿Y cuál quedó en segundo lugar?”
> ¿Segundo lugar de qué?

Con memoria, el agente recupera la agrupación de la pregunta anterior.
Conservamos solo los últimos turnos porque más contexto no siempre significa
mejor contexto.
"""
)

code(
    """
agente_memoria = AgenteVentas(df, planificador=planificador_demo, max_memoria=3)

primera = agente_memoria.preguntar("¿Cuál region tuvo más ventas?")
segunda = agente_memoria.preguntar("¿Y cuál quedó en segundo lugar?")

print("Primera:", primera["valor"])
print("Seguimiento:", segunda["valor"])
print("\\nContexto guardado:\\n", agente_memoria.contexto())
"""
)

code(
    """
agente_memoria.limpiar_memoria()
print(agente_memoria.contexto())
"""
)

md(
    """
### ✋ Tu turno — conversación real

Ejecuta `python main.py` y prueba:

```text
¿Cuál region tuvo más ventas?
¿Y cuál quedó en segundo lugar?
/memoria
/clear
/memoria
```

Observa qué información desaparece después de `/clear`.
"""
)

md(
    """
# 7. Evaluación · 15 minutos

Una demo responde una pregunta. Un sistema necesita demostrar que responde de
forma consistente.

Evaluaremos cuatro capas:

| Capa | Pregunta |
|---|---|
| Contrato | ¿Están todas las claves del JSON? |
| Decisión | ¿Usó operación, columna y orden correctos? |
| Resultado | ¿Coincide con un valor esperado? |
| Robustez | ¿Rechaza columnas y operaciones no permitidas? |

Ejecuta también `python agente/evaluacion.py` y `pytest -q`.
"""
)

code(
    """
casos = [
    ("¿Cuál region tuvo más ventas?", "Sur"),
    ("¿Cuál vendedor tuvo menos ventas?", "Pedro"),
    ("¿Cuál es el promedio de ventas?", 1500.0),
]

for pregunta, esperado in casos:
    respuesta = AgenteVentas(df).preguntar(pregunta)
    valor = respuesta["valor"]
    obtenido = valor.get("nombre") if isinstance(valor, dict) else valor
    contrato_ok = {"valor", "explicacion", "decision", "consistencia"} <= respuesta.keys()
    print("✅" if contrato_ok and obtenido == esperado else "❌", pregunta)
"""
)

code(
    """
# Caso de error controlado
try:
    AgenteVentas(df).ejecutar(Decision("suma", "salario"))
except ValueError as error:
    print("✅ Error capturado:", error)
"""
)

md(
    """
# 8. Reto final · 7 minutos

Abre `agente/reto_final.py`.

Tu misión:

1. formula una pregunta nueva que use `producto` y `cantidad`;
2. ejecuta el agente;
3. añade un `assert` con la respuesta esperada;
4. si terminas pronto, agrega el caso a `agente/evaluacion.py`.

No necesitas cambiar la arquitectura. Esa es precisamente la señal de que el
framework es reutilizable.

Solución de referencia: `respuestas/05_reto_final_solucion.py`.
"""
)

md(
    """
# 9. Cierre · 3 minutos

Empezamos con una instrucción ambigua y terminamos con un sistema que:

- diseña prompts con objetivo, contexto y restricciones;
- exige una decisión JSON;
- usa Ollama local para interpretar;
- aplica reglas explícitas;
- actúa con pandas sobre información real;
- conserva y limpia memoria;
- evalúa contrato, resultado y errores.

## La idea para llevar

> Un buen sistema de IA no confía ciegamente en una respuesta: diseña el
> contexto, limita las acciones, verifica el resultado y hace visible el ciclo.

Siguiente parada: `agente/README.md`. Allí está tu Astra para seguir
experimentando después del taller.
"""
)

nb["cells"] = cells
nb["metadata"] = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.10"},
}
nbf.write(nb, ROOT / "Workshop_Agentes.ipynb")
print(f"Notebook generado: {len(cells)} celdas")
