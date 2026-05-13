from datetime import datetime
class Timer:
    def __init__(self):
        pass
    def getTime(self) -> datetime:
        return datetime.now() #fa parte della libraria datetime
#Anche se è un entity, Timer non ha bisogno di una repository perchè
# i dati non persistono e quindi non ho bisogno del dizionario.