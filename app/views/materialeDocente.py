import os
import re
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, send_from_directory, \
    Blueprint, session
from pymongo import collection

from databaseManager import DatabaseManager
from app.models.materialeModel import MaterialeModel
from app.controllers.MaterialeControl import MaterialeControl
import uuid  # Per generare ID unici

MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'jpeg', 'png', 'txt', 'jpg', 'mp4'}

# Supponiamo che DatabaseManager sia il manager db richiesto

db_manager = DatabaseManager()

# Passa l'istanza di db_manager a MaterialeModel
materiale_control = MaterialeControl(db_manager)
materiale_model = MaterialeModel(db_manager)
materiale_model.set_cartella_uploads('/public/uploads')

MaterialeDocente = Blueprint('MaterialeDocente', __name__)

collezione_materiali = db_manager.get_collection('MaterialeDidattico')
def initialize_materiale_docente_blueprint(app: object) -> object:
    @MaterialeDocente.route('/')
    def index():
        return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    @MaterialeDocente.route('/materiale/docente')
    def visualizza_materiale_docente():
        ID_Classe = session.get('ID_Classe')
        materiali = materiale_model.visualizza_materiali(ID_Classe)
        return render_template('materialeDocente.html', materiali=materiali)

    @MaterialeDocente.route('/servi_file/<path:nomefile>')
    def servi_file(nomefile: str):
        return materiale_model.servi_file(nomefile)

    @MaterialeDocente.route('/carica', methods=['GET', 'POST'])
    def carica_materiale():
        if request.method == 'POST':
            return materiale_model.carica_materiale(request)
        return render_template('caricamentoMateriale.html')

    @MaterialeDocente.route('/modifica/<string:materiale_id>', methods=['GET', 'POST'])
    def modifica_materiale(materiale_id):
        if request.method == 'POST':
            return materiale_model.modifica_materiale(materiale_id, request)

        # Se GET, recupera il materiale per visualizzarlo nel form
        try:
            materiale_obj_id = ObjectId(materiale_id)
            print(f"Recupero materiale con ID: {materiale_obj_id}")

            materiale = collezione_materiali.find_one({"_id": materiale_obj_id})
            if materiale is None:
                print(f"Nessun materiale trovato con ID: {materiale_obj_id}")
                return render_template('modificaMateriale.html', messaggio="Il materiale non è stato trovato.")

            return render_template('modificaMateriale.html', materiale=materiale)
        except Exception as e:
            print(f"Errore nel recupero del materiale: {str(e)}")
            return render_template('modificaMateriale.html', messaggio="Errore nel recupero del materiale.")

    @MaterialeDocente.route('/rimuovi/<materiale_id>')
    def rimuovi_materiale(materiale_id):
        return materiale_model.rimuovi_materiale(materiale_id)

    app.register_blueprint(MaterialeDocente)