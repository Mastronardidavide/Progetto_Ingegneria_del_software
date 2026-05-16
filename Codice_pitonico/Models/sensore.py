#se c'è ereditarietà devo importare qualcosa tipo dispositivo? a

class Sensore(Dispositivo):
    def __init__(self, id: str, nome:str, soglia: float):
        
        super().__init__(id)
        self._nome = nome
        #inizializzo la lista
        self._soglia = soglia
    
    
    def setSoglia(self, nuova_soglia: float) -> None:
        self._soglia = nuova_soglia

    def getSoglia(self) -> float:
        return self._soglia
    def aggiungiSoglia(self, soglia: float) -> None:
        # alzo l'errore se non è float
        if not isinstance(soglia, float):
            raise TypeError("La soglia deve essere float")
        self._soglia.append(soglia)

    def toDict(self) -> dict:
        return {"id": self._id, "nome": self._nome, "soglia": self._soglia}
    
    @classmethod
    def fromDict(cls, d:dict) -> "Sensore":
        return cls(d["id"], d["nome"], d["soglia"])
    #uso un dunder method per stampare i dati
    def __str__(self) -> str:
        return f"Sensore {self._id} (Soglie: {self._soglia})"