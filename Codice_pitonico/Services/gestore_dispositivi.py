from datetime import time
from Models.sensore import Sensore
from Models.attuatore import Attuatore

class GestoreDispositivi:
    #utilizzo la Dependency Inversion: il control riceve la repository dal main
    def __init__(self, dispositivo_repo):
        self._dispositivo_repo = dispositivo_repo
    # Aggiungo il caso d'uso : aggiungi dispositivo
    def aggiungiDispositivo(self, id_disp: str, tipo: str) -> str:
        # verifica preventiva presa fa GEstione prestiti
        disp = self._dispositivo_repo.trovaPerId(id_disp)
        if disp is not None:
            return f"Errore: Dispositivo {id_disp} già presente"
        
        #creo L'entity in base al tipo richiesto
        if tipo == "Sensore":
            nuovo_disp = Sensore(id_disp, tipo)
        elif tipo == "Attuatore":
            nuovo_disp = Attuatore(id_disp, tipo)
        else:
            return ("Errore: Tipo dispositivo non valido")
        
        #aggiungo il dispositivo alla repository
        self._dispositivo_repo.aggiungi(nuovo_disp)
        return f"{tipo} {id_disp} aggiunto con successo"
    #Caso d'uso rimuovi dispositivo
    def rimuoviDispositivo(self, id_disp: str) -> str:
        #recupero l'oggetto prima di rimuoverlo
        disp = self._dispositivo_repo.trovaPerId(id_disp)
        #Gestisco l'errore se non esiste
        if disp is None:
            return f"Errore: Dispositivo {id_disp} non trovato"
    # rimuovo il dispositivo nella ripository
        else:
            self._dispositivo_repo.elimina(id_disp)
            return f"Dispositivo {id_disp} rimosso con successo"
    
    #Caso d'uso: visualizza dati dispositivo
    def visualizzaDispositivo(self,id_disp: str):
        disp = self._dispositivo_repo.trovaPerId(id_disp)
        if disp is None:
            return f"Errore: Dispositivo {id_disp} non trovato"
        return disp #ritorna l'oggetto per poterlo visualizzare
    def configuraDispositivo(self, id: str, nuova_soglia: float = None, nuovo_stato: bool = None, nuovo_orario: time = None):
        disp = self._dispositivo_repo.trovaPerId(id) #controllo che esista
        if disp == None:
            return f"dispositivo non trovato"
        else:
            if isinstance(disp, Sensore):
                disp.setSoglia(nuova_soglia)
            elif isinstance(disp, Attuatore):
                disp.setStato(nuovo_stato)
                disp.setOrario(nuovo_orario)
            return f"dispositivo riconfigurato"
 #violazione controllata di OC: non ci aspettiamo che venga inventato un nuovo tipo di dispositivo in futuro, quindi sviluppiamo il sistema
 #sulla base di sensore e attuatore
 #LINE49