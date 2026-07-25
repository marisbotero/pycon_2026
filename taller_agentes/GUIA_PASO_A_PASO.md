# 👣 De prompts a agentes: guía paso a paso

Esta guía acompaña `Workshop_Agentes.ipynb`. Está escrita como si la
instructora estuviera a tu lado: explica qué hacemos, por qué, qué archivo
interviene, qué ejecutar y cómo interpretar el resultado.

**Duración:** 2 horas

**Nivel:** Python básico

**Motor:** Ollama local con `gemma2:2b`
**Proyecto:** Astra, un pequeño oráculo de datos

---

# Antes de empezar: la idea central

Queremos hacer preguntas como:

```text
¿Cuál región tuvo más ventas?
```

No queremos que un modelo improvise una respuesta. Diseñaremos este ciclo:

```text
Pregunta
   ↓
Ollama interpreta la intención
   ↓
Decisión JSON
   ↓
Python valida y aplica reglas
   ↓
pandas calcula con datos reales
   ↓
Respuesta estructurada
   ↓
Memoria y evaluación
```

La frase del taller es:

> Ollama interpreta; nuestro sistema gobierna.

## Prompt frente a agente

Un prompt es una instrucción:

```text
Dime cuál región vendió más.
```

Un agente es un sistema:

```text
entrada
+ contexto
+ modelo
+ reglas
+ herramientas
+ memoria
+ evaluación
```

Ollama es un componente de Astra. No es todo el agente.

---

# Mapa de las dos horas

| Hora | Estación | Resultado |
|---|---|---|
| 10:30–10:40 | Preparación | Entorno y modelo verificados |
| 10:40–10:55 | De instrucción a prompt | Prompt con contexto y restricciones |
| 10:55–11:10 | Contrato JSON | Decisión legible por Python |
| 11:10–11:30 | Primer agente | Ciclo completo conectado |
| 11:30–11:35 | Pausa | ☕ |
| 11:35–11:50 | Herramientas | Análisis real con pandas |
| 11:50–12:05 | Memoria | Seguimiento, `/memoria` y `/clear` |
| 12:05–12:20 | Evaluación | Contrato, resultado y errores probados |
| 12:20–12:27 | Reto final | Una pregunta nueva |
| 12:27–12:30 | Cierre | Modelo mental reutilizable |

---

# Estación 0 · Preparar el taller

## Qué aprenderás

- Para qué sirve un entorno virtual.
- Qué dependencias utiliza el proyecto.
- Cómo comprobar Ollama antes de comenzar.
- Qué significa *fail fast*.

## Paso 1: clonar o actualizar

Si todavía no tienes el repositorio:

```bash
git clone https://github.com/marisbotero/pycon_2026.git
cd pycon_2026/taller_agentes
```

Si ya lo tienes:

```bash
cd pycon_2026
git pull origin main
cd taller_agentes
```

Comprueba la ubicación:

```bash
pwd
```

Debe terminar en:

```text
pycon_2026/taller_agentes
```

## Paso 2: crear un entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows:

```powershell
.venv\Scripts\activate
```

La terminal mostrará `(.venv)`. Esto significa que las librerías del taller
quedan aisladas de otros proyectos.

## Paso 3: instalar dependencias

```bash
python -m pip install -r requirements.txt
```

`requirements.txt` declara:

| Dependencia | Responsabilidad |
|---|---|
| `pandas` | Analizar el dataset |
| `jupyterlab` | Ejecutar el notebook |
| `ollama` | Conectar Python con el modelo local |
| `pytest` | Probar el comportamiento |

## Paso 4: preparar Ollama

```bash
ollama list
```

Necesitamos `gemma2:2b`. Si no aparece:

```bash
ollama pull gemma2:2b
```

Si Ollama no está activo:

```bash
ollama serve
```

Déjalo ejecutándose en otra terminal.

## Paso 5: ejecutar el diagnóstico

```bash
python verificar_instalacion.py
```

Este archivo comprueba:

1. Python 3.9 o superior.
2. pandas.
3. El cliente Python de Ollama.
4. El servidor local.
5. El modelo `gemma2:2b`.

Resultado esperado:

```text
✅ Python 3.9
✅ pandas
✅ cliente Python de Ollama
✅ Ollama activo y gemma2:2b disponible

✨ Todo listo para construir a Astra.
```

Esto aplica el principio *fail fast*:

> Encontrar problemas de preparación antes de confundirlos con errores del agente.

## Paso 6: establecer una línea base

