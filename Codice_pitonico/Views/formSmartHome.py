class FormSmartHome: # Boundary
    def __init__(self, g_disp, g_dati):
        self._g_disp = g_disp
        self._g_dati = g_dati

    def avvia(self) -> None:
        while True: # Loop infinito che chiede all'attore cosa vuole fare
            print("\n=== SMART HOME ===")
            print("1. Registra dispositivo") # Corrisponde a eseguiRegistra
            print("2. Rimuovi dispositivo")    # Corrisponde a eseguiRimozione
            print("3. Visualizza dispositivo") # Corrisponde a mostraDispositivo
            print("4. Esegui backup")          # Corrisponde a eseguiBackup
            print("0. Esci")

            scelta = input("Scelta: ").strip()
            
            # Switch case identico all'esempio della biblioteca
            if scelta == "1":
                self.eseguiRegistra()
            elif scelta == "2":
                self.eseguiRimozione()
            elif scelta == "3":
                self.mostraDispositivo()
            elif scelta == "4":
                self.eseguiBackup()
            elif scelta == "0":
                print("Arrivederci.")
                break 

    # Ogni funzione raccoglie gli input, invoca il Control e stampa l'esito
    def eseguiRegistra(self) -> None:
        id_disp = input("ID dispositivo: ").strip()
        tipo    = input("Tipo (Sensore/Attuatore): ").strip()
        esito = self._g_disp.aggiungiDispositivo(id_disp, tipo)
        print(f"\n→ {esito}")

    def eseguiRimozione(self) -> None:
        id_disp = input("ID dispositivo da rimuovere: ").strip()
        esito = self._g_disp.rimuoviDispositivo(id_disp)
        print(f"\n→ {esito}")

    def mostraDispositivo(self) -> None:
        id_disp = input("ID dispositivo da cercare: ").strip()
        disp = self._g_disp.visualizzaDispositivo(id_disp)
        
        # Se il controller restituisce una stringa, è un messaggio di errore
        if isinstance(disp, str):
            print(f"\n→ {disp}")
            return
            
        print("\n Dati Dispositivo:")
        print("  ID:  ", disp.getId())
        print("  Tipo:", disp.getTipo())

    def eseguiBackup(self) -> None:
        esito = self._g_dati.eseguiBackup()
        print(f"\n→ {esito}")
