"""
profiloControl.py

Questo modulo gestisce le operazioni sui profili degli utenti, come
il recupero e l'aggiornamento dei profili per studenti e docenti.
Include anche la funzionalità per il cambio password.

Autore: [il tuo nome]
Data di creazione: [data di creazione]
"""

import logging
import re
from flask import flash
from app.models.profiloModel import ProfiloModel

class ProfiloControl:

    """
    Classe che gestisce l'accesso ai profili utente nel database
    e le operazioni di aggiornamento su di essi.
    """

    def __init__(self, db_manager):
        """
        Inizializza un'istanza di ProfiloModel.

        :param db_manager: Gestore del database per accedere ai models.
        """
        self.model = ProfiloModel(db_manager)
        self.db_manager = db_manager

    def get_profilo_studente(self, email):
        """
       Recupera il profilo dello studente tramite l'email.

       :param email: L'email dello studente.
       :return: Lista dei documenti corrispondenti al profilo studente.
       """
        try:
            studente_collection = self.db_manager.get_collection("Studente")
            query = {"email": email}
            return list(studente_collection.find(query))
        except Exception as e:
            logging.error(f"Errore nel recuperare il profilo dello studente per email {email}: {str(e)}")
            return []

    def get_profilo_docente(self, email):
        """
        Recupera il profilo del docente tramite l'email.

        :param email: L'email del docente.
        :return: Lista dei documenti corrispondenti al profilo docente.
        """
        try:
            docente_collection = self.db_manager.get_collection("Docente")
            query = {"email": email}
            return list(docente_collection.find(query))
        except Exception as e:
            logging.error(f"Errore nel recuperare il profilo del docente per email {email}: {str(e)}")
            return []

    def carica_profilo_studente(self, email, nuovi_dati):
        """
        Aggiorna il profilo dello studente con nuovi dati.

        :param email: L'email dello studente da aggiornare.
        :param nuovi_dati: Dizionario contenente i nuovi dati del profilo.
        :return: True se l'aggiornamento ha avuto successo, False altrimenti.
        """
        if not self.valida_dati_profilo(nuovi_dati):
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
        """
       Aggiorna il profilo del docente con nuovi dati.

       :param email: L'email del docente da aggiornare.
       :param nuovi_dati: Dizionario contenente i nuovi dati del profilo.
       :return: True se l'aggiornamento ha avuto successo, False altrimenti.
       """

        if not self.valida_dati_profilo(nuovi_dati):
            logging.error(f"Dati del profilo docente non validi per email {email}")
            return False

        try:
            docente_collection = self.db_manager.get_collection("Docente")
            result = docente_collection.update_one({"email": email}, {"$set": nuovi_dati})
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Errore nell'aggiornamento del profilo docente per email {email}: {str(e)}")
            return False

    def valida_dati_profilo(self, dati):
        """
        Valida i dati del profilo ricevuti.

        :param dati: Dizionario con i dati del profilo da validare.
        :return: True se i dati sono validi, False altrimenti.
        """

        # Regex per la convalida
        email_regex = r"^[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}$"
        nome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        cognome_regex = r"^[A-ZÀ-ÖØ-Ý][a-zà-öø-ý]{2,}(?:['-][A-ZÀ-ÖØ-Ýa-zà-öø-ý]+)*$"
        sda_regex = r"^[A-Za-z0-9À-ù'’\- ]{2,50}$"
        cf_regex = r"^[A-Z]{6}[0-9]{2}[A-EHLMPR-T][0-9]{2}[A-Z0-9]{4}[A-Z]$"
        data_nascita_regex = r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$"

        # Controlli generali sui dati forniti
        if 'email' in dati and not re.match(email_regex, dati['email']):
            flash( "email non valida,devono essere usati solo caratteri alpha numerici,punti,tratti,undersxore perima del simbolo '@'", "message_profile_error")
            return False
        if 'nome' in dati and not re.match(nome_regex, dati['nome']):
            flash(" Nome non valido. Assicurati che inizi con una lettera maiuscola seguita da almeno due lettere minuscole. Possono essere inclusi apostrofi o trattini se necessario.", "message_profile_error")
            return False
        if 'cognome' in dati and not re.match(cognome_regex, dati['cognome']):
            flash(" Cognome non valido. Assicurati che inizi con una lettera maiuscola seguita da almeno due lettere minuscole. Possono essere inclusi apostrofi o trattini se necessario","message_profile_error")
            return False
        if 'sda' in dati and not re.match(sda_regex, dati['sda']):
            flash(" Il campo SDA non è valido. Deve contenere tra 2 e 50 caratteri alfanumerici. Possono essere inclusi spazi, apostrofi e trattini.", "message_profile_error")
            return False
        if 'cf' in dati and not re.match(cf_regex, dati['cf']):
            flash(" Codice fiscale non valido. Assicurati che sia composto da 16 caratteri, rispettando il formato italiano. Deve includere lettere e numeri secondo lo schema standard del codice fiscale italiano.", "message_profile_error")
            return False
        if 'data_nascita' in dati and not re.match(data_nascita_regex, dati['data_nascita']):
            flash("Data di nascita non valida. Assicurati di inserire la data nel formato 'AAAA-MM-GG', dove l'anno è a quattro cifre, il mese è nel range da 01 a 12, e il giorno è nel range adeguato al mese scelto.", "message_profile_error")
            return False


        flash("modifica profilo andata a buon fine", "message_profile_successo")
        return True

    def cambia_password_studente(self, vecchia_password, nuova_password):
        """
        Cambia la password dello studente.

        :param vecchia_password: Vecchia password dello studente.
        :param nuova_password: Nuova password da impostare.
        :return: Risultato del cambiamento password.
        """
        return self.model.cambia_password("Studente", vecchia_password, nuova_password)

    def cambia_password_docente(self, vecchia_password, nuova_password):
        """
        Cambia la password del docente.

        :param vecchia_password: Vecchia password del docente.
        :param nuova_password: Nuova password da impostare.
        :return: Risultato del cambiamento password.
        """
        return self.model.cambia_password("Docente", vecchia_password, nuova_password)
