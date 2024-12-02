class ProfiloControl:
    def __init__(self, db_manager):
        self.docente_collection = db_manager.get_collection('Docente')
        self.studente_collection = db_manager.get_collection('Studente')

    def get_profilo_studente(self, email):
        try:
            query = {"email": email}
            profilo_studente = list(self.studente_collection.find(query))
            return profilo_studente
        except Exception as e:
            print(f"Errore nel recuperare il profilo dello studente dall'email {email}: {str(e)}")
            return []

    def get_profilo_docente(self, email):
        try:
            query = {"email": email}
            profilo_docente = list(self.docente_collection.find(query))
            return profilo_docente
        except Exception as e:
            print(f"Errore nel recuperare il profilo del docente dall'email {email}: {str(e)}")
            return []

    def update_profilo_studente(self, email, nuovi_dati):
        try:
            result = self.studente_collection.update_one({"email": email}, {"$set": nuovi_dati})
            return result.modified_count > 0  # True se almeno un documento è stato modificato
        except Exception as e:
            print(f"Errore nell'aggiornare il profilo dello studente per l'email {email}: {str(e)}")
            return False

    def update_profilo_docente(self, email, nuovi_dati):
        try:
            result = self.docente_collection.update_one({"email": email}, {"$set": nuovi_dati})
            return result.modified_count > 0  # True se almeno un documento è stato modificato
        except Exception as e:
            print(f"Errore nell'aggiornare il profilo del docente per l'email {email}: {str(e)}")
            return False