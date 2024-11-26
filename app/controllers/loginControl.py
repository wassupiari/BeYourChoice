from flask import Blueprint, request, jsonify
from app.models.studenteModel import StudenteModel
import bcrypt
import re

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

        if not re.match(email_regex, email):
            return jsonify({"error": "Formato email non valido!"}), 400

        if not re.match(password_regex, password):
            return jsonify({"error": "Formato password non valido!"}), 400

        # Crea un'istanza del modello StudenteModel per interagire con il database
        studente_model = StudenteModel()

        # Cerca lo studente con l'email fornita
        studente = studente_model.trova_studente(email)

        if studente:
            # Verifica se la password fornita corrisponde a quella nel database
            if bcrypt.checkpw(password.encode('utf-8'), studente['password']):
                return jsonify({"message": "Login effettuato con successo!"})
            else:
                return jsonify({"error": "Password errata!"}), 401
        else:
            return jsonify({"error": "Utente non trovato!"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
