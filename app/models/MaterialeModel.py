class MaterialeModel:
    def __init__(self, titolo, descrizione, filepath, tipo):
        self.titolo = titolo
        self.descrizione = descrizione
        self.filepath = filepath
        self.tipo = tipo

    def to_dict(self):
        return {
            "Titolo": self.titolo,
            "Descrizione": self.descrizione,
            "File_Path": self.filepath,
            "Tipo": self.tipo
        }