from Repos.dispositivo_repository import DispositivoRepository
from Services.gestore_dispositivi import GestoreDispositivi
from Services.gestore_dati import GestoreDati
from Repos.backup_repository import BackupRepository
from Models.dispositivo import Dispositivo
from Models.sensore import Sensore
from Models.attuatore import Attuatore
from datetime import datetime

class BoundaryDispositivo():
    def __init__(self, g_dati, g_disp):
        self._g_dati = g_dati 
        self._g_disp = g_disp

    
    def menu_disp(self):
        while True:
            print("\n=======================================================")
            print("Comandi disponibili: \n'lista' (mostra dispositivi)\n'aggiungi' (aggiungi dispositivo) \n'rimuovi' (rimuovi dispositivo) \n'configura' (configura dispositivo) \n'indietro' (torna alla schermata principale)")
            print("=======================================================\n")
            comando = input("Inserisci comando> ").strip().lower()
            if comando == "lista":
                self._g_disp.lista()
                
            elif comando == "aggiungi": # aggiungo dispositivo, chiedo i dati necessari e faccio il backup dopo ogni modifica
                id = input("ID dispositivo: ").strip()
                tipo = input("Tipo dispositivo (sensore/attuatore): ").strip().lower() # Forziamo minuscolo per compatibilità
                nome = input("Nome dispositivo: ").strip()
                
                soglia_valida = False
                soglia = None
                
                if tipo == "sensore":
                    while not soglia_valida: # controllo che la soglia sia un float valido, se è un attuatore non è obbligatoria
                        try:
                            soglia_input = input("Inserisci una soglia (float) per il sensore: ").strip()
                            soglia = float(soglia_input)
                            soglia_valida = True
                        except ValueError:
                            print("Soglia non valida. Per favore, inserisci un numero decimale (float).")
                    
                    # Chiamata per il sensore passando il parametro soglia
                    feedback = self._g_disp.aggiungiDispositivo(id_disp=id, tipo=tipo, nome=nome, soglia=soglia)
                    print(feedback)
                    
                elif tipo == "attuatore":
                    # Integrazione caso attuatore
                    stato_str = input("Stato iniziale (on/off - default 'off'): ").strip().lower()
                    stato_iniziale = True if stato_str == "on" else False
                    
                    orario_attivazione = None
                    while True:
                        orario_str = input("Orario attivazione (formato HH:MM, premi Invio per nessuno): ").strip()
                        if not orario_str:
                            break
                        try:
                            orario_attivazione = datetime.strptime(orario_str, "%H:%M").time() #converto str in time tramite strinf parse time
                            break
                        except ValueError:
                            print("Formato orario non valido. Usa il formato HH:MM (es. 14:30).")
                    
                    # Chiamata per l'attuatore passando i parametri kwargs stato e orario 
                    feedback = self._g_disp.aggiungiDispositivo(id_disp=id, tipo=tipo, nome=nome, stato=stato_iniziale, orario=orario_attivazione)
                    print(feedback)
                else:
                    print("Errore: Tipo dispositivo non valido. Operazione annullata.")

                dati = self._g_disp.tutte_to_dict()
                self._g_dati.esegui_backup(str(dati))
                

            elif comando == "rimuovi":
                id = input("ID dispositivo da rimuovere: ").strip()
                feedback = self._g_disp.rimuoviDispositivo(id)
                print(feedback)
                #esegui backup dopo ogni modifica
                dati = self._g_disp.tutte_to_dict()
                self._g_dati.esegui_backup(dati)
                
            elif comando == "indietro":
                break
            else:
                print(f"Comando '{comando}' non riconosciuto.")