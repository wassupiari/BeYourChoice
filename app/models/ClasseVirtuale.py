import os
import re
from ftplib import print_line

from pymongo import MongoClient

class ClasseVirtuale:
    def __init__(self, db_url="mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/", db_name="BeYourChoice"):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.classi = self.db.classi
        self.upload_folder = "uploads"

        # Creazione della cartella per i file caricati, se non esiste
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def __del__(self):
        """Chiude la connessione al database quando l'oggetto viene distrutto."""
        self.close_connection()

    def close_connection(self):
        """Chiude la connessione al database."""
        if self.client:
            self.client.close()
            print("Connessione al database chiusa")

    class ClasseVirtuale:
        def __init__(self):
            # Simulazione di un database come un dizionario
            self.classi_virtuali = {}
            self.auto_increment_id = 1 # Simula un campo auto-incremento per gli ID delle classi

    def creazioneClasseVirtuale(self, NomeClasse, Descrizione):
        """
        Crea una nuova classe virtuale, con verifica del formato e lunghezza per nome e descrizione.

        Args:
            NomeClasse (str): Il nome della classe virtuale.
            Descrizione (str): La descrizione della classe virtuale.
        Returns:
            str: Messaggio di successo o errore.

        Raises:
            ValueError: Se ci sono problemi con il formato o la lunghezza.
        """
        # Validazione del nome della classe
        if not (2 <= len(NomeClasse) <= 20):
            raise ValueError("Lunghezza del nome della classe virtuale non corretta.")
        if not re.match(r"^[A-Za-zÀ-ú‘’',\(\)\s]{2,20}$", NomeClasse):
            raise ValueError("Formato del nome della classe virtuale non corretto.")

        # Validazione della descrizione
        if not (2 <= len(Descrizione) <= 255):
            raise ValueError("Lunghezza della descrizione della classe virtuale non corretta.")
        if not re.match(r"^[^§]{2,255}$", Descrizione):
            raise ValueError("Formato della descrizione della classe virtuale non corretto.")
        print("ciao")

        IdClasse = self.auto_increment_id
        self.classi_virtuali[IdClasse] = {
            "id_classe": IdClasse,
            "nome": NomeClasse,
            "descrizione": Descrizione,
            "studenti": []
        }

        print("ciao")
        if not self.classi_virtuali:
            print("Ciao")
        else:
            print("Classi Virtuali dopo la creazione:")
            print(self.classi_virtuali)

        # Incrementa l'ID per la prossima classe
        self.auto_increment_id += 1
        return "Classe virtuale creata"

    def inserimentoClasseStudente(self, IdClasse, IdStudente):
        """
          Aggiunge uno studente a una classe virtuale.

          Args:
              IdClasse (int): L'ID della classe virtuale.
              IdStudente (str): L'ID dello studente da aggiungere.

          Returns:
              str: Messaggio di successo o errore.

          Raises:
              ValueError: Se la classe virtuale non esiste o lo studente è già presente.
          """
        # Verifica se lo studente è già nella classe
        if IdStudente in self.classi_virtuali[IdClasse]["studenti"]:
            raise ValueError(f"Errore: Studente con ID '{IdStudente}' già presente nella classe '{IdClasse}'.")

        # Aggiunge lo studente alla classe
        self.classi_virtuali[IdClasse]["studenti"].append(IdStudente)

        return f"Studente con ID '{IdStudente}' aggiunto con successo alla classe '{IdClasse}'."

    def rimozioneClasseStudente(self, IdClasse, IdStudente):

        """
        Rimuove uno studente da una classe virtuale.

        Args:
            IdClasse(int): L'ID della classe virtuale.
            IdStudente (str): L'ID dello studente da rimuovere.

        Returns:
            str: Messaggio di successo o errore.

        Raises:
            ValueError: Se la classe virtuale non esiste o lo studente non è iscritto.
        """
        # Verifica se la classe virtuale esiste
        if IdClasse not in self.classi_virtuali:
            raise ValueError(f"Errore: Classe virtuale con ID '{IdClasse}' non trovata.")

        # Verifica se lo studente è nella classe
        if IdStudente not in self.classi_virtuali[IdStudente]["studenti"]:
            raise ValueError(f"Errore: Studente con ID '{IdStudente}' non presente nella classe '{IdClasse}'.")

        # Rimuove lo studente dalla classe
        self.classi_virtuali[IdClasse]["studenti"].remove(IdStudente)

        return f"Studente con ID '{IdStudente}' rimosso con successo dalla classe '{IdClasse}'."

    def mostra_classe(self, IdClasse):
        """
        Mostra tutti gli studenti di una classe virtuale.

        Args:
            IdClasse (int): L'ID della classe virtuale.

        Returns:
            str: Elenco degli studenti della classe o messaggio di errore.

        Raises:
            ValueError: Se la classe virtuale non esiste.
        """
        # Verifica se la classe virtuale esiste
        if IdClasse not in self.classi_virtuali:
            raise ValueError(f"Errore: Classe virtuale con ID '{IdClasse}' non trovata.")

        # Recupera la lista degli studenti
        studenti = self.classi_virtuali[IdClasse]["studenti"]

        # Mostra gli studenti o un messaggio se la lista è vuota
        if studenti:
            elenco_studenti = "\n".join(f"- Studente ID: {studente}" for studente in studenti)
            return f"Elenco degli studenti della classe '{IdClasse}':\n{elenco_studenti}"
        else:
            return f"Nessuno studente iscritto alla classe '{IdClasse}'."
