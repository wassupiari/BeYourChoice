from flask import Blueprint, render_template, redirect, url_for, abort, session

from app.controllers.materialeControl import MaterialeControl
from databaseManager import DatabaseManager
from app.models.materialeModel import MaterialeModel

# Crea un Blueprint per la gestione lato studente
MaterialeStudente = Blueprint('MaterialeStudente', __name__)

# Inizializza il controllo del materiale
db_manager = DatabaseManager()
materiale_control = MaterialeControl(db_manager)
materiale_model = MaterialeModel(db_manager)
materiale_control.set_cartella_uploads('/public/uploads')


def initialize_materiale_studente_blueprint(app: object) -> object:
    @MaterialeStudente.route('/')
    def index():
        return redirect(url_for('MaterialeStudente.visualizza_materiale_studente'))

    @MaterialeStudente.route('/materiale/studente')
    def visualizza_materiale_studente():
        """Vista per visualizzare tutti i materiali disponibili per gli studenti."""
        id_classe = session.get('id_classe')
        cf_studente = session.get('cf_studente')

        if cf_studente:
            session['cf_studente'] = cf_studente
        else:
            abort(400, 'Parametro cf_studente mancante')

        if id_classe is None:
            # Passa cf_studente come parametro per costruire correttamente l'URL
            return redirect(url_for('dashboard.storico_studente', cf_studente=cf_studente))

        materiali = materiale_control.visualizza_materiali(id_classe)
        return render_template('materialeStudente.html', ID_Classe=id_classe, materiali=materiali)

    @MaterialeStudente.route('/servi_file/<path:nomefile>')
    def servi_file(nomefile: str):
        """Servizio per servire i file agli studenti."""
        return materiale_control.servi_file(nomefile)

    app.register_blueprint(MaterialeStudente)