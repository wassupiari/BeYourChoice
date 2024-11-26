from flask import Blueprint, request
from app.controllers.ClasseVirtualeControl import ClasseVirtuale

# Crea il blueprint
dashboard_bp = Blueprint('classedocente', __name__, template_folder='../templates')

# Rotta per la dashboard
@dashboard_bp.route('/classedocente')
def classedocente():
    """
    Visualizza la dashboard per un utente specifico.
    """
    # Ottieni i parametri dalla query string
    id_classe = int(request.args.get("ID_classe", 101))

    # Usa il controller per ottenere i dati
    return ClasseVirtuale.mostra_classe(id_classe)