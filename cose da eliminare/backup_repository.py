from datetime import datetime
import json

class BackupRepository:
    def __init__(self, path: str = "Data/backups.json"):
        self._path = path
        self._backups: list = [] #usiamo una lista per conservare la cronologia di backup 
        self.carica()

#da QUI a
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
    def fromDict(cls, d: dict) -> dict:
        return cls(d["orario"], d["contenuto"])
#QUI ci sono le funzioni spostate dalla vecchia classe backup di models in questa, dato che abbiamo dovuto eliminare la prima

    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding = "utf-8") as f:
                dati = json.load(f) #questo ricostrusce gli oggetti usando il metodo fromDict.
                self._backups = [] #svuoto la lista e la riempo ricostruendo gli oggetti Backup
                for d in dati:
                    self._backups.append(self.fromDict(d))
            
        except FileNotFoundError:
            self._backups = [] #se nel primo avvio il file non esiste, la lista rimane vuota

    def salva(self) -> None: #salve i dati sul file prima di chiudere
        with open(self._path,"w", encoding = "utf-8") as f:
            json.dump([b.toDict() for b in self._backups], f, indent = 2) #serializzazione ed uso toDict per trasformare ogni backup in dizionario e salva tutto nel JSON.

    def aggiungi(self, backup: dict) -> None: #Metodo per registraare un nuovo backup
        self._backups.append(backup)
        self.salva()

    def tutti(self) -> list:
        return self.backups