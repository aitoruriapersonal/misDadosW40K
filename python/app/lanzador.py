# -*- coding: utf-8 -*-
"""Modulo que define el servicio lanzador de dados."""

from .tirada import Tirada
from .historico import Historico


class Lanzador:
    """Servicio que gestiona el lanzamiento de dados y el historico."""

    def __init__(self) -> None:
        """Inicializa el lanzador con un historico vacio."""
        self._historico = Historico()

    @property
    def historico(self) -> Historico:
        """Devuelve el historico de tiradas."""
        return self._historico

    def lanzar(self, cantidad: int, lados: int) -> Tirada:
        """
        Crea y lanza una tirada, almacenandola en el historico.

        Args:
            cantidad: Numero de dados a lanzar.
            lados: Numero de lados de cada dado.

        Returns:
            La tirada realizada con sus resultados.
        """
        tirada = Tirada(cantidad, lados)
        tirada.lanzar()
        self._historico.agregar(tirada)
        return tirada

    def resetear_historico(self) -> None:
        """Resetea el historico de tiradas."""
        self._historico.resetear()

    def resetear_todo(self) -> None:
        """
        Resetea todos los datos gestionados por el servicio (actualmente el historico).

        La configuracion de la tirada (cantidad y lados) es responsabilidad de la
        capa de vista y se resetea desde ahi. Este metodo centraliza el reseteo de
        la capa de datos para el caso del reseteo global.
        """
        self._historico.resetear()
