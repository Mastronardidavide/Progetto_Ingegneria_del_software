# 1. Importiamo i Gestori (Control) e il Form (Boundary)
print("Programma parte") #test da terminale
from Services.gestore_dispositivi import GestoreDispositivi
from Services.gestore_dati import GestoreDati
from FormSmartHome import FormSmartHome

# 2. Importiamo le Repository (Data Access) per la Dependency Inversion
from Repositories.dispositivo_repository import DispositivoRepository
from Repositories.backup_repository import BackupRepository

def main():
    # Inizializziamo la persistenza dati
    dispositivo_repo = DispositivoRepository()
    backup_repo = BackupRepository()

    # Creiamo i controller passando le repository (Dependency Inversion)
    g_disp = GestoreDispositivi(dispositivo_repo)
    g_dati = GestoreDati(backup_repo)

    # Avviamo il Form passando i gestori
    form = FormSmartHome(g_disp, g_dati)
    form.avvia()

if __name__ == "__main__":
    main()
