import threading
import time

class Timer:
    def __init__(self, azione_da_eseguire, intervallo_secondi=60): #gli passo la funzione generica in modo da specificare di volta in volta e riutilizzare il codice
        self._azione     = azione_da_eseguire  # Funzione da lanciare
        self._intervallo = intervallo_secondi  
        self._attivo     = False
        self._thread     = None

    def avvia(self):
        if not self._attivo:
            self._attivo = True
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()

    def ferma(self):
        self._attivo = False

    def _loop(self):
        while self._attivo:
            time.sleep(self._intervallo)
            if self._attivo:
                try:
                    self._azione() # Lancia il compito assegnato
                except Exception as e:
                    print(f"[Timer Errore] Operazione fallita: {e}")
