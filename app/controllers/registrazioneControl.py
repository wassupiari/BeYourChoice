import re

from flask import Blueprint, request, jsonify
from app.models.studenteModel import StudenteModel

# Crea un Blueprint
registrazione_bp = Blueprint('registrazione', __name__)

# Crea una rotta per la registrazione
@registrazione_bp.route('/register', methods=['POST'])
def registra_studente():
    try:
        nome = request.form['nome']
        cognome = request.form['cognome']
        sda = request.form['sda']
        email = request.form['email']
        cf = request.form['cf']
        data_nascita = request.form['data-nascita']
        password = request.form['password']

        email_regex = r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$"
        nome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        cognome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        sda_regex = r"^[A-Za-z0-9À-ù'’\- ]{2,50}$"
        cf_regex = r"^[A-Z]{6}[0-9]{2}[A-EHLMPR-T][0-9]{2}[A-Z0-9]{4}[A-Z]$"
        data_nascita_regex = r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,20}$"

        # Controllo formato email
        if not re.match(email_regex, email):
            return jsonify({"error": "Formato email non valido!"}), 400

        # Controllo formato nome
        if not re.match(nome_regex, nome):
            return jsonify({"error": "Formato nome non valido!"}), 400

        # Controllo formato cognome
        if not re.match(cognome_regex, cognome):
            return jsonify({"error": "Formato cognome non valido!"}), 400

        # Controllo formato SDA
        if not re.match(sda_regex, sda):
            return jsonify({"error": "Formato SDA non valido!"}), 400

        # Controllo formato codice fiscale
        if not re.match(cf_regex, cf) or cf is None:
            return jsonify({"error": "Formato codice fiscale non valido!"}), 400

        # Controllo formato data di nascita
        if not re.match(data_nascita_regex, data_nascita):
            return jsonify({"error": "Formato data di nascita non valido!"}), 400

        # Controllo della password (minimo 8 caratteri)
        if not re.match(password_regex, password):
                return jsonify({"error": "Formato password non valido!"}), 400

        studente_dict = {
            "nome": nome,
            "cognome": cognome,
            "sda": sda,
            "email": email,
            "cf": cf,
            "data_nascita": data_nascita,
            "password": password
        }

        studente_model = StudenteModel()
        studente_model.aggiungi_studente(studente_dict)

        return jsonify({"message": "Registrazione completata con successo!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def registra_docente():
        try:
            nomeD = request.form['nome']
            cognomeD = request.form['cognome']
            sdaD = request.form['sda']
            emailD = request.form['email']
            cfD = request.form['cf']
            data_nascitaD = request.form['data-nascita']
            passwordD = request.form['password']
            codice_univoco = request.form['codice_univoco']

            email_regex = r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$"
            nome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
            cognome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
            sda_regex = r"^[A-Za-z0-9À-ù'’\- ]{2,50}$"
            cf_regex = r"^[A-Z]{6}[0-9]{2}[A-EHLMPR-T][0-9]{2}[A-Z0-9]{4}[A-Z]$"
            data_nascita_regex = r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"
            password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,20}$"

            # Controllo formato email
            if not re.match(email_regex, emailD):
                return jsonify({"error": "Formato email non valido!"}), 400

            # Controllo formato nome
            if not re.match(nome_regex, nomeD):
                return jsonify({"error": "Formato nome non valido!"}), 400

            # Controllo formato cognome
            if not re.match(cognome_regex, cognomeD):
                return jsonify({"error": "Formato cognome non valido!"}), 400

            # Controllo formato SDA
            if not re.match(sda_regex, sdaD):
                return jsonify({"error": "Formato SDA non valido!"}), 400

            # Controllo formato codice fiscale
            if not re.match(cf_regex, cfD) or cfD is None:
                return jsonify({"error": "Formato codice fiscale non valido!"}), 400

            # Controllo formato data di nascita
            if not re.match(data_nascita_regex, data_nascitaD):
                return jsonify({"error": "Formato data di nascita non valido!"}), 400

            # Controllo della password (minimo 8 caratteri)
            if not re.match(password_regex, passwordD):
                return jsonify({"error": "Formato password non valido!"}), 400

            docente_dict = {
                "nome": nomeD,
                "cognome": cognomeD,
                "sda": sdaD,
                "email": emailD,
                "cf": cfD,
                "data_nascita": data_nascitaD,
                "password": passwordD,
                "codice_univoco": codice_univoco
            }

            docente_model = StudenteModel()
            docente_model.aggiungi_docente(docente_dict)

            return jsonify({"message": "Registrazione completata con successo!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
