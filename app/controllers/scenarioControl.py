import re
from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from app.models.scenarioModel import ScenarioModel

class scenarioControl:
    @staticmethod
    def registra_scenario(id, titolo, descrizione, modalita, argomento):
        try:
            # Validazione dei campi
            if not titolo or not descrizione or not argomento:
                return redirect(url_for('scenario_bp.scenario_virtuale', error='DatiObbligatori'))

            # Validazioni dei campi
            titolo_regex = r"^[A-Za-z\s]{2,50}$"
            descrizione_regex = r"^[^§]{2,255}$"

            if not re.match(titolo_regex, titolo):
                return redirect(url_for('scenario_bp.scenario_virtuale', error='formatoTitolo'))

            if not re.match(descrizione_regex, descrizione):
                return redirect(url_for('scenario_bp.scenario_virtuale', error='formatoDescrizione'))

            argomento_options = ["Sostenibilità", "Diritti Civili", "Sanità", "Società e Cultura",
                                 "Politica Internazionale", "Economia e Lavoro"]

            if argomento not in argomento_options:
                return redirect(url_for('scenario_bp.scenario_virtuale', error='argomentoNonValido'))

            # Creazione dello scenario
            scenario_dict = {
                'id_scenario': id,
                "titolo": titolo,
                "descrizione": descrizione,
                "argomento": argomento,
                "modalità": modalita
            }

            scenario_model = ScenarioModel()
            scenario_model.aggiungi_scenario(scenario_dict)

            return render_template("visore.html")

        except Exception as e:
            return jsonify({"success": False, "message": f"Errore interno: {str(e)}"})
