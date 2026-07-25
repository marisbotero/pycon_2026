"""Interfaz de terminal del proyecto práctico."""

import argparse
import json
import os

from agente import AgenteVentas, crear_planificador_ollama, planificador_demo
from datos import cargar_ventas


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="Ejecutar sin Ollama")
    args = parser.parse_args()

    modelo = os.getenv("OLLAMA_MODEL", "gemma2:2b")
    planificador = planificador_demo if args.demo else crear_planificador_ollama(modelo)
    agente = AgenteVentas(cargar_ventas(), planificador=planificador)
    motor = "reglas de demostración" if args.demo else f"Ollama ({modelo})"
    print(f"Agente de ventas listo con {motor}.")
    print("Comandos: /memoria, /clear, /salir")
    while True:
        pregunta = input("\nTu pregunta: ").strip()
        comando = pregunta.lower()
        if comando == "/salir":
            break
        if comando == "/memoria":
            print(agente.contexto())
            continue
        if comando == "/clear":
            agente.limpiar_memoria()
            print("Memoria eliminada.")
            continue
        if pregunta:
            try:
                print(json.dumps(agente.preguntar(pregunta), ensure_ascii=False, indent=2))
            except Exception as error:
                print(f"No pude consultar Ollama: {error}")
                print("Comprueba que `ollama serve` esté activo y el modelo descargado.")


if __name__ == "__main__":
    main()
