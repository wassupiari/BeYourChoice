import pytest
from flask import Flask, Blueprint, request
from unittest.mock import MagicMock

# Funzione per creare l'app Flask
def create_app():
    app = Flask(__name__)
    app.secret_key = "test_secret"
    initialize_classe_blueprint(app)
    return app

# Fixture per il client di test
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

# Inizializzazione del blueprint Classe Virtuale
def initialize_classe_blueprint(app):
    classe_blueprint = Blueprint('classe', __name__)

    @classe_blueprint.route('/creazione-classe', methods=['POST'])
    def creazione_classe():
        nome_classe = request.json.get('NomeClasse')
        descrizione = request.json.get('Descrizione')
        id_docente = request.json.get('ID_Docente')

        # Validazioni
        if not nome_classe or len(nome_classe) < 2 or len(nome_classe) > 20:
            return "Lunghezza del nome della classe virtuale non corretta.", 400

        if not descrizione or len(descrizione) < 2 or len(descrizione) > 255:
            return "Lunghezza della descrizione della classe virtuale non corretta.", 400

        if not id_docente or len(id_docente) != 8:
            return "ID docente non valido.", 400

        return "Classe virtuale creata con successo", 200

    app.register_blueprint(classe_blueprint)

import pytest
from flask import Flask, Blueprint, request
import re

# Funzione per creare l'app Flask
def create_app():
    app = Flask(__name__)
    app.secret_key = "test_secret"
    initialize_classe_blueprint(app)
    return app

# Fixture per il client di test
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

# Inizializzazione del blueprint Classe Virtuale
def initialize_classe_blueprint(app):
    classe_blueprint = Blueprint('classe', __name__)

    @classe_blueprint.route('/creazione-classe', methods=['POST'])
    def creazione_classe():
        nome_classe = request.json.get('NomeClasse')
        descrizione = request.json.get('Descrizione')
        id_docente = request.json.get('ID_Docente')

        # Validazioni
        if not nome_classe or len(nome_classe) < 2 or len(nome_classe) > 20:
            return "Lunghezza del nome della classe virtuale non corretta.", 400

        if not re.match(r"^[A-Za-zÀ-ú‘’',\(\)\s0-9]{2,20}$", nome_classe):
            return "Formato del nome della classe virtuale non corretto.", 400

        if not descrizione or len(descrizione) < 2 or len(descrizione) > 255:
            return "Lunghezza della descrizione della classe virtuale non corretta.", 400

        if not re.match(r"^[^§]{2,255}$", descrizione):
            return "Formato della descrizione della classe virtuale non corretto.", 400

        if not id_docente or len(id_docente) != 8:
            return "ID docente non valido.", 400

        return "Classe virtuale creata con successo", 200

    app.register_blueprint(classe_blueprint)

# Test 1: Nome classe con lunghezza non valida
@pytest.mark.parametrize("test_id", ["TC_CCV_1_1"])
def test_creazione_classe_nome_lunghezza_non_valida(client, test_id):
    data = {"NomeClasse": "5", "Descrizione": "Classe di test", "ID_Docente": "DOC12345"}
    response = client.post('/creazione-classe', json=data)
    assert response.status_code == 400
    assert "Lunghezza del nome della classe virtuale non corretta." in response.data.decode('utf-8')
    print(f"Test {test_id}: Nome classe con lunghezza non valida gestito correttamente!")

# Test 2: Nome classe con formato non valido
@pytest.mark.parametrize("test_id", ["TC_CCV_1_2"])
def test_creazione_classe_nome_formato_non_valido(client, test_id):
    data = {"NomeClasse": "Classe 5°D", "Descrizione": "Classe di test", "ID_Docente": "DOC12345"}
    response = client.post('/creazione-classe', json=data)
    assert response.status_code == 400
    assert "Formato del nome della classe virtuale non corretto." in response.data.decode('utf-8')
    print(f"Test {test_id}: Nome classe con formato non valido gestito correttamente!")

# Test 3: Descrizione con lunghezza non valida
@pytest.mark.parametrize("test_id", ["TC_CCV_1_3"])
def test_creazione_classe_descrizione_lunghezza_non_valida(client, test_id):
    data = {"NomeClasse": "Classe 5D", "Descrizione": "A" * 256, "ID_Docente": "DOC12345"}
    response = client.post('/creazione-classe', json=data)
    assert response.status_code == 400
    assert "Lunghezza della descrizione della classe virtuale non corretta." in response.data.decode('utf-8')
    print(f"Test {test_id}: Descrizione con lunghezza non valida gestita correttamente!")

# Test 4: Descrizione con formato non valido
@pytest.mark.parametrize("test_id", ["TC_CCV_1_4"])
def test_creazione_classe_descrizione_formato_non_valido(client, test_id):
    data = {"NomeClasse": "Classe 5D", "Descrizione": "L§ mia classe", "ID_Docente": "DOC12345"}
    response = client.post('/creazione-classe', json=data)
    assert response.status_code == 400
    assert "Formato della descrizione della classe virtuale non corretto." in response.data.decode('utf-8')
    print(f"Test {test_id}: Descrizione con formato non valido gestita correttamente!")

# Test 5: Creazione classe valida
@pytest.mark.parametrize("test_id", ["TC_CCV_1_5"])
def test_creazione_classe_successo(client, test_id):
    data = {"NomeClasse": "Classe 5D", "Descrizione": "La miglior classe dell’istituto", "ID_Docente": "DOC12345"}
    response = client.post('/creazione-classe', json=data)
    assert response.status_code == 200
    assert "Classe virtuale creata con successo" in response.data.decode('utf-8')
    print(f"Test {test_id}: Creazione classe valida gestita correttamente!")
