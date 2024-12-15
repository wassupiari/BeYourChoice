import pytest
from flask import session
from unittest.mock import patch
from server import app
from app.models.quizModel import QuizModel


@pytest.fixture
def client():
    """Crea un client di test per Flask."""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = "test_key"
    with app.test_client() as client:
        with app.app_context():
            yield client


# Mock per bypassare il decoratore @teacher_required
def bypass_teacher_required(func):
    """Mock per ignorare il controllo della sessione per @teacher_required."""
    return func


@patch('app.controllers.loginControl.teacher_required', bypass_teacher_required)
@pytest.mark.parametrize("test_id, payload, expected_status, expected_error", [
    # TC_GMD_1_1: Input valido
    (
        "TC_GMD_1_1",
        {
            "titolo": "Quiz Test",
            "argomento": "Costituzione Italiana",
            "n_domande": 10,
            "modalita_quiz": "4_risposte",
            "durata": 30
        },
        200,
        None
    ),
    # TC_GMD_1_2: Titolo non valido (troppo corto)
    (
        "TC_GMD_1_2",
        {
            "titolo": "Q",
            "argomento": "Costituzione Italiana",
            "n_domande": 10,
            "modalita_quiz": "4_risposte",
            "durata": 30
        },
        400,
        "Il titolo non è valido"
    ),
    # TC_GMD_1_3: Titolo duplicato
    (
        "TC_GMD_1_3",
        {
            "titolo": "Quiz Duplicato",
            "argomento": "Costituzione Italiana",
            "n_domande": 10,
            "modalita_quiz": "4_risposte",
            "durata": 30
        },
        400,
        "Il titolo esiste già nel database"
    ),
    # TC_GMD_1_4: Argomento non valido (troppo corto)
    (
        "TC_GMD_1_4",
        {
            "titolo": "Quiz Test",
            "argomento": "A",
            "n_domande": 10,
            "modalita_quiz": "4_risposte",
            "durata": 30
        },
        400,
        "L'argomento non è valido"
    ),
    # TC_GMD_1_5: Numero di domande fuori range (troppo basso)
    (
        "TC_GMD_1_5",
        {
            "titolo": "Quiz Test",
            "argomento": "Costituzione Italiana",
            "n_domande": 3,
            "modalita_quiz": "4_risposte",
            "durata": 30
        },
        400,
        "Il numero di domande deve essere compreso tra 5 e 20"
    ),
    # TC_GMD_1_6: Numero di domande fuori range (troppo alto)
    (
        "TC_GMD_1_6",
        {
            "titolo": "Quiz Test",
            "argomento": "Costituzione Italiana",
            "n_domande": 25,
            "modalita_quiz": "4_risposte",
            "durata": 30
        },
        400,
        "Il numero di domande deve essere compreso tra 5 e 20"
    ),
    # TC_GMD_1_7: Modalità di risposta non valida
    (
        "TC_GMD_1_7",
        {
            "titolo": "Quiz Test",
            "argomento": "Costituzione Italiana",
            "n_domande": 10,
            "modalita_quiz": "5_risposte",  # Non valida
            "durata": 30
        },
        400,
        "Modalità di risposta non valida"
    )

])
def test_generazione_quiz(client, test_id, payload, expected_status, expected_error):
    """Esegue test parametrizzati per il metodo /genera."""

    with patch('app.models.quizModel.QuizModel.genera_domande') as mock_genera_domande:
        # Configura il mock per i test di successo
        if expected_status == 200:
            mock_genera_domande.return_value = [
                {
                    "testo_domanda": f"Domanda {i + 1}: Qual è la capitale d'Italia?",
                    "opzioni_risposte": ["Roma", "Milano", "Napoli"],
                    "risposta_corretta": "Roma"
                }
                for i in range(payload["n_domande"])
            ]

        # Mock di verifica del titolo duplicato
        with patch('app.models.quizModel.QuizModel.verifica_titolo') as mock_verifica_titolo:
            if "Il titolo esiste già nel database" in (expected_error or ""):
                mock_verifica_titolo.return_value = True
            else:
                mock_verifica_titolo.return_value = False

            # Configura la sessione simulata
            with client.session_transaction() as sess:
                sess['email'] = 'giovanni.verdi@docente.com'
                sess['session_token'] = 'i1kb4v1ik2v4jiubadu'
                sess['role'] = 'docente'
                sess['id_classe'] = 3

            # Esegue la richiesta POST
            response = client.post("/genera", json=payload)

            # Verifica lo status code
            assert response.status_code == expected_status

            # Verifica il messaggio di errore o il contenuto
            if expected_error:
                assert expected_error in response.get_json()["error"]
            else:
                domande = response.get_json()
                assert len(domande) == payload["n_domande"]  # Confronta con il numero di domande
                for i, domanda in enumerate(domande):
                    assert "testo_domanda" in domanda
                    assert domanda["testo_domanda"] == f"Domanda {i + 1}: Qual è la capitale d'Italia?"
                    assert "opzioni_risposte" in domanda
                    assert "risposta_corretta" in domanda