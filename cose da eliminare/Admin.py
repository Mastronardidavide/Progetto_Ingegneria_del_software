from Models.utente import Utente
#importo sensore ed attuatore perche seguo la regola LEGB
#dove anche se sensore e attuatore non sono strettamente collegati con Admin
#quando uso una variabile, python la cerca in un ordine preciso
from Models.sensore import Sensore
from Models.attuatore import Attuatore
class Admin(Utente):
    def __init__(self, id:str, nome:str, password: str):
        #utilizzo la funzione super() per irchiamare il costruttore della classe
        #genitore (utente) senza dover riscrivire self._id = id, ecc.
        super().__init__(id, nome, password)

    def visualizzaDatiDispositivo(self, dispositivo):
        #utilizzo isistance per capire il tipo esatto di dispositivo
        if isinstance(dispositivo, Sensore):
            return f"Sensore: soglia impostata a {dispositivo.getSoglia()}"

        elif isinstance(dispositivo, Attuatore):
            return f"Attuatore: stato attuale {dispositivo.getStato()}"
            #utilizzo return f per il fatto dell' ECB e non i printf
        else:
            return "Dispositivo sconosciuto"
    #Non mettiamo i toDict perche c'è l'ereditarieta data dalla superclasse Utente