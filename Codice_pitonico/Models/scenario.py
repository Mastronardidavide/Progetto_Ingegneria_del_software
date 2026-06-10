from datetime import time

class Scenario:
    def __init__(self, id: int, nome: str = None, orarioScenario: time = None, 
                 sogliaScenario: float = None, id_attuatori: list = None, id_sensore: str = None, orarioDisattivazione: time = None):
        
        self._id = id
        self._nome = nome
        self._orarioScenario = orarioScenario
        self._sogliaScenario = sogliaScenario 
        self._orarioDisattivazione = orarioDisattivazione
        self._id_attuatori = id_attuatori if id_attuatori is not None else []
        self._id_sensore = id_sensore

    def getId(self) -> int: 
        return self._id

    def getNome(self) -> str:
        return self._nome

    def getOrarioScenario(self) -> time:
        return self._orarioScenario

    def getSogliaScenario(self) -> float:
        return self._sogliaScenario

    def getIdAttuatori(self) -> list:
        return self._id_attuatori

    def getIdSensore(self) -> str:
        return self._id_sensore

    def getOrarioDisattivazione(self) -> time:
        return self._orarioDisattivazione

    def impostaSoglia(self, soglia: float) -> None:
        if soglia is not None and not isinstance(soglia, float):
            raise TypeError("la soglia deve essere un numero decimale (float)")
        self._sogliaScenario = soglia

    def associaAttuatore(self, id_attuatore: str) -> None:
        if id_attuatore not in self._id_attuatori:
            self._id_attuatori.append(id_attuatore)

    def rimuoviAttuatore(self, id_attuatore: str) -> None:
        if id_attuatore in self._id_attuatori:
            self._id_attuatori.remove(id_attuatore)

    def toDict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome,
            "orarioScenario": self._orarioScenario.isoformat() if self._orarioScenario else None,
            "orarioDisattivazione": self._orarioDisattivazione.isoformat() if self._orarioDisattivazione else None,
            "sogliaScenario": self._sogliaScenario,
            "id_attuatori": self._id_attuatori,
            "id_sensore": self._id_sensore
        }

    @classmethod
    def fromDict(cls, d: dict) -> "Scenario":
        orario_str = d.get("orarioScenario")
        orarioRiconvertito = time.fromisoformat(orario_str) if orario_str is not None else None
        
        orario_disattivazione_str = d.get("orarioDisattivazione")
        orario_disattivazione_riconvertito = time.fromisoformat(orario_disattivazione_str) if orario_disattivazione_str is not None else None

        return cls(
            id=d["id"], 
            nome=d["nome"], 
            orarioScenario=orarioRiconvertito, 
            sogliaScenario=d.get("sogliaScenario", None),
            id_attuatori=d.get("id_attuatori", []),
            id_sensore=d.get("id_sensore", None),
            orarioDisattivazione=orario_disattivazione_riconvertito
        )

    def __str__(self) -> str:
        info_auto = ""
        if self._orarioScenario:
            info_auto += f" | Orario: {self._orarioScenario.strftime('%H:%M')}"
        if self._id_sensore and self._sogliaScenario is not None:
            info_auto += f" | Sensore: {self._id_sensore} (Soglia: >{self._sogliaScenario})"
            
        return f"Scenario {self._id}: {self._nome} (Attuatori: {self._id_attuatori}{info_auto})"
