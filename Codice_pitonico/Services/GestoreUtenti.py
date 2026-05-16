from Models.utente import Utente

class GestoreUtenti:
    def __init__(self, utenti_repo):
        self._utenti_repo = utenti_repo
    
    def creaAccount(self, id: str, nome: str, pswd: str):
        utente = self._utenti_repo.trovaPerId(id)
        if utente is None:
            nuovo_utente = Utente(id, nome, pswd)
            self._utenti_repo.aggiungi(nuovo_utente)
            return f"Utente creato"
        else:
            return f"Utente già presente"
    
    def eliminaAccount(self, id: str):
        utente_canc = self._utenti_repo.trovaPerId(id)
        if utente_canc is None:
            return f"L'utente cercato non esiste"
        else:
            self._utenti_repo.elimina(id)
            return f"L'utente è stato eliminato"