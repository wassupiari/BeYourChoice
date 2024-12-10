from bson import ObjectId


class MaterialeModel:
    def __init__(self, db_manager):
        self.collection = db_manager.get_collection('MaterialeDidattico')

    def visualizza_tutti_materiali(self):
        return list(self.collection.find())

    def carica_materiali(self, materiale_model):
        from uuid import uuid4
        # Assegna un nuovo ID unico al materiale
        if 'ID_MaterialeDidattico' not in materiale_model or materiale_model['ID_MaterialeDidattico'] is None:
            materiale_model['ID_MaterialeDidattico'] = str(uuid4())

        # Inserisce nel database
        self.collection.insert_one(materiale_model)

    def modifica_materiale(self, materiale_id, dati_caricati):
        self.collection.update_one(
            {"_id": ObjectId(materiale_id)},
            {"$set": dati_caricati}
        )

    def visualizza_materiale(self, criterio_filtro):
        return self.collection.find_one(criterio_filtro)

    def inserisci_documento(self, documento):
        return self.collection.insert_one(documento)

    def trova_documento(self, query):
        return self.collection.find_one(query)

    def carica_documento(self, query, nuovi_valori):
        return self.collection.update_one(query, {"$set": nuovi_valori})

    def rimuovi_documento(self, query):
        return self.collection.delete_one(query)

    def elimina_materiale(self, materiale_id):
        result = self.collection.delete_one({'_id': ObjectId(materiale_id)})
        return result.deleted_count == 1

    def count_documents(self, query):
        return self.collection.count_documents(query)

    def get_tutti_materiali(self):
        materiali = list(self.collection.find())
        print(f"Materiali nel database: {materiali}")
        return materiali

    def get_materiale(self, query):
        return self.collection.find_one(query)

    def get_materiale_tramite_id(self, materiale_id):
        return self.collection.find_one({'_id': ObjectId(materiale_id)})

    def carica_materiale(self, materiale_id, dati_caricati):
        return self.collection.update_one({'_id': ObjectId(materiale_id)}, {'$set': dati_caricati})

    def get_materiali_tramite_id_classe(self, ID_Classe):
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