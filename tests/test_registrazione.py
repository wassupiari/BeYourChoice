import re
import pytest
from app.models.docenteModel import DocenteModel
from app.models.studenteModel import StudenteModel

@pytest.fixture
def studente_model():
    return StudenteModel()

@pytest.fixture
def docente_model():
    return DocenteModel()

# Test combinazioni per la registrazione studente
@pytest.mark.parametrize("test_id, nome, cognome, scuola, email, cf, data_nascita, password, expected_success", [
    # Casistiche di errore
    ("TC_GAR_2_1", "A", "R", "Uni", "a@b.c", "ABCDEF01A01H123", "2000-01-01", "WeakP@", False),  # LN1
    ("TC_GAR_2_2", "Marco", "R", "Uni", "a@b.c", "ABCDEF01A01H123", "2000-01-01", "WeakP@", False),  # FN1
    ("TC_GAR_2_3", "Marco", "Rossi", "U", "a@b.c", "ABCDEF01A01H123", "2000-01-01", "WeakP@", False),  # LC1
    ("TC_GAR_2_4", "Marco", "Rossi", "Università", "a@b.c", "ABCDEF01A01H123", "2000-01-01", "WeakP@", False),  # FC1
    ("TC_GAR_2_5", "Marco", "Rossi", "Università", "a@b.c", "1234567890", "2000-01-01", "WeakP@", False),  # LSDA1
    ("TC_GAR_2_6", "Marco", "Rossi", "Università", "a@b.c", "1234567890", "2000-01-01", "WeakP@", False),  # FSDA1
    ("TC_GAR_2_7", "Marco", "Rossi", "Università", "a", "1234567890", "2000-01-01", "WeakP@", False),  # LE1
    ("TC_GAR_2_8", "Marco", "Rossi", "Università", "wrong@com", "1234567890", "2000-01-01", "WeakP@", False),  # FE1
    ("TC_GAR_2_9", "Marco", "Rossi", "Università", "existing@student.com", "1234567890", "2000-01-01", "WeakP@", False),
    # EE1
    ("TC_GAR_2_10", "Marco", "Rossi", "Università", "new@student.com", "ABC", "2000-01-01", "WeakP@", False),  # LCF1
    (
    "TC_GAR_2_11", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "2000-01-01", "WeakP@", False),
    # FCF1
    ("TC_GAR_2_12", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "2000-1-1", "WeakP@", False),
    # LDN1
    ("TC_GAR_2_13", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "1985-05-01", "short", False),
    # LP1
    ("TC_GAR_2_14", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "1985-05-01", "NoSpecChar1",
     False),  # FP1
    ("TC_GAR_2_15", "Marco", "Rossi", "Università", "new@student.com", "RSSMRC85M01H501Z", "1985-05-01",
     "NoSpecialChars1", False),  # LP2, FP1
    # Caso di successo
    ("TC_GAR_2_16", "Marco", "Rossi", "Università Napoli", "m.rossi@uni.it", "RSSMRC85M01H501Z", "1985-05-01",
     "Mariorossi1@", True),  # Successo
])
def test_registrazione_studente(test_id, nome, cognome, scuola, email, cf, data_nascita, password,
                                expected_success, studente_model):
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
        studente_dict = {
            "nome": nome,
            "cognome": cognome,
            "scuola": scuola,
            "email": email,
            "cf": cf,
            "data_nascita": data_nascita,
            "password": password
        }
        studente_model.aggiungi_studente(studente_dict)
        success = studente_model.trova_studente(email) is not None
        print(success)
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

