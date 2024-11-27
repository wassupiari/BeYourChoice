from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, send_file, abort
from app.controllers.MaterialeControl import MaterialeControl
from databaseManager import DatabaseManager
import os

app = Flask(__name__, template_folder='app/templates', static_folder='public')
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'public/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db_manager = DatabaseManager()
materiale_control = MaterialeControl(db_manager)


@app.route('/')
def index():
    """Pagina iniziale che reindirizza a una pagina con i materiali."""
    return redirect(url_for('visualizza_materiale_docente'))


@app.route('/materiale/docente')
def visualizza_materiale_docente():
    """Visualizza i materiali per docenti."""
    materiali = materiale_control.view_all_materials()
    # Print materiale paths for debugging
    print("Debug: Materiali recuperati - ", materiali)
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
    """Visualizza i materiali per studenti."""
    materiali = materiale_control.view_all_materials()
    return render_template('materialeStudente.html', materiali=materiali)


@app.route('/carica', methods=['GET', 'POST'])
def carica_materiale():
    """Carica un nuovo materiale."""
    if request.method == 'POST':
        titolo = request.form['titolo']
        descrizione = request.form['descrizione']
        tipo = request.form['tipo']
        file = request.files['file']

        filepath = file.filename  # Salva solo il nome del file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        materiale_control.upload_material(titolo, descrizione, filepath, tipo)
        flash("Materiale caricato con successo!", "success")
        return redirect(url_for('visualizza_materiale_docente'))

    return render_template('caricamentoMateriale.html')


@app.route('/modifica/<materiale_id>', methods=['GET', 'POST'])
def modifica_materiale(materiale_id):
    """Modifica un materiale esistente."""
    if request.method == 'POST':
        updated_data = {
            "Titolo": request.form['titolo'],
            "Descrizione": request.form['descrizione'],
            "Tipo": request.form['tipo'],
        }
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            updated_data['File_Path'] = filepath

        materiale_control.edit_material(materiale_id, updated_data)
        flash("Materiale modificato con successo!", "success")
        return redirect(url_for('visualizza_materiale_docente'))

    materiale = materiale_control.view_material({"_id": materiale_id})
    return render_template('modificaMateriale.html', materiale=materiale)


@app.route('/rimuovi/<materiale_id>')
def rimuovi_materiale(materiale_id):
    """Rimuove un materiale esistente."""
    materiale_control.delete_material(materiale_id)
    flash("Materiale rimosso con successo!", "success")
    return redirect(url_for('visualizza_materiale_docente'))


@app.route('/public/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.cli.command("migrate_paths")
def migrate_paths():
    materiali = db_manager.get_all_materials()
    for materiale in materiali:
        if os.path.isabs(materiale['File_Path']):
            materiale['File_Path'] = os.path.basename(materiale['File_Path'])
            db_manager.update_material(materiale['_id'], {'File_Path': materiale['File_Path']})
    print('Migrazione completata.')


if __name__ == '__main__':
    app.run(debug=True)  # Avvia l'app in modalità debug