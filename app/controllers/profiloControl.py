import base64
import logging

import bcrypt
from flask import flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash


class ProfiloControl:
    def __init__(self, db_manager):
        self.docente_collection = db_manager.get_collection('Docente')
        self.studente_collection = db_manager.get_collection('Studente')

    def get_profilo_studente(self, email):
        try:
            query = {"email": email}
            profilo_studente = list(self.studente_collection.find(query))
            return profilo_studente
        except Exception as e:
            logging.error(f"Errore nel recuperare il profilo dello studente dall'email {email}: {str(e)}")
            return []

    def get_profilo_docente(self, email):
        try:
            query = {"email": email}
            profilo_docente = list(self.docente_collection.find(query))
            return profilo_docente
        except Exception as e:
            logging.error(f"Errore nel recuperare il profilo del docente dall'email {email}: {str(e)}")
            return []

    def update_profilo_studente(self, email, nuovi_dati):
        try:
            result = self.studente_collection.update_one({"email": email}, {"$set": nuovi_dati})
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Errore nell'aggiornare il profilo dello studente per l'email {email}: {str(e)}")
            return False

    def update_profilo_docente(self, email, nuovi_dati):
        try:
            result = self.docente_collection.update_one({"email": email}, {"$set": nuovi_dati})
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Errore nell'aggiornare il profilo del docente per l'email {email}: {str(e)}")
            return False

    def decode_base64(self, data):
        if not data:
            raise ValueError("Nessun dato fornito per la decodifica.")

        missing_padding = len(data) % 4
        if missing_padding:
            data += '=' * (4 - missing_padding)

        try:
            # Decodifica base64
            decoded_data = base64.b64decode(data)

            # Tentativo di decodifica UTF-8
            try:
                return decoded_data.decode('utf-8')
            except UnicodeDecodeError as e:
                logging.error(f"Decodifica UTF-8 non riuscita: {e}. Dati problematici: {decoded_data}")
                raise ValueError("Decodifica base64 riuscita, ma i dati non sono UTF-8. Verifica l'origine dei dati.")
        except base64.binascii.Error as e:
            logging.error(f"Errore durante la decodifica base64: {e}")
            raise ValueError(f"Errore durante la decodifica base64: {e}")

    def modifica_password(self, old_password_encoded, new_password_encoded):
        try:
            old_password = self.decode_base64(old_password_encoded)
            new_password = self.decode_base64(new_password_encoded)
        except ValueError as e:
            logging.error(f"Errore decodifica password: {e}")
            return {'error': str(e)}

        try:
            session_email = session.get('email')
            if not session_email:
                logging.error('Email non trovata nella sessione.')
                return jsonify({'error': 'Email non valida.'}), 400

            user_email = session_email.lower()
            user = self.docente_collection.find_one({'email': user_email})

            if user is None:
                flash('Utente non trovato.', 'error')
                return jsonify({'error': 'Utente non trovato.'}), 404

            if not bcrypt.checkpw(old_password.encode('utf-8'), user['password']):
                return {'error': 'La vecchia password non è corretta.'}

            new_password_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            result = self.docente_collection.update_one(
                {'email': user_email},
                {'$set': {'password': new_password_hashed}}
            )
        except Exception as e:
            logging.error(f'Errore durante il cambio della password per l\'utente {user_email}: {str(e)}')
            return jsonify({'error': f'Errore durante il cambio della password.'}), 500
