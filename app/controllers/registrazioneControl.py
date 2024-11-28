import re
from flask import Blueprint, request, jsonify, redirect, url_for
from app.models.studenteModel import StudenteModel  # Assumendo che StudenteModel gestisca entrambi
from app.models.docenteModel import DocenteModel

# Crea un Blueprint
registrazione_bp = Blueprint('registrazione', __name__)

# Crea una rotta per la registrazione
@registrazione_bp.route('/register', methods=['POST'])
def registra():
    try:
        # Raccoglie i dati dal form
        nome = request.form['nome']
        cognome = request.form['cognome']
        sda = request.form['sda']
        email = request.form['email']
        cf = request.form['cf']
        data_nascita = request.form['data-nascita']
        password = request.form['password']
        codice_univoco = request.form.get('codice_univoco')  # Questo campo potrebbe non esistere

        # Regex comuni
        email_regex = r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$"
        nome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        cognome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        sda_regex = r"^[A-Za-z0-9À-ù'’\- ]{2,50}$"
        cf_regex = r"^[A-Z]{6}[0-9]{2}[A-EHLMPR-T][0-9]{2}[A-Z0-9]{4}[A-Z]$"
        data_nascita_regex = r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s])[A-Za-z\d!@#$%^&*()\-_=+\[\]{};:,.<>?/\\|~]{8,20}$"
        codiceUnivoco_regex = r"^\d{6,6}$"

        # Controlli generali
        if not re.match(email_regex, email):
            return redirect(url_for('login', error='formatoEmail'))

        if not re.match(nome_regex, nome):
            return redirect(url_for('login', error='formatoNome'))

        if not re.match(cognome_regex, cognome):
            return redirect(url_for('login', error='formatoCognome'))

        if not re.match(sda_regex, sda):
            return redirect(url_for('login', error='formatoSDA'))

        if not re.match(cf_regex, cf):
            return redirect(url_for('login', error='formatocf'))

        if not re.match(data_nascita_regex, data_nascita):
            return redirect(url_for('login', error='formatoDataNascita'))

        if not re.match(password_regex, password):
            return redirect(url_for('login', error='formatoPassword'))

        if not codice_univoco is None:
            if not re.match(codiceUnivoco_regex, codice_univoco):
                return redirect(url_for('login', error='formatoCU'))

        # Differenzia la registrazione: studente o docente
        if codice_univoco:  # Se è presente, registra come docente
            docente_dict = {
                "nome": nome,
                "cognome": cognome,
                "sda": sda,
                "email": email,
                "cf": cf,
                "data_nascita": data_nascita,
                "password": password,
                "codice_univoco": codice_univoco
            }

            docente_model = DocenteModel()
            docente_model.aggiungi_docente(docente_dict)
            return redirect(url_for('home'))
        else:  # Altrimenti, registra come studente
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
            stud = studente_model.trova_studente(email)
            stud2 = studente_model.trova_studente(cf)
            if stud is not None and stud2 is not None:
                studente_model.aggiungi_studente(studente_dict)
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login', error='AlreadyRegistered'))


    except Exception as e:
        return jsonify({"error": str(e)}), 500
