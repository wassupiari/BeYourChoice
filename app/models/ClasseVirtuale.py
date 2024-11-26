import os
import re

from pymongo import MongoClient

from databaseManager import DatabaseManager


class ClasseVirtuale:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.auto_increment_id = self.get_next_auto_increment_id()

        # Creazione della cartella per i file caricati, se non esiste
        # if not os.path.exists(self.upload_folder):
        #   os.makedirs(self.upload_folder)

    def get_next_auto_increment_id(self):
        """
        Ottiene il prossimo ID auto-incrementale per la classe virtuale.
        """
        counter_collection = self.db_manager.get_collection('counters')
        counter = counter_collection.find_one_and_update(
            {'_id': 'ClasseVirtuale'},
            {'$inc': {'sequence_value': 1}},
            upsert=True,
            return_document=True
        )
        return counter['sequence_value']

    # def __del__(self):
    # """Chiude la connessione al database quando l'oggetto viene distrutto."""
    # self.close_connection()

    # def close_connection(self):
    #    """Chiude la connessione al database."""
    #   if self.client:
    #        self.client.close()
    #       print("Connessione al database chiusa")

    class ClasseVirtuale:
        def __init__(self):
            # Simulazione di un database come un dizionario
            self.classi_virtuali = {}
            self.auto_increment_id = 1  # Simula un campo auto-incremento per gli ID delle classi

    def visualizza_tutti_studenti(self):
        """
        Recupera tutti gli studenti dal database e restituisce i dati completi,
        ma visualizza solo Nome, Cognome e Data_Nascita.

        Returns:
            str: Elenco di studenti con Nome, Cognome e Data di Nascita.
        """
        # Recupera la collezione 'Studenti'
        collection = self.db_manager.get_collection('Studente')

        # Query per ottenere tutti gli studenti
        studenti = collection.find({})  # Ottieni tutti i documenti senza filtri

        # Formatta il risultato in una stringa leggibile
        risultato = []
        for studente in studenti:
            risultato.append(
                f"Nome: {studente.get('Nome', 'N/A')}, Cognome: {studente.get('Cognome', 'N/A')}, "
                f"Data di Nascita: {studente.get('Data_Nascita', 'N/A')}"
            )

        if risultato:
            return "\n".join(risultato)
        else:
            return "Nessuno studente trovato nel database."

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

        # Creazione della classe virtuale
        collection = self.db_manager.get_collection('ClasseVirtuale')
        ID_Classe = self.auto_increment_id  # Usa l'ID auto-incrementale
        documento = {
            'ID_Classe': ID_Classe,
            'Nome_Classe': NomeClasse,
            'Descrizione': Descrizione
        }

        # Inserisci il documento nella collezione
        collection.insert_one(documento)

        # Incrementa l'ID per la prossima classe
        self.auto_increment_id += 1
        studenti_visualizzati = self.visualizza_tutti_studenti()
        print(studenti_visualizzati)  # Mostra il risultato a schermo

        return "Classe virtuale creata con successo"

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
        # Recupera la collezione 'ClasseVirtuale'
        collection = self.db_manager.get_collection('ClasseVirtuale')

        # Verifica se la classe esiste
        classe = collection.find_one({'ID_Classe': IdClasse})
        if not classe:
            raise ValueError(f"Errore: Classe con ID '{IdClasse}' non trovata.")

        # Verifica se lo studente è già nella classe
        if IdStudente in classe["studenti"]:
            raise ValueError(f"Errore: Studente con ID '{IdStudente}' già presente nella classe '{IdClasse}'.")

        # Aggiunge lo studente alla classe
        collection.update_one(
            {'ID_Classe': IdClasse},
            {'$push': {'studenti': IdStudente}}
        )

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
        # Recupera la collezione 'ClasseVirtuale'
        collection = self.db_manager.get_collection('ClasseVirtuale')

        # Verifica se la classe esiste
        classe = collection.find_one({'ID_Classe': IdClasse})
        if not classe:
            raise ValueError(f"Errore: Classe con ID '{IdClasse}' non trovata.")

        # Verifica se lo studente è nella classe
        if IdStudente not in classe["studenti"]:
            raise ValueError(f"Errore: Studente con ID '{IdStudente}' non presente nella classe '{IdClasse}'.")

        # Rimuove lo studente dalla classe
        collection.update_one(
            {'ID_Classe': IdClasse},
            {'$pull': {'studenti': IdStudente}}
        )

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
        # Recupera la collezione 'ClasseVirtuale'
        collection = self.db_manager.get_collection('ClasseVirtuale')

        # Verifica se la classe esiste
        classe = collection.find_one({'ID_Classe': IdClasse})
        if not classe:
            raise ValueError(f"Errore: Classe con ID '{IdClasse}' non trovata.")

        # Recupera la lista degli studenti
        studenti = classe.get("studenti", [])

        # Mostra gli studenti o un messaggio se la lista è vuota
        if studenti:
            elenco_studenti = "\n".join(f"- Studente ID: {studente}" for studente in studenti)
            return f"Elenco degli studenti della classe '{IdClasse}':\n{elenco_studenti}"
        else:
            return f"Nessuno studente iscritto alla classe '{IdClasse}'."
