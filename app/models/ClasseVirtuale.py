import os
import re
from bson import ObjectId

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

    def creazioneClasseVirtuale(self, NomeClasse, Descrizione, ID_Docente):
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
            'Descrizione': Descrizione,
            'ID_Docente' : ID_Docente
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

    def mostra_classe(self, ID_Classe):
        print("ciao2")
        """
        Recupera gli studenti di una classe specifica in ordine alfabetico.

        Args:
            ID_Classe (int): L'ID della classe virtuale.

        Returns:
            list[dict]: Lista di studenti con Nome, Cognome e Data di Nascita.
        """
        try:
            print(f"Recupero gli studenti per la classe con ID: {ID_Classe}")  # Aggiunto per debugging
            studente_collection = self.db_manager.get_collection("Studente")

            # Esegui la query per recuperare gli studenti della classe e ordina per 'Cognome' e 'Nome'
            studenti = list(
                studente_collection.find({"ID_Classe": ID_Classe}).sort([("nome", 1), ("cognome", 1)])
            )

            # Verifica se la query restituisce risultati
            if not studenti:
                print(f"Nessun studente trovato per la classe con ID {ID_Classe}")  # Aggiunto per debugging
                raise ValueError(f"Nessuno studente trovato per la classe con ID {ID_Classe}")

            # Logga il numero di studenti trovati
            print(f"Numero di studenti trovati: {len(studenti)}")  # Aggiunto per debugging

            mostraclasse = []
            for studente in studenti:
                mostraclasse.append({
                    "Nome": studente["nome"],
                    "Cognome": studente["cognome"],
                    "Data_Nascita": studente.get("Data_Nascita", "N/A"),
                    "_id": studente["_id"]
                })
            print(mostraclasse)
            return mostraclasse
        except Exception as e:
            print(f"Errore durante il recupero degli studenti: {e}")  # Aggiunto per debugging
            raise

    def mostra_studenti_istituto(self, scuola_appartenenza):
        """
        Recupera gli studenti di un istituto specifico che non sono assegnati a una classe,
        ordinati alfabeticamente per Cognome e Nome.

        Args:
            scuola_appartenenza (str): La scuola di appartenenza (SdA).

        Returns:
            list[dict]: Lista di studenti con Nome, Cognome e Data di Nascita.
        """
        try:
            print(f"Recupero gli studenti per l'istituto: {scuola_appartenenza}")  # Debug
            studente_collection = self.db_manager.get_collection("Studente")

            # Query per recuperare studenti dell'istituto non assegnati a una classe
            studenti = list(
                studente_collection.find({
                    "SdA": scuola_appartenenza,
                    "$or": [{"ID_Classe": {"$exists": False}}, {"ID_Classe": None}]
                }).sort([("Nome", 1), ("Cognome", 1)])  # Ordina per Cognome e Nome
            )

            # Verifica se ci sono risultati
            if not studenti:
                print(f"Nessun studente trovato per la scuola: {scuola_appartenenza}")  # Debug
                raise ValueError(f"Nessuno studente trovato per la scuola: {scuola_appartenenza}")

            # Log del numero di studenti trovati
            print(f"Numero di studenti trovati: {len(studenti)}")  # Debug

            # Formatta i dati per il ritorno
            studenti_istituto = []
            for studente in studenti:
                studenti_istituto.append({
                    "Nome": studente.get("nome", "N/A"),
                    "Cognome": studente.get("cognome", "N/A"),
                    "Data_Nascita": studente.get("Data_Nascita", "N/A"),
                    "_id": str(studente["_id"])  # Converti ObjectId in stringa
                })

            return studenti_istituto
        except Exception as e:
            print(f"Errore durante il recupero degli studenti: {e}")  # Debug
            raise

    def rimuovi_studente(self, studente_id):
        """
        Imposta il campo ID_Classe dello studente a null.

        Args:
            studente_id (str): ID dello studente da rimuovere.

        Raises:
            Exception: In caso di errore durante l'aggiornamento.
        """
        try:
            studente_collection = self.db_manager.get_collection("Studente")
            result = studente_collection.update_one(
                {"_id": ObjectId(studente_id)},  # Filtra per l'ID dello studente
                {"$set": {"ID_Classe": None}}  # Imposta ID_Classe a null
            )
            if result.modified_count == 0:
                raise Exception("Nessuna modifica effettuata. Verifica l'ID dello studente.")
        except Exception as e:
            print(f"Errore nel modello: {e}")
            raise

    from bson import ObjectId

    def aggiungi_studente(self, studente_id, classe_id):
        """
        Aggiunge uno studente alla classe, impostando l'ID della classe nel documento dello studente.

        Args:
            studente_id (str): L'ID dello studente.
            classe_id (str): L'ID della classe alla quale associare lo studente.

        Returns:
            bool: Se l'operazione è riuscita o meno.
        """
        try:
            # Recupera la collezione 'Studenti'
            studente_collection = self.db_manager.get_collection("Studente")
            # Filtra per l'ID dello studente e aggiungi l'ID della classe
            result = studente_collection.update_one(
                {"_id": ObjectId(studente_id)},  # Filtra per l'ID dello studente
                {"$set": {"ID_Classe": classe_id}}  # Imposta l'ID della classe
            )

            # Verifica se l'operazione è stata eseguita correttamente
            if result.modified_count > 0:
                return True
            else:
                print(f"Errore: Nessuna modifica effettuata per lo studente con ID '{studente_id}'.")
                return False

        except Exception as e:
            print(f"Errore durante l'aggiunta dello studente alla classe: {e}")
            return False
