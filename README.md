# 🔮 De prompts a agentes

### Un taller de Python + Ollama para diseñar sistemas que deciden, actúan y recuerdan

Los prompts son solo el inicio. En dos horas construiremos **Astra**, un
pequeño oráculo de datos que transforma preguntas en decisiones JSON, aplica
reglas, usa pandas como herramienta y conserva contexto para la siguiente
interacción.

```text
“¿Cuál región vendió más?”
              ↓
       Ollama interpreta
              ↓
     decisión JSON validada
              ↓
       pandas calcula
              ↓
      respuesta verificable ✨
```

## Lo que te llevas

- Un agente local, sin API keys.
- Un contrato JSON entre el modelo y Python.
- Memoria conversacional con `/memoria` y `/clear`.
- Evaluaciones de resultados, consistencia y errores.
- Un framework pequeño que puedes adaptar a tus propios datos.

## El taller

| Momento | Construimos |
|---|---|
| Prompt | Objetivo + contexto + restricciones |
| Contrato | Una decisión JSON confiable |
| Agente | Entrada + Ollama + reglas + respuesta |
| Herramientas | Acciones verificables con pandas |
| Memoria | Preguntas de seguimiento |
| Evaluación | Pruebas antes de confiar |
| Reto | Una capacidad nueva para Astra |

## Empieza aquí

1. Lee la [guía del taller](taller_agentes/README.md).
2. Sigue la [guía paso a paso](taller_agentes/GUIA_PASO_A_PASO.md).
3. Abre [Workshop_Agentes.ipynb](taller_agentes/Workshop_Agentes.ipynb).
4. Construye tu agente en [taller_agentes/agente](taller_agentes/agente).

**Duración:** 2 horas · **Nivel:** Python básico · **Motor:** Ollama local
**PyCon 2026** · Taller práctico
