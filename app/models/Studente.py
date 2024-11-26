from databaseManager import DatabaseManager

class Studente:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_classifica_classe(self, id_classe):
        """
        Recupera la classifica ordinata per punteggio decrescente.
        :param id_classe: ID della classe.
        :return: Lista degli studenti.
        """
        try:
            collection = self.db_manager.get_collection("Studente")
            return list(
                collection.find(
                    {"ID_Classe": id_classe},
                    {"_id": 0, "Nome": 1, "Cognome": 1}
                )
            )
        except Exception as e:
            print(f"Errore nel recupero della classifica: {e}")
            return []

    def get_punteggio_personale(self, email_utente):
        """
        Recupera i punteggi personali dell'utente.
        :param email_utente: Email dell'utente.
        :return: Un dizionario con i punteggi.
        """
        try:
            collection = self.db_manager.get_collection("Studente")
            utente = collection.find_one(
                {"Email": email_utente},
                {"_id": 0, "PunteggioQuiz": 1, "PunteggioScenari": 1}
            )
            return utente or {"PunteggioQuiz": 0, "PunteggioScenari": 0}
        except Exception as e:
            print(f"Errore nel recupero del punteggio personale: {e}")
            return {"PunteggioQuiz": 0, "PunteggioScenari": 0}

    def close_connection(self):
        self.db_manager.close_connection()