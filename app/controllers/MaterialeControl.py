from bson import ObjectId


class MaterialeControl:
    def __init__(self, db_manager):
        self.collection = db_manager.get_collection('MaterialeDidattico')

    def view_all_materials(self):
        return list(self.collection.find())

    def upload_material(self, materiale_model):
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
        last_material = self.collection.find().sort("ID_MaterialeDidattico", -1).limit(1)
        last_material_list = list(last_material)
        if len(last_material_list) > 0:
            return last_material_list[0]["ID_MaterialeDidattico"] + 1
        return 1