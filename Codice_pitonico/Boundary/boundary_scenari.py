from datetime import datetime

class BoundaryScenario:
    def __init__(self, g_scenario):
        self._g_scenario = g_scenario

    def menu_scenari(self):
        while True:
            print("\n=======================================================")
            print("Gestione Scenari: \n'lista' (mostra scenari) \n'aggiungi' (crea nuovo scenario) \n'rimuovi' (elimina scenario)")
            print("'rinomina' (aggiorna nome) \n'orario' (imposta finestra temporale) \n'automazione' (imposta sensore+soglia)")
            print("'associa' (collega attuatore) \n'disassocia' (rimuovi attuatore) \n'indietro' (torna al menu principale)")
            print("=======================================================\n")
            
            comando = input("Inserisci comando scenario> ").strip().lower()
            
            if comando == "lista":
                scenari = self._g_scenario._scenario_repo.tutte()
                if not scenari:
                    print("Nessuno scenario presente nel sistema.")
                else:
                    print("\nELENCO SCENARI")
                    for s in scenari:
                        print(f"\n- {s.getNome()}")
                
            elif comando == "aggiungi":
                while True:
                    try:
                        id_scenario = int(input("Inserisci ID scenario (numero intero): ").strip())
                        break
                    except ValueError:
                        print("ID non valido. Inserisci un numero intero.")
                
                nome = input("Inserisci nome scenario: ").strip()
                
                feedback = self._g_scenario.creaScenario(id=id_scenario, nome=nome)
                print(f"\n[Nuovo scenario]: {feedback}")
                
            elif comando == "rimuovi":
                while True:
                    try:
                        id_scenario = int(input("ID dello scenario da rimuovere: ").strip())
                        break
                    except ValueError:
                        print("Inserisci un numero intero valido.")
                
                feedback = self._g_scenario.eliminaScenario(id=id_scenario)
                print(feedback)

            elif comando == "rinomina":
                while True:
                    try:
                        id_scenario = int(input("Inserisci l'ID dello scenario da modificare: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                nuovo_nome = input("Nuovo nome dello scenario [Premi Invio per non modificare]: ").strip()
                if not nuovo_nome:
                    nuovo_nome = None

                feedback = self._g_scenario.modificaScenario(id=id_scenario, nuovo_nome=nuovo_nome)
                print(feedback)

            elif comando == "orario":
                while True:
                    try:
                        id_scenario = int(input("Inserisci l'ID dello scenario da programmare: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                orario_inizio = None
                str_in = input("Inserisci l'orario di accensione (HH:MM): ").strip()
                if str_in:
                    try:
                        orario_inizio = datetime.strptime(str_in, "%H:%M").time()
                    except ValueError:
                        print("Formato errato. L'orario di accensione è stato saltato.")

                orario_fine = None
                str_fi = input("Inserisci l'orario di spegnimento (HH:MM): ").strip()
                if str_fi:
                    try:
                        orario_fine = datetime.strptime(str_fi, "%H:%M").time()
                    except ValueError:
                        print("Formato errato. L'orario di spegnimento è stato saltato.")

                feedback = self._g_scenario.impostaProgrammazioneOraria(id_scenario=id_scenario, orario_inizio=orario_inizio, orario_fine=orario_fine)
                print(feedback)

            elif comando == "automazione":
                while True:
                    try:
                        id_scenario = int(input("Inserisci l'ID dello scenario per configurare l'automazione: ").strip())
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
                
                feedback = self._g_scenario.impostaAutomazioneSensore(id_scenario=id_scenario, id_sensore=id_sensore, valore_soglia=soglia)
                print(feedback)

            elif comando == "associa":
                while True:
                    try:
                        id_scenario = int(input("ID dello scenario a cui collegare l'attuatore: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                id_att = input("Inserisci l'ID dell'attuatore da aggiungere: ").strip()
                feedback = self._g_scenario.associaAttuatoreAScenario(id_scenario=id_scenario, id_attuatore=id_att)
                print(feedback)

            elif comando == "disassocia":
                while True:
                    try:
                        id_scenario = int(input("ID dello scenario da cui rimuovere l'attuatore: ").strip())
                        break
                    except ValueError:
                        print("L'ID deve essere un numero intero.")
                
                id_att = input("Inserisci l'ID dell'attuatore da rimuovere: ").strip()
                feedback = self._g_scenario.rimuoviAttuatoreDaScenario(id_scenario=id_scenario, id_attuatore=id_att)
                print(feedback)
                
            elif comando == "indietro":
                break
            else:
                print(f"Comando '{comando}' non riconosciuto.")
