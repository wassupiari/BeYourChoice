from functools import wraps
from flask import Blueprint, request, jsonify, session, redirect, url_for, flash, render_template
import bcrypt
import re
import uuid
from app.models.docenteModel import DocenteModel
from app.models.studenteModel import StudenteModel

# Crea un Blueprint per la gestione del login
login_bp = Blueprint('login', __name__)


# Decoratore per proteggere le rotte degli studenti
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or 'session_token' not in session:
            flash("Devi effettuare il login per accedere", "error")
            return redirect(url_for('login.login'))  # Se non è loggato, redirige al login

        # Verifica se è uno studente
        studente_model = StudenteModel()
        studente = studente_model.trova_studente(session['email'])

        if studente is None:  # Se l'email non corrisponde a uno studente
            flash("Accesso negato: questa area è riservata agli studenti", "error")
            return redirect(url_for('home'))  # Redirige l'utente alla home

        return f(*args, **kwargs)

    return decorated_function


# Decoratore per proteggere le rotte dei docenti
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session or 'session_token' not in session:
            flash("Devi effettuare il login per accedere", "error")
            return redirect(url_for('login.login'))  # Se non è loggato, redirige al login

        # Verifica se è un docente
        docente_model = DocenteModel()
        docente = docente_model.trova_docente(session['email'])

        if docente is None:  # Se l'email non corrisponde a un docente
            flash("Accesso negato: questa area è riservata ai docenti", "error")
            return redirect(url_for('home'))  # Redirige l'utente alla home

        print("Docente trovato:", docente)  # Aggiungi una stampa di debug per vedere se il docente è trovato
        return f(*args, **kwargs)

    return decorated_function


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'GET':
            return render_template('registrazioneLogin.html')  # Template di login

        email = request.form['email']
        password = request.form['password']

        email_regex = r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$"
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,20}$"

        # Controllo formato email
        if not re.match(email_regex, email):
            flash("Formato email non valido", "error")
            return redirect(url_for('login.login'))

        # Controllo della password (minimo 8 caratteri)
        if not re.match(password_regex, password):
            flash("Password non valida", "error")
            return redirect(url_for('login.login'))

        studente_model = StudenteModel()
        docente_model = DocenteModel()

        studente = studente_model.trova_studente(email)
        docente = docente_model.trova_docente(email)

        if studente:
            # Verifica la password per lo studente
            if bcrypt.checkpw(password.encode('utf-8'), studente['password']):
                session_token = str(uuid.uuid4())
                session['email'] = email
                session['session_token'] = session_token


                cf_studente = studente.get("cf")
                nome_studente = studente.get("nome")

                if studente.get("id_classe"):  # Se "ID_Classe" è presente e ha un valore
                    id_classe = studente["id_classe"]
                else:
                    # Se "ID_Classe" non esiste, assegniamo 0 (oppure il valore dalla sessione, se necessario)
                    id_classe = session.get("id_classe", 0)

                print(id_classe)


                session['cf'] = cf_studente
                session['id_classe'] = id_classe
                session['nome'] = nome_studente
                session['role'] = 'studente'
                flash("Login effettuato con successo", "success")
                return redirect(url_for('dashboard.dashboard_studente'))  # Reindirizza al dashboard dopo il login

            else:
                flash("Password errata", "error")
                return redirect(url_for('login.login'))

        elif docente:
            # Verifica la password per il docente
            if bcrypt.checkpw(password.encode('utf-8'), docente['password']):
                docente_scuola_appartenenza = docente.get("sda")
                docente_codice_univoco = docente.get("codice_univoco")
                nome_profilo = docente.get("nome")

                session_token = str(uuid.uuid4())
                session['email'] = email
                session['session_token'] = session_token
                session['sda'] = docente_scuola_appartenenza
                session['cu'] = docente_codice_univoco
                session['nome'] = nome_profilo
                session['cf'] = docente.get("cf")
                session['role'] = 'docente'

                flash("Login effettuato con successo", "success")
                return redirect(url_for('dashboard.dashboard_docente'))  # Reindirizza al dashboard dopo il login

            else:
                flash("Password errata", "error")
                return redirect(url_for('login.login'))

        else:
            flash("Email non registrata", "error")
            return redirect(url_for('login.login'))

    except Exception as e:
        flash(f"Errore interno: {str(e)}", "error")
        return jsonify({"error": str(e)}), 500


# Route per terminare la sessione (logout)
@login_bp.route('/logout', methods=['POST'])
def logout():
    if 'email' in session:
        # Pulisce la sessione e disconnette l'utente
        session.pop('email', None)
        session.pop('id_classe',None)
        session.pop('session_token', None)
        session.pop('sda', None)
        session.pop('cu', None)
        session.pop('nome', None)
        session.pop('cf', None)
        session.pop('role', None)

        flash("Sei stato disconnesso", "success")
        return redirect(url_for('login.login'))
    else:
        flash("Nessuna sessione attiva", "error")
        return jsonify({"error": "Nessuna sessione attiva o utente già disconnesso!"}), 401