```bash
PYTHONPATH=. pytest -q
```

Esperamos:

```text
8 passed
```

Antes de modificar el proyecto, sabemos que funciona.

---

# Estación 1 · Conocer el repositorio

Para una explicación línea por línea de responsabilidades, mantén abierta
`GUIA_CODIGO.md`.

```text
taller_agentes/
├── Workshop_Agentes.ipynb
├── GUIA_PASO_A_PASO.md
├── verificar_instalacion.py
│
├── agente/
│   ├── datos.py
│   ├── agente.py
│   ├── main.py
│   ├── ejercicios.py
│   ├── evaluacion.py
│   └── reto_final.py
│
├── respuestas/
├── tests/
└── scripts/build_notebook.py
```

## Responsabilidad de cada archivo

### `Workshop_Agentes.ipynb`

Teoría, ejemplos ejecutables y espacios para experimentar.

### `agente/datos.py`

Construye el DataFrame. Mantener los datos separados permite sustituirlos sin
reescribir el agente.

### `agente/agente.py`

Es el corazón de Astra. Contiene:

- `Decision`;
- el esquema JSON;
- la conexión con Ollama;
- reglas explícitas;
- ejecución con pandas;
- memoria;
- manejo de limitaciones.

### `agente/main.py`

Es la interfaz. Lee preguntas, reconoce comandos y muestra respuestas. No
calcula ventas.

### `agente/ejercicios.py`

Práctica guiada con pocos `TODO`.

### `agente/evaluacion.py`

Casos legibles para comprobar calidad.

### `agente/reto_final.py`

Desafío para añadir una pregunta sin cambiar la arquitectura.

### `tests/`

Pruebas automatizadas. Convierten errores descubiertos en reglas permanentes.

### `respuestas/`

Soluciones numeradas. Intenta primero; compara después.

## Concepto: separación de responsabilidades

> Cada componente debe tener un trabajo fácil de explicar.

Esto permite modificar la interfaz sin tocar los datos, o cambiar el modelo sin
reescribir la herramienta.

---

# Estación 2 · Ejecutar a Astra por primera vez

Primero usaremos reglas deterministas:

```bash
cd agente
python main.py --demo
```

Pregunta:

```text
¿Cuál region tuvo más ventas?
```

Respuesta esperada:

```json
{
  "estado": "listo",
  "valor": {
    "nombre": "Sur",
    "valor": 4300.0
  },
  "explicacion": "El resultado calculado es {'nombre': 'Sur', 'valor': 4300.0}.",
  "decision": {
    "operacion": "ranking",
    "columna": "ventas",
    "agrupar_por": "region",
    "orden": "desc",
    "limite": 1
  },
  "consistencia": true,
  "mensaje": null
}
```

## Leer una respuesta, campo por campo

### `estado`

```json
"estado": "listo"
```

El flujo terminó correctamente.

### `valor`

```json
{"nombre": "Sur", "valor": 4300.0}
```

Incluye la categoría y el número calculado.

### `decision`

```json
{
  "operacion": "ranking",
  "columna": "ventas",
  "agrupar_por": "region",
  "orden": "desc",
  "limite": 1
}
```

En lenguaje humano:

```text
Agrupa por región.
Suma las ventas.
Ordena de mayor a menor.
Devuelve el primer lugar.
```

### `consistencia`

```json
"consistencia": true
```

El valor calculado aparece en la explicación. Esto no demuestra todavía que la
intención se haya interpretado correctamente.

### `mensaje`

Es `null` porque no hay una limitación que explicar.

## Concepto: decisión como puente

La decisión JSON conecta:

```text
lenguaje natural ↔ operaciones de Python
```

No necesitamos permitir que el modelo ejecute cualquier código.

---

# Estación 3 · Encontrar una respuesta engañosa

Pregunta:

```text
¿Cuáles fueron las ventas del mes?
```

## El bug original

La primera versión devolvía:

```json
{
  "valor": 2200.0,
  "decision": {
    "operacion": "ranking",
    "columna": "ventas",
    "agrupar_por": null,
    "orden": "desc",
    "limite": 1
  },
  "consistencia": true
}
```

La decisión significaba:

> Ordena todas las ventas de mayor a menor y devuelve la primera.

El cálculo era equivalente a:

```python
df["ventas"].sort_values(ascending=False).head(1)
```

`2200.0` es la venta individual más alta. El cálculo era correcto, pero
respondía otra pregunta.

## Separar las capas de calidad

