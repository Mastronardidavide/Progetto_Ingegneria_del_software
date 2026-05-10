from abc import ABC, abstractmethod

class Dispositivo(ABC):
    def __init__(self, id: str):

        self._id = id

    def getId(self) -> str: return self._id

