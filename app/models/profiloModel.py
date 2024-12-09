from app.controllers.profiloControl import ProfiloControl


class ProfiloModel:
    def __init__(self, db_manager):
        self.control = ProfiloControl(db_manager)

    def get_profilo_studente(self, email):
        return self.control.get_profilo_studente(email)

    def get_profilo_docente(self, email):
        return self.control.get_profilo_docente(email)

    def carica_profilo_studente(self, email, nuovi_dati):
        return self.control.carica_profilo_studente(email, nuovi_dati)

    def carica_profilo_docente(self, email, nuovi_dati):
        return self.control.carica_profilo_docente(email, nuovi_dati)

    def cambia_password_studente(self, vecchia_password, nuova_password):
        return self.control.cambia_password_studente(vecchia_password, nuova_password)

    def cambia_password_docente(self, vecchia_password, nuova_password):
        return self.control.cambia_password_docente(vecchia_password, nuova_password)