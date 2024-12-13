"""
test_profilo.py

Questo file contiene i test per le funzionalità definite nel modulo `profilo`.
Utilizza pytest per eseguire i test e mock per simulare il comportamento dei database.

Autore: [il tuo nome]
Data di creazione: [data di creazione]
"""

import pytest
from unittest.mock import MagicMock, patch
from flask import Flask

from app.controllers.profiloControl import ProfiloControl
from server import initialize_profilo_blueprint


# Fixture per creare una nuova app Flask per ogni test
@pytest.fixture
def app():
    app = Flask(__name__)
    app.secret_key = 'test_secret'

    db_manager = MagicMock()
    profilo_control = ProfiloControl(db_manager)

    # Registra il Blueprint una sola volta su una nuova istanza dell'app
    initialize_profilo_blueprint(app)
    return app


# Fixture per il test client di Flask
@pytest.fixture
def client(app):
    return app.test_client()


# Test per la modifica del profilo (TCS_GP_1)
def test_modifica_profilo_nome_lunghezza_errata(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.post('/profilo/gestione', data={
        'nome': 'M',
        'cognome': 'Rossi',
        'email': 'test@example.com',
        'ruolo': 'studente'
    })
    assert b"Lunghezza nome non corretta" in response.data


def test_modifica_profilo_nome_formato_errato(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.post('/profilo/gestione', data={
        'nome': 'M4rc00',
        'cognome': 'Rossi',
        'email': 'test@example.com',
        'ruolo': 'studente'
    })
    assert b"Formato nome non corretto" in response.data


def test_modifica_profilo_cognome_lunghezza_errata(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.post('/profilo/gestione', data={
        'nome': 'Marco',
        'cognome': 'A',
        'email': 'test@example.com',
        'ruolo': 'docente'
    })
    assert b"Lunghezza cognome non corretta" in response.data


def test_modifica_profilo_email_formato_errato(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.post('/profilo/gestione', data={
        'nome': 'Marco',
        'cognome': 'Rossi',
        'email': 'marcoacierno@@gmail.com',
        'ruolo': 'studente'
    })
    assert b"Formato email non corretto" in response.data


def test_modifica_profilo_dati_validi(client):
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.post('/profilo/gestione', data={
        'nome': 'Marco',
        'cognome': 'Rossi',
        'email': 'marco.acierno@gmail.com',
        'sda': 'ITIS Dorso',
        'ruolo': 'studente'
    })
    assert b"Dati modificati" in response.data


# Test per il cambio password (TCS_GP_2)
@patch('app.models.profiloModel.bcrypt.checkpw')
def test_cambio_password_vecchia_password_errata(mock_checkpw, client):
    mock_checkpw.return_value = False
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.post('/profilo/cambia_password_studente', data={
        'vecchia_password': 'wrongpassword',
        'nuova_password': 'Password123!'
    })
    assert b"Vecchia password errata" in response.data


@patch('app.models.profiloModel.bcrypt.checkpw')
def test_cambio_password_nuova_password_formato_errato(mock_checkpw, client):
    mock_checkpw.return_value = True
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.post('/profilo/cambia_password_studente', data={
        'vecchia_password': 'CorrectPassword1!',
        'nuova_password': 'abc'
    })
    assert b"Formato Nuova Password errato" in response.data


@patch('app.models.profiloModel.bcrypt.hashpw')
@patch('app.models.profiloModel.bcrypt.checkpw')
def test_cambio_password_successo(mock_checkpw, mock_hashpw, client):
    mock_checkpw.return_value = True
    mock_hashpw.return_value = b'hashedpassword'
    with client.session_transaction() as sess:
        sess['email'] = 'test@example.com'

    response = client.post('/profilo/cambia_password_studente', data={
        'vecchia_password': 'CorrectPassword1!',
        'nuova_password': 'Password123!'
    })
    assert b"Password aggiornata con successo!" in response.data