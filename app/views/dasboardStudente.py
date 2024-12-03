from flask import Blueprint, session
from app.controllers.DashboardControl import DashboardController
from app.controllers.LoginControl import student_required

# Crea il blueprint
dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')


# Rotta per la dashboard
@dashboard_bp.route('/dashboard')
@student_required
def dashboard_studente():
    """
    Visualizza la dashboard per un utente specifico.
    """
    cf_studente = session.get('CF')
    id_classe = session.get('ID_Classe')
    # Usa il controller per ottenere i dati
    return DashboardController.mostra_dashboard(cf_studente, id_classe)
