import re

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

# Test combinazioni per il login studente
@pytest.mark.parametrize("test_id, email, password, expected_success", [
    ("TC_GA_1_1", "a@b.c", "Augusto9@", False),  # LE1: Errore
    ("TC_GA_1_2", "test@", "Augusto9@", False),  # LE2, FE1: Errore
    ("TC_GA_1_3", "test@student.com", "Augusto9@", False),  # LE2, FE2, EE1: Errore
    ("TC_GA_1_4", "augusto@studenti.it", "Pass1@", False),  # LE2, FE2, EE2, LP1: Errore
    ("TC_GA_1_5", "augusto@studenti.it", "Augusto9", False),  # LE2, FE2, EE2, LP2, FP1: Errore
    ("TC_GA_1_6", "augusto@studenti.it", "Augusto9!", False),  # LE2, FE2, EE2, LP2, FP2, EP1: Errore
    ("TC_GA_1_7", "augusto@studenti.it", "Augusto9@", True),  # LE2, FE2, EE2, LP2, FP2, EP2: Successo
])
def test_combinazioni_login_studente(studente_model, mongo_client, test_id, email, password, expected_success):
    """
    Test per le combinazioni di login studente, basati sui casi forniti nel documento.
    Ogni caso è denominato con il relativo ID del test case (es. TC_GA_1_1).
    """
    # Flag delle proprietà
    le_ok = len(email) >= 6
    fe_ok = bool(re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$", email))
    found_studente = studente_model.trova_studente(email)
    ee_ok = found_studente is not None
    lp_ok = len(password) > 7  # Simula LP
    fp_ok = bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,20}$",password))  # Simula FP (password corretta)
    ep_ok = found_studente is not None and found_studente is not None and bcrypt.checkpw(password.encode('utf-8'), found_studente['password'])  # Simula FP (password corretta)

    # Output per debug
    print(f"Test ID: {test_id}")
    print(f"LE_OK: {le_ok}, FE_OK: {fe_ok}, EE_OK: {ee_ok}, LP_OK: {lp_ok}, FP_OK: {fp_ok}, EP_OK: {ep_ok}")

    # Validazione del successo atteso
    actual_success = le_ok and fe_ok and ee_ok and lp_ok and fp_ok and ep_ok
    assert actual_success == expected_success, f"{test_id}: Esito inatteso! Atteso: {expected_success}, Ottenuto: {actual_success}"

    # Debug finale
    print(f"{test_id}: Test concluso con successo atteso={expected_success}")

# Test combinazioni per il login docente
@pytest.mark.parametrize("test_id, emaildoc, passworddoc, expected_success", [
    ("TC_GA_1_1", "a@b.c", "Roccocione03@", False),  # LE1: Errore
    ("TC_GA_1_2", "test@", "Roccocione03@", False),  # LE2, FE1: Errore
    ("TC_GA_1_3", "test@docent.com", "Roccocione03@", False),  # LE2, FE2, EE1: Errore
    ("TC_GA_1_4", "roccocione@gmail.com", "Rocc1@", False),  # LE2, FE2, EE2, LP1: Errore
    ("TC_GA_1_5", "roccocione@gmail.com", "Roccocione03", False),  # LE2, FE2, EE2, LP2, FP1: Errore
    ("TC_GA_1_6", "roccocione@gmail.com", "Roccocione03!", False),  # LE2, FE2, EE2, LP2, FP2, EP1: Errore
    ("TC_GA_1_7", "roccocione@gmail.com", "Roccocione03@", True),  # LE2, FE2, EE2, LP2, FP2, EP2: Successo
])

# Test di login per il docente (senza inserimento, solo ricerca)
def test_login_docente_with_db(docente_model, mongo_client, test_id, emaildoc, passworddoc, expected_success):
    # Eseguiamo la ricerca del docente nel database
    """
        Test per le combinazioni di login studente, basati sui casi forniti nel documento.
        Ogni caso è denominato con il relativo ID del test case (es. TC_GA_1_1).
        """
    # Flag delle proprietà
    le_ok = len(emaildoc) >= 6
    fe_ok = bool(re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$", emaildoc))
    found_docente = docente_model.trova_docente(emaildoc)
    ee_ok = found_docente is not None
    lp_ok = len(passworddoc) > 7  # Simula LP
    fp_ok = bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,20}$",
                          passworddoc))  # Simula FP (password corretta)
    ep_ok = found_docente is not None and found_docente is not None and bcrypt.checkpw(passworddoc.encode('utf-8'),
                                                                                         found_docente[
                                                                                             'password'])  # Simula FP (password corretta)

    # Output per debug
    print(f"Test ID: {test_id}")
    print(f"LE_OK: {le_ok}, FE_OK: {fe_ok}, EE_OK: {ee_ok}, LP_OK: {lp_ok}, FP_OK: {fp_ok}, EP_OK: {ep_ok}")

    # Validazione del successo atteso
    actual_success = le_ok and fe_ok and ee_ok and lp_ok and fp_ok and ep_ok
    assert actual_success == expected_success, f"{test_id}: Esito inatteso! Atteso: {expected_success}, Ottenuto: {actual_success}"

    # Debug finale
    print(f"{test_id}: Test concluso con successo atteso={expected_success}")
