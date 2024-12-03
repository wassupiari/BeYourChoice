from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, render_template, session
from app.controllers.LoginControl import teacher_required, student_required
from app.models.quizModel import QuizModel, db_manager
import os
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
        return "ID Classe mancante nella sessione", 400
    return render_template("creaQuiz.html", id_classe=id_classe)

@quiz_blueprint.route("/genera", methods=["POST"])
@teacher_required
def genera_domande():
    """Genera domande per il quiz."""
    try:
        tema = request.json.get("tema")
        numero_domande = int(request.json.get("numero_domande"))
        modalita_risposta = request.json.get("modalita_risposta")

        # Recupera l'ID classe dalla sessione
        id_classe = session.get("ID_Classe")
        if not id_classe:
            return jsonify({"error": "ID Classe mancante nella sessione"}), 400

        if not tema or numero_domande <= 0 or modalita_risposta not in ["3_risposte", "4_risposte", "vero_falso"]:
            return jsonify({"error": "Parametri non validi"}), 400

        # Genera le domande
        domande = QuizModel.genera_domande(
            tema=tema,
            numero_domande=numero_domande,
            modalita_risposta=modalita_risposta,
            api_key=os.getenv("OPENAI_API_KEY")
        )

        return jsonify(domande)
    except Exception as e:
        print(f"Errore durante la generazione delle domande: {e}")
        return jsonify({"error": f"Errore durante la generazione: {str(e)}"}), 500

@quiz_blueprint.route("/salva", methods=["POST"])
@teacher_required
def salva_quiz():
    """Salva un quiz e le sue domande."""
    try:
        data = request.get_json()

        # Recupera l'ID Classe dalla sessione e aggiungilo ai dati
        id_classe = session.get("ID_Classe")
        if not id_classe:
            return jsonify({"error": "ID Classe mancante nella sessione"}), 400
        data["ID_Classe"] = id_classe

        # Salva il quiz utilizzando il modello
        QuizModel.salva_quiz(data)
        return jsonify({"message": "Quiz salvato correttamente!"})
    except Exception as e:
        print(f"Errore durante il salvataggio del quiz: {e}")
        return jsonify({"error": f"Errore durante il salvataggio: {str(e)}"}), 500

@quiz_blueprint.route('/quiz/<int:quiz_id>', methods=['GET'])
@student_required
def visualizza_quiz(quiz_id):
    """
    Visualizza un quiz e le sue domande.
    :param quiz_id: ID del quiz.
    :return: Pagina HTML per il quiz.
    """
    try:
        # Recupera il quiz dal database
        quiz_collection = db_manager.get_collection("Quiz")
        questions_collection = db_manager.get_collection("Domanda")

        quiz = quiz_collection.find_one({"ID_Quiz": quiz_id})
        if not quiz:
            return "Quiz non trovato", 404

        # Recupera o assegna l'ora di inizio
        if "Ora_Inizio" not in quiz:
            quiz["Ora_Inizio"] = datetime.utcnow().isoformat()
            quiz_collection.update_one({"ID_Quiz": quiz_id}, {"$set": {"Ora_Inizio": quiz["Ora_Inizio"]}})

        # Calcola il tempo rimanente in secondi
        ora_inizio = datetime.fromisoformat(quiz["Ora_Inizio"])
        durata_quiz = timedelta(minutes=quiz["Durata"])
        tempo_rimanente = max(0, int((ora_inizio + durata_quiz - datetime.utcnow()).total_seconds()))

        # Recupera le domande
        questions = list(questions_collection.find({"ID_Quiz": quiz_id}))

        return render_template('quiz.html', quiz=quiz, questions=questions, tempo_rimanente=tempo_rimanente)
    except Exception as e:
        print(f"Errore durante il caricamento del quiz: {e}")
        return "Errore durante il caricamento del quiz", 500


@quiz_blueprint.route("/visualizza-quiz", methods=["GET"])
@teacher_required
def visualizza_quiz_classe():
    """
    Recupera tutti i quiz per una specifica classe e li passa al template.
    """
    id_classe = session.get("ID_Classe")

    if not id_classe:
        return "ID Classe non specificato.", 400

    try:
        # Recupera i quiz dal database
        quiz_list = QuizModel.recupera_quiz_per_classe(int(id_classe))

        return render_template("quizPrecedenti.html", quiz_list=quiz_list, id_classe=id_classe)
    except Exception as e:
        print(f"Errore durante il recupero dei quiz: {e}")
        return "Errore durante il recupero dei quiz.", 500

