from flask import Blueprint, request
from app.controllers.DashboardControl import DashboardController
from app.models.docenteModel import DocenteModel
from app.controllers.loginControl import teacher_required

# Crea il blueprint per la dashboard del docente
dashboardDocente_bp = Blueprint('dashboardDocente', __name__, template_folder='../templates')

# Rotta per la dashboard del docente
@dashboardDocente_bp.route('/dashboardDocente', methods=['GET'])
@teacher_required
def dashboard():
    """
    Visualizza la dashboard per il docente autenticato.
    """
    docente_model = DocenteModel()

    # Recupera l'email del docente dalla sessione o dalla query string
    email = request.args.get("email", None)
    if not email:
        return "Email del docente non fornita", 400

    # Recupera il codice univoco del docente utilizzando l'email
    codice_univoco = docente_model.get_codice_univoco_by_email(email)
    if not codice_univoco:
        return "Docente non trovato", 404

    # Usa il controller per ottenere i dati della dashboard
    return DashboardController.mostra_dasboardDocente(codice_univoco)


# Rotta per la classifica di una classe specifica
@dashboardDocente_bp.route('/classificaClasse/<int:id_classe>', methods=['GET'])
@teacher_required
def classifica_classe(id_classe):
    """
    Visualizza la classifica di una specifica classe gestita dal docente.
    """
    return DashboardController.mostra_classifica_classe(id_classe)


# Rotta per lo storico delle attività di uno studente specifico
@dashboardDocente_bp.route('/storicoStudente/<string:cf_studente>', methods=['GET'])
@teacher_required
def storico_studente(cf_studente):
    """
    Visualizza lo storico delle attività svolte da uno studente specifico.
    """
    return DashboardController.mostra_storico_studente(cf_studente)
