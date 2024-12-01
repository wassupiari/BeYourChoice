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

    @profilo.route('/studente/<cf_studente>', methods=['GET'])
    def visualizza_profilo_studente(cf_studente):
        try:
            # Ottieni i dati del profilo dello studente
            profilo = profilo_control.get_profilo_studente(cf_studente)
            return render_template('visualizazzioneProfilo.html', profilo=profilo.to_dict())
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('home'))  # Supponendo che esista una rotta 'home'


    @profilo.route('/docente', methods=['GET'])
    def visualizza_profilo_docente():
        try:
            # Recupera il codice fiscale del docente dalla sessione
            cf_docente = session.get('cf')

            # Verifica se il valore esiste nella sessione
            if not cf_docente:
                flash("Non sei autorizzato a visualizzare questa pagina", "error")
                return redirect(url_for('home'))

            # Ottieni i dati del profilo del docente
            profilo = profilo_control.get_profilo_docente(cf_docente)
            return render_template('profilo_docente.html', profilo=profilo.to_dict())
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('home'))

    app.register_blueprint(profilo)
