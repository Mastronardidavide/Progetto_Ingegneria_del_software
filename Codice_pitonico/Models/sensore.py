#se c'è ereditarietà devo importare qualcosa tipo dispositivo?

class Sensore(Dispositivo):
    def __init__(self, id: str, nome:str, soglia: float):
        
        super().__init__(id)
        self._nome = nome
        self._soglia = soglia

    def toDict(self) -> dict:
        return {"id": self._id, "nome": self._nome, "soglia": self._soglia}
    
    def setSoglia(self, nuova_soglia: float) -> None:
        self._soglia = nuova_soglia

    def getSoglia(self) -> float:
        return self._soglia

    @classmethod
    def fromDict(cls, d:dict) -> "Sensore":
        return cls(d["id"], d["nome"], d["soglia"])