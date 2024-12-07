import pytest
from flask import Flask, session
from app.controllers.RegistrazioneControl import registrazione_bp

# Funzione per creare l'app Flask
def create_app():
    app = Flask(__name__)
    app.secret_key = "test_secret"
    app.register_blueprint(registrazione_bp)
    return app


# Fixture per il client di test
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test per la lunghezza del nome non valida
@pytest.mark.parametrize("test_id", ["TC_REG_1"])
def test_nome_lunghezza_non_valida(client, test_id):
    data = {
        "nome": "A",  # Lunghezza nome non valida
        "cognome": "ValidCognome",
        "sda": "Liceo Scientifico",
        "email": "valid@email.com",
        "cf": "RSSMRA80A01H501Z",
        "data-nascita": "1990-12-12",
        "password": "Valid@1234",
    }
    response = client.post('/register', data=data)
    assert response.status_code == 302  # Redirezione su errore
    assert "formatoNome" in response.location
    print(f"Test {test_id}: Lunghezza nome non valida gestita correttamente!")


# Test per formato cognome non valido
@pytest.mark.parametrize("test_id", ["TC_REG_2"])
def test_cognome_formato_non_valido(client, test_id):
    data = {
        "nome": "ValidNome",
        "cognome": "Invalid@",  # Cognome non valido
        "sda": "Liceo Scientifico",
        "email": "valid@email.com",
        "cf": "RSSMRA80A01H501Z",
        "data-nascita": "1990-12-12",
        "password": "Valid@1234",
    }
    response = client.post('/register', data=data)
    assert response.status_code == 302
    assert "formatoCognome" in response.location
    print(f"Test {test_id}: Formato cognome non valido gestito correttamente!")


# Test per formato email non valido
@pytest.mark.parametrize("test_id", ["TC_REG_3"])
def test_email_formato_non_valido(client, test_id):
    data = {
        "nome": "ValidNome",
        "cognome": "ValidCognome",
        "sda": "Liceo Scientifico",
        "email": "invalidemail@",  # Email non valida
        "cf": "RSSMRA80A01H501Z",
        "data-nascita": "1990-12-12",
        "password": "Valid@1234",
    }
    response = client.post('/register', data=data)
    assert response.status_code == 302
    assert "formatoEmail" in response.location
    print(f"Test {test_id}: Formato email non valido gestito correttamente!")


# Test per codice fiscale non valido
@pytest.mark.parametrize("test_id", ["TC_REG_4"])
def test_cf_formato_non_valido(client, test_id):
    data = {
        "nome": "ValidNome",
        "cognome": "ValidCognome",
        "sda": "Liceo Scientifico",
        "email": "valid@email.com",
        "cf": "INVALIDCF123",  # Codice fiscale non valido
        "data-nascita": "1990-12-12",
        "password": "Valid@1234",
    }
    response = client.post('/register', data=data)
    assert response.status_code == 302
    assert "formatocf" in response.location
    print(f"Test {test_id}: Formato codice fiscale non valido gestito correttamente!")


# Test per registrazione riuscita
@pytest.mark.parametrize("test_id", ["TC_REG_5"])
def test_registrazione_successo(client, test_id):
    data = {
        "nome": "ValidNome",
        "cognome": "ValidCognome",
        "sda": "Liceo Scientifico",
        "email": "valid@email.com",
        "cf": "RSSMRA80A01H501Z",
        "data-nascita": "1990-12-12",
        "password": "Valid@1234",
        "cu": "123456",
    }
    response = client.post('/register', data=data)
    assert response.status_code == 302  # Redirezione su success
    assert "home" in response.location
    print(f"Test {test_id}: Registrazione completata con successo!")


# Test per account già registrato
@pytest.mark.parametrize("test_id", ["TC_REG_6"])
def test_account_gia_registrato(client, test_id, mocker):
    mocker.patch('app.models.studenteModel.StudenteModel.trova_studente', return_value={"email": "valid@email.com"})
    data = {
        "nome": "ValidNome",
        "cognome": "ValidCognome",
        "sda": "Liceo Scientifico",
        "email": "valid@email.com",
        "cf": "RSSMRA80A01H501Z",
        "data-nascita": "1990-12-12",
        "password": "Valid@1234",
    }
    response = client.post('/register', data=data)
    assert response.status_code == 302
    assert "alreadyRegistered" in response.location
    print(f"Test {test_id}: Verifica account già registrato completata!")

