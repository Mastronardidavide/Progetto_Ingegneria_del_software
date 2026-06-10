from Models.zona import Zona
from Models.sensore import Sensore
from Models.attuatore import Attuatore
from datetime import datetime

class GestoreZona:
    def __init__(self, zona_repo, gestore_dispositivi, log_repo):
        self._zona_repo = zona_repo
        self._g_disp = gestore_dispositivi
        self._log_repo = log_repo

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
    def modificaZona(self, id: int, nuovo_nome: str = None) -> str:
        zona = self._zona_repo.trovaPerId(id)
        if zona is None:
            return "Zona non trovata"
        
        # Modifica condizionale: aggiorna solo i campi compilati dall'utente
        if nuovo_nome:
            zona._nome = nuovo_nome
            
        self._zona_repo.salva()
        return "Zona modificata con successo"
    
    #impostiamo la finsetra temporale della zona, invece di un orario unico di attivazione
    def impostaProgrammazioneOraria(self, id_zona: int, orario_inizio, orario_fine) -> str:
        zona = self._zona_repo.trovaPerId(id_zona)
        if zona is None:
            return "Zona non trovata"
        
        # Se si inserisce l'inizio devi inserire la fine e viceversa
        if (orario_inizio and not orario_fine) or (orario_fine and not orario_inizio):
            return "Errore: Devi inserire sia l'orario di inizio sia l'orario di fine."

        # Aggiorniamo l'oggetto rispettando information expret
        zona._orarioZona = orario_inizio
        zona._orarioDisattivazione = orario_fine
        
        # Salviamo la modifica sul file JSON
        self._zona_repo.salva()
        return "Programmazione oraria salvata con successo"


# controllo periodico per verificare se è il momento di attivare le automazioni basate su orario o soglia,
#ci limitiamo a identificare quali attuatori dovrebbero essere accesi e quali no. in tal modo possiamo passare l'informazione
#a gestorescenari, il quale fa un controllo prioritario: dato che sono gli scenari ad avere la priorità, si assicura che se una zona vuole 
#accendere un attuatore, condizione necessaria è che lo scenario non lo richieda spento, in tal modo rispettiamo ECB ed evitiamo
#conflitti tra zone e scenari, in caso uno voglia spegnere un attuatore e l'altro accenderlo
    def calcola_potenziali_attuatori(self) -> dict:
        try:
            orario_corrente = datetime.now().time()
            orario_confronto = orario_corrente.replace(second=0, microsecond=0)
            intenzioni = {}

            for zona in self._zona_repo.tutte(): #imposto le condizioni che mi permettono di dire che un attuatore si dovrebbe accendere
                accensione_orario = False
                accensione_soglia = False

                if zona.getOrarioZona() is not None and zona.getOrarioDisattivazione() is not None: #verifico la condizione per l'orario
                    inizio = zona.getOrarioZona().replace(second=0, microsecond=0)
                    fine = zona.getOrarioDisattivazione().replace(second=0, microsecond=0)
                    if inizio <= orario_confronto < fine:
                        accensione_orario = True

                if not accensione_orario and zona.getIdSensore() is not None: #verifico la condizione per la soglia associata al sensore pilota
                    sensore = self._g_disp._dispositivo_repo.trovaPerId(zona.getIdSensore())
                    if sensore is not None:
                        valore_corrente = sensore.misurazione()
                        if valore_corrente is not None and valore_corrente > zona.getSogliaZona():
                            accensione_soglia = True

                condizione = accensione_orario or accensione_soglia #faccio il merge delle condizioni tramite or

                #qui controllo che l'attuatore in una zona non sia stato considerato in altre zone, o che la condizione di accensione
                # sia verificata, in questo caso avviene la potenziale accensione: l'accensione ha priorità sullo spegnimento,
                # basta una sola condizione per cui l'attuatore si debba accendere per far sì che lo faccia 
                for id_attuatore in zona.getIdAttuatori():
                    if id_attuatore not in intenzioni or condizione:
                        intenzioni[id_attuatore] = condizione

            return intenzioni #ritorno la lista di attuatori potenzialmente da accendere o spegnere

        except Exception as e:
            self._log_repo.scriviErrore(f"GestoreZona.calcola_intenzioni_attuatori() fallito: {str(e)}")
            return {}
