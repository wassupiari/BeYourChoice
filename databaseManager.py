from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class DatabaseManager:
    def __init__(self,  db_name="BeYourChoice;"):
        """
        Inizializza la connessione al database MongoDB.
        :param db_name: Nome del database.
        """

        try:
            # Crea la stringa URI per la connessione
            uri = f"mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority"

            # Crea il client con parametri per TLS
            self.client = MongoClient(uri, tls=True, tlsInsecure=True,
                                      serverSelectionTimeoutMS=5000)  # Timeout di 5 secondi
            self.db = self.client[db_name]

            # Controlla la connessione
            self.client.server_info()  # Genera un'eccezione se la connessione fallisce
            print(f"Connesso con successo al database '{db_name}'")
        except ServerSelectionTimeoutError as e:
            print(f"Errore di connessione a MongoDB: {e}")
            self.client = None
            self.db = None

    def get_collection(self, collection_name):
        """
        Restituisce una collezione del database.
        :param collection_name: Nome della collezione.
        :return: La collezione MongoDB.
        """
        if self.db is not None:  # Controlla esplicitamente se self.db è diverso da None
            return self.db[collection_name]
        else:
            raise Exception("Database non connesso")

    def close_connection(self):
        """
        Chiude la connessione al database.
        """
        if self.client:
            self.client.close()
            print("Connessione al database chiusa")
        else:
            print("Nessuna connessione attiva da chiudere")


