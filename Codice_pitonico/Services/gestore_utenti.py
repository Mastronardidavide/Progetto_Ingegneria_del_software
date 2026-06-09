from Models.utente import Utente
from Repos.utente_repository import UtenteRepository

class GestoreUtenti:
    def __init__(self, utenti_repo):
        self._utenti_repo = utenti_repo
    
    def creaAccount(self, id: str, nome: str, pswd: str):
        utente = self._utenti_repo.trovaPerId(id)
        if utente is None:
            nuovo_utente = Utente(id, nome, pswd, "Ospite")
             #qui è importante specificare Ospite perchè ci sono 4 argomenti obbligatori, un nuovo utente creato sarà sempre infatti ospite
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
        #da qui in poi
    def login(self, id: str, nome: str, pswd: str):
        utente = self._utenti_repo.trovaPerId(id) # cerco l'utente tramite l'ID
        if utente is None:
            print("Errore: utente non trovato")
            return None
        
        # delego il controllo delle credenziali all'utente stesso, ritorna un booleano
        if utente.autentica(nome, pswd):
            return f"Accesso consentito. Benvenuto {utente.getNome()} ({utente.getTipo()})"
        else:
            print("Credenziali errate")
            return None
    
    def tuttiToDict(self):
        return [u.toDict() for u in self._utenti_repo.tutti()]