| Pregunta | Resultado |
|---|---|
| ¿El JSON era válido? | ✅ |
| ¿La decisión podía ejecutarse? | ✅ |
| ¿La explicación contenía `2200.0`? | ✅ |
| ¿La decisión representaba “ventas del mes”? | ❌ |
| ¿El dataset podía responder por mes? | ❌ |

La consistencia numérica no garantiza comprensión de la intención.

## Información faltante

La pregunta no especifica qué mes. Además, el dataset contiene:

```text
producto, region, vendedor, ventas, cantidad
```

No contiene `fecha`, `mes` ni `año`.

## Respuesta corregida

La versión actual devuelve:

```json
{
  "estado": "no_disponible",
  "valor": null,
  "explicacion": "No puedo responder consultas mensuales porque el dataset no contiene una columna de fecha, mes o año.",
  "decision": null,
  "consistencia": null,
  "mensaje": "No puedo responder consultas mensuales porque el dataset no contiene una columna de fecha, mes o año."
}
```

Esto significa:

- `estado`: el flujo se detuvo de manera controlada;
- `valor: null`: no inventó un número;
- `decision: null`: pandas no ejecutó una acción;
- `consistencia: null`: no existe un valor que comparar;
- `mensaje`: explica la limitación.

## Concepto: guardrail

Un *guardrail* es una regla que impide una acción cuando no se cumplen las
condiciones.

```python
limitacion = self._limitacion_de_datos(pregunta)
if limitacion:
    return limitacion
```

La lección:

> Un agente confiable también sabe cuándo no puede responder.

## Si todavía aparece `2200.0`

Python cargó la versión anterior al iniciar:

1. escribe `/salir`;
2. ejecuta `git pull origin main` si trabajas en otra copia;
3. reinicia `python main.py --demo`;
4. repite la pregunta.

---

# Estación 4 · De instrucción a prompt

Regresa a `taller_agentes/` y abre:

```bash
cd ..
jupyter lab Workshop_Agentes.ipynb
```

Una instrucción ambigua:

```text
¿Quién vendió mejor?
```

Un prompt estructurado contiene cinco piezas.

## 1. Rol

```text
Eres el planificador de un agente de ventas.
```

## 2. Objetivo

```text
Determina qué operación identifica al vendedor con mayores ventas totales.
```

## 3. Contexto

```text
El dataset contiene producto, region, vendedor, ventas y cantidad.
```

## 4. Restricciones

```text
- No inventes columnas.
- No inventes el resultado.
- Usa solamente operaciones permitidas.
- No ejecutes todavía el cálculo.
```

## 5. Formato

```text
Devuelve únicamente una decisión JSON.
```

## Tu turno

Completa `mi_prompt` en el notebook. Después compara con:

```text
respuestas/02_prompt_estructurado.md
```

## Concepto: claridad frente a certeza

Un prompt claro mejora la observabilidad, pero no garantiza que el modelo
tenga razón. Por eso todavía necesitamos reglas y evaluación.

---

# Estación 5 · El contrato JSON

Abre `agente/agente.py` y busca:

```python
@dataclass
class Decision:
    operacion: str
    columna: str = "ventas"
    agrupar_por: Optional[str] = None
    orden: str = "desc"
    limite: int = 1
```

`Decision` define el objeto que Python utiliza.

Después busca:

```python
ESQUEMA_DECISION
```

El esquema limita:

- operaciones: `promedio`, `suma`, `ranking`;
- columnas: `ventas`, `cantidad`;
- agrupaciones: `region`, `vendedor`, `producto`;
- orden: `asc`, `desc`;
- límite: entre 1 y 10.

## Concepto: contrato

> Un contrato define qué puede producir un componente para que otro lo acepte.

JSON no se usa solo porque sea bonito. Permite validar antes de actuar.

---

# Estación 6 · Usar Ollama real

Sal de Astra si sigue abierto:

```text
/salir
```

Entra de nuevo a `agente/`:

```bash
cd agente
python main.py
```

Sin `--demo`, `crear_planificador_ollama()` llama al modelo:

```python
respuesta = chat(
    model=modelo,
    messages=[{"role": "user", "content": prompt}],
    format=ESQUEMA_DECISION,
    options={"temperature": 0},
)
```

### `model`

Selecciona `gemma2:2b`.

### `messages`

Envía pregunta, contexto, reglas y ejemplos.

### `format`

Obliga la salida a seguir el esquema JSON.

### `temperature: 0`

Reduce la variabilidad. No convierte al modelo en determinista perfecto.

