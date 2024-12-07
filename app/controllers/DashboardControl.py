from flask import Blueprint, session
from app.models.attivitaModel import Attivita
from app.views.dasboardDocente import TeacherDashboardView
from app.controllers.LoginControl import teacher_required, student_required
from app.views.dasboardStudente import StudentDashboardView

# Blueprint per la dashboard del docente
dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='../templates')

class DashboardController:
    @staticmethod
    @dashboard_blueprint.route('/dashboard-docente', methods=['GET'])
    @teacher_required
    def dashboard_docente():
        codice_univoco = session.get('CU')
        if not codice_univoco:
            return TeacherDashboardView.render_errore("Codice univoco del docente non trovato", 404)

        model = Attivita()
        classi = model.get_classi_docente(codice_univoco)
        return TeacherDashboardView.render_dashboard(classi)

    @staticmethod
    @dashboard_blueprint.route('/classifica/<int:ID_Classe>', methods=['GET'])
    @teacher_required
    def classifica_classe(ID_Classe):
        session['ID_Classe'] = ID_Classe
        model = Attivita()
        classifica = model.get_classifica_classe(ID_Classe)
        return TeacherDashboardView.render_classifica(classifica, ID_Classe)

    @staticmethod
    @dashboard_blueprint.route('/storico/<string:cf_studente>', methods=['GET'])
    @teacher_required
    def storico_studente(cf_studente):
        model = Attivita()
        storico = model.get_storico(cf_studente)
        return TeacherDashboardView.render_storico(storico, cf_studente)

    @staticmethod
    @dashboard_blueprint.route('/dashboard-studente', methods=['GET'])
    @student_required
    def dashboard_studente():
        """
        Mostra la dashboard dello studente con punteggi e storico.
        """
        cf_studente = session.get('cf')
        id_classe = session.get('ID_Classe')

        if not cf_studente:
            return StudentDashboardView.render_errore("Sessione non valida", 400)

        model = Attivita()
        punteggi = model.get_punteggio_personale(cf_studente)
        classifica = model.get_classifica_classe(id_classe)
        storico = model.get_storico(cf_studente)

        return StudentDashboardView.render_dashboard(
            classifica=classifica,
            punteggio_scenario=punteggi.get("PunteggioScenari"),
            punteggio_quiz=punteggi.get("PunteggioQuiz", 0),
            punteggio_totale=punteggi.get("PunteggioScenari", 0) + punteggi.get("PunteggioQuiz", 0),
            storico=storico
        )