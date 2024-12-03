import os
import io
import pytest
from test_app import create_app  # Supponendo che questa funzione esista

UPLOAD_FOLDER = 'test_uploads'  # Usa una posizione adatta per la tua macchina


@pytest.fixture
def client():
    # Configura l'app Flask per il testing
    app = create_app({'TESTING': True, 'UPLOAD_FOLDER': UPLOAD_FOLDER})
    app.config['WTF_CSRF_ENABLED'] = False

    # Crea la cartella di upload se non esiste
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    with app.test_client() as client:
        with app.app_context():
            yield client

    # Rimuovi la cartella dopo i test per pulizia
    if os.path.exists(UPLOAD_FOLDER):
        import shutil
        shutil.rmtree(UPLOAD_FOLDER)

def test_carica_materiale(client):
    # Simula il caricamento file usando Flask's test client
    data = {
        'titolo': 'Titolo Prova',
        'descrizione': 'Descrizione di prova',
        'tipo': 'txt',
        'file': (io.BytesIO(b"Contenuto del file di prova"), 'prova.txt')
    }
    response = client.post('/carica', data=data, follow_redirects=True)

    # Controlla che la richiesta ritorni un successo
    assert response.status_code == 200
    assert b"Materiale caricato con successo!" in response.data


def test_rimuovi_materiale(client):
    # Carica un file per testare la rimozione
    material_id = 'inserisci_id_valido'  # Devi avere un ID materiale valido per i test
    data = {
        'titolo': 'Titolo Prova',
        'descrizione': 'Descrizione di prova',
        'tipo': 'txt',
        'file': (io.BytesIO(b"Contenuto del file di prova"), 'prova.txt')
    }
    client.post('/carica', data=data, follow_redirects=True)

    # Testa la rimozione del materiale
    response = client.get(f'/rimuovi/{material_id}', follow_redirects=True)

    # Verifica che il materiale sia stato rimosso
    assert response.status_code == 200
    assert b"Materiale rimosso con successo!" in response.data