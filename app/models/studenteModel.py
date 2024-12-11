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
        print(studente_collection.find_one({"email": email}))
        return studente_collection.find_one({"email": email})

    def trova_cf_per_email(self, email):
        # Cerca lo studente tramite email e restituisce il codice fiscale
        studente = self.trova_studente(
            email)  # Usa la function che hai già definito per trovare lo studente tramite email
        if studente:
            return studente.get("cf")  # Restituisce il codice fiscale (cf) se esiste
        return None  # Se lo studente non viene trovato o non ha il codice fiscale