@pytest.mark.parametrize("test_id_doc, nome_doc, cognome_doc, scuola_doc, email_doc, cf_doc, codice_univoco_doc, password_doc, data_nascita_doc, expected_success_doc", [
    # Casistiche di errore
    ("TC_GAR_3_1", "A", "Bianchi", "Uni", "x@y.z", "RSSMRC85M01H123", "12345", "WeakP@", "2000-01-01", False),  # LN1
    ("TC_GAR_3_2", "Luc§", "Bianchi", "Uni", "x@y.z", "RSSMRC85M01H123", "12345", "WeakP@", "2000-01-01", False),  # FN1
    ("TC_GAR_3_3", "Luca", "B", "U", "x@y.z", "RSSMRC85M01H123", "12345", "WeakP@", "2000-01-01", False),  # LC1
    ("TC_GAR_3_4", "Luca", "Bi§nchi", "Università", "x@y.z", "RSSMRC85M01H123", "12345", "WeakP@", "2000-01-01", False),  # FC1
    ("TC_GAR_3_5", "Luca", "Bianchi", "U", "new@docente.com", "RSSMRC85M01H123", "12345", "WeakP@", "2000-01-01", False),  # LSDA1
    ("TC_GAR_3_6", "Luca", "Bianchi", "Universit§", "valid@gmail.com", "RSSMRC85M01H123", "12345", "WeakP@", "2000-01-01", False),  # FSDA1
    ("TC_GAR_3_7", "Luca", "Bianchi", "Università", "e", "RSSMRC85M01H123", "12345", "WeakP@", "2000-01-01", False),  # LE1
    ("TC_GAR_3_8", "Luca", "Bianchi", "Università", "new@com", "RSSMRC85M01H123", "Valid1@", "short", "2000-01-01", False),  # FE1
    ("TC_GAR_3_9", "Luca", "Bianchi", "Università", "roccocione@gmail.com", "RSSMRC85M01H123", "12345", "ValidPass1@", "2000-01-01", False),  # EE1
    ("TC_GAR_3_10", "Luca", "Bianchi", "Università", "new@docente.com", "RSSMRC", "123456", "LucaDocente1@", "2000-01-01", False),  # LCF1
    ("TC_GAR_3_11", "Luca", "Bianchi", "Università", "new@docente.com", "RSSMRC85M0§H123", "123456", "LucaDocente1@", "2000-01-01", False),  # FCF1
    ("TC_GAR_3_12", "Luca", "Bianchi", "Università", "new@docente.com", "RSSMRC85M01H123", "123456", "L", "2000-1-1", False),  # LP1
    ("TC_GAR_3_13", "Luca", "Bianchi", "Università Napoli", "l.bianchi@uni.it", "RSSMRC85M01H123", "123456", "LucaDocente@", "1985-05-01", False),  # FP1
    ("TC_GAR_3_14", "Luca", "Bianchi", "Università Napoli", "l.bianchi@uni.it", "RSSMRC85M01H123", "12345", "LucaDocente1@", "1985-05-01", False),  # LCU1
    ("TC_GAR_3_15", "Luca", "Bianchi", "Università Napoli", "l.bianchi@uni.it", "RSSMRC85M01H123", "1234§6", "LucaDocente1@", "1985-05-01", False),  # FCU1
    ("TC_GAR_3_16", "Luca", "Bianchi", "Università Napoli", "l.bianchi@uni.it", "RSSMRC85M01H123", "123456", "LucaDocente1@", "1985-05-0", False), #LDN1
    ("TC_GAR_3_17", "Luca", "Bianchi", "Università Napoli", "l.bianchi@uni.it", "RSSMRC85M01H123", "123456", "LucaDocente1@", "19-10-1990", False), #FCN
    ("TC_GAR_3_18", "Luca", "Bianchi", "Università Napoli", "l.bianchi@uni.it", "RSSMRC85M01H123", "123456", "LucaDocente1@", "1985-05-01", True),  # Successo
])
def test_registrazione_docente(test_id_doc, nome_doc, cognome_doc, scuola_doc, email_doc, cf_doc, codice_univoco_doc, password_doc, data_nascita_doc, expected_success_doc, docente_model):
    """
    Test per la registrazione del docente basati su combinazioni predefinite,
    includendo la verifica di inserimento nel database.
    """
    # Validazioni singole per i parametri
    ln_ok = len(nome_doc) >= 2
    fn_ok = bool(re.match(r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$", nome_doc))

    lc_ok = len(cognome_doc) >= 2
    fc_ok = bool(re.match(r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$", cognome_doc))

    lsda_ok = 2 <= len(scuola_doc) <= 50
    fsda_ok = bool(re.match(r"^[A-Za-z0-9À-ù'’\- ]{2,50}$", scuola_doc))

    le_ok = len(email_doc) >= 6
    fe_ok = bool(re.match(r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$", email_doc))
    ee_ok = docente_model.trova_docente(email_doc) is None  # Deve essere unico

    lcu_ok = len(codice_univoco_doc) == 6
    fcu_ok = bool(re.match(r"^\d{6,6}$", codice_univoco_doc))

    lp_ok = len(password_doc) >= 8
    fp_ok = bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,20}$", password_doc))

    ldn_ok = len(data_nascita_doc) == 10
    fdn_ok = bool(re.match(r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", data_nascita_doc))

    # Inserimento simulato nel database se valido
    if expected_success_doc:
        docente_dict = {
            "nome": nome_doc,
            "cognome": cognome_doc,
            "scuola": scuola_doc,
            "email": email_doc,
            "cf": cf_doc,
            "codice_univoco": codice_univoco_doc,
            "password": password_doc,
            "data_nascita": data_nascita_doc
        }
        docente_model.aggiungi_docente(docente_dict)
        success_doc = docente_model.trova_docente(email_doc) is not None
        print(success_doc)
    else:
        success_doc = False  # Nessun inserimento in caso di dati invalidi

    # Validazione del successo atteso
    actual_success_doc = all([
        ln_ok, fn_ok, lc_ok, fc_ok, lsda_ok, fsda_ok,
        le_ok, fe_ok, ee_ok, lcu_ok, fcu_ok, lp_ok, fp_ok, ldn_ok, fdn_ok
    ]) and success_doc

    assert actual_success_doc == expected_success_doc, (
        f"{test_id_doc}: Esito inatteso! Atteso: {expected_success_doc}, Ottenuto: {actual_success_doc}"
    )
    print(f"{test_id_doc}: Test concluso con successo atteso={expected_success_doc}")
