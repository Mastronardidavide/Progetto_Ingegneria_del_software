from abc import ABC, abstractmethod
class Autenticabile(ABC): #interfaccia
    @abstractmethod
    def autentica(self, utente: str, password: str) -> bool:
        pass
class Utente(Autenticabile): #classe astratta

    def __init__(self, id: str, nome: str, password: str,): #aggiungo la passowrd per l'interfaccia autenticabile
        self._id = id
        self._nome = nome
        self._password = password

        def getID(self) -> str:
            return self._id
        
        def getNome(self) -> str:
            return self._nome
        
        def toDict(self) -> dict: #per il salvataggio dei dati in Json
            return{
                "id": self._id,
                "nome": self._nome,
                "password": self._password
            }
        def autentica(self, utente: str, password: str) -> bool:
            return self._nome == utente and self._password == password
#non posso usare isinstance perche violiamo il principio di SOLID, Open/ Closed
        @abstractmethod #metodo della classe astratta Utente
        def visualizzaDatiDispositivo(self, dispositivo):
            pass