import threading
import time

class Timer:
    def __init__(self, azione_da_eseguire, intervallo_secondi=60):
        """
        Inizializza il timer generico.
        - azione_da_eseguire: la funzione o metodo (callback) da lanciare.
        - intervallo_secondi: il tempo di attesa tra un ciclo e l'altro.
        """
        self._azione     = azione_da_eseguire  # Il compito da svolgere
        self._intervallo = intervallo_secondi  # I secondi di pausa
        self._attivo     = False
        self._thread     = None

    def avvia(self):
        """Attiva il timer e lancia il thread in background"""
        if not self._attivo:
            self._attivo = True
            self._thread = threading.Thread(
                target=self._loop, 
                daemon=True # Si chiude istantaneamente quando termini il main da terminale
            )
            self._thread.start()

    def ferma(self):
        """Disattiva il timer interrompendo in modo sicuro il ciclo continuo"""
        self._attivo = False

    def _loop(self):
        """Ciclo continuo eseguito in parallelo dal thread secondario"""
        while self._attivo:
            time.sleep(self._intervallo) # Il thread si congela per l'intervallo stabilito
            
            # Controllo di sicurezza prima di premere il bottone dell'azione
            if self._attivo:
                try:
                    self._azione() # ESEGUE L'AZIONE PASSATA (es. il backup)
                except Exception as e:
                    print(f"[Timer Errore] Operazione pianificata fallita: {e}")
