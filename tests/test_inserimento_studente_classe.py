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
    id_studente = ""
    id_classe = 10541

    risultato = classe_virtuale_model.aggiungi_studente_classe(id_studente, id_classe)
    assert risultato is False, "Studente aggiunto alla classe virtuale”."

# Test 2:
@pytest.mark.parametrize("test_id", ["TC_GCV_2_2"])
def test_aggiungi_studente_successp(classe_virtuale_model,test_id):
    id_studente = "675432b468ea2d008264cfc2"
    id_classe = 10541

    risultato = classe_virtuale_model.aggiungi_studente_classe(id_studente, id_classe)
    assert risultato is True, "Nessuno studente selezionato”."




