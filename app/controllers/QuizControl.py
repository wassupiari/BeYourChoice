import os
import re
from flask import Blueprint, request, session, jsonify
from app.models.quizModel import QuizModel
from app.views.quizView import QuizView
from app.controllers.LoginControl import teacher_required, student_required
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

quiz_blueprint = Blueprint("quiz", __name__, template_folder="../templates")


@quiz_blueprint.route("/crea-quiz", methods=["GET"])
@teacher_required
def index():
    """Renderizza la pagina di creazione quiz."""
    id_classe = session.get("ID_Classe")
    if not id_classe:
        return QuizView.mostra_errore("ID Classe mancante nella sessione", 400)
    return QuizView.mostra_crea_quiz(id_classe)




@quiz_blueprint.route("/genera", methods=["POST"])
@teacher_required
def genera_domande():
    """Genera domande per il quiz."""
    try:
        titolo = request.json.get("titolo")
        tema = request.json.get("tema")
        numero_domande = request.json.get("numero_domande")
        modalita_risposta = request.json.get("modalita_risposta")
        durata = request.json.get("durata")

        # Controlli di validazione
        if not titolo or not re.match(r"^[A-Za-zÀ-ú0-9\s\-_']{2,255}$", titolo):
            return jsonify({"error": "Il titolo non è valido (2-255 caratteri, formato corretto)."}), 400

        if QuizModel.verifica_titolo(titolo):
            return jsonify({"error": "Il titolo esiste già nel database."}), 400

        if not tema or not re.match(r"^[A-Za-zÀ-ú0-9‘’',\.\(\)\s\/|\\{}\[\],\-!$%&?<>=^+°#*:']{2,255}$", tema):
            return jsonify({"error": "L'argomento non è valido (2-255 caratteri, formato corretto)."}), 400

        if not numero_domande or not (5 <= int(numero_domande) <= 20):
            return jsonify({"error": "Il numero di domande deve essere compreso tra 5 e 20."}), 400

        if modalita_risposta not in ["3_risposte", "4_risposte", "vero_falso"]:
            return jsonify({"error": "Modalità di risposta non valida."}), 400



        # Genera domande
        domande = QuizModel.genera_domande(
            tema=tema,
            numero_domande=int(numero_domande),
            modalita_risposta=modalita_risposta,
            durata=durata,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        return jsonify(domande), 200
    except Exception as e:
        return jsonify({"error": f"Errore durante la generazione: {str(e)}"}), 500






@quiz_blueprint.route("/salva", methods=["POST"])
@teacher_required
def salva_quiz():
    """Salva un quiz e le sue domande."""
    try:
        data = request.get_json()
        id_classe = session.get("ID_Classe")
        if not id_classe:
            return QuizView.mostra_errore("ID Classe mancante nella sessione", 400)
        data["ID_Classe"] = id_classe

        QuizModel.salva_quiz(data)
        return QuizView.mostra_messaggio("Quiz salvato correttamente!")
    except Exception as e:
        return QuizView.mostra_errore(f"Errore durante il salvataggio: {str(e)}")



@quiz_blueprint.route('/quiz/<int:quiz_id>', methods=['GET'])
@student_required
def visualizza_quiz(quiz_id):
    """
    Mostra la pagina del quiz solo se lo studente non lo ha già completato.
    """
    try:
        cf_studente = session.get('cf')
        if not cf_studente:
            return QuizView.mostra_errore("CF dello studente non trovato nella sessione", 403)

        # Controlla se lo studente ha già completato il quiz
        if QuizModel.verifica_completamento_quiz(quiz_id, cf_studente):
            return QuizView.mostra_errore("Hai già completato questo quiz.", 403)

        # Recupera i dati del quiz
        quiz = QuizModel.recupera_quiz(quiz_id)
        if not quiz:
            return QuizView.mostra_errore("Quiz non trovato", 404)

        domande = QuizModel.recupera_domande([d["ID_Domanda"] for d in quiz["Domande"]])
        tempo_rimanente = QuizModel.calcola_tempo_rimanente(quiz_id, cf_studente)

        return QuizView.mostra_quiz(quiz, domande, tempo_rimanente)
    except Exception as e:
        print(f"ERRORE: {e}")
        return QuizView.mostra_errore("Errore durante il caricamento del quiz", 500)








@quiz_blueprint.route('/valuta-quiz', methods=['POST'])
@student_required
def valuta_quiz():
    """
    Valuta le risposte inviate dal form del quiz e salva il risultato.
    """
    try:
        # Recupera il CF dello studente dalla sessione
        cf_studente = session.get('cf')
        if not cf_studente:
            return jsonify({"error": "CF dello studente non trovato nella sessione"}), 400

        # Recupera i dati della richiesta
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nessuna risposta ricevuta"}), 400

        # Estrai gli ID delle domande
        question_ids = [int(key[1:]) for key in data.keys() if key.startswith("q")]
        if not question_ids:
            return jsonify({"error": "Nessuna domanda valida trovata"}), 400

        # Recupera le domande dal database
        domande = QuizModel.recupera_domande(question_ids)
        totale = len(domande)
        if totale == 0:
            return jsonify({"error": "Nessuna domanda trovata nel database"}), 400

        # Valuta le risposte
        corrette = 0
        for domanda in domande:
            risposta_utente = data.get(f"q{domanda['ID_Domanda']}")
            if risposta_utente == domanda["Risposta_Corretta"]:
                corrette += 1

        # Calcola il punteggio
        punteggio = int((corrette / totale) * 100)

        # Prepara il risultato del quiz
        quiz_result = {
            "ID_Quiz": domande[0]["ID_Quiz"],
            "CF_Studente": cf_studente,
            "Punteggio_Quiz": punteggio,
            "Risposte": [data.get(f"q{d['ID_Domanda']}") for d in domande]
        }

        # Salva il risultato del quiz
        QuizModel.salva_risultato_quiz(quiz_result, cf_studente, punteggio)

        return jsonify({
            "message": f"Hai ottenuto un punteggio di {punteggio}%. Domande corrette: {corrette}/{totale}",
            "punteggio": punteggio,
            "corrette": corrette,
            "totale": totale
        })
    except Exception as e:
        print(f"ERRORE durante la valutazione del quiz: {e}")
        return jsonify({"error": "Errore durante la valutazione del quiz"}), 500




@quiz_blueprint.route('/quiz/<int:quiz_id>/domande', methods=['GET'])
@teacher_required
def visualizza_domande_quiz(quiz_id):
    """Visualizza le domande di un quiz selezionato."""
    try:
        quiz = QuizModel.recupera_quiz(quiz_id)
        if not quiz:
            return QuizView.mostra_errore("Quiz non trovato", 404)

        domande = QuizModel.recupera_domande([d["ID_Domanda"] for d in quiz["Domande"]])
        return QuizView.mostra_domande_quiz(quiz, domande)
    except Exception as e:
        return QuizView.mostra_errore("Errore durante la visualizzazione delle domande")


@quiz_blueprint.route('/quiz/<int:quiz_id>/risultati', methods=['GET'])
@teacher_required
def visualizza_risultati_quiz(quiz_id):
    """
    Visualizza i risultati degli studenti per un quiz specifico,
    includendo tutti gli studenti della classe e verificando se hanno completato il quiz.
    """
    try:
        # Recupera il quiz
        quiz = QuizModel.recupera_quiz(quiz_id)
        if not quiz:
            return QuizView.mostra_errore("Quiz non trovato", 404)

        id_classe = quiz.get("ID_Classe")
        titolo_quiz = quiz.get("Titolo")

        # Recupera tutti gli studenti della classe
        studenti_classe = QuizModel.recupera_studenti_classe(id_classe)
        if not studenti_classe:
            return QuizView.mostra_risultati_quiz([], quiz_id)

        # Recupera le attività completate per questo quiz
        attività_completate = QuizModel.recupera_attività_completate(titolo_quiz)
        attività_per_cf = {attività["CF_Studente"].strip().upper(): attività for attività in attività_completate}

        # Combina i risultati con l'elenco degli studenti
        risultati_completi = [
            {
                "Nome": studente["nome"],
                "Cognome": studente["cognome"],
                "Punteggio": attività_per_cf.get(studente["cf"].strip().upper(), {}).get("Punteggio_Attività", "Quiz non svolto")
            }
            for studente in studenti_classe
        ]

        return QuizView.mostra_risultati_quiz(risultati_completi, quiz_id)
    except Exception as e:
        print(f"Errore durante il caricamento dei risultati: {e}")
        return QuizView.mostra_errore("Errore durante il caricamento dei risultati")




@quiz_blueprint.route('/ultimo-quiz', methods=['GET'])
@student_required
def visualizza_ultimo_quiz():
    """Visualizza l'ultimo quiz disponibile per una classe."""
    try:
        cf_studente = session.get('cf')
        id_classe = session.get('ID_Classe')

        if not cf_studente or not id_classe:
            return QuizView.mostra_errore("Sessione non valida", 400)

        ultimo_quiz = QuizModel.recupera_ultimo_quiz(id_classe, cf_studente)
        if not ultimo_quiz:
            return QuizView.mostra_ultimo_quiz(None)

        return QuizView.mostra_ultimo_quiz(ultimo_quiz)
    except Exception as e:
        return QuizView.mostra_errore("Errore durante il caricamento dell'ultimo quiz")

@quiz_blueprint.route("/visualizza-quiz", methods=["GET"])
@teacher_required
def visualizza_quiz_classe():
    """
    Recupera tutti i quiz per una specifica classe e li passa al template per il docente.
    """
    try:
        id_classe = session.get("ID_Classe")  # Recupera l'ID della classe dalla sessione
        if not id_classe:
            return QuizView.mostra_errore("ID Classe non specificato.", 400)

        # Recupera i quiz dal database
        quiz_list = QuizModel.recupera_quiz_per_classe(id_classe)

        # Passa i dati alla view per la visualizzazione
        return QuizView.mostra_quiz_precedenti(quiz_list, id_classe)
    except Exception as e:
        print(f"Errore durante il recupero dei quiz: {e}")
        return QuizView.mostra_errore("Errore durante il recupero dei quiz")
