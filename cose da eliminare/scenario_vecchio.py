from datetime import time

class Scenario:
    def __init__(self, id: str, nome: str, orarioScenario: time, sogliaScenario: float):
        self._id = id
        self._nome = nome
        self._orarioScenario = orarioScenario
        self._sogliaScenario = sogliaScenario if sogliaScenario is not None else [] 

    def getId(self) -> int: 
        return self._id

    def getNome(self) -> str:
        return self._nome

    def getSogliaScenario(self) -> list:
        return self._sogliaScenario

    def getOrarioScenario(self) -> time:
        return self._orarioScenario
    #aggiungo elemetni alla lista
    def aggiungiSoglia(self, soglia: float) -> None:
        if not isinstance(soglia, float):
            raise TypeError("la soglia deve essere float")
        else:
            self._sogliaScenario.append(soglia)
            return f"Soglia aggiunta allo scenario"
    # definisco la serializzazione per i file json

    def toDict(self) -> dict:
        return {
            "id" : self._id,
            "nome" : self._nome,
            "sogliaScenario" : self._sogliaScenario,
            "orarioScenario": self._orarioScenario.isoformat() if self._orarioScenario else None, #converto da time a str così che possa essere elaborato dal dict
        }

    @classmethod
    def fromDict(cls, d: dict) -> "Scenario":
        orario_str = d["orarioScenario"]
        orarioRiconvertito = time.fromisoformat(orario_str) if orario_str is not None else None
        return cls(d["id"], d["nome"], orarioRiconvertito, d["sogliaScenario"]) #riconverto da str a time

    #definisco il dunder per stampare le variabili, è opzionale e serve per passare un determinato valore, io lo metto per sicurezza poi da valutare se si deve togliere
    def __str__(self) -> str:
        return f"Zona {self._id}: {self._nome} (Soglia: {self._sogliaScenario})"