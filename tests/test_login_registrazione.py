import pytest
from flask import Flask, session
from unittest.mock import patch
import bcrypt
from app.controllers.LoginControl import login_bp


# Funzione per creare l'app Flask
def create_app():
    app = Flask(__name__)
    app.secret_key = "test_secret"
    app.register_blueprint(login_bp)
    return app


# Fixture per il client di test
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


# Test per formato email non valido
@pytest.mark.parametrize("test_id", ["TC_LOGIN_1_1"])
def test_login_email_non_valida(client, test_id):
    response = client.post('/login', data={"email": "email_invalid@gmail.com", "password": "Password123@"})
    assert response.status_code == 400
    assert response.json["error"] == "Formato email non valido"
    print(f"Test {test_id}: Formato email non valido gestito correttamente!")


# Test per password non valida
@pytest.mark.parametrize("test_id", ["TC_LOGIN_1_2"])
def test_login_password_non_valida(client, test_id):
    response = client.post('/login', data={"email": "email@example.com", "password": "short"})
    assert response.status_code == 400
    assert response.json["error"] == "Password non valida"
    print(f"Test {test_id}: Password non valida gestita correttamente!")


# Test per login studente con successo
@pytest.mark.parametrize("test_id", ["TC_LOGIN_3_1"])
@patch('app.models.studenteModel.StudenteModel.trova_studente', return_value={
    "email":"augusto@studenti.it",
    "nome":"Giuseppe"
})
def test_login_studente_successo(mock_studente, client, test_id):
    response = client.post('/login', data={"email": "studente@example.com", "password": "Password123@"})
    assert response.status_code == 200
    assert response.json["message"] == "Login effettuato con successo"
    assert session['role'] == 'studente'
    print(f"Test {test_id}: Login come studente gestito correttamente!")


# Test per login docente con successo
@pytest.mark.parametrize("test_id", ["TC_LOGIN_3_2"])
@patch('app.models.docenteModel.DocenteModel.trova_docente', return_value={
    "email": "docente@example.com",
    "password": bcrypt.hashpw("Password123@".encode('utf-8'), bcrypt.gensalt()),
    "SdA": "Scuola001",
    "codice_univoco": "Docente001",
    "nome": "Docente",
    "cf_docente": "CF_DOC001"
})
def test_login_docente_successo(mock_docente, client, test_id):
    response = client.post('/login', data={"email": "docente@example.com", "password": "Password123@"})
    assert response.status_code == 200
    assert response.json["message"] == "Login effettuato con successo"
    assert session['role'] == 'docente'
    print(f"Test {test_id}: Login come docente gestito correttamente!")