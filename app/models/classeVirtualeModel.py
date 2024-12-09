import os
import re
from bson import ObjectId
from flask import session

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

    def creazione_classe_virtuale(self, nome_classe, descrizione, id_docente):
        """
        Crea una nuova classe virtuale, con verifica del formato e lunghezza per nome e descrizione.

        Args:
            nome_classe (str): Il nome della classe virtuale.
            descrizione (str): La descrizione della classe virtuale.
            id_docente (str): L'ID del docente che crea la classe.

        Returns:
            bool: True se la creazione è avvenuta con successo, altrimenti False.

        Raises:
            ValueError: Se ci sono problemi con il formato o la lunghezza.
        """
        try:
            # Validazione del nome della classe
            if not (2 <= len(nome_classe) <= 20):
                raise ValueError("Lunghezza del nome della classe virtuale non corretta.")
            if not re.match(r"^[A-Za-zÀ-ú‘’',\(\)\s0-9]{2,20}$", nome_classe):
                raise ValueError("Formato del nome della classe virtuale non corretto.")

            # Validazione della descrizione
            if not (2 <= len(descrizione) <= 255):
                raise ValueError("Lunghezza della descrizione della classe virtuale non corretta.")
            if not re.match(r"^[a-zA-Z0-9 ]{2,255}$", descrizione):
                raise ValueError("Formato della descrizione della classe virtuale non corretto.")

            # Creazione della classe virtuale
            collection = self.db_manager.get_collection('ClasseVirtuale')
            id_classe = self.auto_increment_id  # Usa l'ID auto-incrementale
            documento = {
                'ID_Classe': id_classe,
                'Nome_Classe': nome_classe,
                'Descrizione': descrizione,
                'ID_Docente': id_docente
            }

            # Inserisci il documento nella collezione
            collection.insert_one(documento)

            # Incrementa l'ID per la prossima classe
            self.auto_increment_id += 1

            return True
        except Exception as e:
            print(f"Errore durante la creazione della classe: {e}")
            return False

    def inserimento_classe_studente(self, id_classe, id_studente):
        """
        Aggiunge uno studente a una classe virtuale.

        Args:
            id_classe (int): L'ID della classe virtuale.
            id_studente (str): L'ID dello studente da aggiungere.

        Returns:
            str: Messaggio di successo o errore.

        Raises:
            ValueError: Se la classe virtuale non esiste o lo studente è già presente.
        """
        # Recupera la collezione 'ClasseVirtuale'
        collection = self.db_manager.get_collection('ClasseVirtuale')

        # Verifica se la classe esiste
        classe = collection.find_one({'ID_Classe': id_classe})
        if not classe:
            raise ValueError(f"Errore: Classe con ID '{id_classe}' non trovata.")

        # Verifica se lo studente è già nella classe
        if id_studente in classe["studenti"]:
            raise ValueError(f"Errore: Studente con ID '{id_studente}' già presente nella classe '{id_classe}'.")

        # Aggiunge lo studente alla classe
        collection.update_one(
            {'ID_Classe': id_classe},
            {'$push': {'studenti': id_studente}}
        )

        return f"Studente con ID '{id_studente}' aggiunto con successo alla classe '{id_classe}'."

    def rimozione_classe_studente(self, id_classe, id_studente):
        """
        Rimuove uno studente da una classe virtuale.

        Args:
            id_classe(int): L'ID della classe virtuale.
            id_studente (str): L'ID dello studente da rimuovere.

        Returns:
            str: Messaggio di successo o errore.

        Raises:
            ValueError: Se la classe virtuale non esiste o lo studente non è iscritto.
        """
        # Recupera la collezione 'ClasseVirtuale'
        collection = self.db_manager.get_collection('ClasseVirtuale')

        # Verifica se la classe esiste
        classe = collection.find_one({'ID_Classe': id_classe})
        if not classe:
            raise ValueError(f"Errore: Classe con ID '{id_classe}' non trovata.")

        # Verifica se lo studente è nella classe
        if id_studente not in classe["studenti"]:
            raise ValueError(f"Errore: Studente con ID '{id_studente}' non presente nella classe '{id_classe}'.")

        # Rimuove lo studente dalla classe
        collection.update_one(
            {'ID_Classe': id_classe},
            {'$pull': {'studenti': id_studente}}
        )

        return f"Studente con ID '{id_studente}' rimosso con successo dalla classe '{id_classe}'."

    def mostra_classe(self, id_classe):
        """
        Recupera gli studenti di una classe specifica in ordine alfabetico.

        Args:
            id_classe (int): L'ID della classe virtuale.

        Returns:
            list[dict]: Lista di studenti con Nome, Cognome e Data di Nascita.
        """
        try:
            print(f"Recupero gli studenti per la classe con ID: {id_classe}")  # Aggiunto per debugging
            studente_collection = self.db_manager.get_collection("Studente")

            # Esegui la query per recuperare gli studenti della classe e ordina per 'Cognome' e 'Nome'
            studenti = list(
                studente_collection.find({"ID_Classe": id_classe}).sort([("nome", 1), ("cognome", 1)])
            )

            # Verifica se la query restituisce risultati
            if not studenti:
                print(f"Nessun studente trovato per la classe con ID {id_classe}")  # Aggiunto per debugging
                raise ValueError(f"Nessuno studente trovato per la classe con ID {id_classe}")

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
            print(f"Errore durante il recupero degli studenti: {e}")  # Aggiunto per debugging
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

    def cerca_studenti(self, query, id_classe):
        """
        Cerca gli studenti della classe specificata in base alla query.

        Args:
            query (str): La query di ricerca.
            id_classe (int): L'ID della classe.

        Returns:
            list[dict]: Studenti filtrati o tutti gli studenti se la query è vuota.
        """
        collection = self.db_manager.get_collection("Studente")
        print("prova del nove", id_classe)
        if not query:
            # Restituisci tutti gli studenti della classe
            studenti = list(collection.find({"ID_Classe": id_classe}))
        else:
            # Cerca studenti in base alla query (case-insensitive match)
            studenti = list(collection.find({
                "ID_Classe": id_classe,
                "$or": [
                    {"nome": {"$regex": query, "$options": "i"}},
                    {"cognome": {"$regex": query, "$options": "i"}}
                ]
            }))
        return [
            {

                "Nome": studente["nome"],
                "Cognome": studente["cognome"],
                "Data_Nascita": studente["Data_Nascita"],
                "_id": str(studente["_id"])
            }

            for studente in studenti

        ]

    def cerca_studenti_istituto(self, query):
        """
        Cerca gli studenti della classe specificata in base alla query.

        Args:
            query (str): La query di ricerca.
            id_classe (int): L'ID della classe.

        Returns:
            list[dict]: Studenti filtrati o tutti gli studenti se la query è vuota.
        """

        sda = session.get('sda')
        collection = self.db_manager.get_collection("Studente")
        if not query:
            # Restituisci tutti gli studenti della classe
            studenti = list(collection.find({"sda": sda}))
        else:
            studenti = list(collection.find({
                "SdA": sda,  # Controlla la scuola di appartenenza
                "$and": [  # Usa l'operatore $and per combinare le condizioni
                    {
                        "$or": [  # Cerca studenti senza classe e che corrispondono alla query
                            {"ID_Classe": {"$exists": False}},  # Studenti senza classe
                            {"ID_Classe": None}  # Studenti con ID_Classe a None
                        ]
                    },
                    {
                        "$or": [  # Cerca per nome o cognome (case-insensitive)
                            {"nome": {"$regex": query, "$options": "i"}},  # Ricerca per nome
                            {"cognome": {"$regex": query, "$options": "i"}}  # Ricerca per cognome
                        ]
                    }
                ]
            }))
            return [
                {

                    "Nome": studente["nome"],
                    "Cognome": studente["cognome"],
                    "Data_Nascita": studente["Data_Nascita"],
                    "_id": str(studente["_id"])
                }

                for studente in studenti

            ]
