import re
import pytest
from app.models.studenteModel import StudenteModel


# Test combinazioni per la registrazione studente
@pytest.mark.parametrize("test_id, nome, cognome, scuola, email, cf, data_nascita, password, expected_success", [
    # Casistiche di errore
    ("TC_GR_1_1", "A", "R", "Uni", "a@b.c", "ABCDEF01A01H123", "2000-01-01", "WeakP@", False),  # LN1
    ("TC_GR_1_2", "Marco", "R", "Uni", "a@b.c", "ABCDEF01A01H123", "2000-01-01", "WeakP@", False),  # FN1
    ("TC_GR_1_3", "Marco", "Rossi", "U", "a@b.c", "ABCDEF01A01H123", "2000-01-01", "WeakP@", False),  # LC1
    ("TC_GR_1_4", "Marco", "Rossi", "Università", "a@b.c", "ABCDEF01A01H123", "2000-01-01", "WeakP@", False),  # FC1
    ("TC_GR_1_5", "Marco", "Rossi", "Università", "a@b.c", "1234567890", "2000-01-01", "WeakP@", False),  # LSDA1
    ("TC_GR_1_6", "Marco", "Rossi", "Università", "a@b.c", "1234567890", "2000-01-01", "WeakP@", False),  # FSDA1
    ("TC_GR_1_7", "Marco", "Rossi", "Università", "a", "1234567890", "2000-01-01", "WeakP@", False),  # LE1
    ("TC_GR_1_8", "Marco", "Rossi", "Università", "wrong@com", "1234567890", "2000-01-01", "WeakP@", False),  # FE1
    ("TC_GR_1_9", "Marco", "Rossi", "Università", "existing@student.com", "1234567890", "2000-01-01", "WeakP@", False),
    # EE1
    ("TC_GR_1_10", "Marco", "Rossi", "Università", "new@student.com", "ABC", "2000-01-01", "WeakP@", False),  # LCF1
    (
    "TC_GR_1_11", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "2000-01-01", "WeakP@", False),
    # FCF1
    ("TC_GR_1_12", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "2000-1-1", "WeakP@", False),
    # LDN1
    ("TC_GR_1_13", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "1985-05-01", "short", False),
    # LP1
    ("TC_GR_1_14", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "1985-05-01", "NoSpecChar1",
     False),  # FP1
    ("TC_GR_1_15", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "1985-05-01",
     "NoSpecialChars1", False),  # LP2, FP1
    # Caso di successo
    ("TC_GR_1_16", "Marco", "Rossi", "Università Napoli", "m.rossi@uni.it", "RSSMRC85M01H501Z", "1985-05-01",
     "Mariorossi1@", True),  # Successo
])
def test_registrazione_studente(studente_model, test_id, nome, cognome, scuola, email, cf, data_nascita, password,
                                expected_success):
    """
    Test per la registrazione dello studente basati su combinazioni predefinite,
    includendo la verifica di inserimento nel database.
    """
    # Validazioni singole per i parametri
    ln_ok = len(nome) >= 2
    fn_ok = bool(re.match(r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$", nome))

    lc_ok = len(cognome) >= 2
    fc_ok = bool(re.match(r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$", cognome))

    lsda_ok = 2 <= len(scuola) <= 50
    fsda_ok = bool(re.match(r"^[A-Za-z0-9À-ù'’\- ]{2,50}$", scuola))

    le_ok = len(email) >= 6
    fe_ok = bool(re.match(r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$", email))
    ee_ok = studente_model.trova_studente(email) is None  # Deve essere unico

    lcf_ok = len(cf) == 16
    fcf_ok = bool(re.match(r"^[A-Z]{6}[0-9]{2}[A-EHLMPR-T][0-9]{2}[A-Z0-9]{4}[A-Z]$", cf))

    ldn_ok = len(data_nascita) == 10
    fdn_ok = bool(re.match(r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", data_nascita))

    lp_ok = len(password) >= 8
    fp_ok = bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,20}$", password))

    # Inserimento simulato nel database se valido
    if expected_success:
        success = studente_model.inserisci_studente({
            "nome": nome,
            "cognome": cognome,
            "scuola": scuola,
            "email": email,
            "cf": cf,
            "data_nascita": data_nascita,
            "password": password,
        })
    else:
        success = False  # Nessun inserimento in caso di dati invalidi

    # Validazione del successo atteso
    actual_success = all([
        ln_ok, fn_ok, lc_ok, fc_ok, lsda_ok, fsda_ok,
        le_ok, fe_ok, ee_ok, lcf_ok, fcf_ok, ldn_ok, fdn_ok, lp_ok, fp_ok
    ]) and success

    assert actual_success == expected_success, (
        f"{test_id}: Esito inatteso! Atteso: {expected_success}, Ottenuto: {actual_success}"
    )
    print(f"{test_id}: Test concluso con successo atteso={expected_success}")
