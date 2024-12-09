import logging
import re
import bcrypt
from flask import session, flash, redirect, url_for


class ProfiloControl:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_profilo_studente(self, email):
        # Recupero profilo studente
        try:
            studente_collection = self.db_manager.get_collection("Studente")
            query = {"email": email}
            return list(studente_collection.find(query))
        except Exception as e:
            logging.error(f"Errore nel recuperare il profilo dello studente per email {email}: {str(e)}")
            return []

    def get_profilo_docente(self, email):
        # Recupero profilo docente
        try:
            docente_collection = self.db_manager.get_collection("Docente")
            query = {"email": email}
            return list(docente_collection.find(query))
        except Exception as e:
            logging.error(f"Errore nel recuperare il profilo del docente per email {email}: {str(e)}")
            return []

    def carica_profilo_studente(self, email, nuovi_dati):
        if not self._valida_dati_profilo(nuovi_dati):
            logging.error(f"Dati del profilo studente non validi per email {email}")
            flash("Errore: Dati non validi, aggiornamento non effettuato.", "message_profile_error")
            return False

        try:
            studente_collection = self.db_manager.get_collection("Studente")
            result = studente_collection.update_one({"email": email}, {"$set": nuovi_dati})
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Errore nell'aggiornamento del profilo studente per email {email}: {str(e)}")
            return False

    def carica_profilo_docente(self, email, nuovi_dati):
        if not self._valida_dati_profilo(nuovi_dati):
            logging.error(f"Dati del profilo docente non validi per email {email}")
            flash("Errore: Dati non validi, aggiornamento non effettuato.", "message_profile_error")
            return False

        try:
            docente_collection = self.db_manager.get_collection("Docente")
            result = docente_collection.update_one({"email": email}, {"$set": nuovi_dati})
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Errore nell'aggiornamento del profilo docente per email {email}: {str(e)}")
            return False

    def _valida_dati_profilo(self, dati):
        # Regex per la convalida
        email_regex = r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$"
        nome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        cognome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        sda_regex = r"^[A-Za-z0-9À-ù'’\- ]{2,50}$"
        cf_regex = r"^[A-Z]{6}[0-9]{2}[A-EHLMPR-T][0-9]{2}[A-Z0-9]{4}[A-Z]$"
        data_nascita_regex = r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"

        # Controlli generali sui dati forniti
        if 'email' in dati and not re.match(email_regex, dati['email']):
            return False
        if 'nome' in dati and not re.match(nome_regex, dati['nome']):
            return False
        if 'cognome' in dati and not re.match(cognome_regex, dati['cognome']):
            return False
        if 'sda' in dati and not re.match(sda_regex, dati['sda']):
            return False
        if 'cf' in dati and not re.match(cf_regex, dati['cf']):
            return False
        if 'data_nascita' in dati and not re.match(data_nascita_regex, dati['data_nascita']):
            return False

        return True

    def cambia_password_studente(self, vecchia_password, nuova_password):
        return self.cambia_password("Studente", vecchia_password, nuova_password)

    def cambia_password_docente(self, vecchia_password, nuova_password):
        return self.cambia_password("Docente", vecchia_password, nuova_password)

    def cambia_password(self, user_type, vecchia_password, nuova_password):
        collection = self.db_manager.get_collection(user_type)
        email = session.get('email')
        if not email:
            return "Errore: Nessuna email trovata nella sessione."

        user = collection.find_one({"email": email})
        if not user:
            return f"Errore: {user_type} non trovato."

        if not bcrypt.checkpw(vecchia_password.encode('utf-8'), user['password']):
            flash("Vecchia password errata", "message_profile_error")
            return redirect(url_for('profilo.gestione_profilo'))

        password_regex = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s])[A-Za-z\d!@#$%^&*()\-_=+\[\]{};:,.<>?/\\|~]{8,20}$"

        if not re.match(password_regex, nuova_password):
            flash(
                "Formato password errato. Deve avere minimo 8 caratteri, una maiuscola, un carattere speciale e almeno un numero",
                "message_profile_error")
            return redirect(url_for('profilo.gestione_profilo'))

        nuova_password_hash = bcrypt.hashpw(nuova_password.encode('utf-8'), bcrypt.gensalt())
        result = collection.update_one({"email": email}, {"$set": {"password": nuova_password_hash}})

        if result.modified_count > 0:
            flash("Password aggiornata con successo!", "message_profile_successo")
        else:
            flash("Errore: Password non aggiornata.", "message_profile_error")

        return redirect(url_for('profilo.gestione_profilo'))