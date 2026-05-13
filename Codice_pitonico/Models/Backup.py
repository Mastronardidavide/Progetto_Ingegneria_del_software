from datetime import datetime
class Backup:
    def __init__(self, orario: datetime, contenuto: str):
        self._orario = orario
        self._contenuto = contenuto
    
    def getOrarioBackup(self) -> datetime:
        return self._orario
    
    def getContenuto(self) -> str:
        return self._contenuto
    
    def toDict(self) -> dict:
        return{
            "orario" : str(self._orario),
            "contenuto" : self._contenuto
        }
    #metodi della classe
    
    @classmethod
    def fromDict(cls, d: dict) -> Backup:
        return cls(d["orario"], d["contenuto"])
