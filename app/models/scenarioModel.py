from databaseManager import DatabaseManager  # Importa la classe DatabaseManager

class ScenarioModel:
    def _init_(self):
        # Utilizza la connessione esistente al database
        self.db_manager = DatabaseManager()

    def aggiungi_scenario(self, scenario_dict):
        scenario_collection = self.db_manager.get_collection("Scenario")
        scenario_collection.insert_one(scenario_dict)
        print("Scenario aggiunto con successo!")