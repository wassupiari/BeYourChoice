"""

Questo modulo definisce le route per la gestione del profilo
degli utenti, inclusi studenti e docenti. Supporta la visualizzazione,
aggiornamento e cambio password.

Autore: [il tuo nome]
Data di creazione: [data di creazione]
"""

from flask import render_template, request, flash, Blueprint, session, redirect, url_for
from app.controllers.profiloControl import ProfiloControl
from databaseManager import DatabaseManager

db_manager = DatabaseManager()
profilo_control = ProfiloControl(db_manager)

profilo = Blueprint('profilo', __name__)


def initialize_profilo_blueprint(app):
    """
   Inizializza il blueprint per la gestione dei profili utente.

   :param app: L'applicazione Flask su cui registrare il blueprint.
   :return: None
   """
    @profilo.route('/cambia_password_docente', methods=['POST'])
    def cambia_password_docente():
        """
       Cambia la password del docente.
       """
        vecchia_password = request.form.get('vecchia_password')
        nuova_password = request.form.get('nuova_password')

        app.logger.info(f"Vecchia password ricevuta: {vecchia_password}")
        app.logger.info(f"Nuova password ricevuta: {nuova_password}")

        # Controlla se vecchia_password è None
        if not vecchia_password or not nuova_password:
            flash("Le password non devono essere vuote", "message_profile_error")
            return redirect(url_for('profilo.gestione_profilo'))

        return profilo_control.cambia_password_docente(vecchia_password, nuova_password)

    @profilo.route('/cambia_password_studente', methods=['POST'])
    def cambia_password_studente():
        """
        Cambia la password dello studente.
        """
        vecchia_password = request.form.get('vecchia_password')
        nuova_password = request.form.get('nuova_password')

        app.logger.info(f"Vecchia password ricevuta: {vecchia_password}")
        app.logger.info(f"Nuova password ricevuta: {nuova_password}")

        # Controlla se vecchia_password è None
        if not vecchia_password or not nuova_password:
            flash("Le password non devono essere vuote", "message_profile_error")
            return redirect(url_for('profilo.gestione_profilo'))

        return profilo_control.cambia_password_studente(vecchia_password, nuova_password)

    @profilo.route('/gestione', methods=['GET', 'POST'])
    def gestione_profilo():
        """
        Gestisce la visualizzazione e modifica del profilo utente.
        """
        email = session.get('email')
        if not email:
            app.logger.info('Nessuna email trovata nella sessione.')
            return redirect(url_for('login.login'))

        if request.method == 'POST':
            nuovi_dati = request.form.to_dict()
            ruolo = request.form.get('ruolo', 'studente')
            successo = False
            if ruolo == 'docente':
                successo = profilo_control.carica_profilo_docente(email, nuovi_dati)
            else:
                successo = profilo_control.carica_profilo_studente(email, nuovi_dati)

            flash('Profilo aggiornato con successo!' if successo else 'Errore nell\'aggiornamento del profilo.',
                  'successo' if successo else 'error')

        profilo_studente = profilo_control.get_profilo_studente(email)
        profilo_docente = profilo_control.get_profilo_docente(email)

        return render_template(
            'gestioneProfilo.html',
            profilo_studente=profilo_studente[0] if profilo_studente else {},
            profilo_docente=profilo_docente[0] if profilo_docente else {}
        )

    app.register_blueprint(profilo, url_prefix='/profilo')