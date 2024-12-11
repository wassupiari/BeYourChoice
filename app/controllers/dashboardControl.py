from flask import Blueprint, session
from app.models.attivitaModel import Attivita
from app.views.dasboardDocente import TeacherDashboardView
from app.controllers.loginControl import teacher_required, student_required
from app.views.dasboardStudente import StudentDashboardView

# Blueprint per la dashboard del docente
dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='../templates')

class DashboardController:
    @staticmethod
    @dashboard_blueprint.route('/dashboard-docente', methods=['GET'])
    @teacher_required
    def dashboard_docente():
        codice_univoco = session.get('cu')
        if not codice_univoco:
            return TeacherDashboardView.render_errore("Codice univoco del docente non trovato", 404)

        model = Attivita()
        classi = model.get_classi_docente(codice_univoco)
        return TeacherDashboardView.render_dashboard(classi)

    @staticmethod
    @dashboard_blueprint.route('/classifica/<int:id_classe>', methods=['GET'])
    @teacher_required
    def classifica_classe(id_classe):
        session['id_classe'] = id_classe
        model = Attivita()
        classifica = model.get_classifica_classe(id_classe)
        return TeacherDashboardView.render_classifica(classifica, id_classe)

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
        Mostra la dashboard dello studente con punteggio_attivita e storico.
        """
        cf_studente = session.get('cf')
        id_classe = session.get('id_classe')

        if not cf_studente:
            return StudentDashboardView.render_errore("Sessione non valida", 400)

        model = Attivita()
        punteggio_attivita = model.get_punteggio_personale(cf_studente)
        classifica = model.get_classifica_classe(id_classe)
        storico = model.get_storico(cf_studente)

        return StudentDashboardView.render_dashboard(
            classifica=classifica,
            punteggio_scenario=punteggio_attivita.get("PunteggioScenari"),
            punteggio_quiz=punteggio_attivita.get("punteggio_quiz"),
            punteggio_totale=punteggio_attivita.get("PunteggioScenari", 0) + punteggio_attivita.get("punteggio_quiz", 0),
            storico=storico
        )