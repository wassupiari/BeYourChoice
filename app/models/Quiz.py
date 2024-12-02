import openai
from datetime import datetime
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

            # Controlla se ci sono abbastanza linee per testo e risposte
            if len(domanda_lines) < 3:
                raise ValueError("Formato della domanda non valido: non ci sono abbastanza righe.")

            # La prima riga è il testo della domanda
            testo_domanda = domanda_lines[0].strip()

            # Trova le opzioni di risposta (devono iniziare con A), B), ecc.)
            opzioni_risposte = [
                line.strip() for line in domanda_lines[1:]
                if line.startswith(("A)", "B)", "C)", "D)"))
            ]

            # Trova la risposta corretta
            risposta_corretta = next(
                (line.replace("Risposta corretta:", "").strip() for line in domanda_lines if
                 "Risposta corretta:" in line),
                None
            )

            # Verifica che tutti i componenti siano presenti
            if not testo_domanda or not opzioni_risposte or not risposta_corretta:
                raise ValueError("Alcuni componenti della domanda sono mancanti.")

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
                 "content": "Sei un assistente esperto in educazione civica italiana. Genera domande per ragazzi delle superiori per un quiz."},
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


                # Effettua il parsing
                domande.append(QuizModel.parse_domanda(domanda))
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
        quiz_collection = db_manager.get_collection("Quiz")
        questions_collection = db_manager.get_collection("Domanda")

        quiz = {
            "ID_Quiz": data["ID_Quiz"],
            "Argomento": data["Argomento"],
            "N_Domande": data["N_Domande"],
            "Modalità_Quiz": data["Modalità_Quiz"],
            "Durata": data["Durata"],
            "Data_Creazione": data["Data_Creazione"],
            "ID_Classe": data["ID_Classe"]
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
