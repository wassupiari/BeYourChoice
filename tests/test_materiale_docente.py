import os
import sys

import pytest
from flask import Flask

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.controllers.MaterialeControl import MaterialeControl
from app.models.materialeModel import MaterialeModel
import io
from bson import ObjectId

from app.views.materialeDocente import db_manager


# Fixture per creare l'app Flask
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    return app


# Fixture per il client di test
@pytest.fixture
def client(app):
    return app.test_client()


# Mock database manager
class MockDatabaseManager:
    def __init__(self):
        self.data = {}

    def get_collection(self, name):
        return MockCollection(self.data)


class MockCollection:
    def __init__(self, data):
        self.data = data

    def insert_one(self, document):
        object_id = ObjectId()
        document['_id'] = object_id
        self.data[object_id] = document
        return object_id

    def find(self, query=None):
        if query:
            return [doc for doc in self.data.values() if all(item in doc.items() for item in query.items())]
        return MockCursor(self.data.values())

    def sort(self, key, direction):
        self.documents.sort(key=lambda doc: doc.get(key, 0), reverse=direction == -1)

    def delete_one(self, query):
        id_to_delete = query.get('_id')
        if id_to_delete in self.data:
            del self.data[id_to_delete]
            return MockDeleteResult(deleted_count=1)
        return MockDeleteResult(deleted_count=0)

class MockDeleteResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count

class MockCursor:
    def __init__(self, documents):
        self.documents = list(documents)
        self.index = 0

    def sort(self, key, direction):
        self.documents.sort(key=lambda doc: doc.get(key, 0), reverse=direction == -1)
        return self

    def limit(self, count):
        self.documents = self.documents[:count]
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.documents):
            doc = self.documents[self.index]
            self.index += 1
            return doc
        else:
            raise StopIteration

mock_db_manager = MockDatabaseManager()

@pytest.fixture
def materiale_control():
    return MaterialeControl(mock_db_manager)


def test_carica_materiale(materiale_control, client):
    # Simula il caricamento di un file
    file_data = io.BytesIO(b'Some initial text data')
    file_data.name = 'test_file.txt'

    nuovo_materiale = MaterialeModel(
        id_MaterialeDidattico='test_id',
        titolo='Test Title',
        descrizione='Test Description',
        filepath=file_data.name,
        tipo='txt',
        ID_Classe='class_id'
    )

    materiale_control.upload_material(nuovo_materiale)

    # Controlla se esiste il materiale caricato
    materiali = materiale_control.get_all_materials()
    assert len(materiali) > 0
    assert any(materiale['Titolo'] == 'Test Title' for materiale in materiali)