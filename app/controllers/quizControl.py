from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, render_template
from app.models.Quiz import QuizModel, db_manager
import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

quiz_blueprint = Blueprint("quiz", __name__, template_folder="../templates")

@quiz_blueprint.route("/ciao1", methods=["GET"])
def index():
    """Renderizza la pagina principale."""
    return render_template("index.html")

@quiz_blueprint.route("/genera", methods=["POST"])
def genera_domande():
    """Genera domande per il quiz."""
    try:
        tema = request.json.get("tema")
        numero_domande = int(request.json.get("numero_domande"))
        modalita_risposta = request.json.get("modalita_risposta")

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
def salva_quiz():
    """Salva un quiz e le sue domande."""
    try:
        data = request.get_json()
        QuizModel.salva_quiz(data)
        return jsonify({"message": "Quiz salvato correttamente!"})
    except Exception as e:
        return jsonify({"error": f"Errore durante il salvataggio: {str(e)}"}), 500

@quiz_blueprint.route('/quiz/<int:quiz_id>', methods=['GET'])
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
