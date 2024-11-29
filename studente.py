from flask import Flask, Blueprint, render_template, send_file, redirect, url_for, abort
from databaseManager import DatabaseManager
from app.controllers.MaterialeControl import MaterialeControl
import os

# Inizializza l'app Flask
app = Flask(__name__, static_folder='public', template_folder='app/templates')

# Set up the upload folder and other configurations
UPLOAD_FOLDER = 'public/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crea un Blueprint per la gestione lato studente
studente_bp = Blueprint('studente_bp', __name__, template_folder='app/templates')

# Inizializza il controllo del materiale
db_manager = DatabaseManager()
materiale_control = MaterialeControl(db_manager)


@studente_bp.route('/')
def home():
    return redirect(url_for('studente_bp.visualizza_materiale_studente'))


@studente_bp.route('/materiale/studente')
def visualizza_materiale_studente():
    """Vista per visualizzare tutti i materiali disponibili per gli studenti."""
    materiali = materiale_control.view_all_materials()
    return render_template('materialeStudente.html', materiali=materiali)


@studente_bp.route('/serve_file/<path:filename>')
def serve_file(filename: str):
    """Servizio per servire i file agli studenti."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath)
    else:
        abort(404)


@app.route('/favicon.ico')
def favicon():
    return '', 204  # restituire una risposta vuota con codice di stato 204


# Registra il blueprint con l'applicazione
app.register_blueprint(studente_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Puoi mantenere questa impostazione o cambiarla
