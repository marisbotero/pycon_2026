# Solución: Ejercicio 3 - Ejecutar Código Pandas

## Pregunta

**¿Cuál fue el vendedor con menos ventas totales?**

---

## Solución

### Paso 1: Entender qué pide la pregunta

- Agrupar por vendedor
- Sumar ventas de cada vendedor
- Encontrar el que tiene MENOS
- Devolver su nombre

---

### Paso 2: Código pandas

```python
# Opción 1: Básica (muy clara)
ventas_por_vendedor = df.groupby('vendedor')['ventas'].sum()
vendedor_menos = ventas_por_vendedor.idxmin()
# Resultado: 'Pedro'

# Opción 2: Una línea (más compacta)
df.groupby('vendedor')['ventas'].sum().idxmin()

# Opción 3: Con toda la info (mejor para entender)
df.groupby('vendedor')['ventas'].sum().sort_values()
# Muestra a todos ordenados de menos a más
```

---

### Paso 3: Ejecutar y verificar

```python
# Copiar esta función del notebook
def ejecutar_codigo_pandas(codigo, df, max_seguro=True):
    """
    Ejecuta código pandas de forma controlada.
    """
    palabras_peligrosas = ['import', 'open', 'exec', 'eval', 'os', 'sys',
                          'subprocess', 'requests', '__import__']

    if max_seguro:
        for palabra in palabras_peligrosas:
            if palabra in codigo.lower():
                return False, None, f"❌ Código bloqueado: contiene '{palabra}'"

    try:
        namespace = {
            'df': df.copy(),
            'pd': pd,
            '__builtins__': {'len': len, 'sum': sum, 'min': min, 'max': max}
        }

        exec(codigo, namespace)
        resultado = eval(codigo, namespace)

        return True, resultado, "✅ Código ejecutado exitosamente"

    except Exception as e:
        return False, None, f"❌ Error: {str(e)}"


# Ejecutar la solución
codigo = "df.groupby('vendedor')['ventas'].sum().idxmin()"

exito, resultado, mensaje = ejecutar_codigo_pandas(codigo, df)

print(f"Ejecutando: {codigo}")
print(f"{mensaje}")

if exito:
    print(f"\n📊 Resultado: {resultado}")
    print(f"\nInterpretación: El vendedor {resultado} tuvo las MENORES ventas.")
```

---

## Resultado esperado

```
Ejecutando: df.groupby('vendedor')['ventas'].sum().idxmin()
✅ Código ejecutado exitosamente

📊 Resultado: Pedro

Interpretación: El vendedor Pedro tuvo las MENORES ventas.
```

---

## Verificación: ¿Es correcto?

```python
# Verificar manualmente
print("\nVerificación:")
print(df.groupby('vendedor')['ventas'].sum().sort_values())
```

Deberías ver algo como:
```
vendedor
Pedro    4300   ← El menor
María    4400
Juan     6300   ← El mayor
Name: ventas, dtype: int64
```

Sí, **Pedro es el vendedor con menos ventas** ✅

---

## Alternativas correctas

Todas estas respuestas también son válidas:

```python
# Opción A: idxmin()
df.groupby('vendedor')['ventas'].sum().idxmin()

# Opción B: sort_values + head(1)
df.groupby('vendedor')['ventas'].sum().sort_values().head(1).index[0]

# Opción C: nsmallest()
df.groupby('vendedor')['ventas'].sum().nsmallest(1).index[0]

# Opción D: con max()
# (Encontramos el vendedor cuyo mín es el máximo de los mínimos...)
# NO, esto es muy complicado. Usa idxmin()
```

---

## Métodos clave que usamos

| Método | Función |
|---|---|
| `groupby()` | Agrupa filas por una columna |
| `sum()` | Suma los valores de un grupo |
| `idxmin()` | Devuelve el ÍNDICE del valor mínimo |
| `min()` | Devuelve el valor mínimo |
| `sort_values()` | Ordena de menor a mayor (o mayor a menor) |
| `head()` | Primeras N filas |

---

## Ejercicio adicional

**Modifica la pregunta a:**

1. "¿Cuál fue el vendedor con MÁS ventas totales?" → Usa `idxmax()` en vez de `idxmin()`

2. "¿Cuál fue el PRODUCTO más vendido (por cantidad)?" → Cambia `'vendedor'` por `'producto'` y suma `'cantidad'` en vez de `'ventas'`

3. "¿En cuál REGIÓN se hizo la mayor cantidad de transacciones?" → Usa `count()` en vez de `sum()`

---

## Depuración: Si tu código falla

```python
# Si obtienes un error, prueba paso a paso:

# Paso 1: ¿El groupby funciona?
print(df.groupby('vendedor')['ventas'].sum())

# Paso 2: ¿El sort funciona?
print(df.groupby('vendedor')['ventas'].sum().sort_values())

# Paso 3: ¿El idxmin funciona?
print(df.groupby('vendedor')['ventas'].sum().idxmin())

# Así encontrarás dónde está el error
```

---

## Próxima lectura

Ver: `../agente/agente.py` para entender cómo integrar la decisión, la
herramienta y la memoria en un agente.
