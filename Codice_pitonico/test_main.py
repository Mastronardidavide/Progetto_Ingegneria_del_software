import time
from Repos.backup_repository import BackupRepository
from Services.gestore_dati import GestoreDati
from Views.timer import Timer

def main():
    print("--- 🏠 AVVIO CONFIGURAZIONE SMART HOME (TEST CLI) ---")

    # 1. Inizializzazione
    backup_repo = BackupRepository()
    g_dati = GestoreDati(backup_repo)

    # 2. Ripristino dati
    dati_salvati = g_dati.recupera_contenuto_backup()
    if dati_salvati:
        print(f"[Ripristino] Stato ripristinato tramite backup: '{dati_salvati}'")
    else:
        print("[Ripristino] Nessun backup trovato. Avvio standard.")

    # 3. Funzione per il Timer
    def cattura_e_salva_stato():
        stato_simulato = "Dispositivi attivi -> Condizionatore: ON (22°C), Luce Cucina: OFF"
        g_dati.esegui_backup(stato_simulato)

    # 4. Avvio Timer (ogni 5 secondi per il test)
    timer_backup = Timer(azione_da_eseguire=cattura_e_salva_stato, intervallo_secondi=5)
    timer_backup.avvia()
    print("[Sistema] Timer in background avviato con successo.")

    # 5. Interazione
    print("\n=======================================================")
    print("Comandi disponibili: 'stato' (mostra JSON), 'esci'")
    print("=======================================================\n")

    while True:
        comando = input("Inserisci comando> ").strip().lower()
        if comando == "esci":
            print("[Sistema] Chiusura in corso...")
            timer_backup.ferma()
            break
        elif comando == "stato":
            print(f"\n[Dati in Memoria] {backup_repo.getBackup()}\n")
        else:
            print(f"Comando '{comando}' non riconosciuto.")

if __name__ == "__main__":
    main()
