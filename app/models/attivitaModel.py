from datetime import datetime
from databaseManager import DatabaseManager


class Attivita:
    """
    La classe Attivita gestisce le operazioni relative alle attività degli utenti.
    """
    db_manager = DatabaseManager()

    def get_classifica_classe(self, id_classe):
        """
        Recupera la classifica della classe con i punteggi totali.
        """
        try:
            studente_collection = self.db_manager.get_collection("Studente")
            scenario_collection = self.db_manager.get_collection("PunteggioScenario")
            quiz_collection = self.db_manager.get_collection("RisultatoQuiz")

            studenti = list(
                studente_collection.find({"ID_Classe": id_classe}, {"_id": 0, "cf": 1, "nome": 1, "cognome": 1}))
            punteggi_totali = {studente["cf"]: {"PunteggioScenari": 0, "PunteggioQuiz": 0} for studente in studenti}

            scenari_punteggi = scenario_collection.aggregate([
                {"$group": {"_id": "$CF_Studente", "PunteggioScenari": {"$sum": "$Punteggio_Scenario"}}}
            ])
            for item in scenari_punteggi:
                if item["_id"] in punteggi_totali:
                    punteggi_totali[item["_id"]]["PunteggioScenari"] = item["PunteggioScenari"]

            quiz_punteggi = quiz_collection.aggregate([
                {"$group": {"_id": "$CF_Studente", "PunteggioQuiz": {"$sum": "$Punteggio_Quiz"}}}
            ])
            for item in quiz_punteggi:
                if item["_id"] in punteggi_totali:
                    punteggi_totali[item["_id"]]["PunteggioQuiz"] = item["PunteggioQuiz"]

            classifica = []
            for studente in studenti:
                cf_studente = studente["cf"]
                punteggio_scenari = punteggi_totali.get(cf_studente, {}).get("PunteggioScenari", 0)
                punteggio_quiz = punteggi_totali.get(cf_studente, {}).get("PunteggioQuiz", 0)
                punteggio_totale = punteggio_scenari + punteggio_quiz

                classifica.append({
                    "CF": cf_studente,
                    "Nome": studente["nome"],
                    "Cognome": studente["cognome"],
                    "PunteggioTotale": punteggio_totale
                })

            classifica.sort(key=lambda x: x["PunteggioTotale"], reverse=True)
            return classifica
        except Exception as e:
            print(f"Errore nel recupero della classifica: {e}")
            return []

    def get_punteggio_personale(self, cf_studente):
        """
        Calcola il punteggio personale dello studente.
        """
        try:
            scenario_collection = self.db_manager.get_collection("PunteggioScenario")
            quiz_collection = self.db_manager.get_collection("RisultatoQuiz")

            scenario_result = scenario_collection.aggregate([
                {"$match": {"CF_Studente": cf_studente}},
                {"$group": {"_id": "$CF_Studente", "PunteggioScenari": {"$sum": "$Punteggio_Scenario"}}}
            ])
            punteggio_scenari = next(scenario_result, {}).get("PunteggioScenari", 0)

            quiz_result = quiz_collection.aggregate([
                {"$match": {"CF_Studente": cf_studente}},
                {"$group": {"_id": "$CF_Studente", "PunteggioQuiz": {"$sum": "$Punteggio_Quiz"}}}
            ])
            punteggio_quiz = next(quiz_result, {}).get("PunteggioQuiz", 0)

            return {"PunteggioQuiz": punteggio_quiz, "PunteggioScenari": punteggio_scenari}
        except Exception as e:
            print(f"Errore nel calcolo del punteggio personale: {e}")
            return {"PunteggioQuiz": 0, "PunteggioScenari": 0}

    def get_storico(self, cf_studente):
        """
        Recupera lo storico dettagliato di tutte le attività dello studente.
        """
        try:
            dashboard_collection = self.db_manager.get_collection("Dashboard")
            attivita_risultati = list(dashboard_collection.find(
                {"CF_Studente": cf_studente},
                {"_id": 0, "ID_Attività": 1, "Data_Attività": 1, "Descrizione_Attività": 1, "punteggio_attività": 1}
            ))

            for attivita in attivita_risultati:
                if isinstance(attivita["Data_Attività"], datetime):
                    attivita["Data_Attività"] = attivita["Data_Attività"].strftime("%d/%m/%Y %H:%M:%S")

            return attivita_risultati
        except Exception as e:
            print(f"Errore durante il recupero dello storico: {e}")
            return []

    def get_classi_docente(self, id_docente):
        """
        Recupera le classi associate a un docente.
        """
        try:
            collection = self.db_manager.get_collection("ClasseVirtuale")
            return list(collection.find({"id_docente": id_docente}, {"_id": 0, "id_classe": 1, "nome_classe": 1}))
        except Exception as e:
            print(f"Errore durante il recupero delle classi del docente: {e}")
            return []
