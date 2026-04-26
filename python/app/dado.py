# -*- coding: utf-8 -*-
"""Modulo que define el modelo de un dado."""

import random


class Dado:
    """Representa un dado con un numero de lados configurable."""

    def __init__(self, lados: int) -> None:
        """
        Inicializa el dado con el numero de lados especificado.

        Args:
            lados: Numero de lados del dado (minimo 2).

        Raises:
            ValueError: Si el numero de lados es menor que 2.
        """
        if lados < 2:
            raise ValueError("Un dado debe tener al menos 2 lados")
        self._lados = lados

    @property
    def lados(self) -> int:
        """Devuelve el numero de lados del dado."""
        return self._lados

    def lanzar(self) -> int:
        """Lanza el dado y devuelve un numero aleatorio entre 1 y los lados."""
        return random.randint(1, self._lados)
