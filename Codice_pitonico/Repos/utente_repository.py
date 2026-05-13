#faccio una repository singola sia per Admin che per Ospite
#riprendo l'esempio della biblioteca LibroRepository.
import json
from Models.admin import Admin
from Models.ospite import Ospite

class UtenteRepository:
    def __init__(self, path: str = "Data/Utenti_rep.json"):
        self._path = path
        self._utenti: dict = {} #dizionario che avrà come chiave l'ID e come valore l'oggetto (admin o ospite)
        self.carica()

    def carica(self) -> None:
        try:
            with open(self._path, "r", encoding = "utf-8") as f:
                dati = json.load(f) #questo ricostrusce gli oggetti usando il metodo fromDict.
                self._utenti = {}
        #ricostruisco gli oggetti passando i parametri ai costruttori
        for d in dati:
            if d.get("ruolo") == "admin":
                utente = Admin(d["id"], d["nome"], d["password"])
            else:
                utente = Ospite(d["id"], d["nome"], d["password"])

        except FileNotFoundError:
            self._utenti = {}     #da errore se il file non esiste ancora, come il primo avvio.
        
    def salva(self) -> None:
        #preparlo la lista da salvare nel JSON
        lista_dizionari = []
        for u in self._utenti.values():
            diz = u.toDict()
            #aggiungo dinamicamente un etichetta "ruolo" usando ifistance
            if isinstance(u, Admin):
                diz["ruolo"] = "admin"
            else:
                diz["ruolo"] = "ospite"
            lista_dizionari.append(diz)
        
        #sovrascrivo il file con la lista aggiornata 
        with open(self._path,"w", encoding = "utf-8") as f:
            json.dump(lista_dizionari,f, indent=4, ensure_ascii=False)
            #json dump prende un ogetto pitone e lo serializza scrivendolo manualmente in un file
            #ensure_ascii=False è uno standard e sta nel pdf della serializzazione, e da quello che ho visto con False
            #permetti al file json di salvare e mantetnere visivamente leggibili i caratteri speciali.
        
        def trovaPerId(self, id_utente: str):
            return self._utenti.get(id_utente) #restituisce None se non lo trova
        
        def aggiungi(self, utente) -> None:
            self._utenti[utente.getID()] = utente
            self.salva()

        def tutti(self) -> list:
            return list(self._utenti.values())