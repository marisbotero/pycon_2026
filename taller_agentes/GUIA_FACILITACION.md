# Guía de facilitación · 2 horas

Esta guía es para quien dirige el taller. El notebook es para participantes.

## Antes de abrir la sala

- Confirmar que `ollama list` muestra `gemma2:2b`.
- Ejecutar `python verificar_instalacion.py`.
- Ejecutar `PYTHONPATH=. pytest -q`.
- Ejecutar una conversación con `python agente/main.py`.
- Tener preparado `python agente/main.py --demo` como plan B.
- Compartir el repositorio y un QR hacia `taller_agentes/README.md`.

## Ritmo

| Hora | Objetivo | Checkpoint |
|---|---|---|
| 10:30 | Crear confianza | Todas las personas ven el dataset |
| 10:40 | Mostrar la ambigüedad | El grupo identifica qué le falta al prompt |
| 10:55 | Presentar el contrato | Todos pueden leer la decisión JSON |
| 11:10 | Revelar el agente | Identifican modelo, reglas, herramienta y respuesta |
| 11:30 | Pausa | Confirmar quién necesita ayuda |
| 11:35 | Darle manos al agente | pandas produce un resultado verificable |
| 11:50 | Darle memoria | Funciona “¿y el segundo?” |
| 12:05 | De demo a sistema | Los casos muestran ✅ o un error comprensible |
| 12:20 | Apropiación | Cada persona cambia una pregunta y un `assert` |
| 12:27 | Cierre | Repetir la idea: el modelo interpreta, el sistema gobierna |

## Preguntas para activar la sala

- ¿Qué podría significar “vendió mejor”?
- ¿Qué parte de la decisión debería controlar el modelo?
- ¿Qué parte nunca deberíamos dejar sin validar?
- ¿Qué necesita recordar el agente para entender “el segundo”?
- ¿Qué prueba te haría confiar un poco más en esta respuesta?

## Qué recortar si el tiempo se comprime

1. Mantener prompt, JSON, primer agente y evaluación.
2. Hacer `ejercicios.py` en parejas.
3. Mostrar `/clear` en vivo en vez de esperar a todos.
4. Convertir el reto final en tarea posterior.

## Plan B

Si Ollama no responde en varios equipos:

```bash
cd agente
python main.py --demo
```

El aprendizaje central se conserva: entrada, decisión, reglas, herramienta,
respuesta, memoria y evaluación. Recuperar la llamada real a Ollama al final.

## Promesa y evidencia

| Prometemos | Evidencia en el taller |
|---|---|
| Prompts con contexto y restricciones | Sección 2 + ejercicio |
| Respuestas JSON confiables | Sección 3 + esquema |
| Agente funcional en Python | `agente/agente.py` y `main.py` |
| Contexto y memoria | Sección 6 + `/memoria` + `/clear` |
| Evaluar calidad y consistencia | Sección 7 + `evaluacion.py` + tests |
| Framework reutilizable | Decisión, planificador y ejecutor desacoplados |
