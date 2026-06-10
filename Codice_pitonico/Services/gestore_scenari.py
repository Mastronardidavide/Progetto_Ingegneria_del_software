from Models.scenario import Scenario
from Models.sensore import Sensore
from Models.attuatore import Attuatore
from datetime import datetime

class GestoreScenario:
    def __init__(self, scenario_repo, gestore_dispositivi, log_repo):
        self._scenario_repo = scenario_repo
        self._g_disp = gestore_dispositivi
        self._log_repo = log_repo

    def creaScenario(self, id: int, nome: str): 
        scenario = self._scenario_repo.trovaPerId(id)
        if scenario is None:
            nuovo_scenario = Scenario(id, nome)
            self._scenario_repo.aggiungi(nuovo_scenario)
            return "Lo scenario è stato creato con successo"
        else:
            return "Lo scenario è già presente"

    def eliminaScenario(self, id: int): 
        scenario_canc = self._scenario_repo.trovaPerId(id)
        if scenario_canc is None:
            return "Scenario non trovato"
        else:
            self._scenario_repo.elimina(id)
            return "Scenario eliminato"

    def visualizzaScenario(self, id: int): 
        scenario_vis = self._scenario_repo.trovaPerId(id)
        if scenario_vis is None:
            return "Scenario non trovato"
        else:
            return scenario_vis

    def impostaAutomazioneSensore(self, id_scenario: int, id_sensore: str, valore_soglia: float) -> str:
        scenario = self._scenario_repo.trovaPerId(id_scenario)
        if scenario is None:
            return "Scenario non trovato"
        
        if (id_sensore and valore_soglia is None) or (valore_soglia is not None and not id_sensore):
            return "Errore: Sensore e Soglia devono essere inseriti insieme."

        if id_sensore:
            sensore_esistente = self._g_disp._dispositivo_repo.trovaPerId(id_sensore)
            if sensore_esistente is None or not isinstance(sensore_esistente, Sensore):
                return f"Errore: Il sensore con ID '{id_sensore}' non esiste nella domotica. Automazione annullata."

        scenario._id_sensore = id_sensore
        scenario.impostaSoglia(valore_soglia)
        
        self._scenario_repo.salva()
        return "Automazione dello scenario configurata con successo"
    
    def associaAttuatoreAScenario(self, id_scenario: int, id_attuatore: str) -> str:
        scenario = self._scenario_repo.trovaPerId(id_scenario)
        if scenario is None:
            return "Scenario non trovato"
        
        attuatore_esistente = self._g_disp._dispositivo_repo.trovaPerId(id_attuatore)
        if attuatore_esistente is None or not isinstance(attuatore_esistente, Attuatore):
            return f"Errore: L'attuatore con ID '{id_attuatore}' non esiste nel sistema."
        
        scenario.associaAttuatore(id_attuatore)
        self._scenario_repo.salva()
        return f"Attuatore '{id_attuatore}' associato allo scenario con successo"
    
    def rimuoviAttuatoreDaScenario(self, id_scenario: int, id_attuatore: str) -> str:
        scenario = self._scenario_repo.trovaPerId(id_scenario)
        if scenario is None:
            return "Scenario non trovato"
        
        if id_attuatore not in scenario.getIdAttuatori():
            return f"L'attuatore '{id_attuatore}' non è associato a questa scenario"
            
        scenario.rimuoviAttuatore(id_attuatore)
        self._scenario_repo.salva()
        return f"Attuatore '{id_attuatore}' rimosso dallo scenario con successo"

    def modificaScenario(self, id: int, nuovo_nome: str = None) -> str:
        scenario = self._scenario_repo.trovaPerId(id)
        if scenario is None:
            return "Scenario non trovato"
        
        if nuovo_nome:
            scenario._nome = nuovo_nome
            
        self._scenario_repo.salva()
        return "Scenario modificato con successo"
    
    def impostaProgrammazioneOraria(self, id_scenario: int, orario_inizio, orario_fine) -> str:
        scenario = self._scenario_repo.trovaPerId(id_scenario)
        if scenario is None:
            return "Scenario non trovato"
        
        if (orario_inizio and not orario_fine) or (orario_fine and not orario_inizio):
            return "Errore: Devi inserire sia l'orario di inizio sia l'orario di fine."

        scenario._orarioScenario = orario_inizio
        scenario._orarioDisattivazione = orario_fine
        
        self._scenario_repo.salva()
        return "Programmazione oraria salvata con successo"

    def check_automazioni_prioritarie(self, gestore_zona) -> None:
        try:
            orario_corrente = datetime.now().time()
            orario_confronto = orario_corrente.replace(second=0, microsecond=0)

            decisioni_attuatori = gestore_zona.calcola_potenziali_attuatori() #mi faccio calcolare i potenziali attuatori delle zone

            for scenario in self._scenario_repo.tutte():
                accensione_scenario = False

                #controllo che l'rario ricada nella finestra temporale
                if scenario.getOrarioScenario() is not None and scenario.getOrarioDisattivazione() is not None:
                    inizio = scenario.getOrarioScenario().replace(second=0, microsecond=0)
                    fine = scenario.getOrarioDisattivazione().replace(second=0, microsecond=0)
                    if inizio <= orario_confronto < fine:
                        accensione_scenario = True
                #controllo analogo sulla soglia del sensore pilota di ciascuno scenario
                if not accensione_scenario and scenario.getIdSensore() is not None:
                    sensore = self._g_disp._dispositivo_repo.trovaPerId(scenario.getIdSensore())
                    if sensore is not None:
                        valore_corrente = sensore.misurazione()
                        if valore_corrente is not None and valore_corrente > scenario.getSogliaScenario():
                            accensione_scenario = True
                #sovrascrivo la volontà della zona in favore di quella dell'attuatore
                if scenario.getOrarioScenario() is not None or scenario.getIdSensore() is not None: 
                    for id_attuatore in scenario.getIdAttuatori():
                        decisioni_attuatori[id_attuatore] = accensione_scenario

            #setto il cambiamento effettivo
            cambiamento_effettuato = False
            for id_attuatore in decisioni_attuatori:
                stato_desiderato = decisioni_attuatori[id_attuatore]
                
                attuatore = self._g_disp._dispositivo_repo.trovaPerId(id_attuatore)
                if attuatore is not None:
                    #se lo stato desiderato è on e l'attuatore è spento, lo accendo
                    if stato_desiderato and attuatore.getStato() == False:
                        attuatore.cambiaStato()
                        cambiamento_effettuato = True
                        print(f"[Automazione Coordinata] Attuatore '{id_attuatore}' ACCESO.")
                    #se lo stato desiderato è off e l'attuatore è acceso, lo spengo
                    elif not stato_desiderato and attuatore.getStato() == True:
                        attuatore.cambiaStato()
                        cambiamento_effettuato = True
                        print(f"[Automazione Coordinata] Attuatore '{id_attuatore}' SPENTO.")

            if cambiamento_effettuato: #salvo le modifiche
                self._g_disp._dispositivo_repo.salva()

        except Exception as e: #salvo eventuali errori nel log
            self._log_repo.scriviErrore(f"GestoreScenario.check_automazioni_coordinate() fallito: {str(e)}")
