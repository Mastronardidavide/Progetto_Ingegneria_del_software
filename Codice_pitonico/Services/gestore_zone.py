from Models.zona import Zona

class GestoreZona:
    def __init__(self, zona_repo):
        self._zona_repo = zona_repo

    def creaZona(self, id: int, nome: str): #creazona controlla che la zona non esista già, dopodiché la crea
        zona = self._zona_repo.trovaPerId(id)
        if zona is None:
            nuova_zona = Zona(id, nome)
            self._zona_repo.aggiungi(nuova_zona)
            return f"La zona è stata creata con successo"
        else:
            return f"La zona è già presente"
    def eliminaZona(self, id: int): #elimina zona fa la stessa cosa ma controlla che esista
        zona_canc = self._zona_repo.trovaPerId(id)
        if zona_canc is None:
            return f"Zona non trovata"
        else:
            self._zona_repo.elimina(id)
            return f"Zona eliminata"
    def visualizzaZona(self, id:int): #visualizzazione mi ritorna la zona
        zona_vis = self._zona_repo.trovaPerId(id)
        if zona_vis is None:
            return f"Zona non trovata"
        else:
            return zona_vis
    def personalizzaDispositivoZona(self, id:str): #
        