import pytest
from flask import Flask, Blueprint, request, jsonify
from unittest.mock import MagicMock


# Funzione per creare l'app Flask
def create_app():
    app = Flask(__name__)
    app.secret_key = "test_secret"
    initialize_quiz_blueprint(app)
    return app


# Fixture per il client di test
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


# Inizializzazione del blueprint Quiz
def initialize_quiz_blueprint(app):
    quiz_blueprint = Blueprint('quiz', __name__)

    # Simula la creazione del quiz
    @quiz_blueprint.route('/genera', methods=['POST'])
    def genera_quiz():
        tema = request.json.get('tema')
        numero_domande = int(request.json.get('numero_domande'))
        modalita_risposta = request.json.get('modalita_risposta')

        if not tema or numero_domande <= 0 or modalita_risposta not in ['3_risposte', '4_risposte']:
            return "Parametri non validi", 400

        return jsonify({"message": "Quiz generato con successo", "quiz_id": 1}), 200

    # Simula il salvataggio dei risultati del quiz
    @quiz_blueprint.route('/salva-risultato', methods=['POST'])
    def salva_risultato():
        data = request.json
        if not data.get('CF_Studente') or not data.get('Punteggio_Quiz'):
            return "Dati mancanti", 400

        # Simuliamo il salvataggio del risultato
        return jsonify({"message": "Risultato salvato correttamente!"}), 200

    # Simula la visualizzazione dei risultati per un quiz
    @quiz_blueprint.route('/quiz/<int:quiz_id>/risultati', methods=['GET'])
    def visualizza_risultati_quiz(quiz_id):
        # Mock per la visualizzazione dei risultati
        risultati = [
            {"CF_Studente": "CF12345", "Nome": "Mario", "Cognome": "Rossi", "Punteggio_Quiz": 80},
            {"CF_Studente": "CF67890", "Nome": "Luigi", "Cognome": "Bianchi", "Punteggio_Quiz": 70}
        ]
        return jsonify(risultati), 200

    app.register_blueprint(quiz_blueprint)


# Test 1: Creazione quiz con parametri validi
@pytest.mark.parametrize("test_id", ["TC_GGDQ_1_1"])
def test_creazione_quiz_successo(client, test_id):
    data = {"tema": "Pollo", "numero_domande": 5, "modalita_risposta": "3_risposte", "durata": "00:30"}
    response = client.post('/genera', json=data)
    assert response.status_code == 200
    assert "Quiz generato con successo" in response.json['message']
    print(f"Test {test_id}: Creazione quiz riuscita!")


# Test 2: Salvataggio dei risultati del quiz
@pytest.mark.parametrize("test_id", ["TC_GGDQ_2_1"])
def test_salvataggio_risultati_quiz(client, test_id):
    data = {"CF_Studente": "CF12345", "Punteggio_Quiz": 80, "Risposte": ["A", "B", "C"]}
    response = client.post('/salva-risultato', json=data)
    assert response.status_code == 200
    assert "Risultato salvato correttamente!" in response.json['message']
    print(f"Test {test_id}: Salvataggio risultato quiz riuscito!")


# Test 3: Visualizzazione dei risultati del quiz
@pytest.mark.parametrize("test_id", ["TC_GGDQ_3_1"])
def test_visualizzazione_risultati_quiz(client, test_id):
    quiz_id = 1  # L'ID del quiz per il quale vogliamo vedere i risultati
    response = client.get(f'/quiz/{quiz_id}/risultati')
    assert response.status_code == 200
    assert len(response.json) > 0  # Verifica che ci siano dei risultati
    print(f"Test {test_id}: Risultati del quiz visualizzati correttamente!")

