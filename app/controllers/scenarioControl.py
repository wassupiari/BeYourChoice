import re
from flask import Blueprint, request, jsonify
from app.models.scenarioModel import ScenarioModel

# Crea un Blueprint per gestire gli scenari
scenario_bp = Blueprint('scenario', __name__)  # Correzione: __name__ invece di _name_


# Crea una rotta per la registrazione di uno scenario
@scenario_bp.route('/scenario', methods=['POST'])
def registra_scenario():
    try:
        # Recupera i dati JSON inviati dal client
        # Recupera i dati del form
        titolo = request.form.get('titolo', '').strip()
        descrizione = request.form.get('descrizione', '').strip()
        argomento = request.form.get('argomento', '').strip()

        # Validazione dei campi
        if not titolo or not descrizione or not argomento:
            return jsonify({"error": "Tutti i campi sono obbligatori."}), 400

        # Validazioni dei campi
        titolo_regex = r"^[A-Za-z\s]{2,50}$"  # Titolo con lettere e spazi, 2-50 caratteri
        descrizione_regex = r"^[^§]{2,255}$"  # Nessun '§', lunghezza 2-255 caratteri

        if not re.match(titolo_regex, titolo):
            return jsonify(
                {"error": "Formato titolo non valido! Deve contenere solo lettere e spazi (2-50 caratteri)."}), 400

        if not re.match(descrizione_regex, descrizione):
            return jsonify({
                               "error": "Formato descrizione non valido! Deve essere tra 2 e 255 caratteri e non contenere '§'."}), 400

        # Selezione di argomento (aggiusta in base ai tuoi argomenti validi)
        argomento_options = ["Sostenibilità", "Diritti Civili", "Sanità", "Società e Cultura",
                             "Politica Internazionale", "Economia e Lavoro"]
        if argomento not in argomento_options:
            return jsonify(
                {"error": f"Argomento non valido! Deve essere uno tra: {', '.join(argomento_options)}."}), 400

        # Crea un dizionario con i dati per lo scenario
        scenario_dict = {
            "titolo": titolo,
            "descrizione": descrizione,
            "argomento": argomento
        }

        print(titolo)
        print(descrizione)
        print(argomento)
        # Qui puoi aggiungere ulteriori elaborazioni (o memorizzare se necessario)
        # scenario_model = ScenarioModel()
        # scenario_model.aggiungi_scenario(scenario_dict)

        return jsonify({"message": "Scenario selezionato con successo!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
