from Repos.backup_repository import BackupRepository

class GestoreDati:
    def __init__(self, backup_repo: BackupRepository, log_repo):
        self._backup_repo = backup_repo
        self._log_repo = log_repo
    def esegui_backup(self, stringa_dati: str) -> None:

        try:
            # Sfrutta il metodo 'sovrascrivi' della tua BackupRepository
            self._backup_repo.sovrascrivi(stringa_dati)
            print("\n[GestoreDati] Stato di sistema catturato e file JSON sovrascritto.")
        except Exception as e:
            self._log_repo.scriviErrore(f"GestoreDati: Salvataggio automatico fallito. Dettaglio: {str(e)}")
    def recupera_contenuto_backup(self) -> str:
        backup = self._backup_repo.getBackup()
        
        return backup.get("contenuto", "")
