import io
import re
from unittest.mock import MagicMock
import pytest
from flask import Flask, Blueprint, request, jsonify


# Funzione per creare ed inizializzare il blueprint
def initialize_profilo_blueprint(app, mockDbManager=None):
    profilo_blueprint = Blueprint('gestione', __name__)

    @profilo_blueprint.route('/modifica', methods=['POST'])
    def gestione_profilo():
        # Estrarre i parametri dalla richiesta
        nome = request.form.get('nome')
        cognome = request.form.get('cognome')
        email = request.form.get('email')
        sda = request.files.get('sda')
        data_nascita = request.form.get('data_nascita')

        # Regex per la validazione
        email_regex = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$"
        nome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        cognome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        sda_regex = r"^[A-Za-z0-9À-ù'’\- ]+$"
        data_nascita_regex = r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"

        # Validazione
        errors = {}

        if not nome or not re.match(nome_regex, nome):
            errors["nome"] = "Lunghezza nome non corretta o formato invalido."

        if not cognome or not re.match(cognome_regex, cognome):
            errors["cognome"] = "Lunghezza cognome non corretta o formato invalido."

        if not email or not re.match(email_regex, email):
            errors["email"] = "Formato email non corretto."

        if not sda or len(sda.filename) < 2 or not re.match(sda_regex, sda.filename):
            errors["sda"] = "Scuola non valida. Deve essere un file valido."

        if not data_nascita or not re.match(data_nascita_regex, data_nascita):
            errors["data_nascita"] = "Data di nascita non valida. Usa il formato YYYY-MM-DD."

        # Se ci sono errori, ritorna la risposta con codice 400
        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        # Se tutto è valido
        return jsonify({"success": True, "message": "Dati ricevuti correttamente"}), 200

    # Registra il blueprint
    app.register_blueprint(profilo_blueprint, url_prefix='/gestione')
    return profilo_blueprint


# Fixture per creare l'app Flask
@pytest.fixture
def app(mockDbManager):
    app = Flask(__name__)
    app.config['TESTING'] = True
    initialize_profilo_blueprint(app, mockDbManager)
    return app


# Fixture del client di test
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


# Test parametrizzati
@pytest.mark.parametrize(
    "test_id, nome, cognome, email, sda_name, data_nascita, expected_message, expected_status_code",
    [
        ("TC_GP_1_1", "M", "Acierno", "marcoacierno@gmail.com", "itis dorso", "2000-01-01",
         "Lunghezza nome non corretta o formato invalido.", 400),
        ("TC_GP_1_2", "M4rc00", "Acierno", "marcoacierno@gmail.com", "itis dorso", "2000-01-01",
         "Lunghezza nome non corretta o formato invalido.", 400),
        ("TC_GP_1_3", "Marco", "A", "marcoacierno@gmail.com", "itis dorso", "2000-01-01",
         "Lunghezza cognome non corretta o formato invalido.", 400),
        ("TC_GP_1_4", "Marco", "Aci3rn0", "marcoacierno@gmail.com", "itis dorso", "2000-01-01",
         "Lunghezza cognome non corretta o formato invalido.", 400),
        ("TC_GP_1_5", "Marco", "Acierno", "a@", "itis dorso", "2000-01-01", "Formato email non corretto.", 400),
        ("TC_GP_1_6", "Marco", "Acierno", "marcoacierno@@gmail.com", "itis dorso", "2000-01-01",
         "Formato email non corretto.", 400),
        ("TC_GP_1_7", "Marco", "Acierno", "marcoacierno@gmail.com", "a", "2000-01-01",
         "Scuola non valida. Deve essere un file valido.", 400),
        ("TC_GP_1_8", "Marco", "Acierno", "marcoacierno@gmail.com", "@itis", "2000-01-01",
         "Scuola non valida. Deve essere un file valido.", 400),
        ("TC_GP_1_9", "Marco", "Acierno", "marcoacierno@gmail.com", "itis dorso", "2000-01-01",
         "Dati ricevuti correttamente", 200),
    ]
)
def test_modifica_profilo(client, test_id, nome, cognome, email, sda_name, data_nascita, expected_message,
                          expected_status_code):
    """
    Test per la modifica del profilo.
    """
    # Mock dei dati inviati via POST
    data = {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "sda": (io.BytesIO(b"contenuto_file"), sda_name),  # Mock del file
        "data_nascita": data_nascita,
    }

    # Esegui POST
    response = client.post(
        "/gestione/modifica",
        data=data,
        content_type="multipart/form-data",
    )

    # Verifica il risultato
    response_text = response.data.decode("utf-8")
    assert expected_message in response_text
    assert response.status_code == expected_status_code
    print(f"Test {test_id}: {expected_message} verificato!")