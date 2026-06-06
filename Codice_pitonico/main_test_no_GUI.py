import time
from Repositories.backup_repository import BackupRepository
from Services.gestore_dati import GestoreDati
from Services.timer_generico import TimerGenerico

def main():
    print("--- 🏠 AVVIO CONFIGURAZIONE SMART HOME (TEST CLI) ---")

    # 1. INIZIALIZZAZIONE COMPONENTI (Dependency Inversion)
    backup_repo = BackupRepository()
    g_dati = GestoreDati(backup_repo)

    # 2. RIPRISTINO DATI ALL'AVVIO
    print("[Sistema] Controllo presenza backup precedenti...")
    dati_salvati = g_dati.recupera_contenuto_backup()
    
    if dati_salvati:
        print(f"[Ripristino] STATO RECONSTRUITO: '{dati_salvati}'")
        # Qui in futuro chiamerai: g_disp.ripristina_stato_dispositivi(dati_salvati)
    else:
        print("[Ripristino] Nessun backup trovato o file vuoto. Avvio standard.")

    # 3. FUNZIONI DI SUPPORTO PER IL TIMER DI TEST
    def cattura_e_salva_stato():
        """
        Questa funzione fa da ponte: preleva i dati correnti 
        e dice al gestore dati di salvarli.
        """
        # TODO: Sostituire questa stringa con 'g_disp.esporta_dati_correnti()'
        stato_simulato = "Dispositivi attivi -> Condizionatore: ON (22°C), Luce Cucina: OFF"
        g_dati.esegui_backup(stato_simulato)

    # 4. CONFIGURAZIONE E AVVIO DEL TIMER (Struttura del Prof)
    # Per i test impostiamo un intervallo breve di 5 secondi per vedere i risultati subito
    print("[Sistema] Inizializzazione timer di backup (ogni 5s)...")
    timer_backup = TimerGenerico(azione_da_eseguire=cattura_e_salva_stato, intervallo_secondi=5)
    timer_backup.avvia()
    print("[Sistema] Timer in background avviato con successo.")

    # 5. CICLO DI INTERAZIONE DA TERMINALE (Tiene vivo il programma)
    print("\n=======================================================")
    print("Il sistema è attivo. Il thread esegue i backup da solo.")
    print("Comandi disponibili: 'stato' (mostra JSON), 'esci'")
    print("=======================================================\n")

    while True:
        # L'input rimane libero al 100% grazie al multithreading del timer
        comando = input("Inserisci comando> ").strip().lower()
        
        if comando == "esci":
            print("[Sistema] Spegnimento dei timer e chiusura in corso...")
            timer_backup.ferma() # Ferma il ciclo del thread in modo sicuro
            break
        elif comando == "stato":
            # Chiediamo alla repo cosa ha attualmente in memoria
            print(f"\n[Dati in Memoria] {backup_repo.getBackup()}\n")
        else:
            print(f"Comando '{comando}' non riconosciuto. Scrivi 'stato' o 'esci'.")

if __name__ == "__main__":
    main()
