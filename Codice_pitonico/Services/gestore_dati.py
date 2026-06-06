from Repos.backup_repository import BackupRepository

class GestoreDati:
    def __init__(self, backup_repo: BackupRepository):
        self._backup_repo = backup_repo

    def esegui_backup(self, stringa_dati: str) -> None:

        try:
            # Sfrutta il metodo 'sovrascrivi' della tua BackupRepository
            self._backup_repo.sovrascrivi(stringa_dati)
            print("\n[GestoreDati] Stato di sistema catturato e file JSON sovrascritto.")
        except Exception as e:
            print(f"\n[GestoreDati Errore] Salvataggio automatico fallito: {e}")

    def recupera_contenuto_backup(self) -> str:
        backup = self._backup_repo.getBackup()
        
        return backup.get("contenuto", "")
