from flask import Blueprint, request, session, render_template
from app.controllers.DashboardControl import DashboardController
from app.models.docenteModel import DocenteModel
from app.controllers.loginControl import teacher_required

# Crea il blueprint per la dashboard del docente
dashboardDocente = Blueprint('dashboardDocente', __name__, template_folder='../templates')
print("entrooooo")
# Rotta per la dashboard del docente
@dashboardDocente.route('/dashboardDocente', methods=['GET'])
@teacher_required  # Usa il decoratore per proteggere la rotta
def dashboard():
    """
    Visualizza la dashboard per il docente autenticato.
    """
    # Verifica se la sessione contiene l'email
    email = session.get('email')
    if not email:
        return "Email del docente non fornita", 400

    # Recupera il codice univoco del docente dalla sessione
    codice_univoco = session.get('CU')
    if not codice_univoco:
        return "Codice univoco del docente non trovato", 404

    # Recupera i dati necessari per il template (ad esempio, la lista delle classi)
    docente_model = DocenteModel()

    # Rendi il template con i dati necessari
    return DashboardController.mostra_dasboardDocente(codice_univoco)



# Rotta per la classifica di una classe specifica
@dashboardDocente.route('/classificaClasse/<int:ID_Classe>', methods=['GET'])
@teacher_required
def classifica_classe(ID_Classe):
    """
    Visualizza la classifica di una specifica classe gestita dal docente.
    """

    return DashboardController.mostra_classifica_classe(ID_Classe)


# Rotta per lo storico delle attività di uno studente specifico
@dashboardDocente.route('/storicoStudente/<string:cf_studente>', methods=['GET'])
@teacher_required
def storico_studente(cf_studente):
    """
    Visualizza lo storico delle attività svolte da uno studente specifico.
    """
    return DashboardController.mostra_storico_studente(cf_studente)
