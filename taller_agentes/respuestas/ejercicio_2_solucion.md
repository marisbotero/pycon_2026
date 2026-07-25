# Solución: Ejercicio 2 - Mejorar un Prompt

## Prompt original (DEFICIENTE)

```
"Analiza el dataset"
```

### ¿Por qué es malo?
- ❌ Sin contexto: el LLM no sabe qué dataset
- ❌ Sin restricciones: puede hacer cualquier cosa
- ❌ Sin formato: la respuesta puede ser caótica
- ❌ Demasiado vago: no tiene objetivo claro

---

## Solución 1: Prompt Estructurado Básico

```python
system_prompt = """
Eres un experto en análisis de datos usando pandas.

Tienes un dataset con las siguientes columnas:
- fecha (datetime): Fecha de la transacción
- producto (str): Producto (A, B, C)
- region (str): Región (Norte, Sur, Centro, Oriente)
- vendedor (str): Nombre del vendedor
- ventas (float): Monto de venta
- cantidad (int): Unidades vendidas

Total de registros: 10
Rango de fechas: 2024-01-01 a 2024-01-10
"""

user_prompt = """
Análisis solicitado:
- ¿Cuál región tuvo mayor volumen de ventas?
- ¿Cuál fue el promedio de ventas?
- ¿Quién es el mejor vendedor?

Responde en formato JSON con tres campos:
- valor_principal: el número más importante
- analisis: explicación de 2-3 lineas
- insight: una conclusión útil
"""
```

### Mejoras aplicadas
✅ **Contexto:** Describe el dataset, sus columnas y tamaño
✅ **Restricciones:** Pide específicamente 3 análisis
✅ **Formato:** Especifica JSON con tres campos
✅ **Objetivo:** Claro y medible

---

## Solución 2: Prompt para Generar Código (La que usamos en el taller)

```python
system_prompt_analizador = """
Eres un experto en análisis de datos.

Tu tarea es analizar un dataset y generar código Python usando pandas.

RESTRICCIONES:
1. Solo usa pandas (pd) y la variable 'df'
2. Genera ÚNICAMENTE código Python, sin explicaciones
3. El código debe ser una sola línea o un bloque breve
4. NO incluyas 'print()' en el código
5. La última línea debe ser el resultado (ej: df.mean())

FORMATO:
Responde ÚNICAMENTE con el código Python. Por ejemplo:
df['ventas'].mean()

o para resultados más complejos:

df.groupby('region')['ventas'].sum().sort_values(ascending=False)
"""

user_prompt_analizador = """
Dataset:
- Columnas: fecha, producto, region, vendedor, ventas, cantidad
- Registros: 10

Pregunta: ¿Cuál región tuvo mayor volumen de ventas?

Genera el código pandas para responder esta pregunta.
"""
```

### Por qué es mejor
✅ **Sistema claro:** El system prompt enseña las reglas una sola vez
✅ **Usuario enfocado:** El user prompt solo tiene la pregunta
✅ **Output predecible:** Pide únicamente código, nada más
✅ **Fácil de reutilizar:** Cambias solo el user_prompt para nuevas preguntas

---

## Solución 3: Prompt Avanzado (Con Memoria)

```python
def crear_prompt_con_memoria(pregunta, historial_reciente, schema):
    """
    Crea un prompt que incluye contexto anterior.
    """

    system_prompt = """
    Eres un analista de datos experto.
    Usas pandas para responder preguntas sobre datos reales.

    REGLAS CRÍTICAS:
    1. Responde ÚNICAMENTE con código pandas
    2. Usa solo: df (el dataset) y pd (pandas)
    3. Sin explicaciones, solo código
    4. La última línea debe ser el cálculo final
    """

    contexto_dataset = f"""
    DATASET SCHEMA:
    {schema}
    """

    historial_prompt = """
    PREGUNTAS ANTERIORES (para dar contexto):
    """

    if historial_reciente:
        for i, (prev_pregunta, prev_respuesta) in enumerate(historial_reciente, 1):
            historial_prompt += f"""
            {i}. P: {prev_pregunta}
               R: {prev_respuesta}
            """
    else:
        historial_prompt += "(Sin historial anterior)"

    user_prompt = f"""
    {contexto_dataset}
    {historial_prompt}

    NUEVA PREGUNTA:
    {pregunta}
    """

    return system_prompt, user_prompt

# Uso
historial = [
    ("¿Cuál región tuvo más ventas?", "df.groupby('region')['ventas'].sum().sort_values(ascending=False)"),
    ("¿Cuál fue la venta más alta?", "df['ventas'].max()")
]

system, user = crear_prompt_con_memoria(
    pregunta="¿Y cuál región quedó en segundo?",
    historial_reciente=historial,
    schema="Columnas: fecha, producto, region, vendedor, ventas, cantidad"
)
```

### Por qué funciona
✅ **Contexto anterior:** El LLM "recuerda" las preguntas previas
✅ **Entiende seguimientos:** "¿Y cuál...?" tiene sentido con historial
✅ **Escalable:** Agregar memoria es solo pasar una lista

---

## Comparación: Antes vs Después

| Aspecto | Prompt Simple | Prompt Mejorado |
|---|---|---|
| **Claridad** | Vaga | Específica |
| **Contexto** | Ninguno | Completo |
| **Restricciones** | Ninguna | Claras |
| **Formato** | Aleatorio | Definido |
| **Reutilizable** | No | Sí |
| **Resultados consistentes** | ❌ | ✅ |

---

## Tips para escribir buenos prompts

### 1. Siempre incluye CONTEXTO
```python
# ❌ Malo
"¿Cuál es el promedio?"

# ✅ Bueno
"Tengo un dataset de ventas con columnas: fecha, producto, región, ventas.
¿Cuál es el promedio de ventas?"
```

### 2. Define RESTRICCIONES
```python
# ❌ Malo
"Analiza los datos"

# ✅ Bueno
"Genera ÚNICAMENTE código pandas.
Usa solo: df y pd.
Responde solo con el código, sin explicaciones."
```

### 3. Especifica el FORMATO de salida
```python
# ❌ Malo
"Dame la respuesta"

# ✅ Bueno
"Responde en JSON con: {valor, explicacion, insight}"
```

### 4. Usa SEPARADORES claros
```python
# ✅ Bueno
system_prompt = """...CONTEXTO..."""
user_prompt = """...PREGUNTA..."""

# No mezcles ambos
```

### 5. Prueba y ITERA
```python
# Versión 1
prompt_v1 = "¿Cuál es el promedio de ventas?"
# Resultado: inventa un número

# Versión 2 (mejorada)
prompt_v2 = "Dataset de ventas. Calcula el promedio de la columna 'ventas'."
# Resultado: mejor, pero aún ambiguo

# Versión 3 (final)
prompt_v3 = "..." # Versión completa con contexto, restricciones, formato
# Resultado: ✅ Funciona bien
```

---

## Próxima lectura

Ver: `ejercicio_3_solucion.md` para entender cómo ejecutar este código.
