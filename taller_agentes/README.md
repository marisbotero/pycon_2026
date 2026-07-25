# ✨ Taller: De prompts a agentes con Python y Ollama

Este directorio contiene todo lo necesario para una experiencia práctica de
dos horas. El notebook es el hilo conductor; la carpeta `agente/` es el
proyecto que cada participante ejecuta y modifica.

## Resultado final

Al terminar tendrás a **Astra**, un agente que:

1. recibe preguntas en lenguaje natural;
2. usa Ollama para producir una decisión JSON;
3. aplica reglas antes de actuar;
4. analiza un dataset con pandas;
5. responde en un formato estructurado;
6. recuerda interacciones recientes;
7. puede limpiar su memoria;
8. comprueba resultados y casos de error.

## Preparación antes del taller

Necesitas Python 3.9+, Git y
[Ollama](https://ollama.com/download). No necesitas una API key.

```bash
git clone https://github.com/marisbotero/pycon_2026.git
cd pycon_2026/taller_agentes

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

ollama pull gemma2:2b
```

En Windows, activa el entorno con:

```powershell
.venv\Scripts\activate
```

Comprueba la preparación:

```bash
python verificar_instalacion.py
PYTHONPATH=. pytest -q
cd agente
python main.py --demo
```

El verificador confirma la versión de Python, pandas, el cliente de Ollama, el
servidor local y la presencia de `gemma2:2b`. Si algo falta, muestra el comando
exacto para corregirlo.

## La ruta de dos horas

| Hora | Momento | Acción |
|---|---|---|
| 10:30–10:40 | Bienvenida | Preparar y ejecutar una prueba |
| 10:40–10:55 | De instrucción a prompt | Mejorar contexto y restricciones |
| 10:55–11:10 | Contrato JSON | Estructurar la decisión |
| 11:10–11:30 | Primer agente | Conectar todos los componentes |
| 11:30–11:35 | Pausa | ☕ |
| 11:35–11:50 | Herramientas | Ejecutar análisis con pandas |
| 11:50–12:05 | Memoria | Seguimiento, `/memoria` y `/clear` |
| 12:05–12:20 | Evaluación | Probar contrato, valores y errores |
| 12:20–12:27 | Reto final | Añadir una pregunta nueva |
| 12:27–12:30 | Cierre | Síntesis y recursos |

## Mapa del repositorio

```text
taller_agentes/
├── Workshop_Agentes.ipynb     teoría, ejemplos y actividades
├── GUIA_PASO_A_PASO.md        instrucciones del participante
├── agente/
│   ├── agente.py              orquestación, Ollama, reglas y memoria
│   ├── datos.py               dataset autocontenido
│   ├── main.py                interfaz conversacional
│   ├── ejercicios.py          tres prácticas breves
│   ├── evaluacion.py          evaluación legible
│   └── reto_final.py          desafío de cierre
├── respuestas/
│   ├── README.md               índice de soluciones
│   ├── CHEAT_SHEET.md         referencia rápida
│   └── 01_* … 05_*            respuestas por actividad
├── tests/                     pruebas automatizadas
├── verificar_instalacion.py   diagnóstico previo
├── GUIA_FACILITACION.md       ritmo, checkpoints y plan B
├── setup_ollama.md            ayuda de instalación
└── scripts/build_notebook.py  fuente reproducible del notebook
```

## Durante el taller

Abre el notebook:

```bash
jupyter lab Workshop_Agentes.ipynb
```

Si prefieres instrucciones lineales, mantén abierta
`GUIA_PASO_A_PASO.md`: cada estación indica qué abrir, ejecutar y observar.

Cuando aparezca **✋ Tu turno**, modifica el archivo indicado. Para usar el
modelo real, mantén Ollama activo y ejecuta:

```bash
cd agente
python main.py
```

Comandos disponibles:

```text
/memoria  muestra el contexto reciente
/clear    elimina la memoria
/salir    termina la conversación
```

Si Ollama falla durante la sesión:

```bash
python main.py --demo
```

El modo demo conserva el flujo pedagógico y permite continuar.

## Verificación

```bash
PYTHONPATH=. pytest -q
python agente/evaluacion.py
```

El proyecto es educativo. Las acciones están limitadas a operaciones
permitidas; no debe presentarse como un sandbox de producción.
