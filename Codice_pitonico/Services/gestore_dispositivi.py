from datetime import time
from Models.sensore import Sensore
from Models.attuatore import Attuatore
from datetime import datetime
import random

class GestoreDispositivi:
    #utilizzo la Dependency Inversion: il control riceve la repository dal main
    def __init__(self, dispositivo_repo):
        self._dispositivo_repo = dispositivo_repo

    # Caso d'uso: aggiungi dispositivo esteso con tutti i parametri necessari (kwargs) in modo da poter gestire sensori e attuatori con un unico metodo, evitando duplicazioni di codice
    def aggiungiDispositivo(self, id_disp: str, tipo: str, nome: str, 
                           soglia: float = None, 
                           stato: bool = False, 
                           orario: time = None) -> str:
        
        disp = self._dispositivo_repo.trovaPerId(id_disp)
        if disp is not None:
            return f"Errore: Dispositivo {id_disp} già presente"
        
        # Creazione dell'Entity specifica in base al tipo richiesto
        if tipo == "sensore":
            nuovo_disp = Sensore(id=id_disp, tipo=tipo, nome=nome, soglia=soglia)
            
        elif tipo == "attuatore":
            nuovo_disp = Attuatore(id=id_disp, tipo=tipo, nome=nome, 
                                   orarioAttivazione=orario, statoAttuatore=stato)
        else:
            return "Errore: Tipo dispositivo non valido"
        # Aggiunta alla repository (salva in automatico nel file JSON)
        self._dispositivo_repo.aggiungi(nuovo_disp)
        
        return f"{tipo} {id_disp} ({nome}) aggiunto con successo"

        
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
            self._dispositivo_repo.salva() #salvo le modifiche
            return f"dispositivo riconfigurato"
    #andiamo a controllare che gli attuatori siano da accendere o spegnere, tenendo conto che se fanno parte di una zona,
    #sarà il gestore zone a decidere
    def check_attuatori(self, zona_repo) -> None:
        orario_corrente = datetime.now().time().replace(second=0, microsecond=0)
        
        # Raccogliamo tutti gli ID degli attuatori che appartengono a una zona
        id_occupati = set()
        for zona in zona_repo.tutte():
            for id_att in zona.getIdAttuatori():
                id_occupati.add(id_att)

        # Cicliamo su tutti i dispositivi del sistema
        for dispositivo in self._dispositivo_repo.tutte():
            # Controlliamo che sia un attuatore e che non sia in una zona
            if isinstance(dispositivo, Attuatore) and dispositivo.getId() not in id_occupati:
                
                # Applichiamo il controllo orario per i dispositivi isolati
                if dispositivo.getOrario() is not None:
                    orario_attuatore = dispositivo.getOrario().replace(second=0, microsecond=0)
                    
                    if orario_corrente == orario_attuatore:
                        # Usiamo lo stesso controllo sicuro che hai ideato tu (evita toggle infiniti)
                        if dispositivo.getStato() == False:
                            dispositivo.cambiaStato()
                            print(f"[Automazione Singola] Attuatore non presente in una zona o scenario '{dispositivo.getId()}' acceso.")


    def check_sensori(self):
        for dispositivo in self._dispositivo_repo.tutte():
            if isinstance(dispositivo, Sensore):
                soglia = dispositivo.getSoglia()
                if soglia is not None:
                    lettura_corrente = round(random.uniform(10.0, 30.0), 1) # Simulazione di una lettura casuale tra 10 e 30 in float
                    if lettura_corrente > soglia:
                        print(f"Il sensore ID 'f{dispositivo.getId()}' ({dispositivo._nome}) ha superato la soglia")
    def lista(self):
        print("\nLista dispositivi:")
        if self._dispositivo_repo.tutte() == []:
            print("Nessun dispositivo presente")
        else:
            for dispositivo in self._dispositivo_repo.tutte():
                if isinstance(dispositivo, Sensore):
                    print(f"- ID: {dispositivo.getId()}, Tipo: {dispositivo._tipo}, Soglia: {dispositivo.getSoglia()}")
                elif isinstance(dispositivo, Attuatore):
                    print(f"- ID: {dispositivo.getId()}, Tipo: {dispositivo._tipo}, Orario: {dispositivo.getOrario()}, Stato: {dispositivo.getStato()}")
    
    def tutte_to_dict(self):
        return [d.toDict() for d in self._dispositivo_repo.tutte()]
 #violazione controllata di OC: non ci aspettiamo che venga inventato un nuovo tipo di dispositivo in futuro, quindi sviluppiamo il sistema
 #sulla base di sensore e attuatore
 #LINE49