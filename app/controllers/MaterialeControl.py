from bson import ObjectId


class MaterialeControl:
    def __init__(self, db_manager):
        self.db = db_manager

    def view_all_materials(self):
        """Restituisce tutti i materiali didattici dal database."""
        materiali = list(self.db.MaterialeDidattico.find())
        print(f"Debug: Materiali recuperati - {materiali}")
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
        self.db.MaterialeDidattico.insert_one(new_material)

    def edit_material(self, material_id, updated_data):
        """Modifica un materiale didattico esistente."""
        self.db.MaterialeDidattico.update_one(
            {"_id": ObjectId(material_id)},
            {"$set": updated_data}
        )

    def delete_material(self, material_id):
        """Elimina un materiale didattico dal database."""
        self.db.MaterialeDidattico.delete_one({"_id": ObjectId(material_id)})

    def view_material(self, filter_criteria):
        """Restituisce un materiale didattico specifico secondo i criteri di filtro."""
        return self.db.MaterialeDidattico.find_one(filter_criteria)

    def get_next_id(self):
        """Restituisce l'ID_MaterialeDidattico successivo disponibile."""
        last_material = self.db.MaterialeDidattico.find().sort("ID_MaterialeDidattico", -1).limit(1)
        if last_material.count() > 0:
            return last_material[0]["ID_MaterialeDidattico"] + 1
        return 1