# Solución: Ejercicio 1 - Identificar Componentes del Agente

## Flujo completo

```
1. Usuario pregunta: "¿Cuántas ventas hubo en la región Norte?"

2. LLM genera:
   df[df['region'] == 'Norte']['ventas'].sum()

3. Python ejecuta → Resultado: 4700

4. LLM explica:
   "La región Norte registró 4,700 en ventas totales,
    lo que la hace líder en el dataset."
```

## Respuestas

### A) Componente de PERCEPCIÓN
**Respuesta:** Paso 1 - La pregunta del usuario

**Por qué:** La percepción es cuando el agente recibe información del entorno (la pregunta del usuario) y el contexto disponible (el dataset).

---

### B) Componente de RAZONAMIENTO
**Respuesta:** Paso 2 - El LLM decide generar código pandas

**Por qué:** El razonamiento es cuando el modelo piensa qué acción ejecutar. En este caso, decide: "voy a filtrar por región 'Norte' y sumar las ventas".

**Nota importante:** Es el LLM quién elige QUÉ código escribir, no el humano. Eso es lo que lo hace "inteligente".

---

### C) Componente de HERRAMIENTA
**Respuesta:** Paso 3 - Python ejecuta el código y obtiene 4700

**Por qué:** La herramienta es la acción real que se ejecuta. En este caso:
- Pandas filtra el DataFrame
- Calcula la suma
- Devuelve un resultado verificable

**Diferencia con prompts:** Un prompt simple aquí diría "aproximadamente 4500". El agente ejecuta de VERDAD y obtiene 4700.

---

### D) Componente de RESPUESTA
**Respuesta:** Paso 4 - El LLM explica el resultado en lenguaje natural

**Por qué:** Después de obtener el resultado técnico (4700), el LLM lo convierte en una explicación clara para el humano.

**En formato JSON:**
```json
{
  "valor": "4700",
  "explicacion": "La región Norte registró 4,700 en ventas totales.",
  "insight": "Lo que la hace líder en el dataset."
}
```

---

## Resumen visual

```
┌─────────────────────────────────────────┐
│  Componentes del Agente                 │
├─────────────────────────────────────────┤
│                                         │
│  👁 PERCEPCIÓN                          │
│  └─ "¿Cuántas ventas en Norte?"         │
│                                         │
│  🧠 RAZONAMIENTO                        │
│  └─ "Voy a filtrar y sumar"             │
│  └─ Genera: df[df['region']...].sum()   │
│                                         │
│  🛠 HERRAMIENTA                         │
│  └─ Python ejecuta → 4700               │
│                                         │
│  💬 RESPUESTA                           │
│  └─ Explica: "La región Norte..."       │
│  └─ Formato: JSON estructurado          │
│                                         │
└─────────────────────────────────────────┘
```

---

## Puntos clave para entender

1. **PERCEPCIÓN ≠ RAZONAMIENTO**
   - Percepción: datos que entra
   - Razonamiento: decisión de qué hacer

2. **RAZONAMIENTO ≠ HERRAMIENTA**
   - Razonamiento: el LLM DECIDE qué código
   - Herramienta: Python EJECUTA ese código

3. **HERRAMIENTA ≠ RESPUESTA**
   - Herramienta: resultado crudo (4700)
   - Respuesta: explicación clara para humanos

4. **El ciclo completo es lo que hace que sea un AGENTE**
   - Si solo tienes LLM + prompt = No es un agente
   - Si tienes Percepción + Razonamiento + Herramienta + Respuesta = Sí es un agente

---

## Ejercicio adicional

**¿Dónde está la MEMORIA en este flujo?**

Hint: Si después preguntases "¿Y cuál quedó en segundo lugar?", ¿qué información necesitaría recordar el agente?

Respuesta: El resultado anterior (que Norte fue el primero). Esto es lo que permite preguntas de seguimiento.
