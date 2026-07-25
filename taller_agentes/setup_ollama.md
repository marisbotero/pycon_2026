# Preparar Ollama

Ollama ejecuta el modelo del taller localmente. No necesitas una API key.

## Antes del taller

1. Instala Ollama desde [ollama.com](https://ollama.com).
2. Descarga el modelo:

```bash
ollama pull gemma2:2b
```

3. Comprueba que funciona:

```bash
ollama run gemma2:2b "Responde solamente: listo"
```

En la mayoría de instalaciones Ollama queda activo automáticamente. Si el
agente muestra un error de conexión, abre otra terminal y ejecuta:

```bash
ollama serve
```

## Desde Python

```python
from ollama import chat

respuesta = chat(
    model="gemma2:2b",
    messages=[{"role": "user", "content": "Explica qué es un promedio"}],
)
print(respuesta.message.content)
```

El agente del taller usa además `format=ESQUEMA_DECISION` para pedir una salida
JSON predecible.

## Problemas frecuentes

- `connection refused`: inicia `ollama serve`.
- `model not found`: ejecuta `ollama pull gemma2:2b`.
- La respuesta tarda: la primera consulta carga el modelo en memoria.
- El equipo tiene pocos recursos: cierra otras aplicaciones antes del taller.
