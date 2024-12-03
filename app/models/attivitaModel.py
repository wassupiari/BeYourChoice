from datetime import datetime

from databaseManager import DatabaseManager


class Attivita:
    """
    La classe Attivita gestisce le operazioni relative alle attività degli studenti,
    come il recupero delle classifiche di classe, il calcolo dei punteggi personali,
    il recupero dello storico delle attività e la gestione delle classi associate a un docente.
    Utilizza DatabaseManager per interagire con il database MongoDB.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_classifica_classe(self, id_classe):
        """
        Recupera la classifica della classe con i punteggi totali di quiz e scenari.
        :param id_classe: ID della classe.
        :return: Lista degli studenti con Nome, Cognome, CF e Punteggio Totale.
        """
        try:
            studente_collection = self.db_manager.get_collection("Studente")
            scenario_collection = self.db_manager.get_collection("PunteggioScenario")
            quiz_collection = self.db_manager.get_collection("RisultatoQuiz")

            # Recupera gli studenti della classe
            studenti = list(
                studente_collection.find(
                    {"ID_Classe": id_classe},
                    {"_id": 0, "cf": 1, "nome": 1, "cognome": 1
                     }))

            # Mappa per i punteggi
            punteggi_totali = {studente.get("cf"): {"PunteggioScenari": 0, "PunteggioQuiz": 0}
                               for studente in studenti}

            # Calcola i punteggi dagli scenari
            scenari_punteggi = scenario_collection.aggregate([
                {"$group": {"_id": "$CF_Studente", "PunteggioScenari": {"$sum":
                                                                            "$Punteggio_Scenario"}}}
            ])
            for item in scenari_punteggi:
                if item["_id"] in punteggi_totali:
                    punteggi_totali[item["_id"]]["PunteggioScenari"] = item["PunteggioScenari"]

            # Calcola i punteggi dai quiz
            quiz_punteggi = quiz_collection.aggregate([
                {"$group": {"_id": "$CF_Studente", "PunteggioQuiz": {"$sum": "$Punteggio_Quiz"}}}
            ])
            for item in quiz_punteggi:
                if item["_id"] in punteggi_totali:
                    punteggi_totali[item["_id"]]["PunteggioQuiz"] = item["PunteggioQuiz"]

            # Combina i dati degli studenti con i punteggi
            classifica = []
            for studente in studenti:
                print(studente)
                cf_studente = studente.get("cf")  # Cambia "CF" con "cf"
                punteggio_scenari = punteggi_totali.get(cf_studente, {}).get("PunteggioScenari", 0)
                punteggio_quiz = punteggi_totali.get(cf_studente, {}).get("PunteggioQuiz", 0)
                punteggio_totale = punteggio_scenari + punteggio_quiz

                classifica.append({
                    "CF": cf_studente,
                    "Nome": studente.get("nome"),
                    "Cognome": studente.get("cognome"),
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
        Calcola il punteggio personale dello studente sommando quiz e scenari.
        :param cf_studente: Codice fiscale dello studente.
        :return: Dizionario con i punteggi dei quiz e degli scenari.
        """
        scenario_collection = self.db_manager.get_collection("PunteggioScenario")
        quiz_collection = self.db_manager.get_collection("RisultatoQuiz")

        # Calcola il punteggio totale degli scenari
        scenario_result = scenario_collection.aggregate([
            {"$match": {"CF_Studente": cf_studente}},
            {"$group": {"_id": "$CF_Studente", "PunteggioScenari": {"$sum": "$Punteggio_Scenario"}}}
        ])
        punteggio_scenari = next(scenario_result, {}).get("PunteggioScenari", 0)

        # Calcola il punteggio totale dei quiz
        quiz_result = quiz_collection.aggregate([
            {"$match": {"CF_Studente": cf_studente}},
            {"$group": {"_id": "$CF_Studente", "PunteggioQuiz": {"$sum": "$Punteggio_Quiz"}}}
        ])
        punteggio_quiz = next(quiz_result, {}).get("PunteggioQuiz", 0)

        return {
            "PunteggioQuiz": punteggio_quiz,
            "PunteggioScenari": punteggio_scenari
        }

    def get_storico(self, cf_studente):
        """
        Recupera lo storico dettagliato di tutte le attività svolte dallo studente dal database Dashboard.
        :param cf_studente: Codice fiscale dello studente.
        :return: Un elenco di attività.
        """
        try:
            # Recupera la collezione Dashboard
            dashboard_collection = self.db_manager.get_collection("Dashboard")

            # Trova tutte le attività per lo studente
            attivita_risultati = list(
                dashboard_collection.find(
                    {"CF_Studente": cf_studente},
                    {"_id": 0, "ID_Attività": 1, "Data_Attività": 1, "Descrizione_Attività": 1, "Punteggio_Attività": 1}
                )
            )

            # Converte le date in un formato leggibile se necessario
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
        :param id_docente: ID del docente.
        :return: Lista delle classi con ID_Classe e Nome_Classe.
        """
        collection = self.db_manager.get_collection("ClasseVirtuale")
        return list(
            collection.find(
                {"ID_Docente": id_docente},
                {"_id": 0, "ID_Classe": 1, "Nome_Classe": 1}
            )
        )

