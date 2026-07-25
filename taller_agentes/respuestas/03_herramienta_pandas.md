# Solución 3: seguir el dato

En `agente/agente.py`:

1. La columna se valida al inicio de `AgenteVentas.ejecutar()`.
2. `groupby()` se aplica cuando `decision.agrupar_por` tiene un valor.
3. El ranking usa `sort_values()` y selecciona la posición indicada por
   `decision.limite`.
4. `AgenteVentas.preguntar()` construye la respuesta final y la agrega a
   `self.memoria`.

Para encontrar el vendedor con menos ventas, la decisión esperada es:

```json
{
  "operacion": "ranking",
  "columna": "ventas",
  "agrupar_por": "vendedor",
  "orden": "asc",
  "limite": 1
}
```

El resultado esperado es `Pedro`, con `4300.0`.
