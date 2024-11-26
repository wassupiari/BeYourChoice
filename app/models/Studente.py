from databaseManager import DatabaseManager

class Studente:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_classifica_classe(self, id_classe):
        """
        Recupera la classifica della classe ordinata per punteggio decrescente.
        Combina i punteggi di scenari e quiz per ciascuno studente.
        :param id_classe: ID della classe.
        :return: Lista degli studenti con Nome, Cognome e Punteggio Totale.
        """
        try:
            # Collezioni necessarie
            studente_collection = self.db_manager.get_collection("Studente")
            scenario_collection = self.db_manager.get_collection("PunteggioScenario")
            quiz_collection = self.db_manager.get_collection("RisultatoQuiz")

            # Recupera gli studenti della classe
            studenti = list(
                studente_collection.find(
                    {"ID_Classe": id_classe},
                    {"_id": 0, "CF": 1, "Nome": 1, "Cognome": 1}
                )
            )

            # Mappa per i punteggi
            punteggi_totali = {}

            # Calcola i punteggi dagli scenari
            scenari_punteggi = scenario_collection.aggregate([
                {"$group": {"_id": "$CF_Studente", "PunteggioScenari": {"$sum": "$Punteggio_Scenario"}}}
            ])

            # Aggiunge i punteggi dagli scenari alla mappa
            for item in scenari_punteggi:
                punteggi_totali[item["_id"]] = {"PunteggioScenari": item["PunteggioScenari"], "PunteggioQuiz": 0}

            # Calcola i punteggi dai quiz
            quiz_punteggi = quiz_collection.aggregate([
                {"$group": {"_id": "$CF_Studente", "PunteggioQuiz": {"$sum": "$Punteggio_Quiz"}}}
            ])

            # Aggiunge i punteggi dai quiz alla mappa
            for item in quiz_punteggi:
                if item["_id"] in punteggi_totali:
                    punteggi_totali[item["_id"]]["PunteggioQuiz"] = item["PunteggioQuiz"]
                else:
                    punteggi_totali[item["_id"]] = {"PunteggioScenari": 0, "PunteggioQuiz": item["PunteggioQuiz"]}

            # Combina i dati degli studenti con i punteggi
            classifica = []
            for studente in studenti:
                cf_studente = studente["CF"]
                punteggio_scenari = punteggi_totali.get(cf_studente, {}).get("PunteggioScenari", 0)
                punteggio_quiz = punteggi_totali.get(cf_studente, {}).get("PunteggioQuiz", 0)
                punteggio_totale = punteggio_scenari + punteggio_quiz

                classifica.append({
                    "Nome": studente["Nome"],
                    "Cognome": studente["Cognome"],
                    "PunteggioTotale": punteggio_totale
                })

            # Ordina la classifica per punteggio totale decrescente
            classifica.sort(key=lambda x: x["PunteggioTotale"], reverse=True)

            return classifica
        except Exception as e:
            print(f"Errore nel recupero della classifica: {e}")
            return []

    def get_punteggio_personale(self, cf_studente):
        """
        Calcola il punteggio personale dello studente sommando tutti i Punteggio_Scenario.
        :param cf_studente: Codice fiscale dello studente.
        :return: Il punteggio totale dello studente.
        """
        try:
            collection = self.db_manager.get_collection("PunteggioScenario")

            # Esegui l'aggregazione per sommare i punteggi
            result = collection.aggregate([
                {"$match": {"CF_Studente": cf_studente}},  # Filtra gli scenari dello studente
                {"$group": {"_id": "$CF_Studente", "PunteggioTotale": {"$sum": "$Punteggio_Scenario"}}}
            ])

            # Recupera il risultato
            punteggio = next(result, None)
            return punteggio["PunteggioTotale"] if punteggio else 0
        except Exception as e:
            print(f"Errore nel calcolo del punteggio personale: {e}")
            return 0

    def get_punteggio_quiz(self, cf_studente):
        """
        Calcola il punteggio personale dello studente sommando tutti i Punteggio_Quiz.
        :param cf_studente: Codice fiscale dello studente.
        :return: Il punteggio totale relativo ai quiz.
        """
        try:
            collection = self.db_manager.get_collection("RisultatoQuiz")

            # Esegui l'aggregazione per sommare i punteggi
            result = collection.aggregate([
                {"$match": {"CF_Studente": cf_studente}},  # Filtra i quiz dello studente
                {"$group": {"_id": "$CF_Studente", "PunteggioTotale": {"$sum": "$Punteggio_Quiz"}}}
            ])

            # Recupera il risultato
            punteggio = next(result, None)
            return punteggio["PunteggioTotale"] if punteggio else 0
        except Exception as e:
            print(f"Errore nel calcolo del punteggio dei quiz: {e}")
            return 0

    def get_storico(self, cf_studente):
        """
        Recupera lo storico dettagliato di tutti i quiz e scenari svolti dallo studente.
        :param cf_studente: Codice fiscale dello studente.
        :return: Un dizionario contenente i dettagli dei quiz e degli scenari svolti.
        """
        try:
            # Collezioni necessarie
            risultato_quiz_collection = self.db_manager.get_collection("RisultatoQuiz")
            risultato_scenario_collection = self.db_manager.get_collection("PunteggioScenario")
            quiz_collection = self.db_manager.get_collection("Quiz")
            scenario_collection = self.db_manager.get_collection("ScenarioVirtuale")

            # Recupera gli ID dei quiz svolti dallo studente
            quiz_risultati = list(
                risultato_quiz_collection.find(
                    {"CF_Studente": cf_studente},
                    {"_id": 0, "ID_Quiz": 1, "Punteggio_Quiz": 1}
                )
            )

            # Recupera i dettagli dei quiz basandosi sugli ID
            quiz_storico = []
            for risultato in quiz_risultati:
                quiz = quiz_collection.find_one(
                    {"ID_Quiz": risultato["ID_Quiz"]},
                    {"_id": 0, "ID_Quiz": 1, "Argomento": 1, "Modalità_Quiz": 1, "N_Domande": 1, "Durata": 1}
                )
                if quiz:
                    quiz["Punteggio"] = risultato["Punteggio_Quiz"]
                    quiz_storico.append(quiz)

            # Recupera gli ID e i punteggi degli scenari svolti dallo studente
            scenario_risultati = list(
                risultato_scenario_collection.find(
                    {"CF_Studente": cf_studente},
                    {"_id": 0, "ID_Scenario": 1, "Punteggio_Scenario": 1}
                )
            )

            # Recupera i dettagli degli scenari basandosi sugli ID
            scenario_storico = []
            for risultato in scenario_risultati:
                scenario = scenario_collection.find_one(
                    {"ID_Scenario": risultato["ID_Scenario"]},
                    {"_id": 0, "ID_Scenario": 1, "Titolo": 1, "Descrizione": 1, "Argomento": 1, "Modalità": 1}
                )
                if scenario:
                    scenario["Punteggio"] = risultato["Punteggio_Scenario"]
                    scenario_storico.append(scenario)

            return {
                "Quiz": quiz_storico,
                "Scenari": scenario_storico
            }
        except Exception as e:
            print(f"Errore nel recupero dello storico: {e}")
            return {"Quiz": [], "Scenari": []}

    def close_connection(self):
        self.db_manager.close_connection()