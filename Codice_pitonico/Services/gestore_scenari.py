from Models.scenario import Scenario

class GestoreScenario:
    def __init__(self, scenario_repo):
        self._scenario_repo = scenario_repo

    def creaScenario(self, id: int, nome: str): #creaScenario controlla che la Scenario non esista già, dopodiché la crea
        scenario = self._scenario_repo.trovaPerId(id)
        if scenario is None:
            nuova_scenario = Scenario(id, nome)
            self._scenario_repo.aggiungi(nuova_scenario)
            return f"Lo scenario è stato creato con successo"
        else:
            return f"Lo scenario è già presente"
    def eliminaScenario(self, id: int): #elimina Scenario fa la stessa cosa ma controlla che esista
        scenario_canc = self._scenario_repo.trovaPerId(id)
        if scenario_canc is None:
            return f"Scenario non trovato"
        else:
            self._scenario_repo.elimina(id)
            return f"Scenario eliminato"
    def visualizzaScenario(self, id:int): #visualizzazione mi ritorna la Scenario
        scenario_vis = self._scenario_repo.trovaPerId(id)
        if scenario_vis is None:
            return f"Scenario non trovato"
        else:
            return scenario_vis
    def personalizzaDispositivoScenario(self, id:str): #
        