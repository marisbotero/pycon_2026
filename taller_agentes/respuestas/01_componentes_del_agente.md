# Solución 1: componentes del agente

Para la pregunta `¿Cuál región tuvo más ventas?`:

| Componente | En Astra |
|---|---|
| Percepción | La pregunta, las columnas disponibles y la memoria |
| Razonamiento | Ollama propone una decisión JSON |
| Reglas | Python normaliza operación, orden y límite |
| Herramienta | pandas agrupa y ordena las ventas |
| Respuesta | Un JSON con valor, explicación, decisión y consistencia |
| Memoria | Se guarda la pregunta junto con su respuesta |

La idea central es que el modelo no controla todo el sistema. Interpreta la
pregunta; Python limita las acciones y ejecuta la herramienta.
