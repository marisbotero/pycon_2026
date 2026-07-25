# 🐍 Guía del código Python

Esta guía explica los archivos `.py` del taller. No es necesario entenderlos
todos al comenzar. La ruta recomendada es:

```text
datos.py
→ main.py
→ agente.py
→ ejercicios.py
→ evaluacion.py
→ tests/test_agente.py
→ reto_final.py
```

---

# 1. `verificar_instalacion.py`

## Responsabilidad

Comprobar que el equipo está listo antes de ejecutar el taller.

## Qué revisa

```text
Python
→ pandas
→ cliente de Ollama
→ servidor de Ollama
→ modelo gemma2:2b
```

La función principal es:

```python
def main() -> int:
```

Devuelve `0` cuando todo funciona y `1` cuando existe algún problema. Esto
permite utilizar el archivo tanto manualmente como en otros procesos.

Ejecutar:

```bash
python verificar_instalacion.py
```

---

# 2. `agente/datos.py`

## Responsabilidad

Crear el dataset del taller.

```python
def cargar_ventas() -> pd.DataFrame:
```

La función construye un diccionario:

```python
datos = {
    "producto": [...],
    "region": [...],
    "vendedor": [...],
    "ventas": [...],
    "cantidad": [...],
}
```

Después lo convierte en un DataFrame:

```python
return pd.DataFrame(datos)
```

Separar los datos permite reemplazarlos posteriormente sin modificar la lógica
del agente.

---

# 3. `agente/main.py`

## Responsabilidad

Administrar la conversación desde la terminal.

Es el archivo que ejecutamos:

```bash
python main.py
```

## Selección del motor

El argumento `--demo` selecciona reglas deterministas:

```bash
python main.py --demo
```

Sin `--demo`, se conecta con Ollama:

```bash
python main.py
```

## Ciclo principal

El programa repite:

```python
while True:
    pregunta = input("Tu pregunta: ").strip()
```

Después reconoce comandos:

```text
/memoria
/clear
/salir
```

Si la entrada es una pregunta:

```python
respuesta = agente.preguntar(pregunta)
```

`main.py` no calcula ventas. Su trabajo es recibir entradas y mostrar salidas.

---

# 4. `agente/agente.py`

Este es el corazón del proyecto.

## 4.1 `Decision`

```python
@dataclass
class Decision:
    operacion: str
    columna: str = "ventas"
    agrupar_por: Optional[str] = None
    orden: str = "desc"
    limite: int = 1
```

Representa el plan de análisis.

Ejemplo:

```json
{
  "operacion": "ranking",
  "columna": "ventas",
  "agrupar_por": "region",
  "orden": "desc",
  "limite": 1
}
```

No contiene el resultado. Describe cómo obtenerlo.

## 4.2 `ESQUEMA_DECISION`

Es el contrato JSON enviado a Ollama.

Limita:

- operaciones;
- columnas;
- agrupaciones;
- orden;
- cantidad de resultados.

El esquema evita que el modelo solicite acciones desconocidas.

## 4.3 `crear_planificador_ollama()`

Crea una función que transforma preguntas en decisiones.

```python
def crear_planificador_ollama(modelo="gemma2:2b"):
```

La llamada principal es:

```python
respuesta = chat(
    model=modelo,
    messages=[{"role": "user", "content": prompt}],
    format=ESQUEMA_DECISION,
    options={"temperature": 0},
)
```

Ollama recibe:

- la pregunta;
- el contexto;
- reglas;
- ejemplos;
- el esquema JSON.

Después convertimos el contenido:

```python
datos = json.loads(respuesta.message.content)
decision = Decision(**datos)
```

## 4.4 `planificador_demo()`

Interpreta preguntas utilizando reglas sencillas:

```python
if "promedio" in texto:
    return Decision("promedio", columna, agrupar)
```

Se usa para:

- explicar el flujo;
- ejecutar pruebas predecibles;
- continuar si Ollama no está disponible.

## 4.5 `aplicar_reglas()`

Normaliza la propuesta del modelo.

Ejemplos:

```text
menos  → orden ascendente
más    → orden descendente
segundo → límite 2
```

Esta función representa una idea fundamental:

> El modelo propone; Python aplica reglas verificables.

## 4.6 `AgenteVentas`

Es la clase que coordina todo el sistema.

### Constructor

```python
def __init__(self, datos, planificador=planificador_demo, max_memoria=3):
```

Recibe:

- el DataFrame;
- el planificador;
- el número máximo de interacciones guardadas.

### `contexto()`

Convierte la memoria reciente en texto para utilizarla en la siguiente
pregunta.

