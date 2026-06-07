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
        stato_simulato = "Dispositivi attivi -> Condizionatore: ON (22°C), Luce Cucina: OFF"
        g_dati.esegui_backup(stato_simulato)

    # Avvio timer
    timer_backup = Timer(azione_da_eseguire=backup, intervallo_secondi=5)
    timer_backup.avvia()
    print("Controllo backup avviato con successo.")

    timer_attuatori = Timer(azione_da_eseguire=g_disp.check_attuatori, intervallo_secondi=10)
    timer_attuatori.avvia()
    print("Controllo attuatori avviato.")

    timer_sensori = Timer(azione_da_eseguire = g_disp.check_sensori, intervallo_secondi=15)
    timer_sensori.avvia()
    print("Controllo sensori avviato.")

    # 5. Interazione
    print("\n=======================================================")
    print("Comandi disponibili: 'stato' (mostra JSON), 'esci', 'lista' (mostra dispositivi)")
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
        else:
            print(f"Comando '{comando}' non riconosciuto.")

if __name__ == "__main__":
    main()
