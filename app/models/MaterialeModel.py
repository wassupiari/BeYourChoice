from pymongo import MongoClient

class MaterialeModel:
    def __init__(self, db_manager):
        """
        Inizializza il modello del materiale didattico.

        :param db_manager: Istanza di DatabaseManager per la connessione al database.
        """
        self.collection = db_manager.get_collection("MaterialeDidattico")

    def upload_material(self, material_data):
        """
        Carica un nuovo materiale didattico.

        :param material_data: Dizionario contenente i dati del materiale (es. titolo, descrizione, URL).
        :return: ID del documento inserito.
        """
        return self.collection.insert_one(material_data).inserted_id

    def view_material(self, query=None):
        """
        Visualizza il materiale didattico in base a una query.

        :param query: Dizionario per filtrare i risultati (opzionale).
        :return: Lista di materiali che soddisfano la query.
        """
        if query is None:
            query = {}
        return list(self.collection.find(query))

    def update_material(self, material_id, updated_data):
        """
        Modifica un materiale didattico esistente.

        :param material_id: ID del materiale da aggiornare.
        :param updated_data: Dizionario con i dati aggiornati.
        :return: Risultato dell'aggiornamento.
        """
        from bson.objectid import ObjectId
        return self.collection.update_one({"_id": ObjectId(material_id)}, {"$set": updated_data})

    def delete_material(self, material_id):
        """
        Rimuove un materiale didattico esistente.

        :param material_id: ID del materiale da rimuovere.
        :return: Risultato della cancellazione.
        """
        from bson.objectid import ObjectId
        return self.collection.delete_one({"_id": ObjectId(material_id)})