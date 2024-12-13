import pytest
from unittest.mock import MagicMock
from flask import Flask
from app.views.profilo import initialize_profilo_blueprint


# Funzione per creare l'app Flask senza ripetere la registrazione del blueprint
def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True  # Configura l'app in modalità di testing
    return app


# Fixture per creare l'app Flask con il blueprint inizializzato
@pytest.fixture
def app():
    app = create_app()  # Usa direttamente create_app senza inizializzare nuovamente il blueprint
    return app


# Fixture per il client di test Flask
@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


# Fixture per il mock del database
@pytest.fixture
def mock_db_manager(mocker):
    db_manager = MagicMock()
    mocker.patch('app.views.profilo.db_manager', db_manager)
    return db_manager


# Test per modifica profilo con nome non valido (nome troppo corto)
@pytest.mark.parametrize("test_id", ["TC_GP_1_1"])
def test_modifica_profilo_nome_non_valido(client, test_id):
    data = {
        'nome': 'A',  # Nome troppo corto
        'cognome': 'Rossi',
        'email': 'testuser@example.com',
        'sda': 'Scuola di Test'
    }
    response = client.post('/profilo/gestione', data=data)
    assert "Nome non valido" in response.data.decode('utf-8')
    print(f"Test {test_id}: Nome non valido gestito correttamente!")


# Test per modifica profilo con cognome non valido (caratteri speciali)
@pytest.mark.parametrize("test_id", ["TC_GP_1_2"])
def test_modifica_profilo_cognome_non_valido(client, test_id):
    data = {
        'nome': 'Mario',
        'cognome': 'R@ssi',  # Cognome con caratteri non validi
        'email': 'testuser@example.com',
        'sda': 'Scuola di Test'
    }
    response = client.post('/profilo/gestione', data=data)
    assert "Cognome non valido" in response.data.decode('utf-8')
    print(f"Test {test_id}: Cognome non valido gestito correttamente!")


# Test per modifica profilo con email non valida
@pytest.mark.parametrize("test_id", ["TC_GP_1_3"])
def test_modifica_profilo_email_non_valida(client, test_id):
    data = {
        'nome': 'Mario',
        'cognome': 'Rossi',
        'email': 'email-non-valida',  # Email non valida
        'sda': 'Scuola di Test'
    }
    response = client.post('/profilo/gestione', data=data)
    assert "Email non valida" in response.data.decode('utf-8')
    print(f"Test {test_id}: Email non valida gestita correttamente!")


# Test per modifica password con vecchia password non corretta
@pytest.mark.parametrize("test_id", ["TC_GP_2_1"])
def test_modifica_password_vecchia_password_non_valida(client, test_id):
    data = {
        'vecchia_password': 'wrongpassword',
        'nuova_password': 'NuovaPassword123!',
        'conferma_password': 'NuovaPassword123!'
    }
    response = client.post('/profilo/cambia_password_docente', data=data)
    assert "Vecchia password non corretta" in response.data.decode('utf-8')
    print(f"Test {test_id}: Vecchia password non corretta gestita correttamente!")


# Test per modifica password con nuova password non valida (troppo corta)
@pytest.mark.parametrize("test_id", ["TC_GP_2_2"])
def test_modifica_password_nuova_password_troppo_corta(client, test_id):
    data = {
        'vecchia_password': 'CorrectPassword123!',
        'nuova_password': '123',
        'conferma_password': '123'
    }
    response = client.post('/profilo/cambia_password_docente', data=data)
    assert "Nuova password non valida" in response.data.decode('utf-8')
    print(f"Test {test_id}: Nuova password troppo corta gestita correttamente!")


# Test per modifica password con successo
@pytest.mark.parametrize("test_id", ["TC_GP_2_3"])
def test_modifica_password_successo(client, test_id):
    data = {
        'vecchia_password': 'CorrectPassword123!',
        'nuova_password': 'NuovaPassword123!',
        'conferma_password': 'NuovaPassword123!'
    }
    response = client.post('/profilo/cambia_password_docente', data=data)
    assert response.status_code == 200
    assert "Password cambiata con successo" in response.data.decode('utf-8')
    print(f"Test {test_id}: Modifica password avvenuta con successo!")
