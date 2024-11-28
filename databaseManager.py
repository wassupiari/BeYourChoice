from bson import ObjectId
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, NetworkTimeout, ConfigurationError

# Caricamento delle variabili d'ambiente dal file .env
load_dotenv()


class DatabaseManager:
    def __init__(self, db_name="BeYourChoice;"):
        """
        Inizializza la connessione al database MongoDB.
        :param db_name: Nome del database.
        """
        try:
            # Ottieni l'URI dal file .env
            uri = os.getenv("MONGO_URI")
            if not uri:
                raise ValueError(
                    "URI MongoDB non definito. Assicurati che la variabile MONGO_URI sia presente nel file .env."
                )

            # Crea il client con l'URI inclusa la configurazione SSL
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[db_name]
            self.collection = self.db['MaterialeDidattico']

            # Testa la connessione
            self.client.server_info()  # Solleva un'eccezione se la connessione fallisce
            print(f"Connessione al database '{db_name}' riuscita")
        except ValueError as e:
            print(f"Errore: {e}")
            self.client = None
            self.db = None
        except ServerSelectionTimeoutError as e:
            print(f"Errore di timeout di connessione a MongoDB: {e}")
            self.client = None
            self.db = None
        except (NetworkTimeout, ConfigurationError) as e:
            print(f"Errore di connessione/configurazione a MongoDB: {e}")
            self.client = None
            self.db = None
        except Exception as e:
            print(f"Si è verificato un errore inatteso: {e}")
            self.client = None
            self.db = None

    def get_collection(self, collection_name):
        """
        Restituisce una collezione dal database.
        :param collection_name: Nome della collezione.
        :return: La collezione MongoDB.
        """
        if self.db is not None:
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

    def insert_document(self, collection_name, document):
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def find_document(self, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    def update_document(self, collection_name, query, new_values):
        collection = self.get_collection(collection_name)
        return collection.update_one(query, {"$set": new_values})

    def delete_document(self, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.delete_one(query)

    def delete_material(self, material_id):
        # Elimina il documento con l'ID fornito
        result = self.collection.delete_one({'_id': ObjectId(material_id)})
        if result.deleted_count == 1:
            return True
        else:
            return False

    def count_documents(self, collection_name, query):
        collection = self.get_collection(collection_name)
        return collection.count_documents(query)

    def get_all_materials(self):
        materials = list(self.get_collection('MaterialeDidattico').find())
        print(f"Materiali nel database: {materials}")
        return materials

    def get_material(self, query):
        return self.collection.find_one(query)

    def get_material_by_id(self, material_id):
        return self.collection.find_one({'_id': material_id})

    def update_material(self, materiale_id, updated_data):
        self.get_collection('MaterialeDidattico').update_one({'_id': materiale_id}, {'$set': updated_data})