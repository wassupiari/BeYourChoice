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
                'id_classe': id_classe,
                'nome_classe': nome_classe,
                'descrizione': descrizione,
                'id_docente': id_docente
            }

            # Inserisci il documento nella collezione
            collection.insert_one(documento)

            # Incrementa l'ID per la prossima classe
            self.auto_increment_id += 1

            return True
        except Exception as e:
            print(f"Errore durante la creazione della classe: {e}")
            return False

    def rimuovi_studente_classe(self, studente_id):
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
                {"$set": {"id_classe": None}}  # Imposta ID_Classe a null
            )
            if result.modified_count == 0:
                raise Exception("Nessuna modifica effettuata. Verifica l'ID dello studente.")
        except Exception as e:
            print(f"Errore nel modello: {e}")
            raise

    from bson import ObjectId

    def aggiungi_studente_classe(self, id_studente, id_classe):
        print("aaaa")
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
            # Controlla se lo studente esiste
            studente = studente_collection.find_one({"_id": ObjectId(id_studente)})
            if not studente:
                print(f"Errore: Studente con ID '{id_studente}' non trovato.")
                return False

            result = studente_collection.update_one(
                {"_id": ObjectId(id_studente)},  # Filtra per l'ID dello studente
                {"$set": {"id_classe": id_classe}}  # Imposta l'ID della classe
            )

            # Verifica se l'operazione è stata eseguita correttamente
            if result.modified_count > 0:
                return True
            else:
                print(f"Errore: Nessuna modifica effettuata per lo studente con ID '{id_studente}'.")
                return False

        except Exception as e:
            print(f"Errore durante l'aggiunta dello studente alla classe: {e}")
            return False

    def mostra_studenti_classe(self, id_classe):
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
                studente_collection.find({"id_classe": id_classe}).sort([("nome", 1), ("cognome", 1)])
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
                    "Data_Nascita": studente.get("data_nascita", "N/A"),
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
                    "sda": scuola_appartenenza,
                    "$or": [{"id_classe": {"$exists": False}}, {"id_classe": None}]
                }).sort([("nome", 1), ("cognome", 1)])  # Ordina per Cognome e Nome
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
                    "Data_Nascita": studente.get("data_nascita", "N/A"),
                    "_id": str(studente["_id"])  # Converti ObjectId in stringa
                })

            return studenti_istituto
        except Exception as e:
            print(f"Errore durante il recupero degli studenti: {e}")  # Aggiunto per debugging
            raise

    def cerca_studenti_classe(self, query, id_classe):
        """
            Cerca gli studenti della classe specificata in base alla query.

        Args:
            query (str): La query di ricerca.
            id_classe (int): L'ID della classe.

        Returns:
            list[dict]: Studenti filtrati o tutti gli studenti se la query è vuota.
        """
        print(query)
        collection = self.db_manager.get_collection("Studente")
        if not query:
            # Restituisci tutti gli studenti della classe
            studenti = list(collection.find({"id_classe": id_classe}))
        else:
            # Cerca studenti in base alla query (case-insensitive match)
            studenti = list(collection.find({
                "id_classe": id_classe,
                "$or": [
                    {"cf": {"$regex": query, "$options": "i"}}
                ]
            }))
        return [
            {

                "Nome": studente["nome"],
                "Cognome": studente["cognome"],
                "Data_Nascita": studente["data_nascita"],
                "_id": str(studente["_id"])
            }

            for studente in studenti

        ]

    def cerca_studenti_istituto(self, query):
        """
          Cerca gli studenti dell'istituto del docente che sta effettuando la ricerca

        Args:
            query (str): La query di ricerca.

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
                "sda": sda,  # Controlla la scuola di appartenenza
                "$and": [  # Usa l'operatore $and per combinare le condizioni
                    {
                        "$or": [  # Cerca studenti senza classe e che corrispondono alla query
                            {"id_classe": {"$exists": False}},  # Studenti senza classe
                            {"id_classe": None}  # Studenti con ID_Classe a None
                        ]
                    },
                    {
                        "$or": [  # Cerca per nome o cognome (case-insensitive)
                            {"cf": {"$regex": query, "$options": "i"}}
                        ]
                    }
                ]
            }))
            return [
                {

                    "Nome": studente["nome"],
                    "Cognome": studente["cognome"],
                    "Data_Nascita": studente["data_nascita"],
                    "_id": str(studente["_id"])
                }

                for studente in studenti

            ]
