from datetime import time 
class Zona:
    def __init__(self, id: int, nome: str = None, orarioZona: time = None, sogliaZona: list = None ):
        self._id = id
        self._nome = nome
        self._orarioZona = orarioZona
#inizializzo correttamente per evitare la condivisione della lista tra oggetti
        self._sogliaZona = sogliaZona if sogliaZona is not None else [] 
    #definisco i getter

    def getId(self) -> int: 
        return self._id

    def getNome(self) -> str:
        return self._nome

    def getSogliaZona(self) -> list:
        return self._sogliaZona

    def getOrarioZona(self) -> time:
        return self._orarioZona
    #aggiungo elemetni alla lista
    def aggiungiSoglia(self, soglia: float) -> None:
        if not isinstance(soglia, float):
            raise TypeError("la soglia deve essere float")
        self._sogliaZona.append(soglia)
    # definisco la serializzazione per i file json

    def toDict(self) -> dict:
        return {
            "id" : self._id,
            "nome" : self._nome,
            "sogliaZona" : self._sogliaZona,
            "orarioZona": self._orarioZona.isoformat() if self._orarioZona else None, #converto da time a str così che possa essere elaborato dal dict
        }

    @classmethod
    def fromDict(cls, d: dict) -> "Zona":
        orario_str = d["orarioZona"]
        orarioRiconvertito = time.fromisoformat(orario_str) if orario_str is not None else None
        return cls(d["id"], d["nome"], orarioRiconvertito, d["sogliaZona"]) #riconverto da str a time

    #definisco il dunder per stampare le variabili, è opzionale e serve per passare un determinato valore, io lo metto per sicurezza poi da valutare se si deve togliere
    def __str__(self) -> str:
        return f"Zona {self._id}: {self._nome} (Soglia: {self._sogliaZona})"
    
