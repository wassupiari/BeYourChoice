from flask import render_template

from app.models.ClasseVirtuale import ClasseVirtuale


class ClasseVirtualeControl:
    def __init__(self):
        self.model = ClasseVirtuale()

    def creazioneClasseVirtuale(self, NomeClasse, Descrizione):
        """
        Crea una nuova classe virtuale.
        """
        try:
            messaggio = self.model.creazioneClasseVirtuale(NomeClasse, Descrizione)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise

    def inserisci_studente_classe(self, IdCasse, IdStudente):
        """
        Inserisce uno studente in una classe virtuale.
        """
        try:
            messaggio = self.model.inserimentoClasseStudente(IdCasse, IdStudente)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise

    def rimozioneClasseStudente(self, IdClasse, IdStudente):
        """
        Rimuove uno studente da una classe virtuale.
        """
        try:
            messaggio = self.model.rimozioneClasseStudente(IdClasse, IdStudente)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise

    def mostra_classe(self, ID_Classe):
        """
        Recupera gli studenti della classe e prepara i dati per il rendering.

        Args:
            ID_Classe (int): L'ID della classe virtuale.

        Returns:
            list[dict]: Lista di studenti con Nome, Cognome e Data di Nascita.
        """
        try:
            studenti = self.model.mostra_classe(ID_Classe)  # Chiama il metodo per recuperare gli studenti
            print(f"Studente recuperati: {len(studenti)}")
            return studenti
        except ValueError as e:
            print(f"Errore: {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"Errore generale: {e}")
            return {"error": "Si è verificato un errore nel recupero degli studenti."}

    def mostra_studenti_istituto(self, scuola_appartenenza):
        """
        Recupera gli studenti della classe e prepara i dati per il rendering.

        Args:
            ID_Classe (int): L'ID della classe virtuale.

        Returns:
            list[dict]: Lista di studenti con Nome, Cognome e Data di Nascita.
        """
        try:
            studenti = self.model.mostra_studenti_istituto(
                scuola_appartenenza)  # Chiama il metodo per recuperare gli studenti
            print(f"Studente recuperati: {len(studenti)}")
            return studenti
        except ValueError as e:
            print(f"Errore: {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"Errore generale: {e}")
            return {"error": "Si è verificato un errore nel recupero degli studenti."}

    def rimuovi_studente(self, studente_id):

        """
        Rimuove uno studente dalla classe impostando ID_Classe a null.

        Args:
            studente_id (str): ID dello studente da rimuovere.

        Returns:
            bool: True se la rimozione ha successo, False altrimenti.
        """
        try:
            self.model.rimuovi_studente(studente_id)
            return True
        except Exception as e:
            print(f"Errore nel controller: {e}")
            return False
