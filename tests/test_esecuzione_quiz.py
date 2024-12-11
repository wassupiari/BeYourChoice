import re
import pytest
from flask import Flask, session
from app.models.quizModel import QuizModel
from app.controllers.quizControl import quiz_blueprint
from unittest.mock import MagicMock
from databaseManager import DatabaseManager

# Fixture per la connessione al database MongoDB usando DatabaseManager
@pytest.fixture(scope='module')
def mongo_client():
    db_manager = DatabaseManager(
        uri="mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority&appName=BeYourChoice"
    )
    assert db_manager.db is not None, "Connessione al database fallita!"
    yield db_manager
    db_manager.close_connection()

# Fixture per la configurazione del client Flask
@pytest.fixture(scope='module')
def test_client():
    app = Flask(__name__)
    app.secret_key = "test_secret_key"  # Necessario per gestire la sessione
    app.register_blueprint(quiz_blueprint, url_prefix="/quiz")
    app.testing = True

    with app.test_client() as client:
        with app.app_context():
            yield client

# Fixture per il mock di QuizModel con connessione al database
@pytest.fixture(scope='function')
def quiz_model(mongo_client):
    quiz_model = QuizModel()
    quiz_model.db_manager.db = mongo_client.db  # Imposta il db di test nel modello
    yield quiz_model

# Test combinazioni per l'esecuzione del quiz
@pytest.mark.parametrize("test_id, id_quiz, session_data, expected_success", [
    ("TC_QZ_1_1", 6,  {"id_classe": "10448", "cf": "BZZMMM29S01F549D"}, True),  # Test se il pulsante viene premuto correttamente
])
def test_combinazioni_esecuzione_quiz(test_client, quiz_model, test_id, id_quiz, session_data, expected_success):
    """
    Test per le combinazioni di esecuzione quiz, basati sui casi forniti nel documento.
    Ogni caso è denominato con il relativo ID del test case (es. TC_QZ_1_1).
    """
    with test_client.session_transaction() as sess:
        sess.update(session_data)  # Simula i dati di sessione

    # Simula la richiesta POST per avviare il quiz
    response = test_client.post("./quiz/6", json={"id_quiz": id_quiz})

    # Output per debug
    print(f"Test ID: {test_id}")
    print(f"Status Code: {response.status_code}, Expected Success: {expected_success}")

    # Validazione del successo atteso
    actual_success = response.status_code == 200
    print(f"Actual Success: {actual_success}")
    assert actual_success == expected_success, (
        f"{test_id}: Esito inatteso! Atteso: {expected_success}, Ottenuto: {actual_success}"
    )

    # Debug finale
    print(f"{test_id}: Test concluso con successo atteso={expected_success}")
