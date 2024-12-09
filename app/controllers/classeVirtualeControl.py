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

    def mostra_studenti_classe(self, id_classe):
        """
            Recupera gli studenti della classe e prepara i dati per il rendering.

        Args:
            id_classe (int): L'ID della classe virtuale.

        Returns:
            list[dict]: Lista di studenti con Nome, Cognome e Data di Nascita.
        """
        try:
            studenti = self.model.mostra_studenti_classe(id_classe)  # Chiama il metodo per recuperare gli studenti
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
            Recupera gli studenti dell'istituto

        Args:
            scuola_appartenenza (string): Scuola di appartenenza del docente che richiama la funzione

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

    def rimuovi_studente_classe(self, id_studente):

        """
            Rimuove uno studente dalla classe impostando id_classe a null.

        Args:
            id_studente (str): ID dello studente da rimuovere.

        Returns:
            bool: True se la rimozione ha successo, False altrimenti.
        """
        try:
            self.model.rimuovi_studente_classe(id_studente)
            return True
        except Exception as e:
            print(f"Errore nel controller: {e}")
            return False

    def aggiungi_studente_classe(self, id_studente, id_classe):

        """
            Aggiunge uno studente  alla classe.

        Args:
            id_studente (str): ID dello studente da aggiungere.
            id_classe: ID della classe in cui aggiungere lo studente

        Returns:
            bool: True se la rimozione ha successo, False altrimenti.
        """
        try:
            self.model.aggiungi_studente_classe(id_studente, id_classe)
            return True
        except Exception as e:
            print(f"Errore nel controller: {e}")
            return False

    def cerca_studenti_classe(self, query, id_classe):
        """
            Ricerca studenti nella classe tramite codice fiscale
        Args:
            id_classe (str): ID della classe in cui cercare.
            query: Caratteri inseriti
        Returns:
            bool: True se la ricerca va a buon fine.
        """
        try:
            return self.model.cerca_studenti_classe(query, id_classe)
        except Exception as e:
            print(f"Errore nel controller: {e}")
            return False

    def cerca_studenti_istituto(self, query):
        """
            Ricerca studenti nell'istituto tramite codice fiscale
        Args:
            query: Caratteri inseriti
        Returns:
            bool: True se la ricerca va a buon fine.
        """
        try:
            return self.model.cerca_studenti_istituto(query)
        except Exception as e:
            print(f"Errore nel controller: {e}")
            return False
