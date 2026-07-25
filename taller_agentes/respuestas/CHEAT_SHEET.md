# Guía rápida: Ollama + agente

## Preparación

```bash
ollama pull gemma2:2b
ollama serve
python -m pip install -r requirements.txt
```

## Flujo

```text
pregunta
  ↓
Ollama genera una decisión JSON
  ↓
Python valida la decisión
  ↓
pandas ejecuta una operación permitida
  ↓
respuesta estructurada + memoria
```

## Llamada mínima

```python
from ollama import chat

respuesta = chat(
    model="gemma2:2b",
    messages=[{"role": "user", "content": "Devuelve una decisión JSON"}],
    format=ESQUEMA_DECISION,
    options={"temperature": 0},
)
```

## Decisión del agente

```json
{
  "operacion": "ranking",
  "columna": "ventas",
  "agrupar_por": "region",
  "orden": "desc",
  "limite": 1
}
```

Operaciones permitidas: `promedio`, `suma`, `ranking`.

Agrupaciones permitidas: `region`, `vendedor`, `producto`.

## Ejecutar

```bash
cd agente
python main.py
```

Modo de respaldo para practicar sin el modelo:

```bash
python main.py --demo
```
