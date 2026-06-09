from datetime import datetime

class BoundaryZona:
    def __init__(self, g_zona):
        """ Riceve l'istanza del GestoreZona per operare sulle zone """
        self._g_zona = g_zona

    def menu_zone(self):
        while True:
            print("\n=======================================================")
            print("Gestione Zone: \n'lista' (mostra zone) \n'aggiungi' (crea nuova zona) \n'rimuovi' (elimina zona)")
            print("'modifica' (aggiorna nome/orario) \n'automazione' (imposta sensore+soglia) \n'associa' (collega attuatore) \n'disassocia' (rimuovi attuatore) \n'indietro' (torna al menu principale)")
            print("=======================================================\n")
            
            comando = input("Inserisci comando zona> ").strip().lower()
            
            if comando == "lista":
                # Otteniamo tutte le zone dal repository sfruttando il metodo del tuo repo
                zone = self._g_zona._zona_repo.tutte()
                if not zone:
                    print("Nessuna zona presente nel sistema.")
                else:
                    print("\n--- ELENCO ZONE ---")
                    for z in zone:
                        print(z) # Sfrutta il dunder method __str__ definito nel modello Zona
                
            elif comando == "aggiungi":
                # 1. Validazione ID Zona
                while True:
                    try:
                        id_zona = int(input("Inserisci ID zona (numero intero): ").strip())
                        break
                    except ValueError:
                        print("ID non valido. Inserisci un numero intero.")
                
                nome = input("Inserisci nome zona: ").strip()
                
                # 2. Creazione iniziale tramite il gestore
                feedback = self._g_zona.creaZona(id=id_zona, nome=nome)
                print(feedback)
                
                # Se la zona è stata creata con successo, avviamo la configurazione guidata degli accessori
                if feedback == "La zona è stata creata con successo":
                    # Recuperiamo l'oggetto appena creato per modificarlo
                    zona_creata = self._g_zona._zona_repo.trovaPerId(id_zona)
                    
                    # 3. Inserimento manuale e continuo degli ID Attuatori
                    print("\n--- Associazione Attuatori ---")
                    while True:
                        id_att = input("Inserisci l'ID di un attuatore da associare (Premi Invio per terminare): ").strip()
                        if not id_att:
                            break
                        # Chiamata al metodo del gestore per associare l'attuatore
                        res = self._g_zona.associaAttuatoreAZona(id_zona=id_zona, id_attuatore=id_att)
                        print(res)

                    # 4. Inserimento Orario opzionale
                    orario_str = input("\nVuoi impostare un orario di attivazione? (HH:MM) [Premi Invio per saltare]: ").strip()
                    if orario_str:
                        try:
                            orario_zona = datetime.strptime(orario_str, "%H:%M").time()
                            self._g_zona.modificaZona(id=id_zona, nuovo_orario=orario_zona)
                            print("Orario di attivazione impostato con successo.")
                        except ValueError:
                            print("Formato orario errato. L'orario è stato saltato.")

                    # 5. OPZIONE B: Richiesta guidata e accoppiata per Sensore + Soglia
                    scelta_auto = input("\nVuoi attivare l'automazione basata su un sensore? (si/no): ").strip().lower()
                    if scelta_auto == "si":
                        id_sensore = input("Inserisci l'ID del sensore pilota: ").strip()
                        while True:
                            try:
                                soglia_input = input(f"Inserisci la soglia (float) oltre la quale attivare gli attuatori: ").strip()
                                soglia = float(soglia_input)
                                break
                            except ValueError:
                                print("Soglia non valida. Inserisci un numero decimale (float).")
                        
                        # Chiamata alla nuova funzione di accoppiamento del gestore
                        res_auto = self._g_zona.impostaAutomazioneSensore(id_zona=id_zona, id_sensore=id_sensore, valore_soglia=soglia)
                        print(res_auto)

            elif comando == "rimuovi":
                while True:
                    try:
                        id_zona = int(input("ID della zona da rimuovere: ").strip())
                        break
                    except ValueError:
                        print("Inserisci un numero intero valido.")
                
                feedback = self._g_zona.eliminaZona(id=id_zona)
                print(feedback)

            elif comando == "modifica":
                while True:
                    try:
                        id_zona = int(input("Inserisci l'ID della zona da modificare: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                nuovo_nome = input("Nuovo nome della zona [Premi Invio per non modificare]: ").strip()
                if not nuevo_nome:
                    nuovo_nome = None
                    
                nuovo_orario = None
                orario_str = input("Nuovo orario (HH:MM) [Premi Invio per non modificare]: ").strip()
                if orario_str:
                    try:
                        nuovo_orario = datetime.strptime(orario_str, "%H:%M").time()
                    except ValueError:
                        print("Formato orario errato. L'orario non verrà modificato.")

                feedback = self._g_zona.modificaZona(id=id_zona, nuovo_nome=nuovo_nome, nuovo_orario=nuovo_orario)
                print(feedback)

            elif comando == "automazione":
                while True:
                    try:
                        id_zona = int(input("Inserisci l'ID della zona per configurare l'automazione: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                id_sensore = input("Inserisci l'ID del sensore pilota: ").strip()
                while True:
                    try:
                        soglia_input = input("Inserisci il valore float della soglia limite: ").strip()
                        soglia = float(soglia_input)
                        break
                    except ValueError:
                        print("Soglia non valida. Inserisci un numero decimale (float).")
                
                feedback = self._g_zona.impostaAutomazioneSensore(id_zona=id_zona, id_sensore=id_sensore, valore_soglia=soglia)
                print(feedback)

            elif comando == "associa":
                while True:
                    try:
                        id_zona = int(input("ID della zona a cui collegare il dispositivo: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                id_att = input("Inserisci l'ID dell'attuatore da aggiungere: ").strip()
                feedback = self._g_zona.associaAttuatoreAZona(id_zona=id_zona, id_attuatore=id_att)
                print(feedback)

            elif comando == "disassocia":
                while True:
                    try:
                        id_zona = int(input("ID della zona da cui rimuovere il dispositivo: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                id_att = input("Inserisci l'ID dell'attuatore da rimuovere: ").strip()
                feedback = self._g_zona.rimuoviAttuatoreDaZona(id_zona=id_zona, id_attuatore=id_att)
                print(feedback)
                
            elif comando == "indietro":
                break
            else:
                print(f"Comando '{comando}' non riconosciuto.")
