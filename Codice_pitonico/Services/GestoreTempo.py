#serve gestore tempo? non possiamo semplicemente far prendere l'orario agli altri gestori che ne hanno bisogno?

from datetime import datetime
from Models.Timer import Timer

class GestoreTempo:
    def __init__(self):
        self._timer = Timer
    
    def checkOrario(self, getOrario: datetime) -> bool:
        if getOrario is None:
            return False
        orario_attuale = self._timer.getTime()

        if orario_attuale >= getOrario:
            return True
        else:
            return False
