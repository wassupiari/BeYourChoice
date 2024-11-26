from flask import render_template
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

        # Recupera dati dal modello
        classifica = model.get_classifica_classe(id_classe)
        punteggio_personale = model.get_punteggio_personale(cf_studente)

        # Chiude la connessione
        model.close_connection()

        # Passa i dati al template
        return render_template(
            "dashboardStudente.html",
            classifica=classifica,
            punteggio_personale=punteggio_personale
        )