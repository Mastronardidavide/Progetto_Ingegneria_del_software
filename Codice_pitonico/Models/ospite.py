from Models.utente import Utente
from Models.sensore import sensore
from Models.attuatore import Attuatore

class Ospite(utente):
    def __init__(self, id: str, nome: str, password: str):
        super().__init__(id, nome, password) #richiamo il costruttore della classe genitore

    def visulizzaDatiDispositivo(self, dispositivo):
        if isinstance(dispositivo, sensore): #per l'ospite non mostriamo la soglia esatta dato che ha meno privilegi
            return f"Sensore: lettura in corso..."
        
        elif isinstance(dispositivo, Attuatore):
            #anche qui, scegliamo di dare meno informazioni
            return f"Attuatore: stato di base..."
        
        else:
            return "Dispositivo sconosciuto o non accessibile"
# non metto i To dict per l'ereditarietà che prendono da utente.