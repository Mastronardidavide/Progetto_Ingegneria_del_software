from datetime import datetime
class Scenario:
    def __init__(self, id: str, nome: str, sogliaScenario: float, orarioScenario: datetime):

        #attributi protetti
        self._id = id
        self._nome = nome
        self.sogliaScenario = sogliaScenario
        self.orarioScenario = orarioScenario

    #getter
    def getId(self) -> str: return self._id
    def getNome(self) -> str: return self._nome
    
    #formattazione della classe in dizionario
    def toDict(self) -> dict:
        return {"id": self._id, "Nome": self._nome, "sogliaScenario": self.sogliaScenario, "orarioScenario":self.orarioScenario}
    
    #e del dizionario in classe
    @classmethod
    def fromDict(cls, d: dict) -> "Scenario":
        return cls(d["id"], d["nome"], d["sogliaScenario"], d["orarioScenario"])
        


    #id diventa str/ getter non necessari per attributi pubblici