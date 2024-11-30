from bson import ObjectId


class MaterialeControl:
    def __init__(self, db_manager):
        self.collection = db_manager.get_collection('MaterialeDidattico')

    def view_all_materials(self):
        return list(self.collection.find())

    def upload_material(self, materiale_model):
        # Assegna un nuovo ID unico al materiale
        if not hasattr(materiale_model, 'ID_MaterialeDidattico') or materiale_model.ID_MaterialeDidattico is None:
            materiale_model.ID_MaterialeDidattico = self.get_next_id()

        # Inserisce nel database
        self.collection.insert_one(materiale_model.to_dict())

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

    def get_next_id(self):
        # Trova l'ultimo documento inserito ordinando per ID_MaterialeDidattico in ordine decrescente
        last_material = self.collection.find().sort("ID_MaterialeDidattico", -1).limit(1)
        last_material_list = list(last_material)

        # Se esiste un materiale precedente, incrementa l'ultimo ID trovato
        if last_material_list:
            last_id = last_material_list[0].get("ID_MaterialeDidattico", 0)
            if isinstance(last_id, int):
                return last_id + 1

        # Se non ci sono materiali nel database, inizia con l'ID 1
        return 1


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
