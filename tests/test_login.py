import bcrypt
import pytest
from app.models.studenteModel import StudenteModel
from app.models.docenteModel import DocenteModel
from databaseManager import DatabaseManager  # Importa la classe DatabaseManager

# Fixture per la connessione al database MongoDB usando DatabaseManager
@pytest.fixture(scope='module')
def mongo_client():
    # Crea un'istanza del singleton DatabaseManager e configura la connessione
    db_manager = DatabaseManager(
        uri="mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority&appName=BeYourChoice"
    )
    # Verifica la connessione al database
    assert db_manager.db is not None, "Connessione al database fallita!"  # Verifica che il db sia connesso
    yield db_manager  # Restituisce il database manager per i test
    db_manager.close_connection()  # Chiude la connessione dopo i test


@pytest.fixture(scope='function')
def studente_model(mongo_client):
    studente_model = StudenteModel()
    studente_model.db_manager.db = mongo_client.db  # Imposta il db di test nel modello
    yield studente_model


@pytest.fixture(scope='function')
def docente_model(mongo_client):
    docente_model = DocenteModel()
    docente_model.db_manager.db = mongo_client.db  # Imposta il db di test nel modello
    yield docente_model


# Test di login per lo studente (senza inserimento, solo ricerca)
def test_login_studente_with_db(studente_model, mongo_client):
    # Eseguiamo la ricerca dello studente nel database
    found_studente = studente_model.trova_studente('augusto@studenti.it')
    assert found_studente is not None  # Verifica che lo studente sia stato trovato
    assert found_studente['email'] == 'augusto@studenti.it'  # Verifica che l'email sia corretta

    # Verifica che la password sia corretta
    assert bcrypt.checkpw('Augusto9@'.encode('utf-8'), found_studente['password'])  # Verifica la password cifrata


# Test di login per il docente (senza inserimento, solo ricerca)
def test_login_docente_with_db(docente_model, mongo_client):
    # Eseguiamo la ricerca del docente nel database
    found_docente = docente_model.trova_docente('roccocione@gmail.com')
    assert found_docente is not None  # Verifica che il docente sia stato trovato
    assert found_docente['email'] == 'roccocione@gmail.com'  # Verifica che l'email sia corretta

    # Verifica che la password sia corretta
    assert bcrypt.checkpw('Roccocione03@'.encode('utf-8'), found_docente['password'])  # Verifica la password cifrata
