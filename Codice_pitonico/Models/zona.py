class Zona:
    def __init__(self, id: int, nome: str, sogliaZona: float, orarioZona: str ):# mi da errore su datedime mi dice di definirlo datetime any, ho messo scome str dettato da gemini
        self._id = id
        self._nome = nome
        self._sogliaZona = sogliaZona
        self._orarioZona = orarioZona

#definisco i getter

def getID(self) -> int: 
    return self._id

def getNome(self) -> str:
    return self._nome

def getSogliaZona(self) -> float:
    return self._sogliaZona

def getorarioZona(self) -> str:
    return self._orarioZona

# definisco la serializzazione per i file json

def toDict(self) -> dict:
    return {
        "id" : self._id,
        "nome" : self._nome,
        "sogliaZona" : self._sogliaZona,
        "orarioZona" : self._orarioZona,
    }

@classmethod
def fromDict(cls, d: dict) -> "Zona":
    return cls(d["id"], d["nome"], d["sogliaZona"], d["orarioZona"])

#definisco il dunder per stampare le variabili, anna pepe dice che è opzionale e serve per passare un determinato valore, io lo metto per sicurezza poi da valutare se si deve togliere
def __str__(self) -> str:
    return f"Zona {self._id}: {self._nome} (Soglia: {self._sogliaZona})"