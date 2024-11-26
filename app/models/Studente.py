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

    def get_punteggio_personale(self, cf_studente):
        """
        Calcola il punteggio personale dello studente sommando tutti i Punteggio_Scenario.
        :param cf_studente: Codice fiscale dello studente.
        :return: Il punteggio totale dello studente.
        """
        try:
            collection = self.db_manager.get_collection("Scenario")

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

    def close_connection(self):
        self.db_manager.close_connection()