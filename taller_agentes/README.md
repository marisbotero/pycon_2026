# De prompts a agentes: sistemas inteligentes con Python

Taller práctico de PyCon 2026 para personas con conocimientos básicos de
Python. No requiere experiencia previa en inteligencia artificial.

## Qué vas a construir

Partiremos de un prompt sencillo y lo convertiremos en un sistema que:

1. recibe una pregunta y su contexto;
2. genera una decisión estructurada;
3. aplica reglas y usa pandas como herramienta;
4. devuelve una respuesta en JSON;
5. conserva memoria reciente;
6. comprueba una condición básica de consistencia.

## Estructura

```text
taller_agentes/
├── Workshop_Agentes.ipynb  # teoría, ejemplos y ejercicios guiados
├── agente/                 # proyecto que cada participante ejecuta
├── respuestas/             # soluciones y material posterior
├── tests/                  # comprobaciones del proyecto
└── requirements.txt
```

## Preparación

Se recomienda Python 3.10 o superior.

```bash
cd taller_agentes
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
jupyter lab Workshop_Agentes.ipynb
```

El taller usa exclusivamente Ollama: el modelo se ejecuta localmente y no
requiere una API key. Antes del taller:

```bash
ollama pull gemma2:2b
ollama serve
```

## Ejecutar el agente

```bash
cd taller_agentes/agente
python main.py
```

Luego abre `ejercicios.py`, completa los tres `TODO` y ejecútalo:

```bash
python ejercicios.py
```

## Comprobar la instalación

Desde la raíz del repositorio:

```bash
PYTHONPATH=taller_agentes python -m pytest -q taller_agentes/tests
```

## Nota de seguridad

El proyecto práctico ejecuta operaciones previamente permitidas; no ejecuta
código arbitrario generado por un modelo. Los ejemplos con `exec` del notebook
son didácticos y no representan un sandbox de producción.
