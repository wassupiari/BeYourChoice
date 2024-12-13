import pytest
from flask import Flask, session, url_for
from unittest.mock import MagicMock
from app.models.quizModel import QuizModel
from app.controllers.quizControl import quiz_blueprint
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
    app.secret_key = "test_secret_key"
    app.config['SERVER_NAME'] = 'localhost:5000'  # Aggiungi la configurazione per SERVER_NAME
    app.config['APPLICATION_ROOT'] = '/'  # Aggiungi la configurazione per l'app root
    app.config['PREFERRED_URL_SCHEME'] = 'http'  # Configura il tipo di schema URL

    # Registriamo il blueprint per il quiz
    app.register_blueprint(quiz_blueprint, url_prefix="/quiz")
    app.testing = True

    # Stampa le route disponibili per il debug
    print("Routes disponibili:")
    for rule in app.url_map.iter_rules():
        print(f"Rule: {rule}, Methods: {rule.methods}")

    with app.test_client() as client:
        with app.app_context():
            yield client


# Fixture per il mock di QuizModel con connessione al database
@pytest.fixture(scope='function')
def quiz_model(mongo_client):
    quiz_model = QuizModel()
    quiz_model.db_manager.db = mongo_client.db  # Imposta il db di test nel modello
    yield quiz_model

# Parametri per il test
@pytest.mark.parametrize("test_id, button_value, expected_success", [
        ("TCS_GGDQ_2_1", None, False),  # Il pulsante non viene premuto
        ("TCS_GGDQ_2_2", True, True),   # Il pulsante viene premuto correttamente
    ])
def test_esecuzione_quiz(test_client, quiz_model, test_id, button_value, expected_success):
    """
    Test per l'esecuzione del quiz basato sui casi di prova TCS_GGDQ_2_1 e TCS_GGDQ_2_2.
    """
    # Simulazione dei dati di sessione dello studente
    session_data = {"cf": "BZZMMM29S01F549D", "email": "augusto@studenti.it", "id_classe": 10448}

    with test_client.session_transaction() as sess:
        sess.update(session_data)  # Aggiorna la sessione con i dati simulati

    if session_data:
        print(f"[DEBUG] Sessione impostata correttamente con i dati: {session_data}")
    else:
        print("[ERROR] Dati di sessione mancanti!")

    # Simula la richiesta POST per avviare il quiz con il valore del pulsante
    response = test_client.post('/quiz/6', json={"button": button_value or "Nessun valore inviato"})

    # Log della risposta per debug
    print(f"[DEBUG] Test ID: {test_id}")
    print(f"[DEBUG] Response Status Code: {response.status_code}")
    print(f"[DEBUG] Response Headers: {response.headers}")
    print(f"[DEBUG] Response Data: {response.data.decode('utf-8')}")
    print(f"[DEBUG] Response JSON: {response.json if response.is_json else 'Nessun JSON restituito'}")

    # Validazione del successo atteso
    actual_success = response.status_code == 200
    assert actual_success == expected_success, (
        f"[ERROR] Test {test_id} fallito! Atteso: {expected_success}, Ottenuto: {actual_success}"
    )

    # Aggiungiamo il test per visualizzare il quiz, verificando che la rotta venga chiamata correttamente
    quiz_id = 6  # Definisci un quiz_id valido per il test
    url = url_for('quiz.visualizza_quiz', quiz_id=quiz_id)  # Usa url_for per ottenere l'URL dinamico

    # Verifica che l'URL venga costruito correttamente
    print(f"[DEBUG] URL generato per visualizzare il quiz: {url}")

    # Simula la richiesta GET per visualizzare il quiz
    response = test_client.get(url)

    # Log della risposta per debug
    print(f"[DEBUG] Response Status Code per visualizzare il quiz: {response.status_code}")
    print(f"[DEBUG] Response Data: {response.data.decode('utf-8')}")

    # Verifica che la risposta sia quella che ti aspetti
    assert response.status_code == 200, f"[ERROR] Test visualizza_quiz fallito! Status Code: {response.status_code}"
