from pymongo import MongoClient
from databaseManager import DatabaseManager  # Importa la classe DatabaseManager
import bcrypt

class DocenteModel:
    def __init__(self):
        # Utilizza la connessione esistente al database
        self.db_manager = DatabaseManager()

    def aggiungi_docente(self, docente_dict):
        """
        Aggiunge un nuovo docente al database.
        """
        # Cifra la password del docente
        docente_collection = self.db_manager.get_collection("Docente")
        docente_dict['password'] = bcrypt.hashpw(docente_dict['password'].encode('utf-8'), bcrypt.gensalt())
        docente_collection.insert_one(docente_dict)

    def trova_docente(self, email):
        """
        Trova un docente in base all'email.
        """
        docente_collection = self.db_manager.get_collection("Docente")
        return docente_collection.find_one({"email": email})

    def trova_docente_by_codice_univoc(self, codice_univoc):
        """
        Trova un docente in base al codice univoco.
        """
        docente_collection = self.db_manager.get_collection("Docente")
        return docente_collection.find_one({"codice_univoc": codice_univoc})

    def aggiorna_docente(self, docente_dict, codice_univoc):
        """
        Aggiorna le informazioni di un docente.
        """
        self.collection.update_one({"codice_univoc": codice_univoc}, {"$set": docente_dict})

    def elimina_docente(self, codice_univoc):
        """
        Elimina un docente dal database.
        """
        docente_collection = self.db_manager.get_collection("Docente")
        docente_collection.delete_one({"codice_univoc": codice_univoc})

    def get_codice_univoco_by_email(self, email):
        """
        Ottiene il codice univoco di un docente a partire dall'email.
        """
        docente = self.trova_docente(email)  # Trova il docente tramite email
        if docente:
            return docente.get("codice_univoco")  # Restituisce il codice univoco se presente
        return None  # Restituisce None se il docente non esiste o non ha un codice univoco