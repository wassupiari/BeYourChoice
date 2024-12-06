from flask import Flask, Blueprint, render_template, send_file, redirect, url_for, abort, session

from app.models.materialeModel import MaterialeModel
from databaseManager import DatabaseManager
from app.controllers.MaterialeControl import MaterialeControl
import os

# Crea un Blueprint per la gestione lato studente
MaterialeStudente = Blueprint('MaterialeStudente', __name__)

# Inizializza il controllo del materiale
db_manager = DatabaseManager()
materiale_control = MaterialeControl(db_manager)
materiale_model = MaterialeModel(db_manager)
materiale_model.set_upload_folder('/public/uploads')

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

        materiali = materiale_model.visualizza_materiali(ID_Classe)
        return render_template('materialeStudente.html', ID_Classe=ID_Classe, materiali=materiali)

    @MaterialeStudente.route('/serve_file/<path:filename>')
    def serve_file(filename: str):
        """Servizio per servire i file agli studenti."""
        return materiale_model.serve_file(filename)

    app.register_blueprint(MaterialeStudente)