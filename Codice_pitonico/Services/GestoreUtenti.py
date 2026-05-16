from Models.utente import Utente

class GestoreUtenti:
    def __init__(self, utenti_repo):
        self._utenti_repo = utenti_repo
    
    