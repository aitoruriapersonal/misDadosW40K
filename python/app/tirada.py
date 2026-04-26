# -*- coding: utf-8 -*-
"""Modulo que define el modelo de una tirada de dados."""

from datetime import datetime
from typing import List, Optional

from .dado import Dado


class Tirada:
    """Representa una tirada de un conjunto de dados del mismo tipo."""

    def __init__(self, cantidad: int, lados: int) -> None:
        """
        Inicializa la tirada con la cantidad y tipo de dados.

        Args:
            cantidad: Numero de dados a lanzar.
            lados: Numero de lados de cada dado.

        Raises:
            ValueError: Si la cantidad o los lados son invalidos.
        """
        if cantidad < 1:
            raise ValueError("La cantidad de dados debe ser al menos 1")
        if lados < 2:
            raise ValueError("Los dados deben tener al menos 2 lados")
        self._cantidad = cantidad
        self._lados = lados
        self._resultados: List[int] = []
        self._fecha: Optional[datetime] = None

    @property
    def cantidad(self) -> int:
        """Devuelve la cantidad de dados."""
        return self._cantidad

    @property
    def lados(self) -> int:
        """Devuelve el numero de lados de cada dado."""
        return self._lados

    @property
    def resultados(self) -> List[int]:
        """Devuelve los resultados de la tirada."""
        return list(self._resultados)

    @property
    def total(self) -> int:
        """Devuelve la suma total de los resultados."""
        return sum(self._resultados)

    @property
    def fecha(self) -> Optional[datetime]:
        """Devuelve la fecha y hora de la tirada."""
        return self._fecha

    def lanzar(self) -> List[int]:
        """
        Lanza todos los dados y almacena los resultados.

        Returns:
            Lista con los resultados de cada dado.
        """
        self._fecha = datetime.now()
        dado = Dado(self._lados)
        self._resultados = [dado.lanzar() for _ in range(self._cantidad)]
        return list(self._resultados)

    def __str__(self) -> str:
        """Devuelve una representacion en texto de la tirada."""
        if not self._resultados:
            return f"{self._cantidad}d{self._lados}: sin tirar"
        resultados_str = ", ".join(str(r) for r in self._resultados)
        return f"{self._cantidad}d{self._lados}: [{resultados_str}] = {self.total}"
