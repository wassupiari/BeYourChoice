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
                studente_collection.find({"id_classe": id_classe}, {"_id": 0, "cf": 1, "nome": 1, "cognome": 1}))
            punteggi_totali = {studente["cf"]: {"punteggio_scenario": 0, "punteggio_quiz": 0} for studente in studenti}

            scenari_punteggi = scenario_collection.aggregate([
                {"$group": {"_id": "$cf_studente", "punteggio_scenario": {"$sum": "$punteggio_scenario"}}}
            ])
            for item in scenari_punteggi:
                if item["_id"] in punteggi_totali:
                    punteggi_totali[item["_id"]]["punteggio_scenario"] = item["punteggio_scenario"]

            quiz_punteggi = quiz_collection.aggregate([
                {"$group": {"_id": "$cf_studente", "punteggio_quiz": {"$sum": "$punteggio_quiz"}}}
            ])
            for item in quiz_punteggi:
                if item["_id"] in punteggi_totali:
                    punteggi_totali[item["_id"]]["punteggio_quiz"] = item["punteggio_quiz"]

            classifica = []
            for studente in studenti:
                cf_studente = studente["cf"]
                punteggio_scenario = punteggi_totali.get(cf_studente, {}).get("punteggio_scenario", 0)
                punteggio_quiz = punteggi_totali.get(cf_studente, {}).get("punteggio_quiz", 0)
                punteggio_totale = punteggio_scenario + punteggio_quiz

                classifica.append({
                    "cf": cf_studente,
                    "nome": studente["nome"],
                    "cognome": studente["cognome"],
                    "punteggio_totale": punteggio_totale
                })

            classifica.sort(key=lambda x: x["punteggio_totale"], reverse=True)
            return classifica
        except Exception as e:
            print(f"Errore nel recupero della classifica: {e}")
            return []

    def get_punteggio_personale(self, cf_studente):
        try:
            scenario_collection = self.db_manager.get_collection("PunteggioScenario")
            quiz_collection = self.db_manager.get_collection("RisultatoQuiz")

            print(f"DEBUG: Recupero punteggio per lo studente {cf_studente}")

            scenario_result = scenario_collection.aggregate([
                {"$match": {"CF_Studente": cf_studente}},
                {"$group": {"_id": "$CF_Studente", "PunteggioScenari": {"$sum": "$Punteggio_Scenario"}}}
            ])
            print(f"DEBUG: Risultato scenari: {list(scenario_result)}")

            quiz_result = quiz_collection.aggregate([
                {"$match": {"cf_studente": cf_studente}},  # Filtra per studente
                {"$group": {"_id": "$cf_studente", "punteggio_quiz": {"$sum": "$punteggio_quiz"}}}  # Somma i punteggi
            ])
            punteggio_quiz = next(quiz_result, {}).get("punteggio_quiz", 0)  # Ottieni il valore o 0

            print(f"DEBUG: Risultato quiz: {list(quiz_result)}")

            punteggio_scenari = next(scenario_result, {}).get("PunteggioScenari", 0)


            return {"punteggio_quiz": punteggio_quiz, "PunteggioScenari": punteggio_scenari}
        except Exception as e:
            print(f"Errore nel calcolo del punteggio personale: {e}")
            return {"punteggio_quiz": 0, "PunteggioScenari": 0}

    def get_storico(self, cf_studente):
        """
        Recupera lo storico dettagliato di tutte le attività dello studente.
        """
        try:
            dashboard_collection = self.db_manager.get_collection("Dashboard")
            attivita_risultati = list(dashboard_collection.find(
                {"cf_studente": cf_studente},
                {"_id": 0, "id_attivita": 1, "data_attivita": 1, "descrizione_attivita": 1, "punteggio_attivita": 1}
            ))

            for attivita in attivita_risultati:
                if isinstance(attivita["data_attivita"], datetime):
                    attivita["data_attivita"] = attivita["data_attivita"].strftime("%d/%m/%Y %H:%M:%S")

            return attivita_risultati
        except Exception as e:
            print(f"Errore durante il recupero dello storico: {e}")
            return []

    def get_classi_docente(self, id_docente):
        """
        Recupera le classi associate a un docente e calcola il punteggio totale di ogni classe.
        """
        print("prova")
        try:
            collection = self.db_manager.get_collection("ClasseVirtuale")
            studente_collection = self.db_manager.get_collection("Studente")
            quiz_collection = self.db_manager.get_collection("RisultatoQuiz")
            scenario_collection = self.db_manager.get_collection("PunteggioScenario")

            # Recupera tutte le classi del docente
            classi = list(collection.find({"id_docente": id_docente}, {"_id": 0, "id_classe": 1, "nome_classe": 1}))

            for classe in classi:
                id_classe = classe["id_classe"]

                # Recupera gli studenti della classe
                studenti = list(studente_collection.find({"id_classe": id_classe}, {"cf": 1}))

                # Calcola il punteggio totale dei quiz per la classe
                cf_studenti = [studente["cf"] for studente in studenti]

                punteggio_quiz = quiz_collection.aggregate([
                    {"$match": {"cf_studente": {"$in": cf_studenti}}},
                    {"$group": {"_id": None, "totale_quiz": {"$sum": "$punteggio_quiz"}}}
                ])
                punteggio_quiz_totale = next(punteggio_quiz, {}).get("totale_quiz", 0)

                # Calcola il punteggio totale degli scenari per la classe
                punteggio_scenario = scenario_collection.aggregate([
                    {"$match": {"CF_Studente": {"$in": cf_studenti}}},
                    {"$group": {"_id": None, "totale_scenario": {"$sum": "$Punteggio_Scenario"}}}
                ])
                punteggio_scenario_totale = next(punteggio_scenario, {}).get("totale_scenario", 0)

                # Somma i punteggi totali
                classe["punteggio_totale"] = punteggio_quiz_totale + punteggio_scenario_totale

            # Ordina le classi per punteggio totale in ordine decrescente
            classi.sort(key=lambda x: x["punteggio_totale"], reverse=True)

            return classi
        except Exception as e:
            print(f"Errore durante il recupero delle classi del docente: {e}")
            return []

