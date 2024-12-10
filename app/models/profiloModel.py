"""
profiloModel.py

Questo modello funge da interfaccia per le operazioni sui profili
degli utenti. Si collega tramite ProfiloControl per eseguire operazioni
come il recupero e l'aggiornamento dei profili e delle password.

Autore: [il tuo nome]
Data di creazione: [data di creazione]
"""

from app.controllers.profiloControl import ProfiloControl


class ProfiloModel:
    """
Classe ProfiloModel che fornisce interfacce per accedere e
modificare i profili degli utenti nel database.
"""
    def __init__(self, db_manager):
        """
        Inizializza un'istanza di ProfiloModel.

        :param db_manager: Gestore del database per accedere ai controller.
        """
        self.control = ProfiloControl(db_manager)

    def get_profilo_studente(self, email):
        """
       Recupera il profilo studente tramite ProfiloControl.

       :param email: L'email dello studente da cercare.
       :return: Informazioni del profilo studente.
       """
        return self.control.get_profilo_studente(email)

    def get_profilo_docente(self, email):
        """
        Recupera il profilo docente tramite ProfiloControl.

        :param email: L'email del docente da cercare.
        :return: Informazioni del profilo docente.
        """
        return self.control.get_profilo_docente(email)

    def carica_profilo_studente(self, email, nuovi_dati):
        """
        Aggiorna il profilo studente con nuovi dati tramite ProfiloControl.

        :param email: L'email dello studente.
        :param nuovi_dati: Nuovi dati per aggiornare il profilo.
        :return: Risultato dell'update.
        """
        return self.control.carica_profilo_studente(email, nuovi_dati)

    def carica_profilo_docente(self, email, nuovi_dati):
        """
        Aggiorna il profilo docente con nuovi dati tramite ProfiloControl.

        :param email: L'email del docente.
        :param nuovi_dati: Nuovi dati per aggiornare il profilo.
        :return: Risultato dell'update.
        """
        return self.control.carica_profilo_docente(email, nuovi_dati)

    def cambia_password_studente(self, vecchia_password, nuova_password):
        """
        Cambia la password dello studente tramite ProfiloControl.

        :param vecchia_password: Vecchia password dello studente.
        :param nuova_password: Nuova password da impostare.
        :return: Risultato del cambio password.
        """
        return self.control.cambia_password_studente(vecchia_password, nuova_password)

    def cambia_password_docente(self, vecchia_password, nuova_password):
        """
        Cambia la password del docente tramite ProfiloControl.

        :param vecchia_password: Vecchia password del docente.
        :param nuova_password: Nuova password da impostare.
        :return: Risultato del cambio password.
        """
        return self.control.cambia_password_docente(vecchia_password, nuova_password)