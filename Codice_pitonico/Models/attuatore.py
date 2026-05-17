from datetime import datetime

class Attuatore(Dispositivo): #eredita da dispositivo
    def __init__(self, id: str,tipo :str, nome:str = None, orarioAttivazione: datetime = None, statoAttuatore: bool = None):
        
        super().__init__(id, tipo)
        self._nome = nome
        self._orarioAttivazione = orarioAttivazione
        self._statoAttuatore = statoAttuatore #forse si deve inizializzare a uno stato spento?

    #passo a dizionario
    def toDict(self) -> dict:
        return {"id": self._id, "nome": self._nome, "orario": self._orarioAttivazione, "stato": self._statoAttuatore}
    
    #definisco i metodi della classe
    def setOrario(self, nuovo_orario: datetime) -> None:
        self._orarioAttivazione = nuovo_orario

    def getOrario(self) -> datetime:
        return self._orarioAttivazione
    
    def getStato(self) -> bool:
        return self._statoAttuatore

    def cambiaStato(self) -> None: #cambia stato facendo un toggle
        self._statoAttuatore = not self._statoAttuatore

    #passo a oggetto da dizionario
    @classmethod
    def fromDict(cls, d:dict) -> "Attuatore":
        return cls(d["id"], d["nome"], d["orario"], d["stato"])