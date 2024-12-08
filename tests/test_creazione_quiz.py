import pytest
from flask import session
from unittest.mock import patch
from app import create_app


@pytest.fixture
def client():
    """Crea un client di test per Flask"""
    app = create_app()
    app.testing = True

    with app.test_client() as client:
        with app.app_context():
            yield client


# Mock per bypassare il decoratore @teacher_required
def bypass_teacher_required(func):
    """Mock per ignorare il controllo della sessione per @teacher_required"""
    return func


@patch('app.controllers.LoginControl.teacher_required', bypass_teacher_required)
@pytest.mark.parametrize("test_id, payload, expected_status, expected_error", [
    (
        "TC_GMD_1_1",  # Test ID: Creazione quiz con input validi
        {
            "titolo": "Quiz Test",
            "tema": "Costituzione Italiana",
            "numero_domande": 10,
            "modalita_risposta": "4_risposte",
            "durata": 30
        },
        200,
        None
    ),
    (
        "TC_GMD_1_2",  # Test ID: Titolo non valido
        {
            "titolo": "A",  # Titolo troppo corto
            "tema": "Costituzione Italiana",
            "numero_domande": 10,
            "modalita_risposta": "4_risposte",
            "durata": 30
        },
        400,
        "Il titolo non è valido"
    ),
    (
        "TC_GMD_1_3",  # Test ID: Argomento non valido
        {
            "titolo": "Quiz Test",
            "tema": "A",  # Argomento troppo corto
            "numero_domande": 10,
            "modalita_risposta": "4_risposte",
            "durata": 30
        },
        400,
        "L'argomento non è valido"
    ),
    (
        "TC_GMD_1_4",  # Test ID: Numero di domande non valido
        {
            "titolo": "Quiz Test",
            "tema": "Costituzione Italiana",
            "numero_domande": 25,  # Fuori range
            "modalita_risposta": "4_risposte",
            "durata": 30
        },
        400,
        "Il numero di domande deve essere compreso tra 5 e 20"
    ),
    (
        "TC_GMD_1_5",  # Test ID: Durata non valida
        {
            "titolo": "Quiz Test",
            "tema": "Costituzione Italiana",
            "numero_domande": 10,
            "modalita_risposta": "4_risposte",
            "durata": 150  # Durata troppo lunga
        },
        400,
        "La durata deve essere compresa tra 1 e 120 minuti"
    ),
    (
        "TC_GMD_1_6",  # Test ID: Sessione mancante
        {
            "titolo": "Quiz Test",
            "tema": "Costituzione Italiana",
            "numero_domande": 10,
            "modalita_risposta": "4_risposte",
            "durata": 30
        },
        400,
        "ID Classe mancante nella sessione"
    ),
])
def test_creazione_quiz(client, test_id, payload, expected_status, expected_error):
    """Esegue test parametrizzati per la creazione quiz"""
    if test_id != "TC_GMD_1_6":  # Configura la sessione solo per test con sessione valida
        with client.session_transaction() as sess:
            sess['email'] = 'roccocione@gmail.com'
            sess['session_token'] = 'i1kb4v1ik2v4jiubadu'
            sess['role'] = 'docente'
            sess['ID_Classe'] = 3

    response = client.post("/genera", json=payload)
    assert response.status_code == expected_status

    if expected_error:
        data = response.get_json()
        assert expected_error in data["error"]
    else:
        data = response.get_json()
        assert len(data) == payload["numero_domande"]
        for domanda in data:
            assert "Testo_Domanda" in domanda
            assert "Opzioni_Risposte" in domanda
            assert "Risposta_Corretta" in domanda
