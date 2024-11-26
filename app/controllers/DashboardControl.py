from flask import render_template

from app.models.Docente import Docente
from app.models.Studente import Studente

class DashboardController:
    @staticmethod
    def mostra_dashboard(cf_studente, id_classe):
        """
        Mostra la dashboard per un determinato utente e classe.
        :param cf_studente: Codice fiscale dello studente.
        :param id_classe: ID della classe.
        :return: Il rendering della vista 'dashboard.html'.
        """
        model = Studente()

        # Recupera i punteggi
        classifica = model.get_classifica_classe(id_classe)
        punteggio_scenario = model.get_punteggio_personale(cf_studente)  # Punteggio dagli scenari
        punteggio_quiz = model.get_punteggio_quiz(cf_studente)  # Punteggio dai quiz

        # Totale generale
        punteggio_totale = punteggio_scenario + punteggio_quiz

        storico = model.get_storico(cf_studente)
        # Chiude la connessione
        model.close_connection()

        # Passa i dati al template
        return render_template(
            "dashboardStudente.html",
            classifica=classifica,
            punteggio_scenario=punteggio_scenario,
            punteggio_quiz=punteggio_quiz,
            punteggio_totale=punteggio_totale,
            storico = storico
        )

    @staticmethod
    def mostra_dasboardDocente(id_docente):
        model = Docente()
        classi = model.get_classi_docente(id_docente)
        model.close_connection()

        return render_template(
            "dashboardDocente.html",
            classi=classi
        )

    @staticmethod
    def mostra_classifica_classe(id_classe):
        """
        Recupera la classifica di una specifica classe.
        :param id_classe: ID della classe.
        :return: Il rendering della classifica della classe.
        """
        try:
            model = Docente()
            classifica = model.get_classifica_classe(id_classe)
            model.close_connection()
            return render_template("classificaClasse.html", classifica=classifica, id_classe=id_classe)
        except Exception as e:
            print(f"Errore nella gestione della classifica classe: {e}")

    @staticmethod
    def mostra_storico_studente(cf_studente):
        """
        Recupera lo storico di tutte le attività svolte da uno studente specifico.
        :param cf_studente: Codice fiscale dello studente.
        :return: Il rendering della pagina dello storico dello studente.
        """
        try:
            model = Docente()

            # Recupera lo storico dello studente
            storico = model.get_storico(cf_studente)

            # Chiude la connessione al database
            model.close_connection()

            # Renderizza il template con lo storico
            return render_template("storicoStudenti.html", storico=storico, cf_studente=cf_studente)
        except Exception as e:
            print(f"Errore nella gestione dello storico studente: {e}")