Pregunta:

```text
¿Cuál vendedor tuvo menos ventas?
```

Inspecciona la decisión antes de mirar el resultado.

## Concepto: modelo y reglas

Después de Ollama, `aplicar_reglas()` corrige aspectos verificables:

```text
“menos” → orden ascendente
“más” → orden descendente
“segundo” → límite 2
```

El modelo interpreta. Las reglas protegen invariantes del sistema.

---

# Estación 7 · Darle herramientas con pandas

Busca:

```python
AgenteVentas.ejecutar()
```

Su recorrido es:

```text
validar columna
→ validar agrupación
→ seleccionar serie
→ agrupar
→ aplicar operación
→ ordenar
→ seleccionar posición
```

Ejemplo:

```python
self.datos.groupby("vendedor")["ventas"].sum()
```

Para “menos ventas”:

```python
serie.sort_values(ascending=True)
```

## Concepto: herramienta

Ollama no calcula sobre el DataFrame. Propone una decisión. pandas ejecuta un
cálculo reproducible sobre datos reales.

## Tu turno

Completa:

```text
agente/ejercicios.py
```

Compara después con:

```text
respuestas/04_ejercicios_solucion.py
```

---

# Estación 8 · Contexto y memoria

Ejecuta:

```bash
python main.py --demo
```

Conversación:

```text
¿Cuál region tuvo más ventas?
¿Y cuál quedó en segundo lugar?
/memoria
```

La segunda pregunta no dice “segundo lugar por región”. El contexto permite
recuperar esa agrupación.

La memoria conserva los últimos turnos:

```python
self.memoria[-self.max_memoria:]
```

Ahora:

```text
/clear
/memoria
```

Esperamos:

```text
Memoria eliminada.
Sin conversaciones anteriores.
```

## Concepto: memoria no es conocimiento

La memoria solo conserva contexto reciente. No entrena el modelo ni garantiza
que el agente comprenda todas las referencias.

---

# Estación 9 · Evaluar antes de confiar

Desde `taller_agentes/`:

```bash
cd ..
python agente/evaluacion.py
PYTHONPATH=. pytest -q
```

Evaluamos distintas capas:

| Capa | Pregunta |
|---|---|
| Contrato | ¿Aparecen las claves esperadas? |
| Decisión | ¿Operación, columna y orden son correctos? |
| Resultado | ¿Coincide con un valor conocido? |
| Consistencia | ¿Valor y explicación coinciden? |
| Limitación | ¿Evita responder sin datos suficientes? |
| Memoria | ¿Conserva y elimina contexto correctamente? |

El bug mensual se convirtió en una prueba:

```python
def test_consulta_mensual_sin_fecha_no_inventa_resultado():
    respuesta = agente.preguntar("¿Cuáles fueron las ventas del mes?")
    assert respuesta["estado"] == "no_disponible"
    assert respuesta["valor"] is None
    assert respuesta["decision"] is None
```

## Concepto: una prueba es memoria del sistema

La prueba recuerda un error incluso cuando las personas que lo descubrieron ya
no están trabajando en el código.

---

# Estación 10 · Reto final

Abre:

```text
agente/reto_final.py
```

Tu misión:

1. formula una pregunta que use `producto` y `cantidad`;
2. predice la decisión JSON;
3. ejecuta el agente;
4. añade un `assert` con el resultado esperado;
5. agrega el caso a `evaluacion.py` si terminas pronto.

Compara al final con:

```text
respuestas/05_reto_final_solucion.py
```

Si puedes añadir una capacidad sin cambiar la arquitectura, el framework está
cumpliendo su propósito.

---

# Estación 11 · Cierre

Empezamos con una instrucción y terminamos con:

```text
pregunta
→ contexto
→ Ollama
→ decisión JSON
→ reglas
→ pandas
→ respuesta
→ memoria
→ evaluación
```

## Conceptos que debes poder explicar

- Diferencia entre prompt y agente.
- Rol, objetivo, contexto, restricciones y formato.
- JSON como contrato.
- Ollama como intérprete, no como sistema completo.
- Reglas como guardrails.
- pandas como herramienta.
- Memoria para preguntas de seguimiento.
- Diferencia entre formato, consistencia e intención.
- Evaluación de resultados y casos de error.
- Por qué un agente debe saber cuándo no responder.

## La idea para llevar

> Un sistema de IA confiable no solo produce respuestas. Hace visible su
> decisión, limita sus acciones, verifica sus resultados y reconoce sus
> límites.
