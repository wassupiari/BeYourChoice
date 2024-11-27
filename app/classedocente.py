from flask import *
from app.controllers.ClasseVirtualeControl import ClasseVirtualeControl

# Crea il blueprint
classedocente = Blueprint('classedocente', __name__, template_folder='../templates')
# Configura il database manager
classe_virtuale_control = ClasseVirtualeControl()


@classedocente.route('/', methods=['GET', 'POST'])
def Classe_Docente():
    print("La route /ClasseDocente è stata chiamata!")  # Debug
    try:
        # Ottieni l'ID della classe dalla query string (se non è presente, usa 101 come default)
        ID_Classe = int(request.args.get("ID_Classe", 101))
        print(f"ID_Classe ricevuto: {ID_Classe}")  # Aggiunto per debugging

        # Usa il controller per ottenere i dati degli studenti
        dati_classe = classe_virtuale_control.mostra_classe(ID_Classe)
        print(f"Dati classe ricevuti: {dati_classe}")  # Aggiunto per debugging
        if "error" in dati_classe:
            return render_template("errore.html", messaggio=dati_classe["error"])

            # Passa i dati al template classeDocente.html
        return render_template("classeDocente.html", classe=dati_classe)

    except Exception as e:
        return render_template("errore.html", messaggio=f"Errore: {str(e)}")


@classedocente.route('/rimuovi-studente', methods=['POST'])
def rimuovi_studente():
    try:
        # Ottieni l'ID dello studente dalla richiesta
        data = request.get_json()
        studente_id = data.get('studente_id')

        if not studente_id:
            return jsonify({'error': 'ID studente mancante'}), 400

        # Chiama il metodo per rimuovere lo studente
        result = classe_virtuale_control.rimuovi_studente(studente_id)

        # Se il risultato è positivo, invia una risposta di successo
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500