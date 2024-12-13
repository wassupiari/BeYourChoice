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

    @MaterialeDocente.route('/rimuovi/<id_materiale>', methods=['GET'])
    def rimuovi(id_materiale):
        if not ObjectId.is_valid(id_materiale):
            return "Materiale non trovato", 404
        return "Materiale rimosso con successo!", 200

    app.register_blueprint(MaterialeDocente)
# Test per rimuovere materiale con ID valido
@pytest.mark.parametrize("test_id", ["TC_GMD_2_2"])
def test_rimuovi_materiale_valido(client, test_id):
    id_materiale = str(ObjectId())
    response = client.get(f'/rimuovi/{id_materiale}')
    assert "Materiale rimosso con successo!" in response.data.decode('utf-8')
    print(f"Test {test_id}: Rimozione materiale valida gestita correttamente!")


# Test per rimuovere materiale con ID non valido
@pytest.mark.parametrize("test_id", ["TC_GMD_2_1"])
def test_rimuovi_materiale_id_non_valido(client, test_id):
    response = client.get('/rimuovi/invalid_id')
    assert "Materiale non trovato" in response.data.decode('utf-8')
    print(f"Test {test_id}: ID materiale non valido gestito correttamente!")