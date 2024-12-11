"""

Questo modulo definisce le route per gestire il materiale didattico
lato docente. Permette operazioni di visualizzazione, caricamento,
modifica e rimozione di materiali.

Autore: [il tuo nome]
Data di creazione: [data di creazione]
"""

from bson import ObjectId
from flask import render_template, request, redirect, url_for, Blueprint, session

from app.controllers.loginControl import teacher_required
from databaseManager import DatabaseManager
from app.controllers.materialeControl import MaterialeControl
from app.models.materialeModel import MaterialeModel

MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'jpeg', 'png', 'txt', 'jpg', 'mp4'}

# Supponiamo che DatabaseManager sia il manager db richiesto

db_manager = DatabaseManager()

# Passa l'istanza di db_manager a MaterialeModel
materiale_control = MaterialeControl(db_manager)
materiale_model = MaterialeModel(db_manager)
materiale_control.set_cartella_uploads('public/uploads')

MaterialeDocente = Blueprint('MaterialeDocente', __name__)

collezione_materiali = db_manager.get_collection('MaterialeDidattico')
def initialize_materiale_docente_blueprint(app: object) -> object:
    """
    Inizializza il blueprint per le operazioni del docente sui materiali.

    :param app: L'applicazione Flask su cui registrare il blueprint.
    :return: None
    """
    @MaterialeDocente.route('/')
    def index():
        """
        Redireziona alla visualizzazione del materiale docente.
        """
        return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    @MaterialeDocente.route('/materiale/docente')
    @teacher_required
    def visualizza_materiale_docente():
        """
       Mostra i materiali associati alla classe corrente del docente.
       """
        id_classe = session.get('id_classe')
        materiali = materiale_control.visualizza_materiali(id_classe)
        return render_template('materialeDocente.html', materiali=materiali)

    @MaterialeDocente.route('/servi_file/<path:nome_file>')
    def servi_file(nome_file: str):
        """
        Serve un file all'utente dato il nome del file richiesto.

        :param nome_file: Nome del file da servire.
        :return: Risposta del file servito.
        """
        return materiale_control.servi_file(nome_file)

    @MaterialeDocente.route('/carica', methods=['GET', 'POST'])
    @teacher_required
    def carica_materiale():
        """
       Gestisce il caricamento di nuovi materiali.
       """
        if request.method == 'POST':
            return materiale_control.carica_materiale(request)
        return render_template('caricamentoMateriale.html')

    @MaterialeDocente.route('/modifica/<string:id_materiale>', methods=['GET', 'POST'])
    @teacher_required
    def modifica_materiale(id_materiale):
        """
       Modifica un materiale già esistente.

       :param id_materiale: ID del materiale da modificare.
       """
        if request.method == 'POST':
            return materiale_control.modifica_materiale(id_materiale, request)

        # Se GET, recupera il materiale per visualizzarlo nel form
        try:
            id_materiale_obj = ObjectId(id_materiale)
            print(f"Recupero materiale con ID: {id_materiale_obj}")

            materiale = collezione_materiali.find_one({"_id": id_materiale_obj})
            if materiale is None:
                print(f"Nessun materiale trovato con ID: {id_materiale_obj}")
                return render_template('modificaMateriale.html', messaggio="Il materiale non è stato trovato.")

            return render_template('modificaMateriale.html', materiale=materiale)
        except Exception as e:
            print(f"Errore nel recupero del materiale: {str(e)}")
            return render_template('modificaMateriale.html', messaggio="Errore nel recupero del materiale.")

    @MaterialeDocente.route('/rimuovi/<id_materiale>')
    @teacher_required
    def rimuovi_materiale(id_materiale):
        """
        Rimuove un materiale dalla base dati e dal file system se presente.

        :param id_materiale: ID del materiale da rimuovere.
        """
        return materiale_control.rimuovi_materiale(id_materiale)

    app.register_blueprint(MaterialeDocente)