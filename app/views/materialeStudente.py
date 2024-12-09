from flask import Flask, Blueprint, render_template, send_file, redirect, url_for, abort, session

from app.models.materialeModel import MaterialeModel
from databaseManager import DatabaseManager
from app.controllers.materialeControl import MaterialeControl
import os

# Crea un Blueprint per la gestione lato studente
MaterialeStudente = Blueprint('MaterialeStudente', __name__)

# Inizializza il controllo del materiale
db_manager = DatabaseManager()
materiale_control = MaterialeControl(db_manager)
materiale_model = MaterialeModel(db_manager)
materiale_model.set_cartella_uploads('/public/uploads')


def initialize_materiale_studente_blueprint(app: object) -> object:
    @MaterialeStudente.route('/')
    def index():
        return redirect(url_for('MaterialeStudente.visualizza_materiale_studente'))

    @MaterialeStudente.route('/materiale/studente')
    def visualizza_materiale_studente():
        """Vista per visualizzare tutti i materiali disponibili per gli studenti."""
        id_classe = session.get('id_classe')
        cf_studente = session.get('cf_studente')

        if cf_studente is None:
            # Tentativo di recupero del cf_studente, simulando una fonte, ad esempio un database
            cf_studente = recupera_cf_studente()
            if cf_studente:
                session['cf_studente'] = cf_studente
            else:
                abort(400, 'Parametro cf_studente mancante')

        if id_classe is None:
            # Passa cf_studente come parametro per costruire correttamente l'URL
            return redirect(url_for('dashboard.storico_studente', cf_studente=cf_studente))

        materiali = materiale_model.visualizza_materiali(id_classe)
        return render_template('materialeStudente.html', ID_Classe=id_classe, materiali=materiali)

    @MaterialeStudente.route('/servi_file/<path:nomefile>')
    def servi_file(nomefile: str):
        """Servizio per servire i file agli studenti."""
        return materiale_model.servi_file(nomefile)

    app.register_blueprint(MaterialeStudente)


def recupera_cf_studente():
    # Implementa qui la logica per ottenere cf_studente
    # Per scopi di esempio, restituiamo un valore fisso
    return 'cf_studente_esempio'  # Sostituisci con la logica effettiva