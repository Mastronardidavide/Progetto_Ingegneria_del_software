from datetime import time

class Zona:
    # la soglia ora è un valore float singolo opzionale, non più una lista, mentre si possono avere più attuatori associati
    def __init__(self, id: int, nome: str = None, orarioZona: time = None, 
                 sogliaZona: float = None, id_attuatori: list = None, id_sensore: str = None):
        
        self._id = id
        self._nome = nome
        self._orarioZona = orarioZona
        self._sogliaZona = sogliaZona 
        
        # Manteniamo la lista degli attuatori associati manualmente
        self._id_attuatori = id_attuatori if id_attuatori is not None else []
        self._id_sensore = id_sensore

    # Getter

    def getId(self) -> int: 
        return self._id

    def getNome(self) -> str:
        return self._nome

    def getOrarioZona(self) -> time:
        return self._orarioZona

    def getSogliaZona(self) -> float:
        return self._sogliaZona

    def getIdAttuatori(self) -> list:
        return self._id_attuatori

    def getIdSensore(self) -> str:
        return self._id_sensore

    # Configurazione

    def impostaSoglia(self, soglia: float) -> None:
        """ Sostituisce il vecchio metodo aggiungiSoglia: ora sovrascrive il singolo valore """
        if soglia is not None and not isinstance(soglia, float):
            raise TypeError("la soglia deve essere un numero decimale (float)")
        self._sogliaZona = soglia

    def associaAttuatore(self, id_attuatore: str) -> None:
        if id_attuatore not in self._id_attuatori:
            self._id_attuatori.append(id_attuatore)

    def rimuoviAttuatore(self, id_attuatore: str) -> None:
        if id_attuatore in self._id_attuatori:
            self._id_attuatori.remove(id_attuatore)

    # Serializzazione

    def toDict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "orarioZona": self._orarioZona.isoformat() if self._orarioZona else None,
            "sogliaZona": self._sogliaZona,
            "id_attuatori": self._id_attuatori,
            "id_sensore": self._id_sensore
        }

    @classmethod
    def fromDict(cls, d: dict) -> "Zona":
        orario_str = d.get("orarioZona")
        orarioRiconvertito = time.fromisoformat(orario_str) if orario_str is not None else None #formattazione del tempo da stringa a time
        
        return cls(
            id=d["id"], 
            nome=d["nome"], 
            orarioZona=orarioRiconvertito, 
            sogliaZona=d.get("sogliaZona", None),
            id_attuatori=d.get("id_attuatori", []),
            id_sensore=d.get("id_sensore", None)
        )

    def __str__(self) -> str: #definisco il dunder per stampare le variabili, in caso esse siano definite
        info_auto = ""
        if self._orarioZona:
            info_auto += f" | Orario: {self._orarioZona.strftime('%H:%M')}" #metodo che formatta il tempo in ore e minuti
        if self._id_sensore and self._sogliaZona is not None:
            info_auto += f" | Sensore: {self._id_sensore} (Soglia: >{self._sogliaZona})"
            
        return f"Zona {self._id}: {self._nome} (Attuatori: {self._id_attuatori}{info_auto})"
