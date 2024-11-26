from flask import render_template
from app.models.Studente import Studente

class DashboardController:
    @staticmethod
    def mostra_dashboard(id_classe, email_utente):
        """
        Recupera i dati per la dashboard e li passa alla vista.
        """
        model = Studente()

        # Recupera dati dal modello
        classifica = model.get_classifica_classe(id_classe)
        punteggio_personale = model.get_punteggio_personale(email_utente)

        # Chiude la connessione
        model.close_connection()

        # Passa i dati al template
        return render_template(
            "dashboardStudente.html",
            classifica=classifica,
            punteggio_personale=punteggio_personale
        )