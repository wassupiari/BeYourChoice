from flask import Flask, Blueprint, render_template, send_file, redirect, url_for, abort, session
from databaseManager import DatabaseManager
from app.controllers.MaterialeControl import MaterialeControl
import os

# Crea un Blueprint per la gestione lato studente
MaterialeStudente = Blueprint('MaterialeStudente', __name__)

# Inizializza il controllo del materiale
db_manager = DatabaseManager()
materiale_control = MaterialeControl(db_manager)

def initialize_materiale_studente_blueprint(app: object) -> object:

    @MaterialeStudente.route('/')
    def index():
        return redirect(url_for('MaterialeStudente.visualizza_materiale_studente'))

    @MaterialeStudente.route('/materiale/studente')
    def visualizza_materiale_studente():
        """Vista per visualizzare tutti i materiali disponibili per gli studenti."""
        ID_Classe = session.get('ID_Classe')
        if ID_Classe is None:
            return redirect(url_for('dashboardStudente'))

        materiali =materiale_control.get_materials_by_id(ID_Classe)
        return render_template('materialeStudente.html', ID_Classe=ID_Classe, materiali=materiali)



    @MaterialeStudente.route('/serve_file/<path:filename>')
    def serve_file(filename: str):
        """Servizio per servire i file agli studenti."""
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            abort(404)

    @MaterialeStudente.route('/favicon.ico')
    def favicon():
        return '', 204  # restituire una risposta vuota con codice di stato 204



    # Registra il blueprint con l'applicazione
    app.register_blueprint(MaterialeStudente)