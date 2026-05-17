from datetime import time

class Attuatore(Dispositivo): #eredita da dispositivo
    def __init__(self, id: str,tipo :str, nome:str = None, orarioAttivazione: time = None, statoAttuatore: bool = None):
        
        super().__init__(id, tipo)
        self._nome = nome
        self._orarioAttivazione = orarioAttivazione
        self._statoAttuatore = statoAttuatore #forse si deve inizializzare a uno stato spento?

    #passo a dizionario
    def toDict(self) -> dict:
        return {"id": self._id,
                "tipo": self._tipo,
                "nome": self._nome,
                "orarioAttivazione": self._orarioAttivazione.isoformat() if self._orarioAttivazione else None, 
                "stato": self._statoAttuatore}
    
    #definisco i metodi della classe
    def setOrario(self, nuovo_orario: time) -> None:
        self._orarioAttivazione = nuovo_orario

    def getOrario(self) -> time:
        return self._orarioAttivazione
    
    def getStato(self) -> bool:
        return self._statoAttuatore

    def cambiaStato(self) -> None: #cambia stato facendo un toggle
        self._statoAttuatore = not self._statoAttuatore

    #passo a oggetto da dizionario
    @classmethod
    def fromDict(cls, d:dict) -> "Attuatore":
        orario_str = d["orarioAttivazione"]
        orarioRiconvertito = time.fromisoformat(orario_str) if orario_str is not None else None
        return cls(d["id"], d["tipo"], d["nome"], orarioRiconvertito, d["stato"])