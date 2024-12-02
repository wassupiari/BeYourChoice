import os
import re
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, send_from_directory, \
    Blueprint, session

from databaseManager import DatabaseManager
from app.models.profiloModel import ProfiloStudente, ProfiloDocente
from app.controllers.profiloControl import ProfiloControl
import uuid  # Per generare ID unici

database_uri = "mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority&appName=BeYourChoice"  # URI di connessione al database
db_manager = DatabaseManager(database_uri)  # <--- Inizializza qui il tuo db_manager con l'URI

profilo_control = ProfiloControl(db_manager)

profilo = Blueprint('profilo', __name__)

def initialize_profilo_blueprint(app):
    @profilo.route('/profilo/studente')
    def visualizza_profilo_studente():
            email = session.get('email')
            if not email:
                app.logger.info('Nessuna email trovata nella sessione.')
            profilo = profilo_control.get_profilo_studente(email)
            if isinstance(profilo, list) and len(profilo) > 0:
                profilo = profilo[0]
            elif isinstance(profilo, list) and len(profilo) == 0:
                profilo = {}
            return render_template('gestioneProfilo.html', profilo=profilo)

    @profilo.route('/profilo/docente')
    def visualizza_profilo_docente():
            email = session.get('email')
            if not email:
                app.logger.info('Nessuna email trovata nella sessione.')
            profilo = profilo_control.get_profilo_docente(email)
            if isinstance(profilo, list) and len(profilo) > 0:
                profilo = profilo[0]
            elif isinstance(profilo, list) and len(profilo) == 0:
                profilo = {}
            app.logger.info('Profilo Docente: %s', profilo)
            return render_template('gestioneProfilo.html', profilo=profilo)

    def initialize_profilo_blueprint(app):
        # ... codice esistente ...

        @profilo.route('/profilo/studente', methods=['GET', 'POST'])
        def gestione_profilo_studente():
            email = session.get('email')
            if not email:
                app.logger.info('Nessuna email trovata nella sessione.')
                return redirect(url_for('login'))

            if request.method == 'POST':
                nuovi_dati = request.form.to_dict()
                if profilo_control.update_profilo_studente(email, nuovi_dati):
                    flash('Profilo aggiornato con successo!', 'success')
                else:
                    flash('Errore nell aggiornamento del profilo.', 'error')
                    profilo = profilo_control.get_profilo_studente(email)
            return render_template('gestioneProfilo.html', ruolo='studente', profilo=profilo[0] if profilo else {})

        # Gestione profilo per Docente
        @profilo.route('/profilo/docente', methods=['GET', 'POST'])
        def gestione_profilo_docente():
            email = session.get('email')
            if not email:
                app.logger.info('Nessuna email trovata nella sessione.')
                return redirect(url_for('login'))

            if request.method == 'POST':
                nuovi_dati = request.form.to_dict()
                if profilo_control.update_profilo_docente(email, nuovi_dati):
                    flash('Profilo aggiornato con successo!', 'success')
                else:
                    flash('Errore nell aggiornamento del profilo.', 'error')
                    profilo = profilo_control.get_profilo_docente(email)
            return render_template('gestioneProfilo.html', ruolo='docente', profilo=profilo[0] if profilo else {})

    app.register_blueprint(profilo)