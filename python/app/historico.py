# -*- coding: utf-8 -*-
"""Modulo que define el modelo del historico de tiradas."""

from typing import List

from .tirada import Tirada


class Historico:
    """Almacena y gestiona el historial de tiradas realizadas."""

    def __init__(self) -> None:
        """Inicializa el historico vacio."""
        self._entradas: List[Tirada] = []

    def agregar(self, tirada: Tirada) -> None:
        """
        Agrega una tirada al historico.

        Args:
            tirada: La tirada a agregar.
        """
        self._entradas.append(tirada)

    def resetear(self) -> None:
        """Elimina todas las entradas del historico."""
        self._entradas.clear()

    @property
    def entradas(self) -> List[Tirada]:
        """Devuelve una copia de las entradas del historico."""
        return list(self._entradas)

    def __len__(self) -> int:
        """Devuelve el numero de entradas en el historico."""
        return len(self._entradas)
