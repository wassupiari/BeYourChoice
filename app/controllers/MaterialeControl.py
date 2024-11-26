from app.models.MaterialeModel import MaterialeModel


class MaterialeControl:
    def __init__(self, db_manager):
        """
        Inizializza il controllore per il materiale didattico.

        :param db_manager: Connessione al database.
        """
        self.model = MaterialeModel(db_manager)

    def upload_material(self, titolo, descrizione, filepath, tipo):
        """
        Carica un nuovo materiale nel sistema.

        :param titolo: Titolo del materiale.
        :param descrizione: Descrizione del materiale.
        :param filepath: Percorso del file.
        :param tipo: Tipo di materiale (documento, video, altro).
        :return: ID del materiale caricato.
        """
        material_data = {
            "Titolo": titolo,
            "Descrizione": descrizione,
            "File_Path": filepath,
            "Tipo": tipo
        }
        return self.model.upload_material(material_data)

    def view_all_materials(self):
        """Visualizza tutti i materiali."""
        return self.model.view_material()

    def edit_material(self, materiale_id, updated_data):
        """Modifica i dettagli di un materiale esistente."""
        return self.model.update_material(materiale_id, updated_data)

    def delete_material(self, materiale_id):
        """Rimuove un materiale dal sistema."""
        return self.model.delete_material(materiale_id)