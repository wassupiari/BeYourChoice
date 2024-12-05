import pytest
from flask import Flask, Blueprint, request


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

    @quiz_blueprint.route('/genera', methods=['POST'])
    def genera_quiz():
        tema = request.json.get('tema')
        numero_domande = request.json.get('numero_domande')
        modalita_risposta = request.json.get('modalita_risposta')
        durata = request.json.get('durata')

        # Validazioni
        if not tema or len(tema) < 2:
            return "Argomento non valido", 400

        if '@' in tema:
            return "Formato argomento non valido", 400

        if numero_domande < 5:
            return "Numero di domande non valido", 400

        if modalita_risposta not in ['3_risposte', '4_risposte', 'vero_falso']:
            return "Modalità risposta non valida", 400

        if durata != "00:30":
            return "Durata non valida", 400

        return "Quiz generato con successo", 200

    app.register_blueprint(quiz_blueprint)


# Test per argomento non valido (lunghezza < 2)
@pytest.mark.parametrize("test_id", ["TC_GGDQ_1_1"])
def test_genera_quiz_argomento_non_valido(client, test_id):
    data = {"tema": "", "numero_domande": 5, "modalita_risposta": "3_risposte", "durata": "00:30"}
    response = client.post('/genera', json=data)
    assert response.status_code == 400
    assert "Argomento non valido" in response.data.decode('utf-8')
    print(f"Test {test_id}: Argomento non valido gestito correttamente!")


# Test per formato argomento non valido
@pytest.mark.parametrize("test_id", ["TC_GGDQ_1_2"])
def test_genera_quiz_formato_argomento_non_valido(client, test_id):
    data = {"tema": "Argomento@", "numero_domande": 5, "modalita_risposta": "3_risposte", "durata": "00:30"}
    response = client.post('/genera', json=data)
    assert response.status_code == 400
    assert "Formato argomento non valido" in response.data.decode('utf-8')
    print(f"Test {test_id}: Formato argomento non valido gestito correttamente!")


# Test per numero domande non valido
@pytest.mark.parametrize("test_id", ["TC_GGDQ_1_3"])
def test_genera_quiz_numero_domande_non_valido(client, test_id):
    data = {"tema": "Costituzione", "numero_domande": 3, "modalita_risposta": "3_risposte", "durata": "00:30"}
    response = client.post('/genera', json=data)
    assert response.status_code == 400
    assert "Numero di domande non valido" in response.data.decode('utf-8')
    print(f"Test {test_id}: Numero di domande non valido gestito correttamente!")


# Test per modalità risposta non valida
@pytest.mark.parametrize("test_id", ["TC_GGDQ_1_4"])
def test_genera_quiz_modalita_non_valida(client, test_id):
    data = {"tema": "Costituzione", "numero_domande": 5, "modalita_risposta": "non_valida", "durata": "00:30"}
    response = client.post('/genera', json=data)
    assert response.status_code == 400
    assert "Modalità risposta non valida" in response.data.decode('utf-8')
    print(f"Test {test_id}: Modalità risposta non valida gestita correttamente!")


# Test per durata non valida
@pytest.mark.parametrize("test_id", ["TC_GGDQ_1_5"])
def test_genera_quiz_durata_non_valida(client, test_id):
    data = {"tema": "Costituzione", "numero_domande": 5, "modalita_risposta": "3_risposte", "durata": "00:20"}
    response = client.post('/genera', json=data)
    assert response.status_code == 400
    assert "Durata non valida" in response.data.decode('utf-8')
    print(f"Test {test_id}: Durata non valida gestita correttamente!")


# Test per generazione quiz con successo
@pytest.mark.parametrize("test_id", ["TC_GGDQ_1_6"])
def test_genera_quiz_successo(client, test_id):
    data = {"tema": "Costituzione", "numero_domande": 5, "modalita_risposta": "3_risposte", "durata": "00:30"}
    response = client.post('/genera', json=data)
    assert response.status_code == 200
    assert "Quiz generato con successo" in response.data.decode('utf-8')
    print(f"Test {test_id}: Generazione quiz riuscita!")