@quiz_blueprint.route('/valuta-quiz', methods=['POST'])
@student_required
def valuta_quiz():
    """
    Valuta le risposte inviate dal form del quiz e salva il risultato.
    """
    try:
        # Recupera il CF dalla sessione
        cf_studente = session.get('cf')
        if not cf_studente:
            return jsonify({"message": "CF dello studente non trovato in sessione."}), 400


        # Recupera le risposte inviate
        data = request.get_json()
        if not data:
            return jsonify({"message": "Nessuna risposta ricevuta"}), 400

        # Filtra solo le chiavi che iniziano con "q" per estrarre gli ID delle domande
        question_ids = [int(key[1:]) for key in data.keys() if key.startswith("q")]
        if not question_ids:
            return jsonify({"message": "Nessuna domanda trovata"}), 400

        # Recupera le domande
        domande = QuizModel.recupera_domande(question_ids)
        totale = len(domande)
        if totale == 0:
            return jsonify({"message": "Nessuna domanda valida trovata per il quiz"}), 400

        # Valutazione delle risposte
        corrette = 0
        risposte_utente = []
        for domanda in domande:
            risposta_utente = data.get(f"q{domanda['ID_Domanda']}")
            risposte_utente.append(risposta_utente)
            if risposta_utente == domanda["Risposta_Corretta"]:
                corrette += 1

        # Calcolo del punteggio
        punteggio = int((corrette / totale) * 100)

        # Salva il risultato del quiz e registra l'attività
        quiz_result = {
            "ID_Quiz": domande[0]["ID_Quiz"],
            "CF_Studente": cf_studente,
            "Punteggio_Quiz": punteggio,
            "Risposte": risposte_utente
        }
        QuizModel.salva_risultato_quiz(quiz_result, cf_studente, punteggio)

        return jsonify({"message": f"Hai ottenuto un punteggio di {punteggio}%. Domande corrette: {corrette}/{totale}"})
    except Exception as e:
        print(f"Errore durante la valutazione del quiz: {e}")
        return jsonify({"message": "Errore durante la valutazione del quiz"}), 500

@quiz_blueprint.route('/quiz/<int:quiz_id>/domande', methods=['GET'])
@teacher_required
def visualizza_domande_quiz(quiz_id):
    """
    Visualizza le domande di un quiz selezionato.
    """
    try:
        # Recupera il quiz e le sue domande dal database
        quiz_collection = db_manager.get_collection("Quiz")
        questions_collection = db_manager.get_collection("Domanda")

        quiz = quiz_collection.find_one({"ID_Quiz": quiz_id})
        if not quiz:
            return jsonify({"message": "Quiz non trovato"}), 404

        domande = list(questions_collection.find({"ID_Quiz": quiz_id}))

        # Passa i dati al template
        return render_template('domandeQuizPrecedenti.html', quiz=quiz, domande=domande)
    except Exception as e:
        print(f"Errore durante la visualizzazione delle domande del quiz: {e}")
        return jsonify({"message": "Errore durante la visualizzazione delle domande"}), 500

@quiz_blueprint.route('/quiz/<int:quiz_id>/risultati', methods=['GET'])
@teacher_required
def visualizza_risultati_quiz(quiz_id):
    """
    Visualizza i risultati degli studenti per un quiz specifico.
    """
    try:
        # Recupera i risultati degli studenti dal database
        quiz_results_collection = db_manager.get_collection("RisultatoQuiz")
        studenti_collection = db_manager.get_collection("Studente")

        risultati = list(quiz_results_collection.find({"ID_Quiz": quiz_id}))

        # Unisci i risultati con i dettagli degli studenti
        risultati_completi = []
        for risultato in risultati:
            studente = studenti_collection.find_one({"cf": risultato["CF_Studente"]})  # Campo corretto: "cf"
            risultati_completi.append({
                "Nome": studente["nome"] if studente else "Studente Sconosciuto",
                "Cognome": studente["cognome"] if studente else "",
                "Punteggio": risultato["Punteggio_Quiz"]
            })

        return render_template('risultatiQuizPrecedenti.html', risultati=risultati_completi, quiz_id=quiz_id)
    except Exception as e:
        print(f"Errore durante il caricamento dei risultati: {e}")
        return jsonify({"message": "Errore durante il caricamento dei risultati"}), 500

@quiz_blueprint.route('/ultimo-quiz', methods=['GET'])
def visualizza_ultimo_quiz():
    """
    Visualizza l'ultimo quiz creato dal docente per lo studente,
    ma solo se non è stato già completato.
    """
    try:
        # Recupera l'ultimo quiz dalla collezione Quiz
        quiz_collection = db_manager.get_collection("Quiz")
        activities_collection = db_manager.get_collection("Dashboard")

        # Recupera l'ultimo quiz ordinando per data di creazione in ordine decrescente
        ultimo_quiz = quiz_collection.find_one(sort=[("Data_Creazione", -1)])
        if not ultimo_quiz:
            return render_template('quizDisponibile.html', quiz=None)

        # Controlla se lo studente ha già completato il quiz
        cf_studente = session.get('cf')
        if not cf_studente:
            return jsonify({"message": "Errore: codice fiscale non trovato nella sessione"}), 403

        attività_completate = activities_collection.find_one({
            "CF_Studente": cf_studente
        })

        # Se il quiz è stato completato, non mostrarlo
        if attività_completate:
            return render_template('quizDisponibile.html', quiz=None)

        # Recupera le domande associate al quiz
        questions_collection = db_manager.get_collection("Domanda")
        domande = list(questions_collection.find({"ID_Quiz": ultimo_quiz["ID_Quiz"]}))

        return render_template('quizDisponibile.html', quiz=ultimo_quiz, domande=domande)
    except Exception as e:
        print(f"Errore durante il caricamento dell'ultimo quiz: {e}")
        return jsonify({"message": "Errore durante il caricamento dell'ultimo quiz"}), 500






