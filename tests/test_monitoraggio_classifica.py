from contextlib import nullcontext

import pytest
from app.models.quizModel import QuizModel

# Fixture per il modello ClasseVirtuale
@pytest.fixture
def qui_model():
    return QuizModel()
@pytest.mark.parametrize("test_id", ["TC_MC_2_1"])
def test_aggiungi_attivita_studente(qui_model,test_id):
    risultato_quiz = 0
    cf_studente =
    punteggio =

    risultato = qui_model.salva_risultato_quiz((risultato_quiz, cf_studente, punteggio)
    assert risultato is False, "Studente aggiunto alla classe virtuale”."

# Test 2:
@pytest.mark.parametrize("test_id", ["TC_MC_2_2"])
def test_aggiungi_studente_successp(classe_virtuale_model,test_id):
    studente_id = "675432b468ea2d008264cfc2"
    classe_id = 10541

    risultato = classe_virtuale_model.aggiungi_studente_classe(studente_id, classe_id)
    assert risultato is True, "Nessuno studente selezionato”."




