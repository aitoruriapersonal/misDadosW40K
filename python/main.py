# -*- coding: utf-8 -*-
"""
Punto de entrada de la aplicacion lanzadora de dados Warhammer 40K.

Modo de uso:
  python main.py              -> Modo ventana (interfaz grafica)
  python main.py <cant> <lados> -> Modo consola (salida en terminal)
"""

import sys

from app.lanzador import Lanzador


def modo_consola(cantidad: int, lados: int) -> None:
    """
    Ejecuta la aplicacion en modo consola con los argumentos dados.

    Args:
        cantidad: Numero de dados a lanzar.
        lados: Numero de lados de cada dado.
    """
    lanzador = Lanzador()
    tirada = lanzador.lanzar(cantidad, lados)
    print(tirada)


def modo_ventana() -> None:
    """Ejecuta la aplicacion en modo ventana (interfaz grafica)."""
    from app.ventana import VentanaPrincipal
    app = VentanaPrincipal()
    app.iniciar()


def main() -> None:
    """Funcion principal que determina el modo de ejecucion."""
    if len(sys.argv) == 1:
        modo_ventana()
    elif len(sys.argv) == 3:
        try:
            cantidad = int(sys.argv[1])
            lados = int(sys.argv[2])
            modo_consola(cantidad, lados)
        except ValueError:
            print("Error: Los argumentos deben ser numeros enteros.")
            print("Uso: python main.py <cantidad_dados> <lados>")
            sys.exit(1)
    else:
        print("Uso: python main.py [<cantidad_dados> <lados>]")
        print("  Sin argumentos    -> modo ventana (interfaz grafica)")
        print("  Con 2 argumentos  -> modo consola")
        sys.exit(1)


if __name__ == "__main__":
    main()
