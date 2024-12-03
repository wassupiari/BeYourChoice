import os
import re
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, send_from_directory, \
    Blueprint, session

from databaseManager import DatabaseManager
from app.models.materialeModel import MaterialeModel
from app.controllers.MaterialeControl import MaterialeControl
import uuid  # Per generare ID unici

MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'jpeg', 'png', 'txt', 'jpg', 'mp4'}

# Supponiamo che DatabaseManager sia il manager db richiesto
database_uri = "mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority&appName=BeYourChoice"  # URI di connessione al database
db_manager = DatabaseManager(database_uri)  # <--- Inizializza qui il tuo db_manager con l'URI

# Passa l'istanza di db_manager a MaterialeModel
materiale_control = MaterialeControl(db_manager)

MaterialeDocente = Blueprint('MaterialeDocente', __name__)


def initialize_materiale_docente_blueprint(app: object) -> object:

    @MaterialeDocente.route('/')
    def index():
        return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    @MaterialeDocente.route('/materiale/docente')
    def visualizza_materiale_docente():
        ID_Classe = session.get('ID_Classe')
        materiali = materiale_control.get_materials_by_id(ID_Classe)
        return render_template('materialeDocente.html', materiali=materiali)

    @MaterialeDocente.route('/serve_file/<path:filename>')
    def serve_file(filename: str):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            abort(404)



    def is_title_valid(title):
        return bool(re.match(r'^[A-Za-z0-9 ]{2,20}$', title))

    def is_description_valid(description):
        return 2 <= len(description) <= 255

    def is_file_type_valid(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def is_file_size_valid(file):
        return file.content_length <= MAX_FILE_SIZE_MB * 1024 * 1024

    @MaterialeDocente.route('/carica', methods=['GET', 'POST'])
    def carica_materiale():
        if request.method == 'POST':
            titolo = request.form['titolo']
            descrizione = request.form['descrizione']
            tipo = request.form['tipo']
            file = request.files['file']
            ID_Classe = session.get('ID_Classe')

            if not is_title_valid(titolo):
                flash("Il titolo non è valido. Deve essere tra 2 e 20 caratteri e contenere solo lettere e numeri.",
                      "error")
                return redirect(request.url)

            if not is_description_valid(descrizione):
                flash("La descrizione deve avere una lunghezza tra i 2 e i 255 caratteri.", "error")
                return redirect(request.url)

            if not is_file_type_valid(file.filename):
                flash("Il tipo di file non è valido. Ammessi: docx, pdf, jpeg, png, txt, jpg, mp4.", "error")
                return redirect(request.url)

            file_extension = file.filename.rsplit('.', 1)[1].lower()
            if tipo != file_extension:
                flash(
                    "Il tipo di file selezionato non corrisponde all'estensione del file. Seleziona il tipo corretto.",
                    "error")
                return redirect(request.url)

            if not is_file_size_valid(file):
                flash(f"La dimensione del file non deve superare i {MAX_FILE_SIZE_MB} MB.", "error")
                return redirect(request.url)

            filepath = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filepath))

            id_MaterialeDidattico = uuid.uuid4().hex

            nuovo_materiale = MaterialeModel(id_MaterialeDidattico, titolo, descrizione, filepath, tipo, ID_Classe)
            materiale_control.upload_material(nuovo_materiale)
            flash("Materiale caricato con successo!", "materiale_success")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        return render_template('caricamentoMateriale.html')

    @MaterialeDocente.route('/modifica/<materiale_id>', methods=['GET', 'POST'])
    def modifica_materiale(materiale_id):
        try:
            material_id_obj = ObjectId(materiale_id)
        except Exception:
            flash("ID del materiale non valido.", "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        materiale = materiale_control.view_material({"_id": material_id_obj})

        if materiale is None:
            flash("Materiale non trovato.", "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        if request.method == 'POST':
            titolo = request.form['titolo']
            descrizione = request.form['descrizione']

            if not is_title_valid(titolo):
                flash("Il titolo non è valido. Deve essere tra 2 e 20 caratteri e contenere solo lettere e numeri.",
                      "error")
                return redirect(request.url)

            if not is_description_valid(descrizione):
                flash("La descrizione deve avere una lunghezza tra i 2 e i 255 caratteri.", "error")
                return redirect(request.url)

            file = request.files.get('file', None)
            if file:
                if not is_file_type_valid(file.filename):
                    flash("Il tipo di file non è valido. Ammessi: docx, pdf, jpeg, png, txt, jpg, mp4.", "error")
                    return redirect(request.url)

                if not is_file_size_valid(file):
                    flash(f"La dimensione del file non deve superare i {MAX_FILE_SIZE_MB} MB.", "error")
                    return redirect(request.url)

                filepath = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filepath))
                materiale['File_Path'] = filepath

            updated_data = {
                "Titolo": titolo,
                "Descrizione": descrizione,
                "File_Path": materiale.get('File_Path')
            }

            materiale_control.edit_material(material_id_obj, updated_data)
            flash("Materiale modificato con successo!", "materiale_success")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        if materiale['Tipo'] == 'txt':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], materiale['File_Path'])
            with open(file_path, 'r') as f:
                contenuto = f.read()
        else:
            contenuto = None

        return render_template('modificaMateriale.html', materiale=materiale, contenuto=contenuto)

    @MaterialeDocente.route('/rimuovi/<materiale_id>')
    def rimuovi_materiale(materiale_id):
        try:
            material_id_obj = ObjectId(materiale_id)
        except Exception as e:
            flash("ID del materiale non valido: " + str(e), "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        materiale = materiale_control.view_material({"_id": material_id_obj})

        if materiale is None:
            flash("Materiale non trovato.", "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        # Prova ad eliminare il materiale
        delete_success = materiale_control.delete_material(material_id_obj)

        if not delete_success:
            flash("Errore durante la rimozione del materiale dal database.", "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        file_path = materiale.get('File_Path')
        if file_path:
            full_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_path)
            if os.path.exists(full_file_path):
                try:
                    os.remove(full_file_path)
                    flash("Materiale rimosso con successo!", "success")
                except OSError as e:
                    flash(f"Errore durante l'eliminazione del file: {e}", "error")
            else:
                flash("File non trovato, ma materiale rimosso dal database.", "warning")

        return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    @MaterialeDocente.route('/public/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @MaterialeDocente.cli.command("migrate_paths")
    def migrate_paths():
        materiali = materiale_control.view_all_materials()
        for materiale in materiali:
            if os.path.isabs(materiale['File_Path']):
                materiale['File_Path'] = os.path.basename(materiale['File_Path'])
                materiale_control.edit_material(materiale['_id'], {'File_Path': materiale['File_Path']})
        print('Migrazione completata.')

    app.register_blueprint(MaterialeDocente)