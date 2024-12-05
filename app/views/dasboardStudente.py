from flask import Blueprint, render_template, jsonify, session

# Crea il blueprint per la dashboard dello studente
student_dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='../templates')

class StudentDashboardView:
    @staticmethod
    def render_dashboard(classifica, punteggio_scenario, punteggio_quiz, punteggio_totale, storico):
        """
        Mostra la dashboard dello studente con classifica, punteggi e storico.
        """
        return render_template(
            "dashboardStudente.html",
            classifica=classifica,
            punteggio_scenario=punteggio_scenario,
            punteggio_quiz=punteggio_quiz,
            punteggio_totale=punteggio_totale,
            storico=storico
        )


    @staticmethod
    def render_errore(messaggio, codice_http):
        """
        Mostra un errore generico per le pagine dello studente.
        """
        return jsonify({"error": messaggio}), codice_http
