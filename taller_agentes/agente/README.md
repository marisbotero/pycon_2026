# 🔮 Astra: tu agente de datos

Esta es la carpeta que vas a tocar durante el taller. Astra recibe una
pregunta, pide a Ollama una decisión JSON, aplica reglas, consulta los datos con
pandas y guarda la interacción en memoria.

## Ejecutar con Ollama

```bash
ollama serve
```

En otra terminal:

```bash
python main.py
```

El modelo predeterminado es `gemma2:2b`. Puedes cambiarlo:

```bash
OLLAMA_MODEL=otro-modelo python main.py
```

## Comandos

- `/memoria`: muestra las interacciones recientes.
- `/clear`: elimina el historial.
- `/salir`: termina el programa.

## Modo de respaldo

```bash
python main.py --demo
```

Usa reglas deterministas, pero conserva el mismo ciclo del agente.

## Archivos para explorar

| Archivo | Propósito |
|---|---|
| `datos.py` | Dataset del taller |
| `agente.py` | Decisión, Ollama, reglas, acción y memoria |
| `main.py` | Conversación y comandos |
| `ejercicios.py` | Práctica guiada |
| `evaluacion.py` | Tres casos de calidad |
| `reto_final.py` | Desafío de cierre |

## Secuencia sugerida

```bash
python main.py --demo
python ejercicios.py
python evaluacion.py
python reto_final.py
python main.py
```

Prueba esta conversación:

```text
¿Cuál region tuvo más ventas?
¿Y cuál quedó en segundo lugar?
/memoria
/clear
```

> Astra no ejecuta código arbitrario del modelo. Ollama propone una decisión
> limitada y Python decide si puede ejecutarse.

Cuando termines un ejercicio, compara tu trabajo con el índice de
`../respuestas/README.md`.
