#DA ELIMINARE PERCHè MANCA VISUALIZZADISPOSITIVI
from datetime import time

class GestoreDispositivi:

    def __init__(self, DispositiviRepo):
        self._DispositiviRepo = DispositiviRepo
    
    def aggiungiDispositivo(self, id: str):
        dispositivo = Dispositivo(id) #poi il sensore ha la soglia mentre l'attuatore ha lo stato, come li passo gli argomenti?
        self._DispositiviRepo.aggiungi(dispositivo)#oppure mantengo il setsoglia e setstato che sono in sensore e attuatore?
    
    def rimuoviDispositivo(self, id: str):
        dispositivo = self._DispositiviRepo.trovaPerId(id) #controllo che il dispositivo esista
        if dispositivo == None:
            return f"Dispositivo non trovato"
        else:
            self._DispositiviRepo.rimuoviDispositivo(id) #lo rimuovo se trovo l'id
            self._DispositiviRepo.salva()
            return f"Dispositivo rimosso"
    def configuraDispositivo(self, id: str, nuova_soglia: float = None, nuovo_stato: bool = None, nuovo_orario: time = None):
        dispositivo = self._DispositiviRepo.trovaPerId(id) #controllo che esista
        if dispositivo == None:
            return f"Dispositivo non trovato"
        else:
            if isinstance(dispositivo, Sensore):
                dispositivo.setSoglia(nuova_soglia)
            else:
                dispositivo.setStato(nuovo_stato)
                dispositivo.setOrario(nuovo_orario)
            return f"Dispositivo riconfigurato"
 #non sto violando l'OC? se venisse aggiunto un nuovo tipo di dispositivo il codice dovrebbe essere modificato
 #LINE25