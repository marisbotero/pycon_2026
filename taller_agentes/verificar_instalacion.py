"""Comprobación amigable antes de comenzar el taller."""

import sys


def ok(mensaje: str) -> None:
    print(f"✅ {mensaje}")


def error(mensaje: str, solucion: str) -> None:
    print(f"❌ {mensaje}")
    print(f"   Solución: {solucion}")


def main() -> int:
    fallos = 0

    if sys.version_info >= (3, 9):
        ok(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    else:
        error("Se requiere Python 3.9 o superior", "instala una versión reciente de Python")
        fallos += 1

    try:
        import pandas

        ok(f"pandas {pandas.__version__}")
    except ImportError:
        error("pandas no está instalado", "python -m pip install -r requirements.txt")
        fallos += 1

    try:
        import ollama

        ok("cliente Python de Ollama")
        try:
            modelos = ollama.list()
            nombres = [modelo.model for modelo in modelos.models]
            if any(nombre.startswith("gemma2:2b") for nombre in nombres):
                ok("Ollama activo y gemma2:2b disponible")
            else:
                error("Falta el modelo gemma2:2b", "ollama pull gemma2:2b")
                fallos += 1
        except Exception:
            error("No fue posible conectar con Ollama", "abre Ollama o ejecuta ollama serve")
            fallos += 1
    except ImportError:
        error("El cliente de Ollama no está instalado", "python -m pip install -r requirements.txt")
        fallos += 1

    print()
    if fallos:
        print(f"Preparación incompleta: {fallos} punto(s) por resolver.")
        return 1
    print("✨ Todo listo para construir a Astra.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
