class ProfiloStudente:
    def __init__(self, nome, cognome, SdA, email, CF, Data_Nascita, password):
        self.nome = nome
        self.cognome = cognome
        self.SdA = SdA
        self.email = email
        self.CF = CF
        self.Data_Nascita = Data_Nascita
        self.password = password

    def to_dict(self):
        return {
            "nome": self.nome,
            "cognome": self.cognome,
            "sda": self.SdA,
            "email": self.email,
            "cf": self.CF,
            "Data_Nascita": self.Data_Nascita,
            "password": self.password,
        }


class ProfiloDocente:
    def __init__(self, nome, cognome, sda, email, cf, data_nascita, password):
        self.nome = nome
        self.cognome = cognome
        self.sda = sda
        self.email = email
        self.cf = cf
        self.data_nascita = data_nascita
        self.password = password

    def to_dict(self):
        return {
            "nome": self.nome,
            "cognome": self.cognome,
            "sda": self.sda,
            "email": self.email,
            "cf": self.cf,
            "data_nascita": self.data_nascita,
            "password": self.password,
        }