### `limpiar_memoria()`

```python
self.memoria.clear()
```

Se activa mediante `/clear`.

### `_limitacion_de_datos()`

Detecta consultas que necesitan información inexistente.

Por ejemplo:

```text
¿Cuáles fueron las ventas del mes?
```

Como no existe una columna temporal, devuelve:

```json
{
  "estado": "no_disponible",
  "valor": null,
  "decision": null
}
```

El guion bajo inicial comunica que es un método interno.

### `ejecutar()`

Convierte una decisión en una operación pandas.

Primero valida:

```python
if decision.columna not in {"ventas", "cantidad"}:
    raise ValueError("Columna no permitida")
```

Después agrupa si es necesario:

```python
serie = self.datos.groupby(
    decision.agrupar_por
)[decision.columna].sum()
```

Finalmente ejecuta:

```text
promedio
suma
ranking
```

### `preguntar()`

Es el director de orquesta:

```text
revisar limitaciones
→ generar decisión
→ ejecutar
→ construir respuesta
→ guardar memoria
```

Se utiliza así:

```python
respuesta = agente.preguntar("¿Cuál region tuvo más ventas?")
```

---

# 5. `agente/__init__.py`

## Responsabilidad

Definir qué elementos se ofrecen al importar el paquete.

Permite escribir:

```python
from agente import AgenteVentas, cargar_ventas
```

en lugar de:

```python
from agente.agente import AgenteVentas
from agente.datos import cargar_ventas
```

Es la puerta de entrada del paquete.

---

# 6. `agente/ejercicios.py`

## Responsabilidad

Ofrecer una práctica corta.

Contiene marcadores:

```python
# TODO
```

La persona modifica preguntas y observa cómo cambia la decisión.

Solución:

```text
respuestas/04_ejercicios_solucion.py
```

---

# 7. `agente/evaluacion.py`

## Responsabilidad

Ejecutar una evaluación fácil de leer.

Contiene pares:

```python
("¿Cuál region tuvo más ventas?", "Sur")
```

Para cada caso comprueba:

- contrato;
- resultado;
- consistencia.

También verifica que una consulta mensual sea rechazada.

Ejecutar:

```bash
python agente/evaluacion.py
```

Este archivo está pensado para aprender. Las pruebas automatizadas viven en
`tests/`.

---

# 8. `tests/test_agente.py`

## Responsabilidad

Evitar que comportamientos ya corregidos vuelvan a romperse.

Las pruebas comprueban:

- región con mayores ventas;
- “quién” como referencia a vendedor;
- ventas totales como ranking entre vendedores;
- límite de memoria;
- preguntas de seguimiento;
- aplicación de reglas;
- `/clear`;
- consulta mensual sin fechas.

Ejecutar:

```bash
PYTHONPATH=. pytest -q
```

Una prueba tiene tres partes:

```text
preparar
→ ejecutar
→ afirmar
```

Ejemplo:

```python
respuesta = agente.preguntar("¿Cuáles fueron las ventas del mes?")

assert respuesta["estado"] == "no_disponible"
assert respuesta["valor"] is None
```

---

# 9. `agente/reto_final.py`

## Responsabilidad

Permitir que cada participante agregue una consulta propia.

El reto pide:

1. cambiar la pregunta;
2. predecir la decisión;
3. ejecutar;
4. añadir un `assert`;
5. comprobar el resultado.

Solución:

```text
respuestas/05_reto_final_solucion.py
```

---

# 10. `scripts/build_notebook.py`

## Responsabilidad

Generar `Workshop_Agentes.ipynb` de forma reproducible.

El notebook es JSON y resulta difícil editarlo manualmente. Este script utiliza
`nbformat` para crear celdas Markdown y Python.

Ejecutar:

```bash
python scripts/build_notebook.py
```

Este archivo es principalmente para mantener el material, no para los
ejercicios del participante.

---

# El recorrido completo del código

```text
main.py
  │ recibe la pregunta
  ▼
AgenteVentas.preguntar()
  │
  ├── _limitacion_de_datos()
  │      └── puede detener el flujo
  │
  ├── planificador_demo()
  │        o
  ├── crear_planificador_ollama()
  │
  ├── aplicar_reglas()
  │
  ├── ejecutar()
  │      └── pandas
  │
  ├── construir respuesta JSON
  │
  └── guardar memoria
         ▼
main.py muestra la respuesta
```

## Idea final

El código separa las decisiones probabilísticas de las reglas verificables:

```text
Ollama interpreta
Python limita
pandas calcula
las pruebas verifican
```
