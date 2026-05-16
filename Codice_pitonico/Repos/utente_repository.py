#faccio una repository singola sia per Admin che per Ospite
#riprendo l'esempio della biblioteca LibroRepository.
import json
from Models.utente import Utente

class UtenteRepository:
    def __init__(self, path: str = "Data/Utenti_rep.json"):
        self._path = path
        self._utenti: dict = {} #dizionario che avrà come chiave l'ID e come valore l'oggetto (admin o ospite)
        self.carica()

    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding = "utf-8") as f:
                dati = json.load(f) #questo ricostrusce gli oggetti usando il metodo fromDict.
                #ho usato la dictionary comprehension
                self._utenti = {d["id"]: Utente.fromDict(d) for d in dati}
        except FileNotFoundError:
            self._utenti = {}     #da errore se il file non esiste ancora, come il primo avvio.
        
    def salva(self) -> None:
        #preparlo la lista da salvare nel JSON        
        with open(self._path,"w", encoding = "utf-8") as f:
            json.dump([u.toDict() for u in self._utenti.values()],f, indent=4, ensure_ascii=False)
            #u.dict() prende gli ogetti utente dalla memoria e li impachetta in dizionari che poi li unisce in una lista e stampa questa lista nel file sul disco
            #json dump prende un oggetto pitone e lo serializza scrivendolo manualmente in un file
            #ensure_ascii=False è uno standard e sta nel pdf della serializzazione, e da quello che ho visto con False
            #permetti al file json di salvare e mantetnere visivamente leggibili i caratteri speciali.
        
    def trovaPerId(self, id_utente: str):
        return self._utenti.get(id_utente) #restituisce None se non lo trova
    
    def aggiungi(self, utente: Utente) -> None:
        self._utenti[utente.getId()] = utente
        self.salva()

    def tutti(self) -> list:
        return list(self._utenti.values())

    def elimina(self, id_utente: str) -> None:
        if id_utente in self._utenti:
            del self._utenti[id_utente] #uso il del come nelle slide
            self.salva()