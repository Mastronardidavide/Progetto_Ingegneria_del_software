#se c'è ereditarietà devo importare qualcosa tipo dispositivo? a

class Sensore(Dispositivo):
    def __init__(self, id: str,tipo : str, nome:str = None, soglia: float = None):
        
        super().__init__(id, tipo)
        self._nome = nome
        #inizializzo la lista
        self._soglia = soglia

    def getSoglia(self) -> float:
        return self._soglia
    def setSoglia(self, nuova_soglia: float) -> None:
        # alzo l'errore se non è float
        if not isinstance(nuova_soglia, float):
            raise TypeError("La soglia deve essere float")
        else:
            self._soglia = nuova_soglia

    def toDict(self) -> dict:
        return {"id": self._id, "tipo": self._tipo,"nome": self._nome, "soglia": self._soglia}
    
    @classmethod
    def fromDict(cls, d:dict) -> "Sensore":
        return cls(d["id"],d["tipo"], d["nome"], d["soglia"])
    #uso un dunder method per stampare i dati
    def __str__(self) -> str:
        return f"Sensore {self._id} (Soglie: {self._soglia})"