import json
from datetime import datetime
#questo log si occupa di intercettare gli errori di gestore dati, gestore zone e gestore scenari,e riportarli in un file JSON apposito invece di far crashare il codice
class LogRepository:
    # Salviamo il file direttamente nella cartella principale, coerente con i tuoi backup
    def __init__(self, path: str = "errori.json"):
        self._path = path

    #carica il file json con gli errori, appenda quello nuovo e lo salva
    def scriviErrore(self, messaggio: str) -> None:
        #Tentiamo di caricare la lista di errori già salvati nel file
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                lista_errori = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se il file non esiste ancora o è vuoto, partiamo da una lista vuota
            lista_errori = []

        #creiamo il dizionario per il nuovo errore con data e ora
        nuovo_errore = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tipo": "ERROR",
            "messaggio": messaggio
        }

        #aggiungiamo il nuovo errore alla lista
        lista_errori.append(nuovo_errore)

        #riscriviamo il file JSON aggiornato o lo scriviamo per la prima volta se non esisteva in precedenza
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(lista_errori, f, indent=2, ensure_ascii=False)

    #ritorna la lista di log
    def leggiTutti(self) -> list:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
