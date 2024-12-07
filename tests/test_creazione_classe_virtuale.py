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

# Test 1: Nome della classe con lunghezza non valida
@pytest.mark.parametrize("test_id", ["TC_CCV_1_1"])
def test_nome_classe_lunghezza_non_valida(classe_virtuale_model, test_id):
        nome_classe = "5"
        descrizione = "La miglior classe"
        id_docente = "121212"
        risultato = classe_virtuale_model.creazioneClasseVirtuale(nome_classe, descrizione, id_docente)
        assert risultato is False, "Lunghezza del nome della classe virtuale non corretta"


# Test 2: Nome classe con formato non valido
@pytest.mark.parametrize("test_id", ["TC_CCV_1_2"])
def test_nome_classe_formato_non_valido(classe_virtuale_model, test_id):
        nome_classe = "Classe 5°D"
        descrizione = "La miglior classe"
        id_docente = "121212"
        risultato = classe_virtuale_model.creazioneClasseVirtuale(nome_classe, descrizione, id_docente)
        assert risultato is False, "Formato del nome della classe virtuale non corretta”."

# Test 3: Descrizione con lunghezza non valida
@pytest.mark.parametrize("test_id", ["TC_CCV_1_3"])
def test_descrizione_lunghezza_non_valida(classe_virtuale_model, test_id):
        nome_classe = "Classe 5D"
        descrizione = "A"
        id_docente = "121212"
        risultato = classe_virtuale_model.creazioneClasseVirtuale(nome_classe, descrizione, id_docente)
        assert risultato is False, "Lunghezza della descrizione della classe virtuale non corretta."

# Test 4: Descrizione con formato non valido
@pytest.mark.parametrize("test_id", ["TC_CCV_1_4"])
def test_descrizione_formato_non_valido(classe_virtuale_model, test_id):
    nome_classe = "Classe 5D"
    descrizione = "L§ mia classe"
    id_docente = "121212"
    risultato = classe_virtuale_model.creazioneClasseVirtuale(nome_classe, descrizione, id_docente)
    assert risultato is False, "Formato della descrizione della classe non corretto"


# Test 5: Creazione della classe virtuale con successo
@pytest.mark.parametrize("test_id", ["TC_CCV_1_5"])
def test_creazione_classe_successo(classe_virtuale_model, test_id):
    nome_classe = "Classe 5D"
    descrizione = "La miglior classe"
    id_docente = "121212"

    risultato = classe_virtuale_model.creazioneClasseVirtuale(nome_classe, descrizione, id_docente)
    assert risultato is True, "Creazione della classe virtuale fallita"
    print(f"Test {test_id}: Classe virtuale creata")
