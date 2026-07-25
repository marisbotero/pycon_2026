# Solución 2: prompt estructurado

Una posible mejora para `¿Quién vendió mejor?`:

```text
ROL:
Eres el planificador de un agente que analiza un dataset de ventas.

OBJETIVO:
Determina qué operación debe ejecutar el sistema para identificar al vendedor
con mayores ventas totales.

CONTEXTO:
El dataset contiene vendedor, producto, region, ventas y cantidad.

RESTRICCIONES:
- Usa únicamente columnas existentes.
- No calcules ni inventes el resultado.
- Las operaciones permitidas son promedio, suma y ranking.
- Para "mayor" utiliza un ranking descendente.

FORMATO:
Devuelve únicamente una decisión JSON con operacion, columna, agrupar_por,
orden y limite.
```

Lo importante no es copiar las palabras exactas. La respuesta debe tener un
objetivo inequívoco, datos disponibles, límites y un formato verificable.
