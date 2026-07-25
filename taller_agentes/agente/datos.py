"""Dataset pequeño para que el taller funcione sin archivos externos."""

import pandas as pd


def cargar_ventas() -> pd.DataFrame:
    datos = {
        "producto": ["A", "B", "A", "C", "B", "A", "B", "C", "A", "C"],
        "region": ["Norte", "Sur", "Centro", "Norte", "Oriente",
                   "Sur", "Centro", "Oriente", "Norte", "Sur"],
        "vendedor": ["Juan", "María", "Pedro", "Juan", "María",
                     "Pedro", "Juan", "María", "Pedro", "Juan"],
        "ventas": [1000, 1500, 2000, 1200, 1800, 900, 2200, 1100, 1400, 1900],
        "cantidad": [10, 15, 20, 12, 18, 9, 22, 11, 15, 19],
    }
    return pd.DataFrame(datos)
