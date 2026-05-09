class utente:
    def __init__(self, id: str, nome: str): #definisco il costruttore
        self._id = id
        self._nome = nome
    
    def getId(self) -> str: return self._id #metodi dell'utente
    def getNome(self) -> str: return self._nome

    def toDict(self) -> dict: #metodo che lo restituisce in dizionario per convertirlo in JSON
        return {"id": self._id, "nome": self._nome}
    
    #implementazione del metodo di visualizzazione di dispositivo, controlla che esso sia sensore o attuatore, e implementa i metodi relativi, se non è nessuno dei due
    #allora ritorna il dizionario vuoto
    def visualizzaDispositivo(self, d: Dispositivo) -> dict: 
        if isinstance(d, Sensore):
            return{"id_sensore": d.getId(),"soglia_sensore": d.getSoglia()}
        if isinstance(d, Attuatore):
            return{"id_attuatore": d.getId(),"stato_attuatore": d.getStato(), "orario_attivazione": d.getOrario()}
        return{}
    
    @classmethod #mi permette di riportare i dati di un dizionario (id, nome) in un utente
    def fromDict(cls, d: dict) -> "Utente":
        return cls(d["id"], d["nome"])