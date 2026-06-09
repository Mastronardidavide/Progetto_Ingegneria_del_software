from datetime import datetime

class BoundaryZona:
    def __init__(self, g_zona):
        """ Riceve l'istanza del GestoreZona per operare sulle zone """
        self._g_zona = g_zona

    def menu_zone(self):
        while True:
            print("\n=======================================================")
            print("Gestione Zone: \n'lista' (mostra zone) \n'aggiungi' (crea nuova zona) \n'rimuovi' (elimina zona)")
            print("'rinomina' (aggiorna nome) \n'orario' (imposta finestra temporale) \n'automazione' (imposta sensore+soglia)")
            print("'associa' (collega attuatore) \n'disassocia' (rimuovi attuatore) \n'indietro' (torna al menu principale)")
            print("=======================================================\n")
            
            comando = input("Inserisci comando zona> ").strip().lower()
            
            if comando == "lista":
                zone = self._g_zona._zona_repo.tutte()
                if not zone:
                    print("Nessuna zona presente nel sistema.")
                else:
                    print("\nELENCO ZONE")
                    for z in zone:
                        print(f"\n- {z.getNome()}")
                
            elif comando == "aggiungi":
                # Validazione ID Zona, aggiungo la zona ma non ne inserisco immediatamente orari e dispositivi
                while True:
                    try:
                        id_zona = int(input("Inserisci ID zona (numero intero): ").strip())
                        break
                    except ValueError:
                        print("ID non valido. Inserisci un numero intero.")
                
                nome = input("Inserisci nome zona: ").strip()
                
                # crea una zona vuota passandogli solo ID e Nome
                feedback = self._g_zona.creaZona(id=id_zona, nome=nome)
                print(f"\n[Nuova zona]: {feedback}")
                
            elif comando == "rimuovi":
                while True:
                    try:
                        id_zona = int(input("ID della zona da rimuovere: ").strip())
                        break
                    except ValueError:
                        print("Inserisci un numero intero valido.")
                
                feedback = self._g_zona.eliminaZona(id=id_zona)
                print(feedback)

            elif comando == "rinomina":
                while True:
                    try:
                        id_zona = int(input("Inserisci l'ID della zona da modificare: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                nuovo_nome = input("Nuovo nome della zona [Premi Invio per non modificare]: ").strip()
                if not nuovo_nome:
                    nuovo_nome = None

                feedback = self._g_zona.modificaZona(id=id_zona, nuovo_nome=nuovo_nome)
                print(feedback)

            # configurazione finestra oraria di accensione della zona
            elif comando == "orario":
                while True:
                    try:
                        id_zona = int(input("Inserisci l'ID della zona da programmare: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                # Richiesta e validazione dell'orario di accensione
                orario_inizio = None
                str_in = input("Inserisci l'orario di accensione (HH:MM): ").strip()
                if str_in:
                    try:
                        orario_inizio = datetime.strptime(str_in, "%H:%M").time()
                    except ValueError:
                        print("Formato errato. L'orario di accensione è stato saltato.")

                # Richiesta e validazione dell'orario di spegnimento
                orario_fine = None
                str_fi = input("Inserisci l'orario di spegnimento (HH:MM): ").strip()
                if str_fi:
                    try:
                        orario_fine = datetime.strptime(str_fi, "%H:%M").time()
                    except ValueError:
                        print("Formato errato. L'orario di spegnimento è stato saltato.")

                # Chiamata alla funzione del gestore
                feedback = self._g_zona.impostaProgrammazioneOraria(id_zona=id_zona, orario_inizio=orario_inizio, orario_fine=orario_fine)
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
                        id_zona = int(input("ID della zona a cui collegare l'attuatore: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                id_att = input("Inserisci l'ID dell'attuatore da aggiungere: ").strip()
                feedback = self._g_zona.associaAttuatoreAZona(id_zona=id_zona, id_attuatore=id_att)
                print(feedback)

            elif comando == "disassocia":
                while True:
                    try:
                        id_zona = int(input("ID della zona da cui rimuovere l'attuatore: ").strip())
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
