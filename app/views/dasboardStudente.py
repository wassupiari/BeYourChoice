from flask import Blueprint, request
from app.controllers.DashboardControl import DashboardController

# Crea il blueprint
dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')

# Rotta per la dashboard
@dashboard_bp.route('/dashboard')
def dashboard():
    """
    Visualizza la dashboard per un utente specifico.
    """
    # Ottieni i parametri dalla query string
    email_utente = request.args.get("email", "utente@example.com")
    id_classe = int(request.args.get("id_classe", 101))

    # Usa il controller per ottenere i dati
    return DashboardController.mostra_dashboard(id_classe, email_utente)
