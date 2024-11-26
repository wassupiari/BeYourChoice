from flask import Blueprint, request
from app.controllers.DashboardControl import DashboardController

# Crea il blueprint
dashboardDocente_bp = Blueprint('dashboardDocente', __name__, template_folder='../templates')

# Rotta per la dashboard
@dashboardDocente_bp.route('/dashboardDocente')
def dashboard():
    """
    Visualizza la dashboard per un utente specifico.
    """
    # Ottieni i parametri dalla query string

    id_docente = int(request.args.get("id_docente", 1001))

    # Usa il controller per ottenere i dati
    return DashboardController.mostra_dasboardDocente(id_docente)

@dashboardDocente_bp.route('/classificaClasse/<int:id_classe>')
def classifica_classe(id_classe):
    """
    Visualizza la classifica di una specifica classe.
    """
    return DashboardController.mostra_classifica_classe(id_classe)
@dashboardDocente_bp.route('/storicoStudente/<string:cf_studente>')
def storico_studente(cf_studente):
    """
    Visualizza lo storico di tutte le attività svolte da uno studente specifico.
    """
    return DashboardController.mostra_storico_studente(cf_studente)
