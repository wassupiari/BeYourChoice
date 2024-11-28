from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, send_from_directory
from databaseManager import DatabaseManager
from app.models.MaterialeModel import MaterialeModel
from app.controllers.MaterialeControl import MaterialeControl
import os
import re

app = Flask(__name__, template_folder='app/templates', static_folder='public')
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'public/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'jpeg', 'png', 'txt', 'jpg', 'mp4'}

db_manager = DatabaseManager()
materiale_control = MaterialeControl(db_manager)


@app.route('/')
def index():
    return redirect(url_for('visualizza_materiale_docente'))


@app.route('/materiale/docente')
def visualizza_materiale_docente():
    materiali = materiale_control.view_all_materials()
    return render_template('materialeDocente.html', materiali=materiali)


@app.route('/serve_file/<path:filename>')
def serve_file(filename: str):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    else:
        abort(404)


@app.route('/materiale/studente')
def visualizza_materiale_studente():
    materiali = materiale_control.view_all_materials()
    return render_template('materialeStudente.html', materiali=materiali)


def is_title_valid(title):
    return bool(re.match(r'^[A-Za-z0-9]{2,20}$', title))


def is_description_valid(description):
    return 2 <= len(description) <= 255


def is_file_type_valid(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_file_size_valid(file):
    return file.content_length <= MAX_FILE_SIZE_MB * 1024 * 1024


@app.route('/carica', methods=['GET', 'POST'])
def carica_materiale():
    if request.method == 'POST':
        titolo = request.form['titolo']
        descrizione = request.form['descrizione']
        tipo = request.form['tipo']
        file = request.files['file']

        # Validazione titolo
        if not is_title_valid(titolo):
            flash("Il titolo non è valido. Deve essere tra 2 e 20 caratteri e contenere solo lettere e numeri.",
                  "error")
            return redirect(request.url)

        # Validazione descrizione
        if not is_description_valid(descrizione):
            flash("La descrizione deve avere una lunghezza tra i 2 e i 255 caratteri.", "error")
            return redirect(request.url)

        # Validazione tipo di file
        if not is_file_type_valid(file.filename):
            flash("Il tipo di file non è valido. Ammessi: docx, pdf, jpeg, png, txt, jpg, mp4.", "error")
            return redirect(request.url)

        # Controlla che il tipo selezionato corrisponda all'estensione del file
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        if tipo != file_extension:
            flash("Il tipo di file selezionato non corrisponde all'estensione del file. Seleziona il tipo corretto.",
                  "error")
            return redirect(request.url)

        # Validazione dimensione del file
        if not is_file_size_valid(file):
            flash(f"La dimensione del file non deve superare i {MAX_FILE_SIZE_MB} MB.", "error")
            return redirect(request.url)

        filepath = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filepath))

        nuovo_materiale = MaterialeModel(titolo, descrizione, filepath, tipo)
        materiale_control.upload_material(nuovo_materiale)
        flash("Materiale caricato con successo!", "success")
        return redirect(url_for('visualizza_materiale_docente'))

    return render_template('caricamentoMateriale.html')

@app.route('/modifica/<materiale_id>', methods=['GET', 'POST'])
def modifica_materiale(materiale_id):
    try:
        material_id_obj = ObjectId(materiale_id)
    except Exception:
        flash("ID del materiale non valido.", "error")
        return redirect(url_for('visualizza_materiale_docente'))

    materiale = materiale_control.view_material({"_id": material_id_obj})

    if materiale is None:
        flash("Materiale non trovato.", "error")
        return redirect(url_for('visualizza_materiale_docente'))

    if request.method == 'POST':
        titolo = request.form['titolo']
        descrizione = request.form['descrizione']

        # Validazione del titolo
        if not is_title_valid(titolo):
            flash("Il titolo non è valido. Deve essere tra 2 e 20 caratteri e contenere solo lettere e numeri.",
                  "error")
            return redirect(request.url)

        # Validazione della descrizione
        if not is_description_valid(descrizione):
            flash("La descrizione deve avere una lunghezza tra i 2 e i 255 caratteri.", "error")
            return redirect(request.url)

        file = request.files.get('file', None)
        if file:
            # Validazione del tipo di file
            if not is_file_type_valid(file.filename):
                flash("Il tipo di file non è valido. Ammessi: docx, pdf, jpeg, png, txt, jpg, mp4.", "error")
                return redirect(request.url)

            # Validazione della dimensione del file
            if not is_file_size_valid(file):
                flash(f"La dimensione del file non deve superare i {MAX_FILE_SIZE_MB} MB.", "error")
                return redirect(request.url)

            filepath = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filepath))
            # Aggiornare anche il percorso del file nel database
            materiale['File_Path'] = filepath

        updated_data = {
            "Titolo": titolo,
            "Descrizione": descrizione,
            "File_Path": materiale.get('File_Path')  # Aggiorna se cambiato
        }

        materiale_control.edit_material(material_id_obj, updated_data)
        flash("Materiale modificato con successo!", "success")
        return redirect(url_for('visualizza_materiale_docente'))

    if materiale['Tipo'] == 'txt':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], materiale['File_Path'])
        with open(file_path, 'r') as f:
            contenuto = f.read()
    else:
        contenuto = None

    return render_template('modificaMateriale.html', materiale=materiale, contenuto=contenuto)


@app.route('/rimuovi/<materiale_id>')
def rimuovi_materiale(materiale_id):
    try:
        material_id_obj = ObjectId(materiale_id)
    except Exception:
        flash("ID del materiale non valido.", "error")
        return redirect(url_for('visualizza_materiale_docente'))

    materiale = materiale_control.delete_material(material_id_obj)

    if materiale is None:
        flash("Materiale non trovato.", "error")
        return redirect(url_for('visualizza_materiale_docente'))

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], materiale['File_Path'])

    if os.path.exists(file_path):
        os.remove(file_path)

    flash("Materiale rimosso con successo!", "success")
    return redirect(url_for('visualizza_materiale_docente'))


@app.route('/public/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.cli.command("migrate_paths")
def migrate_paths():
    materiali = materiale_control.view_all_materials()
    for materiale in materiali:
        if os.path.isabs(materiale['File_Path']):
            materiale['File_Path'] = os.path.basename(materiale['File_Path'])
            materiale_control.edit_material(materiale['_id'], {'File_Path': materiale['File_Path']})
    print('Migrazione completata.')


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Cambia la porta per evitare conflitti