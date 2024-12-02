from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, render_template, session
from app.controllers.loginControl import teacher_required, student_required
from app.models.Quiz import QuizModel, db_manager
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