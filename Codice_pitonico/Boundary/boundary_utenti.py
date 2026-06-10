class BoundaryUtente:
    def __init__(self, g_utenti, g_dati, utenti_repo):
        self._g_utenti = g_utenti
        self._g_dati = g_dati
        self._utenti_repo = utenti_repo

    def form_registrazione(self):
        print("\n--- REGISTRAZIONE NUOVO UTENTE ---")
        id_ut = input("Inserisci ID utente: ").strip()
        nome = input("Inserisci Nome utente: ").strip()
        pswd = input("Inserisci Password: ").strip()
        
        feedback = self._g_utenti.creaAccount(id=id_ut, nome=nome, pswd=pswd)
        print(feedback)
        

    def form_login(self):

        print("\n--- ACCESSO AL SISTEMA ---")
        id_ut = input("Inserisci il tuo ID: ").strip()
        nome = input("Inserisci il tuo Nome Utente: ").strip()
        pswd = input("Inserisci la tua Password: ").strip()
        
        # Delega il controllo delle credenziali al Gestore Utenti
        utente = self._g_utenti.login(id=id_ut, nome=nome, pswd=pswd)
        return utente

    def menu_utenti(self):
        while True:
            print("\n=======================================================")
            print("Gestione Utenti: \n'registra' (crea nuovo account)\n'elimina' (rimuovi account) \n'indietro' (torna al menu precedente)")
            print("=======================================================\n")
            
            comando = input("Inserisci comando utente> ").strip().lower()
            
            if comando == "registra":
                self.form_registrazione()

            elif comando == "elimina":
                id_ut = input("Inserisci l'ID dell'account da eliminare: ").strip()
                
                feedback = self._g_utenti.eliminaAccount(id=id_ut)
                print(feedback)
                
                # Esecuzione del backup dopo l'eliminazione
                dati = self._g_utenti.tuttiToDict()
                self._g_dati.esegui_backup(str(dati))

            elif comando == "indietro":
                break
            else:
                print(f"Comando '{comando}' non riconosciuto.")
