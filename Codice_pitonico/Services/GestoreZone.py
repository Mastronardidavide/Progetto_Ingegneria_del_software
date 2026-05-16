from Models.zona import Zona

class GestoreZona:
    def __init__(self, zona_repo):
        self._zona_repo = zona_repo

    def creaZona(self, id: int, nome: str):
        zona = self._zona_repo.trovaPerId(id)
        if zona is None:
            nuova_zona = Zona(id, nome)
            self._zona_repo.aggiungi(nuova_zona)
        else:
            return f"La zona è già presente"
    def eliminaZona(self, id: int):
        zona_canc = self._zona_repo.trovaPerId(id)
        if zona_canc is None:
            return f"Zona non trovata"
        else:
            self._zona_repo.elimina(id)
            return("Zona eliminata")
