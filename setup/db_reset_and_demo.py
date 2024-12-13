from databaseManager import DatabaseManager
import bcrypt

# Connessione al database
DB_NAME = "BeYourChoice"
db_manager = DatabaseManager()
db = db_manager.get_collection

# Funzione per hash della password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# Funzione per verificare la password
def verifica_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Script per svuotare le collection
def svuota_collection():
    try:
        # Svuota le collection "Docente", "Studente" e "ClasseVirtuale"
        db("Docente").delete_many({})
        db("Studente").delete_many({})
        db("ClasseVirtuale").delete_many({})
        db("Dashboard").delete_many({})
        db("Domanda").delete_many({})
        db("RisultatoQuiz").delete_many({})
        db("ScenarioVirtuale").delete_many({})
        db("MaterialeDidattico").delete_many({})
        db("PunteggioScenario").delete_many({})
        db("Quiz").delete_many({})
        print("Le Collection del db sono state svuotate con successo!")
    except Exception as e:
        print(f"Errore durante la pulizia delle collection: {e}")

# Script per ripopolare il database
def ripopola_database():
    try:
        # Inserisce il docente
        docente = {
            "nome": "Giovanni'",
            "cognome": "Verdi",
            "email": "giovanni.verdi@docente.com",
            "password": hash_password("Rocco03@"),  # Hash della password come byte
            "codice_univoco": 123456,
            "id_classe": 200,
            "sda": "Liceo Classico Dante Alighieri",
        }
        docente_id = db("Docente").insert_one(docente).inserted_id
        print("Docente inserito con successo!")

        # Inserisce gli studenti
        studenti = [
            {
                "nome": "Luca",
                "cognome": "Rossi",
                "email": "luca.rossi@studenti.it",
                "cf": "RSSLCU99A01H501X",
                "password": hash_password("Rocco03@"),  # Hash della password come byte
                "sda": "Liceo Classico Dante Alighieri",
                "data_nascita": "1999-01-01",
                "id_classe": 20001,
                "ruolo": "studente",
            },
            {
                "nome": "Martina",
                "cognome": "Bianchi",
                "email": "martina.bianchi@studenti.it",
                "cf": "BNCMRT02B15F205Z",
                "password": hash_password("Rocco03@"),  # Hash della password come byte
                "sda": "Liceo Scientifico Galileo Galilei",
                "data_nascita": "2002-02-15",
                "id_classe": 20001,
                "ruolo": "studente",
            },
        ]
        studenti_ids = db("Studente").insert_many(studenti).inserted_ids
        print("Studenti inseriti con successo!")

        # Crea una nuova classe virtuale per il docente inserito
        classe_virtuale = {
            "id_classe": 20001,  # ID incrementale
            "nome_classe": "Classe 1A",
            "descrizione": "Classe prima A per l'anno accademico.",
            "id_docente": docente["codice_univoco"],
            "studenti": [str(id) for id in studenti_ids],
        }
        db("ClasseVirtuale").insert_one(classe_virtuale)
        print("Classe virtuale creata e studenti associati!")

    except Exception as e:
        print(f"Errore durante il ripopolamento del database: {e}")

# Verifica di accesso usando la password
def verifica_accesso(email, password):
    try:
        studente = db("Studente").find_one({"email": email})
        if not studente:
            print("Studente non trovato!")
            return False

        # Verifica la password usando bcrypt
        if verifica_password(password, studente["password"]):
            print("Accesso consentito!")
            return True
        else:
            print("Password errata!")
            return False
    except Exception as e:
        print(f"Errore durante la verifica dell'accesso: {e}")
        return False

# Esecuzione degli script
if __name__ == "__main__":
    print("Svuotamento delle collection...")
    svuota_collection()
    print("Ripopolamento del database...")
    ripopola_database()
