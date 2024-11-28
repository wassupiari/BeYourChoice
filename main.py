from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, abort, send_from_directory
from databaseManager import DatabaseManager
from app.models.MaterialeModel import MaterialeModel
from app.controllers.MaterialeControl import MaterialeControl
import os

app = Flask(__name__, template_folder='app/templates', static_folder='public')
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'public/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


@app.route('/carica', methods=['GET', 'POST'])
def carica_materiale():
    if request.method == 'POST':
        titolo = request.form['titolo']
        descrizione = request.form['descrizione']
        tipo = request.form['tipo']
        file = request.files['file']

        filepath = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

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
        updated_data = {
            "Titolo": request.form['titolo'],
            "Descrizione": request.form['descrizione'],
        }

        if materiale['Tipo'] == 'txt':
            contenuto = request.form.get('contenuto', '')
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], materiale['File_Path'])
            with open(file_path, 'w') as f:
                f.write(contenuto)

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
    app.run(debug=True)