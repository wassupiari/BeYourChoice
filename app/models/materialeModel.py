"""
materialeModel.py

Questo modulo fornisce le funzioni di accesso ai dati per i materiali didattici.
Permette di eseguire operazioni CRUD (Create, Read, Update, Delete) sui documenti
memorizzati in una collezione del database.

Autore: [il tuo nome]
Data di creazione: [data di creazione]
"""

from bson import ObjectId


class MaterialeModel:
    """
    Classe responsabile della gestione delle operazioni di database
    per i materiali didattici.
    """

    def __init__(self, db_manager):

        """
        Inizializza l'istanza di MaterialeModel.

        :param db_manager: Gestore del database per accedere alla collezione.
        """

        self.collection = db_manager.get_collection('MaterialeDidattico')

    def visualizza_tutti_materiali(self):

        """
        Recupera tutti i documenti dalla collezione.

        :return: Lista di tutti i materiali didattici.
        """

        return list(self.collection.find())

    def carica_materiali(self, materiale_model):

        """
       Salva un nuovo materiale nella collezione.

       :param materiale_model: Dizionario contenente i dettagli del materiale.
       """

        from uuid import uuid4
        # Assegna un nuovo ID unico al materiale
        if 'ID_MaterialeDidattico' not in materiale_model or materiale_model['ID_MaterialeDidattico'] is None:
            materiale_model['ID_MaterialeDidattico'] = str(uuid4())

        # Inserisce nel database
        self.collection.insert_one(materiale_model)

    def modifica_materiale(self, materiale_id, dati_caricati):

        """
        Aggiorna un materiale esistente nel database.

        :param materiale_id: ID del materiale da aggiornare.
        :param dati_caricati: Dizionario dei dati aggiornati.
        """

        self.collection.update_one(
            {"_id": ObjectId(materiale_id)},
            {"$set": dati_caricati}
        )

    def visualizza_materiale(self, criterio_filtro):

        """
        Recupera un singolo materiale in base al criterio fornito.

        :param criterio_filtro: Criterio di ricerca per il materiale.
        :return: Documento del materiale trovato.
        """

        return self.collection.find_one(criterio_filtro)

    def inserisci_documento(self, documento):
        return self.collection.insert_one(documento)

    def trova_documento(self, query):
        return self.collection.find_one(query)

    def carica_documento(self, query, nuovi_valori):
        return self.collection.update_one(query, {"$set": nuovi_valori})

    def rimuovi_documento(self, query):
        return self.collection.delete_one(query)

    def elimina_materiale(self, materiale_id):
        result = self.collection.delete_one({'_id': ObjectId(materiale_id)})
        return result.deleted_count == 1

    def count_documents(self, query):
        return self.collection.count_documents(query)

    def get_tutti_materiali(self):
        materiali = list(self.collection.find())
        print(f"Materiali nel database: {materiali}")
        return materiali

    def get_materiale(self, query):
        return self.collection.find_one(query)

    def get_materiale_tramite_id(self, materiale_id):

        """
        Esegue una query per ottenere i materiali di una specifica classe.

        :param ID_Classe: ID della classe di cui ottenere i materiali.
        :return: Lista di materiali appartenenti alla classe.
        """

        return self.collection.find_one({'_id': ObjectId(materiale_id)})

    def get_materiali_tramite_id_classe(self, ID_Classe):
        """Esegui una query MongoDB per ottenere i materiali per una specifica classe."""
        try:
            query = {"ID_Classe": ID_Classe}
            print(f"Eseguendo query con ID_Classe: {ID_Classe}")
            materiali_della_classe = list(self.collection.find(query))
            if not materiali_della_classe:
                print(f"Nessun materiale trovato per la classe {ID_Classe}.")
            return materiali_della_classe
        except Exception as e:
            print(f"Errore nel recuperare i materiali per la classe {ID_Classe}: {str(e)}")
            return []