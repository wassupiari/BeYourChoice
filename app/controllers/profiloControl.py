import base64
import logging
from flask import flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


class ProfiloControl:
    def __init__(self, db_manager):
        self.docente_collection = db_manager.get_collection('Docente')
        self.studente_collection = db_manager.get_collection('Studente')
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





def decode_base64_password(stored_password_binary):
    # Decodifica la password Base64
    decoded_bytes = base64.b64decode(stored_password_binary)
    # Converti i bytes decodificati in una stringa, supponendo sia una stringa UTF-8
    decoded_password = decoded_bytes.decode('utf-8')
    return decoded_password




def cambiapassword(self, email, old_password, new_password):
    try:
        if not email:
            flash('Email non valida.', 'error')
            return jsonify({'error': 'Email non valida.'}), 400

        user_email = email.lower()
        user = self.docente_collection.find_one({'email': user_email})

        if user is None:
            flash('Utente non trovato.', 'error')
            return jsonify({'error': 'Utente non trovato.'}), 404

        stored_password_binary = user['password']

        try:
            stored_password_hash = decode_base64_password(stored_password_binary)
        except Exception as e:
            flash(f'Errore durante la decodifica della password: {str(e)}', 'error')
            return jsonify({'error': f'Errore durante la decodifica della password: {str(e)}'}), 500

        if check_password_hash(stored_password_hash, old_password):
            new_password_hash = generate_password_hash(new_password)
            new_password_binary = base64.b64encode(new_password_hash.encode('utf-8'))

            result = self.docente_collection.update_one(
                {'email': user_email},
                {'$set': {'password': new_password_binary}}
            )
            if result.modified_count > 0:
                flash('Password cambiata con successo!', 'success')
                return jsonify({'message': 'Password cambiata con successo!'}), 200
            else:
                flash('Errore nella modifica della password.', 'error')
                return jsonify({'error': 'Errore nella modifica della password.'}), 500
        else:
            flash('Vecchia password errata.', 'error')
            return jsonify({'error': 'Vecchia password errata.'}), 401

    except Exception as e:
        flash(f'Errore durante il cambio della password: {str(e)}', 'error')
        return jsonify({'error': f'Errore durante il cambio della password: {str(e)}'}), 500
