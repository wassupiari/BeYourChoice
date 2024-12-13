import io
from unittest.mock import MagicMock

import pytest
from bson import ObjectId
from flask import Flask, Blueprint, request


# Funzione per creare l'app Flask
def create_app():
    app = Flask(__name__)
    initialize_materiale_docente_blueprint(app)
    return app


# Fixture per il client di test
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


# Mock del db manager
@pytest.fixture
def mockDbManager():
    dbManager = MagicMock()
    collectionMock = MagicMock()
    dbManager.get_collection.return_value = collectionMock
    return dbManager


# Inizializzazione del blueprint MaterialeDocente
def initialize_materiale_docente_blueprint(app):
    MaterialeDocente = Blueprint('MaterialeDocente', __name__)

    @MaterialeDocente.route('/carica', methods=['POST'])
    def carica():
        titolo = request.form.get('titolo')
        tipo = request.form.get('tipo')
        descrizione = request.form.get('descrizione')
        file = request.files.get('file')

        # Validazione del titolo
        if not titolo or len(titolo) < 2 or '@' in titolo:
            return "Formato titolo non supportato", 400

        # Validazione lunghezza titolo
        if len(titolo) > 20:
            return "Lunghezza titolo non supportata", 400

        # Validazione tipo file
        if tipo not in ['pdf', 'docx', 'jpeg', 'jpg', 'mp4', 'txt', 'png']:
            return "Tipo formato non supportato", 400

        # Validazione dimensione file
        if not file:
            return "File mancante", 400
        file_size = len(file.read())
        file.seek(0)  # Riposiziona il cursore all'inizio
        if file_size > 6 * 1024 * 1024:  # 6 MB limite
            return "Dimensione file non supportata", 400

        # Validazione descrizione
        if not descrizione or '§' in descrizione:
            return "Formato descrizione non supportato", 400

        # Validazione lunghezza descrizione
        if len(descrizione) > 255:
            return "Lunghezza descrizione non supportata", 400

        return "Caricamento avvenuto con successo", 302


# Test per tipo non supportato
@pytest.mark.parametrize("test_id", ["TC_GMD_1_1"])
def test_carica_materiale_tipo_non_supportato(client, test_id):
    data = {
        'titolo': 'FileNonSupportato',
        'tipo': 'mp3',
        'descrizione': 'Descrizione valida',
        'file': (io.BytesIO(b'contenuto file'), 'file.mp3')
    }
    response = client.post('/carica', data=data, content_type='multipart/form-data')
    assert "Tipo formato non supportato" in response.data.decode('utf-8')
    print(f"Test {test_id}: Tipo file non supportato gestito correttamente!")


# Test per dimensione non supportata
@pytest.mark.parametrize("test_id", ["TC_GMD_1_2"])
def test_carica_materiale_dimensione_non_supportata(client, test_id):
    data = {
        'titolo': 'FileTroppoGrande',
        'tipo': 'pdf',
        'descrizione': 'Descrizione valida',
        'file': (io.BytesIO(b'a' * (7 * 1024 * 1024)), 'file.pdf')  # 6 MB
    }
    response = client.post('/carica', data=data, content_type='multipart/form-data')
    assert "Dimensione file non supportata" in response.data.decode('utf-8')
    print(f"Test {test_id}: Dimensione file non supportata gestita correttamente!")


# Test per formato titolo non supportato
@pytest.mark.parametrize("test_id", ["TC_GMD_1_3"])
def test_carica_materiale_formato_titolo_non_supportato(client, test_id):
    data = {
        'titolo': 'Titolo@Errato',
        'tipo': 'pdf',
        'descrizione': 'Descrizione valida',
        'file': (io.BytesIO(b'contenuto file'), 'file.pdf')
    }
    response = client.post('/carica', data=data, content_type='multipart/form-data')
    assert "Formato titolo non supportato" in response.data.decode('utf-8')
    print(f"Test {test_id}: Formato titolo non supportato gestito correttamente!")


# Test per lunghezza titolo non supportata
@pytest.mark.parametrize("test_id", ["TC_GMD_1_4"])
def test_carica_materiale_lunghezza_titolo_non_supportata(client, test_id):
    data = {
        'titolo': 'T' * 101,  # 101 caratteri
        'tipo': 'pdf',
        'descrizione': 'Descrizione valida',
        'file': (io.BytesIO(b'contenuto file'), 'file.pdf')
    }
    response = client.post('/carica', data=data, content_type='multipart/form-data')
    assert "Lunghezza titolo non supportata" in response.data.decode('utf-8')
    print(f"Test {test_id}: Lunghezza titolo non supportata gestita correttamente!")


# Test per formato descrizione non supportato
@pytest.mark.parametrize("test_id", ["TC_GMD_1_5"])
def test_carica_materiale_formato_descrizione_non_supportato(client, test_id):
    data = {
        'titolo': 'TitoloValido',
        'tipo': 'pdf',
        'descrizione': 'Descrizione§Errata',
        'file': (io.BytesIO(b'contenuto file'), 'file.pdf')
    }
    response = client.post('/carica', data=data, content_type='multipart/form-data')
    assert "Formato descrizione non supportato" in response.data.decode('utf-8')
    print(f"Test {test_id}: Formato descrizione non supportato gestito correttamente!")


# Test per lunghezza descrizione non supportata
@pytest.mark.parametrize("test_id", ["TC_GMD_1_6"])
def test_carica_materiale_lunghezza_descrizione_non_supportata(client, test_id):
    data = {
        'titolo': 'TitoloValido',
        'tipo': 'pdf',
        'descrizione': 'D' * 501,  # 501 caratteri
        'file': (io.BytesIO(b'contenuto file'), 'file.pdf')
    }
    response = client.post('/carica', data=data, content_type='multipart/form-data')
    assert "Lunghezza descrizione non supportata" in response.data.decode('utf-8')
    print(f"Test {test_id}: Lunghezza descrizione non supportata gestita correttamente!")


# Test per caricamento avvenuto con successo
@pytest.mark.parametrize("test_id", ["TC_GMD_1_7"])
def test_carica_materiale_successo(client, test_id):
    data = {
        'titolo': 'TitoloValido',
        'tipo': 'pdf',
        'descrizione': 'Descrizione valida',
        'file': (io.BytesIO(b'contenuto file'), 'file.pdf')
    }
    response = client.post('/carica', data=data, content_type='multipart/form-data')
    assert response.status_code == 302
    print(f"Test {test_id}: Caricamento avvenuto con successo!")


