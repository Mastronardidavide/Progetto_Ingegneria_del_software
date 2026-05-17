class Utente():

    def __init__(self, id: str, nome: str, password: str,tipo: str): #aggiungo la passowrd per l'interfaccia autenticabile
        self._id = id
        self._nome = nome
        self._password = password
        self._tipo = tipo

    def getId(self) -> str:
        return self._id

    def getNome(self) -> str:
        return self._nome

    def getTipo(self) -> str:
        return self._tipo
    
    def toDict(self) -> dict: #per il salvataggio dei dati in Json
        return{
            "id": self._id,
            "nome": self._nome,
            "password": self._password,
            "tipo": self._tipo
            }
    def autentica(self, utente: str, password: str) -> bool:
        return self._nome == utente and self._password == password #DA IMPLEMENTARE IN GESTORE UTENTI
#non posso usare isinstance perche violiamo il principio di SOLID, Open/ Closed
    @classmethod #definisce un metodo che non riceve la singola istanza dell oggetto come primo argomento
    #ma riceve la classe stessa (cls).
    def fromDict(cls, d: dict) -> "Utente":
        return cls(d["id"], d["nome"], d["password"], d["tipo"])