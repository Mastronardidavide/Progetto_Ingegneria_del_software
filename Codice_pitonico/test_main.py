import time
from Boundary.boundary_dispositivi import BoundaryDispositivo
from Boundary.boundary_utenti import BoundaryUtente
from Boundary.boundary_zone import BoundaryZona
from Models.attuatore import Attuatore
from Models.sensore import Sensore
from Models.zona import Zona
from datetime import datetime
from Repos.dispositivo_repository import DispositivoRepository
from Repos.backup_repository import BackupRepository
from Repos.utente_repository import UtenteRepository
from Repos.zona_repository import ZonaRepository
from Repos.log_repository import LogRepository
from Services.gestore_dati import GestoreDati
from Services.gestore_dispositivi import GestoreDispositivi
from Services.gestore_utenti import GestoreUtenti
from Services.gestore_zone import GestoreZona
from Views.Timer import Timer

def main():
    print("Avvio")

    # Inizializzazione
    backup_repo = BackupRepository()
    dispositivo_repo = DispositivoRepository()
    utenti_repo = UtenteRepository()
    zona_repo = ZonaRepository()
    log_repo = LogRepository()
    g_dati = GestoreDati(backup_repo, log_repo)
    g_disp = GestoreDispositivi(dispositivo_repo)
    g_utenti = GestoreUtenti(utenti_repo)
    g_zona = GestoreZona(zona_repo, g_disp, log_repo) #in questo caso passiamo anche g_disp per fare un check sull'esistenza di dispositivi prima di associarli
    boundary_disp = BoundaryDispositivo(g_dati, g_disp)
    boundary_utenti = BoundaryUtente(g_utenti, g_dati, utenti_repo)
    boundary_zone = BoundaryZona(g_zona)

    # Ripristino dati
    dati_salvati = g_dati.recupera_contenuto_backup()
    if dati_salvati:
        print(f"[Ripristino] Stato ripristinato tramite backup: '{dati_salvati}'")
    else:
        print("[Ripristino] Nessun backup trovato. Avvio standard.")

    # Spazio definizione funzioni da eseguire periodicamente, e che prendano argomenti, come dati per backup o repo per check attuatori
    #se non definissimo queste funzioni ausiliarie, non potremmo passare argomenti ai metodi da eseguire periodicamente
    def backup():
        dati = dispositivo_repo.tutte()
        g_dati.esegui_backup(dati)

    def esegui_check_attuatori():
        g_disp.check_attuatori(zona_repo)

    # Avvio timer
    timer_backup = Timer(azione_da_eseguire=backup, intervallo_secondi=360) #qui posso senza problemi passare backup, perché è una funzione che non richiede argomenti
    timer_backup.avvia()
    print("Controllo backup avviato con successo.")

    timer_attuatori = Timer(azione_da_eseguire=esegui_check_attuatori, intervallo_secondi=60) #qui posso passare la funzione perché "impacchetta"
    #la vera funzione di chec_attuatori, la quale di per se richiede argomenti
    timer_attuatori.avvia()

    timer_sensori = Timer(azione_da_eseguire = g_disp.check_sensori, intervallo_secondi=60)
    timer_sensori.avvia()

    timer_zone = Timer(azione_da_eseguire = g_zona.check_automazioni_zone, intervallo_secondi=60)
    timer_zone.avvia()

    #registrazione o autenticazione utente
    utente_autenticato = None

    while utente_autenticato is None:
        print("\n=======================================================")
        print(" ACCESSO AL SISTEMA RICHIESTO ")
        print("=======================================================")
        print("Comandi: \n'login' (accedi al pannello) \n'registra' (crea account) \n'esci'")
        print("=======================================================\n")
        
        scelta = input("Scegli un'opzione> ").strip().lower()

        if scelta == "esci":
            print("Chiusura in corso...")
            timer_backup.ferma()
            timer_attuatori.ferma()
            timer_sensori.ferma()
            timer_zone.ferma()
            return

        elif scelta == "registra":
            # Richiama la funzione separata del boundary
            boundary_utenti.form_registrazione()

        elif scelta == "login":
            # Richiama la funzione del boundary che restituisce l'utente o None
            utente_autenticato = boundary_utenti.form_login()
            
        else:
            print(f"Opzione '{scelta}' non valida.")

    # 5. Interazione



    while True:
        print("Schermata principale. Inserisci un comando:")
        print("\n=======================================================")
        print("Comandi disponibili: \n'stato' (mostra JSON) \n'esci' \n'dispositivi' (gestione dispositivi)", "\n'utenti' (gestione utenti)")
        print("'zone' (gestione zone)")
        print("=======================================================\n")
        comando = input("Inserisci comando> ").strip().lower()
        if comando == "esci":
            print("Chiusura in corso...")
            timer_backup.ferma()
            timer_attuatori.ferma()
            timer_sensori.ferma()
            break
        elif comando == "stato":
            print(f"\n[Dati in Memoria] {backup_repo.getBackup()}\n")
        elif comando == "dispositivi": #con il comando dispositivi entriamo in un altro ciclo while nel boundary, che può essere rotto solo dal comando indietro, pertanto quando si sbaglia ad inserire un comando si rimane nella sezione dispositivi
            boundary_disp.menu_disp()
        elif comando == "utenti":
            boundary_utenti.menu_utenti()
        elif comando == "zone":
            boundary_zone.menu_zone()
        else:
            print(f"Comando '{comando}' non riconosciuto.")

if __name__ == "__main__":
    main()