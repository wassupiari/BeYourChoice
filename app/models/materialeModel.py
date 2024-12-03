class MaterialeModel:
    def __init__(self, id_MaterialeDidattico, titolo, descrizione, filepath, tipo, ID_Classe):
        self.id_MaterialeDidattico = id_MaterialeDidattico
        self.titolo = titolo
        self.descrizione = descrizione
        self.filepath = filepath
        self.tipo = tipo
        self.ID_Classe= ID_Classe

    def to_dict(self):
        return {
            "ID_MaterialeDidattico": self.id_MaterialeDidattico,
            "Titolo": self.titolo,
            "Descrizione": self.descrizione,
            "File_Path": self.filepath,
            "Tipo": self.tipo,
            "ID_Classe":self.ID_Classe
        }