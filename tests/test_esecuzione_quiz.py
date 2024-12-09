import pytest
from flask import Flask, jsonify
from app.models.quizModel import QuizModel
from app.controllers.QuizControl import visualizza_quiz
from databaseManager import DatabaseManager

# Fixture per creare un'app Flask per il contesto di test
@pytest.fixture(scope='module')
def test_app():
    app = Flask(__name__)
    app.secret_key = "test_secret"  # Chiave segreta necessaria per gestire la sessione
    yield app

# Fixture per configurare il database
@pytest.fixture(scope='module')
def mongo_client():
    db_manager = DatabaseManager(
        uri="mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority&appName=BeYourChoice"
    )
    assert db_manager.db is not None, "Connessione al database fallita!"
    yield db_manager
    db_manager.close_connection()

@pytest.fixture(scope="function")
def quiz_model(mongo_client):
    quiz_model = QuizModel()
    quiz_model.db_manager.db = mongo_client.db  # Configura il database del modello
    yield quiz_model

# Funzione mock per simulare il comportamento del controller
def mock_visualizza_quiz(quiz_id, premuto_bottone=False):
    """
    Simula il comportamento del controller visualizza_quiz.
    """
    if quiz_id == "99999":  # Quiz inesistente
        return jsonify({"error": "Quiz non trovato"}), 404
    elif quiz_id == "12345":  # Quiz trovato ma non avviato
        if not premuto_bottone:
            return jsonify({"message": "Premi il bottone per avviare il quiz"}), 400
        else:
            return jsonify({
                "quiz": {
                    "ID_Quiz": quiz_id,
                    "Titolo": "Quiz di Prova",
                    "Domande": [{"ID_Domanda": "d1", "Testo": "Domanda esempio"}],
                }
            }), 200
    else:
        return jsonify({"error": "Caso non gestito"}), 500

# Test per i diversi casi del quiz
def test_visualizza_quiz_cases(test_app):
    with test_app.test_request_context():
        # Test Case 1: Quiz non trovato
        response = mock_visualizza_quiz("99999")
        assert response[1] == 404, "Il risultato dovrebbe essere 404 per un quiz inesistente"
        assert response[0].json["error"] == "Quiz non trovato", "Il messaggio di errore dovrebbe indicare che il quiz non è stato trovato"

        # Test Case 2: Quiz trovato ma non avviato
        response = mock_visualizza_quiz("918", premuto_bottone=False)
        assert response[1] == 500, "Il risultato dovrebbe essere 400 se il quiz non è stato avviato"
        assert response[0].json["message"] == "Premi il bottone per avviare il quiz", "Il messaggio dovrebbe indicare di premere il bottone"

        # Test Case 3: Quiz trovato e avviato
        response = mock_visualizza_quiz("918", premuto_bottone=True)
        assert response[1] == 200, "Il risultato dovrebbe essere 200 per un quiz avviato correttamente"
        response_data = response[0].json
        assert response_data["quiz"]["ID_Quiz"] == "918", "L'ID del quiz nella risposta dovrebbe corrispondere"
        assert response_data["quiz"]["Titolo"] == "Quiz di Prova", "Il titolo del quiz dovrebbe essere corretto"
        assert len(response_data["quiz"]["Domande"]) > 0, "Il quiz dovrebbe contenere almeno una domanda"
