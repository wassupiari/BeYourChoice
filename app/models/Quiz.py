from datetime import datetime

import openai
from flask import session

from databaseManager import DatabaseManager

db_manager = DatabaseManager()


class QuizModel:

    @staticmethod
    def parse_domanda(domanda_testo):
        """
        Elabora il testo della domanda generata da OpenAI per estrarre:
        - Testo della domanda
        - Opzioni di risposta
        - Risposta corretta
        """
        try:
            domanda_lines = domanda_testo.strip().split("\n")

            # Controlla se ci sono abbastanza linee
            if len(domanda_lines) < 3:
                raise ValueError("Formato della domanda non valido.")

            # La prima riga è il testo della domanda
            testo_domanda = domanda_lines[0].strip()

            # Opzioni di risposta (iniziano con A), B), C), D))
            opzioni_risposte = [
                line.strip() for line in domanda_lines[1:] if line.startswith(("A)", "B)", "C)", "D)"))
            ]

            # Risposta corretta (formato: "Risposta corretta: X)")
            risposta_corretta = next(
                (line.replace("Risposta corretta:", "").strip() for line in domanda_lines if
                 "Risposta corretta:" in line),
                None
            )

            # Validazione dei componenti
            if not testo_domanda or not opzioni_risposte or not risposta_corretta:
                raise ValueError("Alcuni componenti essenziali della domanda sono mancanti.")

            # Rimuovi prefissi da opzioni
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
                 "content":
                            "Sei un assistente esperto in educazione civica italiana e devi generare domande per un quiz destinato a studenti delle scuole superiori. Le domande devono essere educative, coinvolgenti e adatte al livello di conoscenza degli studenti. Ogni domanda deve:"+
                            "Essere chiara e formulata correttamente."+
                            "Affrontare temi fondamentali di educazione civica italiana, come Costituzione, diritti e doveri dei cittadini, funzionamento dello Stato, istituzioni pubbliche, elezioni, legalità, cittadinanza attiva e sostenibilità."+
                            "Essere accompagnata da opzioni di risposta:"+
                            "Se modalità scelta multipla con 3 risposte: fornisci 3 opzioni di risposta, di cui solo 1 è corretta."+
                            "Se modalità scelta multipla con 4 risposte: fornisci 4 opzioni di risposta, di cui solo 1 è corretta."},
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

                # Effettua il parsing e aggiunge la domanda alla lista
                parsed_domanda = QuizModel.parse_domanda(domanda)
                domande.append(parsed_domanda)
            except ValueError as parse_error:
                print(f"Errore nel parsing della domanda: {parse_error}")
                continue  # Salta questa domanda e continua con la successiva
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

            # Recupera l'ID della classe dalla sessione
            id_classe = session.get("ID_Classe")
            if not id_classe:
                raise ValueError("ID Classe mancante nella sessione.")

            # Prepara il documento per il quiz
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

            # Inserisci ogni domanda nel database
            for domanda in data["Domande"]:
                question = {
                    "ID_Domanda": domanda["ID_Domanda"],
                    "Testo_Domanda": domanda["Testo_Domanda"],
                    "Opzioni_Risposte": [
                        opzione.replace("A)", "").replace("B)", "").replace("C)", "").replace("D)", "").strip()
                        for opzione in domanda["Opzioni_Risposte"]
                    ],
                    "Risposta_Corretta": domanda["Risposta_Corretta"].replace("A)", "").replace("B)", "").replace("C)",
                                                                                                                  "").replace(
                        "D)", "").strip(),
                    "ID_Quiz": data["ID_Quiz"]
                }
                questions_collection.insert_one(question)
        except Exception as e:
            raise ValueError(f"Errore durante il salvataggio del quiz: {e}")

    def recupera_quiz_per_classe(id_classe):
        """
        Recupera tutti i quiz associati a una specifica classe.
        :param id_classe: ID della classe
        :return: Lista di quiz
        """
        try:
            quiz_collection = db_manager.get_collection("Quiz")
            quiz_list = list(quiz_collection.find({"ID_Classe": id_classe}))

            # Converte l'ObjectId in stringa
            for quiz in quiz_list:
                quiz["_id"] = str(quiz["_id"])
            return quiz_list
        except Exception as e:
            raise ValueError(f"Errore durante il recupero dei quiz per la classe {id_classe}: {e}")

    @staticmethod
    def recupera_domande(question_ids):
        """
        Recupera le domande dal database in base agli ID.
        """
        try:
            questions_collection = db_manager.get_collection("Domanda")
            return list(questions_collection.find({"ID_Domanda": {"$in": question_ids}}))
        except Exception as e:
            raise ValueError(f"Errore durante il recupero delle domande: {e}")

    @staticmethod
    def salva_risultato_quiz(quiz_result, cf_studente, punteggio):
        """
        Salva il risultato del quiz nel database.
        """
        try:
            quiz_results_collection = db_manager.get_collection("RisultatoQuiz")
            quiz_results_collection.insert_one(quiz_result)

            # Genera l'ID incrementale per l'attività
            attività_collection = db_manager.get_collection("Attività")
            last_attività = attività_collection.find_one(sort=[("ID_Attività", -1)])  # Recupera l'ultima attività
            nuovo_id_attività = last_attività["ID_Attività"] + 1 if last_attività else 1

            # Salva l'attività svolta
            attività = {
                "ID_Attività": nuovo_id_attività,
                "Data_Attività": datetime.utcnow(),  # Assicura che venga salvato come Date
                "Descrizione_Attività": f"Completamento Quiz {quiz_result['ID_Quiz']}",
                "Punteggio_Attività": punteggio,
                "CF_Studente": cf_studente
            }

            # Inserisce l'attività nel database
            attività_collection.insert_one(attività)
        except Exception as e:
            raise ValueError(f"Errore durante il salvataggio del risultato: {e}")

