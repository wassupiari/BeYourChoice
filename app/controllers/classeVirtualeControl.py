from app.models.classeVirtualeModel import ClasseVirtuale


class ClasseVirtualeControl:
    def __init__(self):
        self.model = ClasseVirtuale()

    def creazione_classe_virtuale(self, nome_classe, descrizione, id_docente):
        """
        Crea una nuova classe virtuale.
        """
        try:
            messaggio = self.model.creazione_classe_virtuale(nome_classe, descrizione, id_docente)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise

    def inserisci_studente_classe(self, id_casse, id_studente):
        """
        Inserisce uno studente in una classe virtuale.
        """
        try:
            messaggio = self.model.inserimento_classe_studente(id_casse, id_studente)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise

    def rimozione_classe_studente(self, id_classe, id_studente):
        """
        Rimuove uno studente da una classe virtuale.
        """
        try:
            messaggio = self.model.rimozione_classe_studente(id_classe, id_studente)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise

    def mostra_classe(self, id_classe):
        """
        Recupera gli studenti della classe e prepara i dati per il rendering.

        Args:
            id_classe (int): L'ID della classe virtuale.

        Returns:
            list[dict]: Lista di studenti con Nome, Cognome e Data di Nascita.
        """
        try:
            studenti = self.model.mostra_classe(id_classe)  # Chiama il metodo per recuperare gli studenti
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
            studenti = self.model.mostra_studenti_istituto(scuola_appartenenza)  # Chiama il metodo per recuperare gli studenti
            print(f"Studente recuperati: {len(studenti)}")
            return studenti
        except ValueError as e:
            print(f"Errore: {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"Errore generale: {e}")
            return {"error": "Si è verificato un errore nel recupero degli studenti."}

    def rimuovi_studente(self, id_studente):

        """
        Rimuove uno studente dalla classe impostando ID_Classe a null.

        Args:
            studente_id (str): ID dello studente da rimuovere.

        Returns:
            bool: True se la rimozione ha successo, False altrimenti.
        """
        try:
            self.model.rimuovi_studente(id_studente)
            return True
        except Exception as e:
            print(f"Errore nel controller: {e}")
            return False

    def aggiungi_studente(self, id_studente, classe_id):

        """
        Rimuove uno studente dalla classe impostando ID_Classe a null.

        Args:
            studente_id (str): ID dello studente da rimuovere.

        Returns:
            bool: True se la rimozione ha successo, False altrimenti.
        """
        try:
            self.model.aggiungi_studente(id_studente, classe_id)
            return True
        except Exception as e:
            print(f"Errore nel controller: {e}")
            return False

    def cerca_studenti(self, query,id_classe):

        """
        Rimuove uno studente dalla classe impostando ID_Classe a null.

        Args:
            studente_id (str): ID dello studente da rimuovere.

        Returns:
            bool: True se la rimozione ha successo, False altrimenti.
        """
        try:
            return self.model.cerca_studenti(query, id_classe)
        except Exception as e:
            print(f"Errore nel controller: {e}")
            return False

    def cerca_studenti_istituto(self, query):
        try:
            return self.model.cerca_studenti_istituto(query)
        except Exception as e:
            print(f"Errore nel controller: {e}")
            return False
