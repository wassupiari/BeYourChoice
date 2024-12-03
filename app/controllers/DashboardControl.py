from flask import render_template, session
from app.models.Attivita import Attivita


class DashboardController:
    """
    Controller per la gestione delle dashboard di studenti e docenti.

    Metodi:
    - mostra_dashboard(cf_studente, id_classe): Mostra la dashboard per uno studente
        in una determinata classe.
    - mostra_dashboard_docente(id_docente): Mostra la dashboard per un docente
        con le classi gestite.
    - mostra_classifica_classe(id_classe): Mostra la classifica di una specifica classe.
    - mostra_storico_studente(cf_studente): Mostra lo storico delle attività svolte da
        uno studente.
    """

    @staticmethod
    def mostra_dashboard(cf_studente, id_classe):
        """
        Mostra la dashboard per uno studente in una determinata classe.
        :param cf_studente: Codice fiscale dello studente.
        :param id_classe: ID della classe.
        :return: Il rendering della vista 'dashboardStudente.html'.
        """
        session['ID_Classe'] = id_classe

        model = Attivita()

        # Recupera i punteggi dello studente
        punteggi = model.get_punteggio_personale(cf_studente)
        punteggio_scenario = punteggi.get("PunteggioScenari", 0)
        punteggio_quiz = punteggi.get("PunteggioQuiz", 0)
        punteggio_totale = punteggio_scenario + punteggio_quiz

        # Recupera la classifica e lo storico dello studente
        classifica = model.get_classifica_classe(id_classe)
        storico = model.get_storico(cf_studente)



        # Passa i dati al template
        return render_template(
            "dashboardStudente.html",
            classifica=classifica,
            punteggio_scenario=punteggio_scenario,
            punteggio_quiz=punteggio_quiz,
            punteggio_totale=punteggio_totale,
            storico=storico
        )

    @staticmethod
    def mostra_dashboard_docente(id_docente):
        """
        Mostra la dashboard per un docente con le classi gestite.
        :param id_docente: ID del docente.
        :return: Il rendering della vista 'dashboardDocente.html'.
        """
        model = Attivita()

        # Recupera le classi associate al docente
        classi = model.get_classi_docente(id_docente)



        # Passa i dati al template
        return render_template(
            "dashboardDocente.html",
            classi=classi
        )

    @staticmethod
    def mostra_classifica_classe(id_classe):
        """
        Mostra la classifica di una specifica classe.
        :param id_classe: ID della classe.
        :return: Il rendering della vista 'classificaClasse.html'.
        """
        session['ID_Classe'] = id_classe

        model = Attivita()

        # Recupera la classifica della classe
        classifica = model.get_classifica_classe(id_classe)



        # Passa i dati al template
        return render_template(
            "classificaClasse.html",
            classifica=classifica,
            ID_Classe=id_classe
        )

    @staticmethod
    def mostra_storico_studente(cf_studente):
        """
        Mostra lo storico delle attività svolte da uno studente.
        :param cf_studente: Codice fiscale dello studente.
        :return: Il rendering della vista 'storicoStudente.html'.
        """
        model = Attivita()

        # Recupera lo storico dello studente
        storico = model.get_storico(cf_studente)



        # Passa i dati al template
        return render_template(
            "storicoStudenti.html",
            storico=storico,
            cf_studente=cf_studente
        )
