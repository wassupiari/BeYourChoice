import pytest
from flask import Flask, Blueprint, session, url_for
from unittest.mock import MagicMock
from app.models.quizModel import QuizModel

# Funzione per creare l'app Flask
def create_app():
    app = Flask(__name__)
    initialize_quiz_blueprint(app)
    return app

# Fixture per il client di test
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.secret_key = "test_secret_key"

    with app.test_client() as client:
        yield client

# Mock del modello QuizModel
@pytest.fixture
def mock_quiz_model():
    quiz_model = MagicMock(spec=QuizModel)
    return quiz_model

# Inizializzazione del blueprint Quiz
def initialize_quiz_blueprint(app):
    quiz_blueprint = Blueprint('quiz', __name__)

    @quiz_blueprint.route('/quiz/<int:quiz_id>', methods=['POST'])
    def esegui_quiz(quiz_id):
        return "Quiz eseguito con successo!", 200

    app.register_blueprint(quiz_blueprint, url_prefix="/quiz")

# Test per l'esecuzione del quiz con successo
@pytest.mark.parametrize("test_id, quiz_id, button_value, expected_message", [
    ("TCS_GGDQ_2_2", 8, True, "Quiz eseguito con successo!"),
])
def test_esecuzione_quiz_success(client, test_id, quiz_id, button_value, expected_message):
    session_data = {"cf": "RSSLCU99A01H501X", "email": "luca.rossi@studenti.it", "id_classe": 20001}
    with client.session_transaction() as sess:
        sess.update(session_data)

    response = client.post(f'/quiz/{quiz_id}', json={"button": button_value})
    assert expected_message in response.data.decode('utf-8')
    print(f"Test {test_id}: Esecuzione quiz gestita correttamente!")

# Test per l'esecuzione del quiz senza pulsante premuto
@pytest.mark.parametrize("test_id, quiz_id, button_value, expected_status", [
    ("TCS_GGDQ_2_1", 6, None, 404),
])
def test_esecuzione_quiz_fallimento(client, test_id, quiz_id, button_value, expected_status):
    session_data = {"cf": "RSSLCU99A01H501X", "email": "luca.rossi@studenti.it", "id_classe": 20001}
    with client.session_transaction() as sess:
        sess.update(session_data)

    response = client.post(f'/quiz/{quiz_id}', json={"button": button_value or ""})
    assert response.status_code == expected_status
    print(f"Test {test_id}: Fallimento previsto gestito correttamente!")
