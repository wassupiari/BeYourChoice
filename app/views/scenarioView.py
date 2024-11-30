from flask import Blueprint, render_template, request

# Crea un Blueprint per il modulo Scenario
scenario_bp = Blueprint('scenario_bp', __name__)

@scenario_bp.route('/scenarioVirtuale')
def scenario_virtuale():
    # Recupera l'eventuale parametro 'error' dalla query string
    error = request.args.get('error')
    # Renderizza il template passando l'errore (se esiste)
    return render_template('scenarioVirtuale.html', error=error)
