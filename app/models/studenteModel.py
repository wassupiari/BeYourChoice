from databaseManager import DatabaseManager  # Importa la classe DatabaseManager
import bcrypt


class StudenteModel:
    def __init__(self):
        # Utilizza la connessione esistente al database
        self.db_manager = DatabaseManager()

    def aggiungi_studente(self, studente_dict):
        studente_collection = self.db_manager.get_collection("Studente")
        # Cifra la password prima di salvarla
        hash = bcrypt.hashpw(studente_dict['password'].encode('utf-8'), bcrypt.gensalt())
        studente_dict['password'] = hash
        studente_collection.insert_one(studente_dict)
        print("Studente aggiunto con successo!")

    def trova_studente(self, email):
        # Cerca uno studente per email
        studente_collection = self.db_manager.get_collection("Studente")
        return studente_collection.find_one({"email": email})