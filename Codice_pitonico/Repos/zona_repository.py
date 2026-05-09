import json

from Models.zona import Zona #importo la classe zona dal package Models, ma se runni da errore perche una regola fondamentale dell'ECB dice che non si devono mai avviare file che stanno in sottocartelle
#regola scritta nel documento 1.3 Entry Point
class ZonaRepository:
    def __init__(self, path: str = "Zona_Rep.json"):
        self._path
        self._zone: dict = {} #dizionario che avrà come chiave l'ID.
        self.carica() #carica automaticamente i dati dal file JSON nella memoria del programma nel momento in cui lo avvio.

#da qwui ho un metodo per trasformare i dati dal file Json e trasformarli in oggetti.
def carica(self) -> None:
    try:
        with open(self._path, "r", encoding = "utf-8") as f:
            dati = json.load(f) #questo ricostrusce gli oggetti usando il metodo fromDict.
            self._zone = {d["id"]: Zona.fromDict(d) for d in dati}
    except FileNotFoundError:
        self._zone = {}     #da errore se il file non esiste ancora, come il primo avvio.

#Qui utilizzo un altro metodo per salvare tutti gli oggetti e trasformandoli di nuovo in testo JSON
def salva(self) -> None:
        with open(self._path, "w", encoding="utf-8") as f:
            # Usa toDict() per "decomporsi" prima del salvataggio
            json.dump([z.toDict() for z in self._zone.values()], f, indent=2, ensure_ascii=False)

#Qui anna pepe da altri metodi per interagire con le zone dal resto del programma, lo riporto ma si puo sempre eliminare se non serve. mi sono riferito all esempio del libro.
def trovaPerId(self, id: int):
        return self._zone.get(id)  # Restituisce None se non trova la zona

def aggiungi(self, zona: Zona) -> None:
        self._zone[zona.getId()] = zona
        self.salva()  # Salva automaticamente nel file ogni volta che aggiungi una zona

def tutte(self) -> list: #dall esempio anche del libro qui il nostro programma consegna una lista completa di tutti gli oggetti zona che sono caricati in memoria dal file.
        return list(self._zone.values())