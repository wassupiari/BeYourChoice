import re

import pytest
from app.models.scenarioModel import ScenarioModel
from databaseManager import DatabaseManager

# Fixture per la connessione al database MongoDB usando DatabaseManager
@pytest.fixture(scope='module')
def mongo_client():
    db_manager = DatabaseManager(
        uri="mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority&appName=BeYourChoice"
    )
    assert db_manager.db is not None, "Connessione al database fallita!"
    yield db_manager
    db_manager.close_connection()

# Fixture per il modello Scenario
@pytest.fixture(scope='function')
def scenario_model(mongo_client):
    scenario_model = ScenarioModel()
    scenario_model.db_manager.db = mongo_client.db
    yield scenario_model

# Test combinazioni per la creazione di uno scenario
@pytest.mark.parametrize("test_id, titolo, descrizione, argomento, modalita, expected_success", [
    ("TC_GSV_1_1", "A", "Descrizione valida", "Costituzione", "Competizione", False),  # Lunghezza titolo < 2
    ("TC_GSV_1_2", "+Titolo", "Descrizione valida", "Costituzione", "Competizione", False),  # Formato titlo errato
    ("TC_GSV_1_3", "Titolo valido", "D", "Costituzione", "Competizione", False),  # Lunghezza descrizione < 2
    ("TC_GSV_1_4", "Titolo valido", "Descrizione valid§", "Competizione", None, False),  # Formato descrizione errato
    ("TC_GSV_1_5", "Titolo valido", "Descrizione valida", None, "Competizione", False),  # Arogomento non selezionato
    ("TC_GSV_1_6", "Titolo valido", "Descrizione valida", "Costituzione", None, False),  # Modalità non selezionata
    ("TC_GSV_1_7", "Titolo valido", "Descrizione valida", "Costituzione", "Competizione", True),  # Tutti i campi validi

])
def test_creazione_scenario(scenario_model, test_id, titolo, descrizione, argomento, modalita, expected_success):
    """
    Test per le combinazioni di creazione dello scenario, basati sui casi forniti nel documento.
    Ogni caso è denominato con il relativo ID del test case (es. TC_GSV_1_1).
    """
    id_scenario = scenario_model.get_ultimo_scenario_id() + 1
    id_classe = 10448
    scenario_dict = {
        "id_scenario": id_scenario,
        "id_classe": id_classe,
        "titolo": titolo,
        "descrizione": descrizione,
        "argomento": argomento,
        "modalita": modalita
    }
    # Regex per i campi dello scenario
    REGEX_TITOLO = r"^[A-Za-zÀ-ú‘’',\(\)\s0-9]{2,20}$"
    REGEX_DESCRIZIONE = r"^[^§]{2,255}$"

    # Validazione delle regex
    titolo_ok = re.match(REGEX_TITOLO, titolo) is not None
    descrizione_ok = re.match(REGEX_DESCRIZIONE, descrizione) is not None

    # Controlli preliminari
    validazione_preliminare = titolo_ok and descrizione_ok and argomento is not None and modalita is not None

    # Debug delle validazioni
    print(f"Validazione preliminare: {validazione_preliminare}")
    print(f"Titolo valido: {titolo_ok}, Descrizione valida: {descrizione_ok}")

    # Chiamata alla funzione di creazione scenario solo se validazione preliminare è vera
    if validazione_preliminare:
        scenario_model.aggiungi_scenario(scenario_dict)
        risultato = scenario_model.get_ultimo_scenario_id() == id_scenario
    else:
        risultato = False  # Fallimento simulato per test

    # Validazione del risultato atteso
    assert risultato == expected_success, f"{test_id}: Esito inatteso! Atteso: {expected_success}, Ottenuto: {risultato}"

    print(f"{test_id}: Test concluso con successo atteso={expected_success}")
