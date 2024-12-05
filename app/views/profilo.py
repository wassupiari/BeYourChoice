from flask import render_template, request, flash, Blueprint, session

from app.controllers.LoginControl import student_required, teacher_required
from app.controllers.ProfiloControl import ProfiloControl
from databaseManager import DatabaseManager

database_uri = "mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority&appName=BeYourChoice"  # URI di connessione al database
db_manager = DatabaseManager(database_uri)  # <--- Inizializza qui il tuo db_manager con l'URI

profilo_control: ProfiloControl = ProfiloControl(db_manager)

profilo = Blueprint('profilo', __name__)

def initialize_profilo_blueprint(app):
    @profilo.route('/change_password_docente', methods=['POST'])
    def change_password_docente():
        vecchia_password = request.form['old_password']
        nuova_password = request.form['new_password']
        email = session.get('email')

        return profilo_control.cambia_password_docente(vecchia_password, nuova_password)

    @profilo.route('/change_password_studente', methods=['POST'])

    def change_password_studente():
        vecchia_password = request.form['old_password']
        nuova_password = request.form['new_password']
        email = session.get('email')

        return profilo_control.cambia_password_studente(vecchia_password, nuova_password)

    @profilo.route('/gestione', methods=['GET', 'POST'])

    def gestione_profilo():
        email = session.get('email')
        if not email:
            app.logger.info('Nessuna email trovata nella sessione.')

        if request.method == 'POST':
            nuovi_dati = request.form.to_dict()
            # Determina il tipo di utente: studente o docente
            if 'ruolo' in request.form and request.form['ruolo'] == 'docente':
                if profilo_control.update_profilo_docente(email, nuovi_dati):
                    flash('Profilo Docente aggiornato con successo!', 'success')
                else:
                    flash('Errore nell\'aggiornamento del profilo.', 'error')
            else:
                if profilo_control.update_profilo_studente(email, nuovi_dati):
                    flash('Profilo Studente aggiornato con successo!', 'success')
                else:
                    flash('Errore nell\'aggiornamento del profilo.', 'error')

        # Recupera il profilo
        profilo_studente = profilo_control.get_profilo_studente(email)
        profilo_docente = profilo_control.get_profilo_docente(email)

        return render_template(
            'gestioneProfilo.html',
            profilo_studente=profilo_studente[0] if profilo_studente else {},
            profilo_docente=profilo_docente[0] if profilo_docente else {}
        )

    app.register_blueprint(profilo, url_prefix='/profilo')