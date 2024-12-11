"""
profiloModel.py

Questo modello funge da interfaccia per le operazioni sui profili
degli utenti. Si collega tramite ProfiloControl per eseguire operazioni
come il recupero e l'aggiornamento dei profili e delle password.

Autore: [il tuo nome]
Data di creazione: [data di creazione]
"""
import re

import bcrypt
from flask import session, flash, redirect, url_for

class ProfiloModel:
    """
Classe ProfiloModel che fornisce interfacce per accedere e
modificare i profili degli utenti nel database.
"""
    def __init__(self, db_manager):

        """
        Inizializza l'istanza di MaterialeModel.

        :param db_manager: Gestore del database per accedere alla collezione.
        """

        self.db_manager = db_manager

    def cambia_password(self, user_type, vecchia_password, nuova_password):
        """
        Cambia la password per un tipo di utente specificato.

        :param user_type: Tipo di utente (Studente o Docente).
        :param vecchia_password: Vecchia password dell'utente.
        :param nuova_password: Nuova password da impostare.
        :return: Redirect alla gestione profilo con risultato dell'operazione.
        """
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