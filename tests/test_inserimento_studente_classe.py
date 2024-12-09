from contextlib import nullcontext

import pytest
from app.models.classeVirtualeModel import ClasseVirtuale

# Fixture per il modello ClasseVirtuale
@pytest.fixture
def classe_virtuale_model():
    return ClasseVirtuale()
import pytest
from app.models.classeVirtualeModel import ClasseVirtuale

# Fixture per il modello ClasseVirtuale
@pytest.fixture
def classe_virtuale_model():
    return ClasseVirtuale()

# Test 1:
@pytest.mark.parametrize("test_id", ["TC_GCV_2_1"])
def test_aggiungi_studente_fallimento(classe_virtuale_model,test_id):
    studente_id = ""
    classe_id = 10541

    risultato = classe_virtuale_model.aggiungi_studente_classe(studente_id, classe_id)
    assert risultato is False, "Studente aggiunto alla classe virtuale”."

# Test 2:
@pytest.mark.parametrize("test_id", ["TC_GCV_2_2"])
def test_aggiungi_studente_successp(classe_virtuale_model,test_id):
    studente_id = "675432b468ea2d008264cfc2"
    classe_id = 10541

    risultato = classe_virtuale_model.aggiungi_studente_classe(studente_id, classe_id)
    assert risultato is True, "Nessuno studente selezionato”."




