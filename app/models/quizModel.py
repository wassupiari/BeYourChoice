import uuid
from datetime import datetime, timedelta
import openai
from flask import session
from databaseManager import DatabaseManager




class QuizModel:

    db_manager = DatabaseManager(db_name="BeYourChoice;")

    @staticmethod
    def parse_domanda(domanda_testo):
        """Elabora il testo della domanda generata da OpenAI per estrarre i dettagli."""
        try:
            domanda_lines = domanda_testo.strip().split("\n")

            if len(domanda_lines) < 3:
                raise ValueError("Formato della domanda non valido.")

            testo_domanda = domanda_lines[0].strip()

            opzioni_risposte = [
                line.strip() for line in domanda_lines[1:] if line.startswith(("A)", "B)", "C)", "D)"))
            ]

            risposta_corretta = next(
                (line.replace("Risposta corretta:", "").strip() for line in domanda_lines if
                 "Risposta corretta:" in line),
                None
            )

            if not testo_domanda or not opzioni_risposte or not risposta_corretta:
                raise ValueError("Alcuni componenti essenziali della domanda sono mancanti.")

            opzioni_risposte = [
                opzione.replace("A)", "").replace("B)", "").replace("C)", "").replace("D)", "").strip()
                for opzione in opzioni_risposte
            ]

            return {
                "Testo_Domanda": testo_domanda,
                "Opzioni_Risposte": opzioni_risposte,
                "Risposta_Corretta": risposta_corretta
            }
        except Exception as e:
            raise ValueError(f"Errore nel parsing della domanda: {e}")

    @staticmethod
    def genera_domande(tema, numero_domande, modalita_risposta, api_key):
        """Genera domande utilizzando OpenAI GPT."""
        openai.api_key = api_key
        domande = []
        prompt_base = f"Genera una domanda sul tema: {tema}. "

        if modalita_risposta == "3_risposte":
            prompt_base += "La domanda deve avere 3 opzioni di risposta: una corretta e due sbagliate."
        elif modalita_risposta == "4_risposte":
            prompt_base += "La domanda deve avere 4 opzioni di risposta: una corretta e tre sbagliate."

        while len(domande) < numero_domande:
            messages = [
                {"role": "system",
                 "content": (
                     "Sei un assistente esperto in educazione civica italiana. Genera domande educative, coinvolgenti e "
                     "adatte al livello delle scuole superiori. Ogni domanda deve essere chiara, affrontare temi come "
                     "Costituzione, diritti, doveri, cittadinanza e sostenibilità, e includere opzioni di risposta."
                 )},
                {"role": "user", "content": prompt_base}
            ]
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=200,
                    temperature=0.7,
                )
                domanda = response.choices[0].message["content"].strip()

                parsed_domanda = QuizModel.parse_domanda(domanda)
                domande.append(parsed_domanda)
            except ValueError as parse_error:
                continue
            except Exception as e:
                print(f"Errore durante la richiesta OpenAI: {e}")
                raise ValueError(f"Errore OpenAI: {e}")
        return domande

    @staticmethod
    def salva_quiz(data):
        """Salva un quiz e le sue domande nel database."""
        try:
            quiz_collection = QuizModel.db_manager.get_collection("Quiz")
            questions_collection = QuizModel.db_manager.get_collection("Domanda")
            if "iq_quiz" not in data or quiz_collection.find_one({"id_quiz": data["ID_Quiz"]}):
                data["ID_Quiz"] = str(uuid.uuid4())  # Genera un ID univoco

            id_classe = session.get("ID_Classe")
            if not id_classe:
                raise ValueError("ID Classe mancante nella sessione.")

            quiz = {
                "id_quiz": data["ID_Quiz"],
                "titolo": data["Titolo"],
                "argomento": data["Argomento"],
                "n_domande": data["N_Domande"],
                "domande": data["Domande"],
                "modalita_quiz": data["Modalità_Quiz"],
                "durata": data["Durata"],
                "data_creazione": data["Data_Creazione"],
                "id_classe": id_classe
            }
            quiz_collection.insert_one(quiz)

            for domanda in data["Domande"]:
                question = {
                    "id_domanda": domanda["ID_Domanda"],
                    "testo_domanda": domanda["Testo_Domanda"],
                    "opzioni_risposte": domanda["Opzioni_Risposte"],
                    "risposta_corretta": domanda["Risposta_Corretta"],
                    "id_quiz": data["ID_Quiz"]
                }
                questions_collection.insert_one(question)
        except Exception as e:
            raise ValueError(f"Errore durante il salvataggio del quiz: {e}")

    @staticmethod
    def recupera_domande(id_domanda):
        """Recupera le domande dal database in base agli ID."""
        try:
            questions_collection = QuizModel.db_manager.get_collection("Domanda")
            return list(questions_collection.find({"id_domanda": {"$in": id_domanda}}))
        except Exception as e:
            raise ValueError(f"Errore durante il recupero delle domande: {e}")

    @staticmethod
    def recupera_quiz(quiz_id):
        """Recupera un quiz in base al suo ID."""
        try:
            quiz_collection = QuizModel.db_manager.get_collection("Quiz")
            quiz = quiz_collection.find_one({"id_quiz": quiz_id})
            if not quiz:
                raise ValueError("Quiz non trovato.")
            quiz["_id"] = str(quiz["_id"])  # Convert ObjectId to string
            return quiz
        except Exception as e:
            raise ValueError(f"Errore durante il recupero del quiz: {e}")

    @staticmethod
    def recupera_quiz_per_classe(id_classe):
        """Recupera tutti i quiz per una classe specifica."""
        try:
            quiz_collection = QuizModel.db_manager.get_collection("Quiz")
            quiz_list = list(quiz_collection.find({"id_classe": id_classe}))
            for quiz in quiz_list:
                quiz["_id"] = str(quiz["_id"])  # Convert ObjectId
            return quiz_list
        except Exception as e:
            raise ValueError(f"Errore durante il recupero dei quiz: {e}")

    @staticmethod
    def recupera_risultati_per_quiz(quiz_id):
        """Recupera i risultati di un quiz."""
        try:
            risultati_collection = QuizModel.db_manager.get_collection("RisultatoQuiz")
            return list(risultati_collection.find({"id_quiz": quiz_id}))
        except Exception as e:
            raise ValueError(f"Errore durante il recupero dei risultati: {e}")

    @staticmethod
    def recupera_ultimo_quiz(id_classe, cf_studente):
        """Recupera l'ultimo quiz non completato da uno studente."""
        try:
            quiz_collection = QuizModel.db_manager.get_collection("Quiz")
            dashboard_collection = QuizModel.db_manager.get_collection("Dashboard")

            ultimo_quiz = quiz_collection.find_one(
                {"id_classe": id_classe},
                sort=[("data_creazione", -1)]
            )

            if not ultimo_quiz:
                return None

            completato = dashboard_collection.find_one({
                "cf_studente": cf_studente,
                "descrizione_attivita": {"$regex": f"Completamento Quiz: {ultimo_quiz['Titolo']}"}
            })

            return None if completato else ultimo_quiz
        except Exception as e:
            raise ValueError(f"Errore durante il recupero dell'ultimo quiz: {e}")

    @staticmethod
    def recupera_studenti_classe(id_classe):
        """Recupera tutti gli studenti di una classe."""
        try:
            studenti_collection = QuizModel.db_manager.get_collection("Studente")
            return list(studenti_collection.find({"id_classe": id_classe}))
        except Exception as e:
            raise ValueError(f"Errore durante il recupero degli studenti: {e}")

    @staticmethod
    def recupera_attività_completate(titolo_quiz):
        """
        Recupera le attività completate per un determinato quiz basandosi sul titolo del quiz.
        :param titolo_quiz: Titolo del quiz
        :return: Lista di attività completate
        """
        try:
            dashboard_collection = QuizModel.db_manager.get_collection("Dashboard")
            return list(dashboard_collection.find({
                "descrizione_attivita": {"$regex": f"Completamento Quiz: {titolo_quiz}"}
            }))
        except Exception as e:
            raise ValueError(f"Errore durante il recupero delle attività completate: {e}")

    @staticmethod
    def calcola_tempo_rimanente(quiz_id, cf_studente):
        """
        Calcola il tempo rimanente per un quiz specifico.
        """
        quiz_collection = QuizModel.db_manager.get_collection("Quiz")

        # Recupera l'ora di inizio dal database o impostala
        sessione = quiz_collection.find_one({"id_quiz": quiz_id, "cf_studente": cf_studente})
        ora_attuale = datetime.utcnow()

        if not sessione:
            # Se la sessione non esiste, creala
            ora_inizio = ora_attuale
        else:
            ora_inizio = sessione["Ora_Inizio"]

        # Recupera la durata del quiz
        quiz = quiz_collection.find_one({"id_quiz": quiz_id})
        durata_quiz = quiz["Durata"] if quiz else 30  # Default a 30 minuti

        # Calcola il tempo rimanente in secondi
        fine_quiz = ora_inizio + timedelta(minutes=durata_quiz)
        tempo_rimanente = max(0, int((fine_quiz - ora_attuale).total_seconds()))

        return tempo_rimanente

    @staticmethod
    def salva_risultato_quiz(risultato_quiz, cf_studente, punteggio):
        """
        Salva il risultato del quiz nel database e registra l'attività nella dashboard.
        :param quiz_result: Dati del risultato del quiz da salvare.
        :param cf_studente: Codice fiscale dello studente.
        :param punteggio: Punteggio ottenuto dallo studente.
        """
        try:
            # Collezioni necessarie
            quiz_results_collection = QuizModel.db_manager.get_collection("RisultatoQuiz")
            attività_collection = QuizModel.db_manager.get_collection("Dashboard")
            quiz_collection = QuizModel.db_manager.get_collection("Quiz")

            # Salva il risultato del quiz
            quiz_results_collection.insert_one(risultato_quiz)

            # Recupera il titolo del quiz
            quiz = quiz_collection.find_one({"id_quiz": risultato_quiz["iq_quiz"]}, {"titolo": 1})
            if not quiz:
                raise ValueError(f"Quiz con ID {risultato_quiz['id_quiz']} non trovato.")
            titolo_quiz = quiz["Titolo"]

            # Genera l'attività svolta
            attività = {
                "id_attivita": attività_collection.count_documents({}) + 1,  # Genera un ID incrementale
                "data_attivita": datetime.utcnow(),
                "descrizione_attivita": f"Completamento Quiz: {titolo_quiz}",
                "punteggio_attivita": punteggio,
                "cf_studente": cf_studente
            }

            # Inserisce l'attività nella dashboard
            attività_collection.insert_one(attività)
            print(f"DEBUG: Risultato del quiz e attività salvati correttamente per lo studente {cf_studente}")
        except Exception as e:
            raise ValueError(f"Errore durante il salvataggio del risultato: {e}")

    @staticmethod
    def verifica_completamento_quiz(quiz_id, cf_studente):
        """
        Verifica se uno studente ha già completato un quiz specifico.
        """
        try:
            risultati_collection = QuizModel.db_manager.get_collection("RisultatoQuiz")
            risultato = risultati_collection.find_one({"id_quiz": quiz_id, "cf_studente": cf_studente})
            return risultato is not None  # Restituisce True se il quiz è completato
        except Exception as e:
            print(f"ERRORE durante la verifica del completamento del quiz: {e}")
            return False

    @staticmethod
    def verifica_titolo(titolo):
        """Verifica se il titolo del quiz esiste già nel database."""
        try:
            quiz_collection = QuizModel.db_manager.get_collection("Quiz")
            # Cerca un documento con il titolo specificato
            return quiz_collection.find_one({"titolo": titolo}) is not None
        except Exception as e:
            raise ValueError(f"Errore durante la verifica del titolo: {e}")

