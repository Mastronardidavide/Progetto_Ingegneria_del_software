from datetime import datetime
import json

#in questo modo l'implementazione è più snella rispetto ad avere una classe a parte che effettivamente si dovrebbe occupare esclusivamente di un solo dizionario
class BackupRepository:
    def __init__(self, path: str = "Data/backups.json"):
        self._path = path
        self._backup_corrente: dict = {} # Un singolo dizionario (backup) da sovrascrivere periodicamente
        self.carica()

    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                # Carica direttamente il singolo dizionario del backup
                self._backup_corrente = json.load(f)
        except FileNotFoundError:
            self._backup_corrente = {} # Se il file non esiste, il backup parte vuoto

    def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            # Salva il dizionario, ossia il backup
            json.dump(self._backup_corrente, f, indent=2, ensure_ascii=False)

    def sovrascrivi(self, contenuto_da_salvare: str) -> None:
        # sovrascrive il vecchio backup
        self._backup_corrente = {
            "orario": datetime.now().isoformat(),
            "contenuto": contenuto_da_salvare
        }
        self.salva()

    def getBackup(self) -> dict:
        # Ritorna l'unico backup presente in memoria
        return self._backup_corrente
    