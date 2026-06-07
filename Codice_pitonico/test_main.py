import time
from Repos.backup_repository import BackupRepository
from Models.attuatore import Attuatore
from datetime import datetime
from Repos.dispositivo_repository import DispositivoRepository
from Services.gestore_dati import GestoreDati
from Services.gestore_dispositivi import GestoreDispositivi
from Views.Timer import Timer

def main():
    print("Avvio")

    # 1. Inizializzazione
    backup_repo = BackupRepository()
    dispositivo_repo = DispositivoRepository()
    g_dati = GestoreDati(backup_repo)
    g_disp = GestoreDispositivi(dispositivo_repo)

    # 2. Ripristino dati
    dati_salvati = g_dati.recupera_contenuto_backup()
    if dati_salvati:
        print(f"[Ripristino] Stato ripristinato tramite backup: '{dati_salvati}'")
    else:
        print("[Ripristino] Nessun backup trovato. Avvio standard.")

    # Spazio definizione funzioni da eseguire periodicamente
    def backup():
        dati = dispositivo_repo.tutte()
        g_dati.esegui_backup(dati)

    # Avvio timer
    timer_backup = Timer(azione_da_eseguire=backup, intervallo_secondi=360)
    timer_backup.avvia()
    print("Controllo backup avviato con successo.")

    timer_attuatori = Timer(azione_da_eseguire=g_disp.check_attuatori, intervallo_secondi=3)
    timer_attuatori.avvia()

    timer_sensori = Timer(azione_da_eseguire = g_disp.check_sensori, intervallo_secondi=60)
    timer_sensori.avvia()

    # 5. Interazione
    print("\n=======================================================")
    print("Comandi disponibili: \n'stato' (mostra JSON) \n'esci' \n'lista' (mostra dispositivi)\n'aggiungi' (aggiungi dispositivo) \n'rimuovi' (rimuovi dispositivo) \n'configura' (configura dispositivo)")
    print("=======================================================\n")


    while True:
        comando = input("Inserisci comando> ").strip().lower()
        if comando == "esci":
            print("[Sistema] Chiusura in corso...")
            timer_backup.ferma()
            timer_attuatori.ferma()
            timer_sensori.ferma()
            break
        elif comando == "stato":
            print(f"\n[Dati in Memoria] {backup_repo.getBackup()}\n")
        elif comando == "lista":
            g_disp.lista()
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
                feedback = g_disp.aggiungiDispositivo(id_disp=id, tipo=tipo, nome=nome, soglia=soglia)
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
                feedback = g_disp.aggiungiDispositivo(id_disp=id, tipo=tipo, nome=nome, stato=stato_iniziale, orario=orario_attivazione)
                print(feedback)
            else:
                print("Errore: Tipo dispositivo non valido. Operazione annullata.")

            dati = g_disp.tutte_to_dict()
            g_dati.esegui_backup(str(dati))

        elif comando == "rimuovi":
            id = input("ID dispositivo da rimuovere: ").strip()
            feedback = g_disp.rimuoviDispositivo(id)
            print(feedback)
            #esegui backup dopo ogni modifica
            dati = g_disp.tutte_to_dict()
            g_dati.esegui_backup(dati)
        else:
            print(f"Comando '{comando}' non riconosciuto.")

if __name__ == "__main__":
    main()
