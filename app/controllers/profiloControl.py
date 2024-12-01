from app.models.profiloModel import ProfiloStudente, ProfiloDocente


class ProfiloControl:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_profilo_studente(self, cf_studente):
        collection = self.db_manager.get_collection('Studente')
        studente_data = collection.find_one({"CF": cf_studente})

        if studente_data:
            return ProfiloStudente(
                nome=studente_data["nome"],
                cognome=studente_data["cognome"],
                SdA=studente_data["sda"],
                email=studente_data["email"],
                CF=studente_data["cf"],
                Data_Nascita=studente_data["Data_Nascita"],
                password=studente_data["password"]
            )
        else:
            raise ValueError("Studente non trovato nel database")

    def get_profilo_docente(self, cf_docente):
        collection = self.db_manager.get_collection('Docente')
        docente_data = collection.find_one({"cf": cf_docente})

        if docente_data:
            return ProfiloDocente(
                nome=docente_data["nome"],
                cognome=docente_data["cognome"],
                sda=docente_data["sda"],
                email=docente_data["email"],
                cf=docente_data["cf"],
                data_nascita=docente_data["data_nascita"],
                password=docente_data["password"]
            )
        else:
            raise ValueError("Docente non trovato nel database")