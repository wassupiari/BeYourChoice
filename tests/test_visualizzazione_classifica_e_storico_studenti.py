import pytest
from flask import Flask, Blueprint, request, jsonify


# Funzione per creare l'app Flask
def create_app():
    app = Flask(__name__)
    app.secret_key = "test_secret"
    initialize_monitoraggio_blueprint(app)
    return app


# Fixture per il client di test
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


# Inizializzazione del blueprint Monitoraggio
def initialize_monitoraggio_blueprint(app):
    monitoraggio_blueprint = Blueprint('monitoraggio', __name__)

    # Mock database
    classifica_mock = {
        101: [
            {"Studente": "Mario Rossi", "Punti": 120},
            {"Studente": "Luigi Bianchi", "Punti": 110}
        ]
    }

    storico_mock = {
        "RSSMRA80A01H501Z": [
            {"Attivita": "Quiz Matematica", "Punti": 30, "Data": "2024-11-28"},
            {"Attivita": "Esercizi Italiano", "Punti": 20, "Data": "2024-11-29"}
        ],
        "RSSFNC90B02C501X": [
            {"Attivita": "Scenari Storia", "Punti": 40, "Data": "2024-11-27"}
        ]
    }

    # Route per visualizzare la classifica
    @monitoraggio_blueprint.route('/classifica/<int:ID_Classe>', methods=['GET'])
    def classifica(ID_Classe):
        classifica = classifica_mock.get(ID_Classe, [])
        if not classifica:
            return "Classe non trovata", 404
        return jsonify({"Classifica": classifica}), 200

    # Route per visualizzare lo storico
    @monitoraggio_blueprint.route('/storico/<string:CF_Studente>', methods=['GET'])
    def storico(CF_Studente):
        storico = storico_mock.get(CF_Studente, [])
        if not storico:
            return "Studente non trovato", 404
        return jsonify({"Storico": storico}), 200

    # Route per aggiungere un nuovo quiz
    @monitoraggio_blueprint.route('/aggiungi-quiz', methods=['POST'])
    def aggiungi_quiz():
        quiz_data = request.json
        for studente in storico_mock:
            storico_mock[studente].append({
                "Attivita": quiz_data["Attivita"],
                "Punti": quiz_data["Punti"],
                "Data": quiz_data["Data"]
            })
        for studente in classifica_mock[quiz_data["ID_Classe"]]:
            studente["Punti"] += quiz_data["Punti"]
        return "Quiz aggiunto con successo", 200

    app.register_blueprint(monitoraggio_blueprint)


# Test monitoraggio classifiche e storico
def test_monitoraggio_classifiche_e_storico(client):
    # Prima del nuovo quiz
    response_classifica = client.get('/classifica/101')
    assert response_classifica.status_code == 200
    classifica_prima = response_classifica.json["Classifica"]
    assert len(classifica_prima) == 2
    assert classifica_prima[0]["Punti"] == 120
    assert classifica_prima[1]["Punti"] == 110
    print("Classifica prima dell'aggiunta:", classifica_prima)

    response_storico = client.get('/storico/RSSMRA80A01H501Z')
    assert response_storico.status_code == 200
    storico_prima = response_storico.json["Storico"]
    assert len(storico_prima) == 2
    print("Storico prima dell'aggiunta:", storico_prima)

    # Aggiungi un nuovo quiz
    nuovo_quiz = {
        "ID_Classe": 101,
        "Attivita": "Quiz Scienze",
        "Punti": 10,
        "Data": "2024-12-01"
    }
    response_aggiungi = client.post('/aggiungi-quiz', json=nuovo_quiz)
    assert response_aggiungi.status_code == 200
    assert "Quiz aggiunto con successo" in response_aggiungi.data.decode('utf-8')
    print("Nuovo quiz aggiunto con successo")

    # Dopo il nuovo quiz
    response_classifica = client.get('/classifica/101')
    assert response_classifica.status_code == 200
    classifica_dopo = response_classifica.json["Classifica"]
    assert len(classifica_dopo) == 2
    assert classifica_dopo[0]["Punti"] == 130  # Punti aggiornati
    assert classifica_dopo[1]["Punti"] == 120
    print("Classifica dopo l'aggiunta:", classifica_dopo)

    response_storico = client.get('/storico/RSSMRA80A01H501Z')
    assert response_storico.status_code == 200
    storico_dopo = response_storico.json["Storico"]
    assert len(storico_dopo) == 3
    assert storico_dopo[-1]["Attivita"] == "Quiz Scienze"
    print("Storico dopo l'aggiunta:", storico_dopo)
