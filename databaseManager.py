from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, NetworkTimeout, ConfigurationError

class DatabaseManager:
    _instance = None  # Singleton instance

    def __new__(cls, uri=None, db_name=None):
        """
        Crea un'istanza singleton di DatabaseManager.
        """
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize(uri, db_name)
        return cls._instance

    def _initialize(self, uri, db_name):
        """
        Inizializza la connessione al database MongoDB.
        :param uri: URI di connessione.
        :param db_name: Nome del database.
        """
        try:
            self.client = MongoClient(uri or "mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority&appName=BeYourChoice",
                                      tls=True, tlsInsecure=True,
                                      serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name or "BeYourChoice;"]
            print(f"Connessione al database '{db_name}' riuscita")
        except (ValueError, ServerSelectionTimeoutError, NetworkTimeout, ConfigurationError) as e:
            print(f"Errore di connessione a MongoDB: {e}")
            self.client = None
            self.db = None

    def get_collection(self, collection_name):
        if self.db is not None:
            return self.db[collection_name]
        else:
            raise Exception("Database non connesso")

    def close_connection(self):
        if self.client:
            self.client.close()
            print("Connessione al database chiusa")
