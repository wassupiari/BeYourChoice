from bson import ObjectId


class MaterialeControl:
    def __init__(self, db_manager):
        self.collection = db_manager.get_collection('MaterialeDidattico')

    def view_all_materials(self):
        return list(self.collection.find())

    def upload_material(self, materiale_model):
        from uuid import uuid4
        # Assegna un nuovo ID unico al materiale
        if 'ID_MaterialeDidattico' not in materiale_model or materiale_model['ID_MaterialeDidattico'] is None:
            materiale_model['ID_MaterialeDidattico'] = str(uuid4())

        # Inserisce nel database
        self.collection.insert_one(materiale_model)

    def edit_material(self, material_id, updated_data):
        self.collection.update_one(
            {"_id": ObjectId(material_id)},
            {"$set": updated_data}
        )

    def delete_material(self, material_id):
        materiale = self.collection.find_one({"_id": ObjectId(material_id)})
        if materiale:
            self.collection.delete_one({"_id": ObjectId(material_id)})
            return materiale
        return None

    def view_material(self, filter_criteria):
        return self.collection.find_one(filter_criteria)




    def insert_document(self, document):
        return self.collection.insert_one(document)

    def find_document(self, query):
        return self.collection.find_one(query)

    def update_document(self, query, new_values):
        return self.collection.update_one(query, {"$set": new_values})

    def delete_document(self, query):
        return self.collection.delete_one(query)

    def delete_material(self, material_id):
        result = self.collection.delete_one({'_id': ObjectId(material_id)})
        return result.deleted_count == 1

    def count_documents(self, query):
        return self.collection.count_documents(query)

    def get_all_materials(self):
        materials = list(self.collection.find())
        print(f"Materiali nel database: {materials}")
        return materials

    def get_material(self, query):
        return self.collection.find_one(query)

    def get_material_by_id(self, material_id):
        return self.collection.find_one({'_id': ObjectId(material_id)})

    def update_material(self, materiale_id, updated_data):
        return self.collection.update_one({'_id': ObjectId(materiale_id)}, {'$set': updated_data})

    def get_materials_by_id(self, ID_Classe):
        """Esegui una query MongoDB per ottenere i materiali per una specifica classe."""
        try:
            query = {"ID_Classe": ID_Classe}
            print(f"Eseguendo query con ID_Classe: {ID_Classe}")
            materiali_della_classe = list(self.collection.find(query))
            if not materiali_della_classe:
                print(f"Nessun materiale trovato per la classe {ID_Classe}.")
            return materiali_della_classe
        except Exception as e:
            print(f"Errore nel recuperare i materiali per la classe {ID_Classe}: {str(e)}")
            return []