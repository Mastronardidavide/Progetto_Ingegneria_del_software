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


# controllo periodico per verificare se è il momento di attivare le automazioni basate su orario o soglia
    def check_automazioni_zone(self) -> None:
        #proviamo a svolgere la funzione, ma intercettiamo gli errori se presenti e li scriviamo nel log
        try:

            orario_corrente = datetime.now().time()
            # forziamo il confronto al minuto per non gestire secondi e sopratutto microsecondi
            orario_confronto = orario_corrente.replace(second=0, microsecond=0)

            # Cicliamo su tutte le zone presenti nel sistema
            for zona in self._zona_repo.tutte():
                accensione_orario = False
                accensione_soglia = False

                #Controllo Orario, mi assicuro che abbia un orario di attivazione e disattivazione
                if zona.getOrarioZona() is not None and zona.getOrarioDisattivazione() is not None:
                    # Allineiamo anche l'orario della zona al minuto per sicurezza nel confronto
                    inizio = zona.getOrarioZona().replace(second=0, microsecond=0)
                    fine = zona.getOrarioDisattivazione().replace(second=0, microsecond=0)
                    #controllo che l'orario ricada nella finestra temporale
                    if inizio <= orario_confronto < fine: #non metto l'uguale perché se è esattamente l'orario di disattivazione, la zona deve spegnersi
                        print(f"[Automazione Orario] Raggiunto l'orario per la zona '{zona.getNome()}'.")
                        accensione_orario = True

                # Controll sulla soglia, se l'orario non è superato
                if not accensione_orario and zona.getIdSensore() is not None:
                    # Recuperiamo il sensore dalla repository dei dispositivi per
                    sensore = self._g_disp._dispositivo_repo.trovaPerId(zona.getIdSensore())
                    
                    # Verifichiamo che il sensore esista
                    if sensore is not None:
                        valore_corrente = sensore.misurazione()
                        
                        if valore_corrente is not None and valore_corrente > zona.getSogliaZona():
                            print(f"[Automazione Sensore] Il sensore '{zona.getIdSensore()}' ({valore_corrente}) ha superato la soglia ({zona.getSogliaZona()}) per la zona '{zona.getNome()}'.")
                            accensione_soglia = True

                # attivazione degli attuatori, prendo lo stato desiderato "condizione" tramite logica OR
                condizione = accensione_orario or accensione_soglia
                
                    # Se almeno uno dei criteri è soddisfatto, accendiamo tutti gli attuatori della zona
                for id_attuatore in zona.getIdAttuatori():
                    attuatore = self._g_disp._dispositivo_repo.trovaPerId(id_attuatore)
                    if attuatore is not None:
                        # Chiamiamo il metodo per accendere l'attuatore.
                        #primo caso: la condizione è soddisfatta e l'attuatore è spento, lo accendiamo
                        if condizione and attuatore.getStato() == False:
                            attuatore.cambiaStato()
                            print("attuatore acceso,per debug", id_attuatore) #per debug, da rimuovere
                        elif not condizione and attuatore.getStato() == True:
                            attuatore.cambiaStato()
                            print("attuatore spento, per debug", id_attuatore) #per debug, da rimuovere
                    # Salviamo tutto in repo
                    self._g_disp._dispositivo_repo.salva()
        except Exception as e:
            #intercettiamo gli errori e li riportiamo nel log
            self._log_repo.scriviErrore(f"GestoreZona.check_automazioni_zone() fallito: {str(e)}")