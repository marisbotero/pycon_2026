# 👣 Guía paso a paso del participante

Usa esta guía junto con `Workshop_Agentes.ipynb`. No tienes que memorizar los
comandos: avanza una estación a la vez.

## Estación 0 · Preparar

### Abre

Una terminal en `taller_agentes/`.

### Ejecuta

```bash
source .venv/bin/activate
ollama list
python verificar_instalacion.py
PYTHONPATH=. pytest -q
```

### Observa

- `gemma2:2b` aparece en la lista.
- Las pruebas terminan correctamente.

### Si algo falla

Consulta `setup_ollama.md` o continúa temporalmente con `--demo`.

---

## Estación 1 · Conocer a Astra

### Ejecuta

```bash
cd agente
python main.py --demo
```

Pregunta:

```text
¿Cuál region tuvo más ventas?
```

### Observa

La respuesta tiene cuatro partes:

1. `valor`: resultado calculado;
2. `explicacion`: representación legible;
3. `decision`: plan que se ejecutó;
4. `consistencia`: coincidencia entre valor y explicación.

---

## Estación 2 · Descubrir una respuesta engañosa

Pregunta:

```text
¿Cuáles fueron las ventas del mes?
```

En una primera versión del agente obteníamos `2200.0`. Conservamos el caso
porque muestra un error importante de diseño. La versión corregida debe devolver
`estado: no_disponible`.

### Paso 1: leer la decisión

```json
{
  "operacion": "ranking",
  "columna": "ventas",
  "agrupar_por": null,
  "orden": "desc",
  "limite": 1
}
```

Esto significa:

```text
Ordena todas las ventas de mayor a menor y devuelve la primera.
```

El cálculo encuentra la venta individual más alta:

```python
df["ventas"].sort_values(ascending=False).head(1)
```

### Paso 2: separar las capas de calidad

| Comprobación | Resultado |
|---|---|
| ¿El JSON tiene el formato esperado? | ✅ |
| ¿Python ejecutó la decisión? | ✅ |
| ¿La explicación contiene `2200.0`? | ✅ |
| ¿La decisión representa “ventas del mes”? | ❌ |
| ¿El dataset permite consultar un mes? | ❌ |

`consistencia: true` solo significa que el resultado y la explicación
coinciden. No significa que el agente comprendió correctamente la intención.

### Paso 3: encontrar la información faltante

La pregunta no especifica qué mes. Además, el dataset contiene:

```text
producto, region, vendedor, ventas, cantidad
```

No contiene `fecha`, `mes` ni `año`.

### Paso 4: decidir el comportamiento correcto

El agente corregido responde:

```json
{
  "estado": "no_disponible",
  "mensaje": "No puedo calcular ventas mensuales porque no existe una columna de fecha."
}
```

La lección:

> Un agente confiable también debe saber cuándo no puede responder.

Ejecuta nuevamente la pregunta y comprueba que `valor` y `decision` sean
`null`, y que el mensaje mencione la ausencia de una fecha.

---

## Estación 3 · Mejorar el prompt

Abre el notebook en la sección **De instrucción a prompt**.

Completa un prompt con:

- rol;
- objetivo;
- contexto;
- restricciones;
- formato.

Compara después con `respuestas/02_prompt_estructurado.md`.

---

## Estación 4 · Leer el contrato JSON

Abre `agente/agente.py` y busca:

```python
ESQUEMA_DECISION
```

Identifica:

- operaciones permitidas;
- columnas numéricas;
- agrupaciones;
- campos obligatorios.

Después busca `aplicar_reglas()`. Ollama propone; esta función gobierna.

---

## Estación 5 · Seguir una pregunta completa

Usa:

```text
¿Cuál vendedor tuvo menos ventas?
```

Sigue el recorrido:

```text
pregunta
→ decisión JSON
→ aplicar_reglas()
→ ejecutar()
→ respuesta
→ memoria
```

Compara con `respuestas/03_herramienta_pandas.md`.

---

## Estación 6 · Probar memoria

En `python main.py --demo`:

```text
¿Cuál region tuvo más ventas?
¿Y cuál quedó en segundo lugar?
/memoria
/clear
/memoria
```

Antes de `/clear` existe contexto. Después debe aparecer:

```text
Sin conversaciones anteriores.
```

---

## Estación 7 · Evaluar

Desde `taller_agentes/`:

```bash
python agente/evaluacion.py
PYTHONPATH=. pytest -q
```

No mires solo cuántas pruebas pasan. Pregunta qué propiedad comprueba cada una.

---

## Estación 8 · Reto final

Abre:

```text
agente/reto_final.py
```

1. Cambia la pregunta.
2. Predice la decisión JSON.
3. Ejecuta.
4. Añade un `assert`.
5. Compara con `respuestas/05_reto_final_solucion.py`.

Al terminar deberías poder explicar no solo qué respondió Astra, sino por qué
el sistema tomó esa decisión.
