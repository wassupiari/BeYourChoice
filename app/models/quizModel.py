from datetime import datetime, timedelta
import openai
from flask import session
from databaseManager import DatabaseManager

db_manager = DatabaseManager()


class QuizModel:

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
        elif modalita_risposta == "vero_falso":
            prompt_base += "La domanda deve essere nella modalità vero/falso con la risposta corretta specificata."

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
                print(f"Errore nel parsing della domanda: {parse_error}")
                continue
            except Exception as e:
                print(f"Errore durante la richiesta OpenAI: {e}")
                raise ValueError(f"Errore OpenAI: {e}")
        return domande

    @staticmethod
    def salva_quiz(data):
        """Salva un quiz e le sue domande nel database."""
        try:
            quiz_collection = db_manager.get_collection("Quiz")
            questions_collection = db_manager.get_collection("Domanda")

            id_classe = session.get("ID_Classe")
            if not id_classe:
                raise ValueError("ID Classe mancante nella sessione.")

            quiz = {
                "ID_Quiz": data["ID_Quiz"],
                "Titolo": data["Titolo"],
                "Argomento": data["Argomento"],
                "N_Domande": data["N_Domande"],
                "Domande": data["Domande"],
                "Modalità_Quiz": data["Modalità_Quiz"],
                "Durata": data["Durata"],
                "Data_Creazione": data["Data_Creazione"],
                "ID_Classe": id_classe
            }
            quiz_collection.insert_one(quiz)

            for domanda in data["Domande"]:
                question = {
                    "ID_Domanda": domanda["ID_Domanda"],
                    "Testo_Domanda": domanda["Testo_Domanda"],
                    "Opzioni_Risposte": domanda["Opzioni_Risposte"],
                    "Risposta_Corretta": domanda["Risposta_Corretta"],
                    "ID_Quiz": data["ID_Quiz"]
                }
                questions_collection.insert_one(question)
        except Exception as e:
            raise ValueError(f"Errore durante il salvataggio del quiz: {e}")

    @staticmethod
    def recupera_domande(question_ids):
        """Recupera le domande dal database in base agli ID."""
        try:
            questions_collection = db_manager.get_collection("Domanda")
            return list(questions_collection.find({"ID_Domanda": {"$in": question_ids}}))
        except Exception as e:
            raise ValueError(f"Errore durante il recupero delle domande: {e}")

    @staticmethod
    def recupera_quiz(quiz_id):
        """Recupera un quiz in base al suo ID."""
        try:
            quiz_collection = db_manager.get_collection("Quiz")
            quiz = quiz_collection.find_one({"ID_Quiz": quiz_id})
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
            quiz_collection = db_manager.get_collection("Quiz")
            quiz_list = list(quiz_collection.find({"ID_Classe": id_classe}))
            for quiz in quiz_list:
                quiz["_id"] = str(quiz["_id"])  # Convert ObjectId
            return quiz_list
        except Exception as e:
            raise ValueError(f"Errore durante il recupero dei quiz: {e}")

    @staticmethod
    def recupera_risultati_per_quiz(quiz_id):
        """Recupera i risultati di un quiz."""
        try:
            risultati_collection = db_manager.get_collection("RisultatoQuiz")
            return list(risultati_collection.find({"ID_Quiz": quiz_id}))
        except Exception as e:
            raise ValueError(f"Errore durante il recupero dei risultati: {e}")

    @staticmethod
    def recupera_ultimo_quiz(id_classe, cf_studente):
        """Recupera l'ultimo quiz non completato da uno studente."""
        try:
            quiz_collection = db_manager.get_collection("Quiz")
            dashboard_collection = db_manager.get_collection("Dashboard")

            ultimo_quiz = quiz_collection.find_one(
                {"ID_Classe": id_classe},
                sort=[("Data_Creazione", -1)]
            )

            if not ultimo_quiz:
                return None

            completato = dashboard_collection.find_one({
                "CF_Studente": cf_studente,
                "Descrizione_Attività": {"$regex": f"Completamento Quiz: {ultimo_quiz['Titolo']}"}
            })

            return None if completato else ultimo_quiz
        except Exception as e:
            raise ValueError(f"Errore durante il recupero dell'ultimo quiz: {e}")

    @staticmethod
    def recupera_studenti_classe(id_classe):
        """Recupera tutti gli studenti di una classe."""
        try:
            studenti_collection = db_manager.get_collection("Studente")
            return list(studenti_collection.find({"ID_Classe": id_classe}))
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
            dashboard_collection = db_manager.get_collection("Dashboard")
            return list(dashboard_collection.find({
                "Descrizione_Attività": {"$regex": f"Completamento Quiz: {titolo_quiz}"}
            }))
        except Exception as e:
            raise ValueError(f"Errore durante il recupero delle attività completate: {e}")

    @staticmethod
    def calcola_tempo_rimanente(quiz):
        """Calcola il tempo rimanente per completare un quiz."""
        try:
            ora_inizio = datetime.fromisoformat(quiz["Ora_Inizio"])
            durata_quiz = quiz["Durata"]
            fine = ora_inizio + timedelta(minutes=durata_quiz)
            tempo_rimanente = max(0, (fine - datetime.utcnow()).total_seconds())
            return int(tempo_rimanente)
        except KeyError as e:
            raise ValueError(f"Errore nel calcolo del tempo rimanente: campo mancante {e}")
        except Exception as e:
            raise ValueError(f"Errore nel calcolo del tempo rimanente: {e}")

    @staticmethod
    def salva_risultato_quiz(quiz_result, cf_studente, punteggio):
        """
        Salva il risultato del quiz nel database e registra l'attività nella dashboard.
        :param quiz_result: Dati del risultato del quiz da salvare.
        :param cf_studente: Codice fiscale dello studente.
        :param punteggio: Punteggio ottenuto dallo studente.
        """
        try:
            # Collezioni necessarie
            quiz_results_collection = db_manager.get_collection("RisultatoQuiz")
            attività_collection = db_manager.get_collection("Dashboard")
            quiz_collection = db_manager.get_collection("Quiz")

            # Salva il risultato del quiz
            quiz_results_collection.insert_one(quiz_result)

            # Recupera il titolo del quiz
            quiz = quiz_collection.find_one({"ID_Quiz": quiz_result["ID_Quiz"]}, {"Titolo": 1})
            if not quiz:
                raise ValueError(f"Quiz con ID {quiz_result['ID_Quiz']} non trovato.")
            titolo_quiz = quiz["Titolo"]

            # Genera l'attività svolta
            attività = {
                "ID_Attività": attività_collection.count_documents({}) + 1,  # Genera un ID incrementale
                "Data_Attività": datetime.utcnow(),
                "Descrizione_Attività": f"Completamento Quiz: {titolo_quiz}",
                "Punteggio_Attività": punteggio,
                "CF_Studente": cf_studente
            }

            # Inserisce l'attività nella dashboard
            attività_collection.insert_one(attività)
            print(f"DEBUG: Risultato del quiz e attività salvati correttamente per lo studente {cf_studente}")
        except Exception as e:
            raise ValueError(f"Errore durante il salvataggio del risultato: {e}")
