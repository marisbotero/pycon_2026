# Tu agente

Esta carpeta contiene el proyecto práctico del taller. Ollama convierte cada
pregunta en una decisión JSON y pandas ejecuta únicamente operaciones
permitidas. No se usa OpenAI ni se necesita una API key.

## Ejecutar

Primero instala Ollama y descarga el modelo del taller:

```bash
ollama pull gemma2:2b
ollama serve
```

En otra terminal, desde esta carpeta:

```bash
python3 main.py
```

Prueba estas preguntas:

- `¿Cuál región tuvo más ventas?`
- `¿Cuál vendedor tuvo menos ventas?`
- `¿Cuál es el promedio de ventas?`

La respuesta incluye el valor, una explicación, la decisión estructurada y una
verificación sencilla de consistencia.

Para comprobar el proyecto sin tener Ollama activo:

```bash
python3 main.py --demo
```

## Ejercicios

Abre `ejercicios.py`, reemplaza los tres `TODO` y ejecútalo:

```bash
python3 ejercicios.py
```

El objetivo no es escribir mucho código: es observar cómo cambia el
comportamiento del sistema al cambiar su entrada, sus reglas y su memoria.

> Este proyecto es educativo. No ejecuta código arbitrario generado por un
> modelo y no debe presentarse como un sandbox de producción.
