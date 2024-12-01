from databaseManager import DatabaseManager  # Importa la classe DatabaseManager

class ScenarioModel:
    def __init__(self):
        # Utilizza la connessione esistente al database
        self.db_manager = DatabaseManager()

    def aggiungi_scenario(self, scenario_dict):
        scenario_collection = self.db_manager.get_collection("ScenarioVirtuale")
        scenario_collection.insert_one(scenario_dict)
        print("Scenario aggiunto con successo!")
