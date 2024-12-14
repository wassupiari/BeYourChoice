import pytest
from flask import Flask, jsonify, request, Blueprint
from unittest.mock import MagicMock
import re


# Funzione per creare e inizializzare il blueprint
def initialize_profilo_blueprint(app, mockDbManager=None):
    profilo_blueprint = Blueprint('cambia_password', __name__)

    @profilo_blueprint.route('/cambia_password_docente', methods=['POST'])
    def cambia_password_docente():
        vecchia_password = request.form.get('vecchia_password')
        nuova_password = request.form.get('nuova_password')

        # Verifica esistenza, lunghezza e formato della vecchia password
        if not vecchia_password or len(vecchia_password) < 8 or not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])',
                                                                             vecchia_password):
            return jsonify({"message": "Vecchia Password mancante, troppo corta o con formato errato"}), 400

        # Verifica lunghezza e formato della nuova password
        if len(nuova_password) < 8 or not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])', nuova_password):
            return jsonify({"message": "Nuova Password troppo corta o con formato errato"}), 400

        # Verifica esistenza della vecchia password nel database o valore predefinito
        if mockDbManager:
            if not mockDbManager.get_password(vecchia_password):
                return jsonify({"message": "Vecchia Password non trovata"}), 400
        else:
            if vecchia_password != "password1!":
                return jsonify({"message": "Vecchia Password non trovata"}), 400

        # Cambio della password avvenuto con successo
        return jsonify({"success": True, "message": "Password modificata con successo"}), 200

    app.register_blueprint(profilo_blueprint)
    return profilo_blueprint


# Fixture per creare l'app Flask
@pytest.fixture
def app(mockDbManager):
    app = Flask(__name__)
    app.config['TESTING'] = True
    initialize_profilo_blueprint(app, mockDbManager)
    return app


# Fixture per il client di test
@pytest.fixture
def client(app):
    return app.test_client()


# Mock del database manager
@pytest.fixture
def mockDbManager():
    dbManager = MagicMock()
    collectionMock = MagicMock()
    dbManager.get_collection.return_value = collectionMock
    return dbManager

@pytest.mark.parametrize(
    "test_id, vecchia_password, nuova_password, expected_message, expected_status_code",
    [
        # Caso 1: Vecchia password assente, troppo corta o con formato errato
        ("TC_GP_2_1", "a", "5password?", "Vecchia Password mancante, troppo corta o con formato errato", 400),
        ("TC_GP_2_2", "1234567", "5password?", "Vecchia Password mancante, troppo corta o con formato errato",
         400),
        ("TC_GP_2_3", None, "5password?", "Vecchia Password mancante, troppo corta o con formato errato", 400),

        # Caso 2: Nuova password troppo corta o con formato errato
        ("TC_GP_2_4", "password1!", "pa", "Nuova Password troppo corta o con formato errato", 400),
        ("TC_GP_2_5", "password1!", "12345678", "Nuova Password troppo corta o con formato errato", 400),

        # Caso 4: Password valida -> modifica avvenuta
        ("TC_GP_2_6", "password1!", "5password?", "Password modificata con successo", 200),
    ]
)


def test_modifica_password(client, test_id, vecchia_password, nuova_password, expected_message, expected_status_code):
    """
    Test per la modifica della password.
    """
    # Mock dei dati inviati via POST
    data = {
        "vecchia_password": vecchia_password,
        "nuova_password": nuova_password,
    }

    # Esegui POST
    response = client.post(
        "/cambia_password_docente",
        data=data,
        content_type="multipart/form-data",
    )

    # Verifica che la risposta sia JSON valida
    response_json = response.get_json()
    assert response_json is not None, "La risposta non contiene dati JSON validi!"

    # Verifica i messaggi e il codice di stato
    assert response_json["message"] == expected_message
    assert response.status_code == expected_status_code
    print(f"Test {test_id}: {expected_message} verificato!")