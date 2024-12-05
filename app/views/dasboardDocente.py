from flask import render_template, jsonify

class TeacherDashboardView:
    @staticmethod
    def render_dashboard(classi):
        return render_template("dashboardDocente.html", classi=classi)

    @staticmethod
    def render_classifica(classifica, id_classe):
        return render_template("classificaClasse.html", classifica=classifica, ID_Classe=id_classe)

    @staticmethod
    def render_storico(storico, cf_studente):
        return render_template("storicoStudenti.html", storico=storico, cf_studente=cf_studente)

    @staticmethod
    def render_errore(messaggio, codice_http):
        return jsonify({"error": messaggio}), codice_http
