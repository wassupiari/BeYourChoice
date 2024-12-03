from flask import Flask
from databaseManager import DatabaseManager
from app.views.materialeDocente import initialize_materiale_docente_blueprint


def create_app(config=None):
    # Inizializza l'app Flask
    app = Flask(__name__)

    app.secret_key = 'supersegreta'

    # Configura l'app utilizzando un dizionario di configurazione
    if config:
        app.config.update(config)

    # Configurazione predefinita
    app.config.setdefault('UPLOAD_FOLDER', '/path/to/upload')  # Cambia con il percorso che hai scelto

    # Configurazione del database
    database_uri = "mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/?retryWrites=true&w=majority&appName=BeYourChoice"
    db_manager = DatabaseManager(database_uri)

    # Configura e registra i blueprint

    initialize_materiale_docente_blueprint(app)

    # Inizializza altri componenti o estensioni se necessario

    @app.route('/ping')
    def ping():
        return "pong"

    return app