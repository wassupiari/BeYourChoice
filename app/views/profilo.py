from flask import render_template, request, flash, Blueprint, session, redirect, url_for
from app.models.profiloModel import ProfiloModel
from databaseManager import DatabaseManager

db_manager = DatabaseManager()
profilo_model = ProfiloModel(db_manager)

profilo = Blueprint('profilo', __name__)


def initialize_profilo_blueprint(app):
    @profilo.route('/change_password_docente', methods=['POST'])
    def change_password_docente():
        vecchia_password = request.form['old_password']
        nuova_password = request.form['new_password']
        return profilo_model.cambia_password_docente(vecchia_password, nuova_password)

    @profilo.route('/change_password_studente', methods=['POST'])
    def change_password_studente():
        vecchia_password = request.form['old_password']
        nuova_password = request.form['new_password']
        return profilo_model.cambia_password_studente(vecchia_password, nuova_password)

    @profilo.route('/gestione', methods=['GET', 'POST'])
    def gestione_profilo():
        email = session.get('email')
        if not email:
            app.logger.info('Nessuna email trovata nella sessione.')
            return redirect(url_for('login'))

        if request.method == 'POST':
            nuovi_dati = request.form.to_dict()
            ruolo = request.form.get('ruolo', 'studente')
            success = False
            if ruolo == 'docente':
                success = profilo_model.update_profilo_docente(email, nuovi_dati)
            else:
                success = profilo_model.update_profilo_studente(email, nuovi_dati)

            flash('Profilo aggiornato con successo!' if success else 'Errore nell\'aggiornamento del profilo.',
                  'success' if success else 'error')

        profilo_studente = profilo_model.get_profilo_studente(email)
        profilo_docente = profilo_model.get_profilo_docente(email)

        return render_template(
            'gestioneProfilo.html',
            profilo_studente=profilo_studente[0] if profilo_studente else {},
            profilo_docente=profilo_docente[0] if profilo_docente else {}
        )

    app.register_blueprint(profilo, url_prefix='/profilo')