from flask import Blueprint, request, jsonify, session, redirect, url_for, flash
from app.models.studenteModel import StudenteModel
import bcrypt
import re, os

# Crea un Blueprint per la gestione del login
login_bp = Blueprint('login', __name__)


# Crea una rotta per il login
@login_bp.route('/login', methods=['POST'])
def login_studente():
    try:
        # Recupera i dati dal form HTML
        email = request.form['email']
        password = request.form['password']

        email_regex = r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$"
        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=])[A-Za-z\d@#$%^&+=]{8,20}$"

        # Controllo formato email
        if not re.match(email_regex, email):
            return redirect(url_for('login', error='password'))

            # Controllo della password (minimo 8 caratteri)
        if not re.match(password_regex, password):
            return redirect(url_for('login', error='password'))

        # Crea un'istanza del modello StudenteModel per interagire con il database
        studente_model = StudenteModel()

        # Cerca lo studente con l'email fornita
        studente = studente_model.trova_studente(email)

        if studente:
            # Verifica se la password fornita corrisponde a quella nel database
            if bcrypt.checkpw(password.encode('utf-8'), studente['password']):
                session['email'] = email
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login', error='password'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route per ottenere i dati della sessione
@login_bp.route('/profile', methods=['POST'])
def profile():
    if 'email' in session:
        email = session['email']
        return f'Profilo di {email}'
    else:
        return redirect(url_for('login.home'))

# Route per terminare la sessione (logout)
@login_bp.route('/logout', methods=['POST'])
def logout():
    if 'email' in session:
        session.pop('email', None)
        return redirect(url_for('home'))
    else:
        return jsonify({"error": "Nessuna sessione attiva o utente già disconnesso!"}), 401