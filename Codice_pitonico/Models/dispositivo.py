from abc import ABC, abstractmethod

class Dispositivo(ABC):
    def __init__(self, id: str, tipo: str):

        self._id = id
        self._tipo = tipo

    def getId(self) -> str: return self._id
    def getTipo(self) ->str: return self._tipo