from Models.zona import Zona
from Models.sensore import Sensore
from Models.attuatore import Attuatore

class GestoreZona:
    def __init__(self, zona_repo, gestore_dispositivi):
        self._zona_repo = zona_repo
        self._g_disp = gestore_dispositivi

    def creaZona(self, id: int, nome: str): 
        zona = self._zona_repo.trovaPerId(id)
        if zona is None:
            nuova_zona = Zona(id, nome)
            self._zona_repo.aggiungi(nuova_zona)
            return "La zona è stata creata con successo"
        else:
            return "La zona è già presente"

    def eliminaZona(self, id: int): 
        zona_canc = self._zona_repo.trovaPerId(id)
        if zona_canc is None:
            return "Zona non trovata"
        else:
            self._zona_repo.elimina(id)
            return "Zona eliminata"

    def visualizzaZona(self, id: int): 
        zona_vis = self._zona_repo.trovaPerId(id)
        if zona_vis is None:
            return "Zona non trovata"
        else:
            return zona_vis

        #imposta la coppia sensore-soglia per ogni zona
    def impostaAutomazioneSensore(self, id_zona: int, id_sensore: str, valore_soglia: float) -> str:
        zona = self._zona_repo.trovaPerId(id_zona)
        if zona is None:
            return "Zona non trovata"
        
        if (id_sensore and valore_soglia is None) or (valore_soglia is not None and not id_sensore):
            return "Errore: Sensore e Soglia devono essere inseriti insieme."

        # Verifichiamo che il sensore esista nel sistema tramite il gestore dispositivi
        if id_sensore:
            sensore_esistente = self._g_disp._dispositivo_repo.trovaPerId(id_sensore)
            if sensore_esistente is None or not isinstance(sensore_esistente, Sensore):
                return f"Errore: Il sensore con ID '{id_sensore}' non esiste nella domotica. Automazione annullata."

        zona._id_sensore = id_sensore
        zona.impostaSoglia(valore_soglia)
        
        self._zona_repo.salva()
        return "Automazione della zona configurata con successo"
    
    # aggiunge un attuatore alla zona, se non è già presente, e salva le modifiche
    def associaAttuatoreAZona(self, id_zona: int, id_attuatore: str) -> str:
        zona = self._zona_repo.trovaPerId(id_zona)
        if zona is None:
            return "Zona non trovata"
        
        #Chiediamo al repository dei dispositivi se l'ID esiste
        attuatore_esistente = self._g_disp._dispositivo_repo.trovaPerId(id_attuatore)
        if attuatore_esistente is None or not isinstance(attuatore_esistente, Attuatore):
            return f"Errore: L'attuatore con ID '{id_attuatore}' non esiste nel sistema."
        
        # Se esiste, procediamo all'inserimento
        zona.associaAttuatore(id_attuatore)
        self._zona_repo.salva()
        return f"Attuatore '{id_attuatore}' associato alla zona con successo"
    
    #secondo lo stesso principio del metodo precedente, rimuove un attuatore dalla zona se è presente e salva le modifiche
    def rimuoviAttuatoreDaZona(self, id_zona: int, id_attuatore: str) -> str:
        zona = self._zona_repo.trovaPerId(id_zona)
        if zona is None:
            return "Zona non trovata"
        
        if id_attuatore not in zona.getIdAttuatori():
            return f"L'attuatore '{id_attuatore}' non è associato a questa zona"
            
        zona.rimuoviAttuatore(id_attuatore)
        self._zona_repo.salva()
        return f"Attuatore '{id_attuatore}' rimosso dalla zona con successo"

    # aggiorna il nome e/o l'orario di una zona
    def modificaZona(self, id: int, nuovo_nome: str = None, nuovo_orario = None) -> str:
        zona = self._zona_repo.trovaPerId(id)
        if zona is None:
            return "Zona non trovata"
        
        # Modifica condizionale: aggiorna solo i campi compilati dall'utente
        if nuovo_nome:
            zona._nome = nuovo_nome
            
        if nuovo_orario:
            zona._orarioZona = nuovo_orario
            
        self._zona_repo.salva()
        return "Zona modificata con successo"
