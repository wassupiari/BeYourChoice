from bson import ObjectId


class MaterialeControl:
    def __init__(self, db_manager):
        self.db = db_manager
        self.collection = self.db.get_collection('MaterialeDidattico')
        print("Debug: Collezione ottenuta", self.collection)

    def get_collection(self, collection_name):
        return self.db.get_collection(collection_name)

    def view_all_materials(self):
        """Restituisce tutti i materiali didattici dal database."""
        try:
            materiali = list(self.collection.find())
            print(f"Debug: Materiali recuperati - {materiali}")
        except Exception as e:
            print(f"Errore durante il recupero dei materiali: {e}")
            materiali = []
        return materiali

    def upload_material(self, titolo, descrizione, filepath, tipo):
        """Carica un nuovo materiale didattico nel database."""
        new_material = {
            "Titolo": titolo,
            "Descrizione": descrizione,
            "File_Path": filepath,
            "Tipo": tipo,
            "ID_MaterialeDidattico": self.get_next_id()
        }
        self.collection.insert_one(new_material)

    def edit_material(self, material_id, updated_data):
        """Modifica un materiale didattico esistente."""
        self.collection.update_one(
            {"_id": ObjectId(material_id)},
            {"$set": updated_data}
        )

    def delete_material(self, material_id):
        # Trova il materiale da eliminare
        materiale = self.collection.find_one({"_id": material_id})
        if materiale:
            self.collection.delete_one({"_id": material_id})
            return materiale  # Restituisce il materiale eliminato
        return None

    def view_material(self, filter_criteria):
        """Restituisce un materiale didattico specifico secondo i criteri di filtro."""
        return self.collection.find_one(filter_criteria)

    def get_next_id(self):
        """Restituisce l'ID_MaterialeDidattico successivo disponibile."""
        last_material = self.collection.find().sort("ID_MaterialeDidattico", -1).limit(1)
        last_material_list = list(last_material)  # Converti il cursore in una lista per ottenere i risultati
        if len(last_material_list) > 0:
            return last_material_list[0]["ID_MaterialeDidattico"] + 1
        return 1