from flask import *
from app.controllers.ClasseVirtualeControl import ClasseVirtualeControl
from app.controllers.loginControl import teacher_required, student_required

# Crea il blueprint
classedocente = Blueprint('classedocente', __name__)
# Configura il database manager
classe_virtuale_control = ClasseVirtualeControl()


@classedocente.route('/classe/<int:ID_Classe>', methods=['GET', 'POST'])
@teacher_required
def Classe_Docente(ID_Classe):
    # Assumendo che l'ID_Classe sia passato come parametro o derivato da un'altra fonte
    print("La route /ClasseDocente è stata chiamata!")  # Debug
    session['ID_Classe'] = ID_Classe
    try:
        # Ottieni l'ID della classe dalla query string (se non è presente, usa 101 come default)
        print(f"ID_Classe ricevuto: {ID_Classe}")  # Aggiunto per debugging
        return render_template('classeDocente.html', ID_Classe=ID_Classe)
        # Usa il controller per ottenere i dati degli studenti
        dati_classe = classe_virtuale_control.mostra_classe(ID_Classe)
        print(f"Dati classe ricevuti: {dati_classe}")  # Aggiunto per debugging
        if "error" in dati_classe:
            return render_template("classeDocente.html")

            # Passa i dati al template classeDocente.html
        return render_template("classeDocente.html", classe=dati_classe)

    except Exception as e:
        return render_template("errore.html", messaggio=f"Errore: {str(e)}")




@classedocente.route('/classestudente/<int:ID_Classe>', methods=['GET', 'POST'])
@student_required
def Classe_Studente(ID_Classe):
    print("La route /ClasseStudente è stata chiamata!")  # Debug
    if ID_Classe == 0:
        # Se ID_Classe è 0, reindirizza alla pagina noclasse
        return redirect(url_for('classedocente.NoClasse'))

    try:
        print(f"ID_Classe ricevuto: {ID_Classe}")  # Debug
        dati_classe = classe_virtuale_control.mostra_classe(ID_Classe)
        print(f"Dati classe ricevuti: {dati_classe}")  # Debug

        if "error" in dati_classe:
            return render_template("errore.html", messaggio=dati_classe["error"])

        return render_template("classeStudente.html", classe=dati_classe)

    except Exception as e:
        return render_template("errore.html", messaggio=f"Errore: {str(e)}")


# Route per la pagina noclasse
@classedocente.route('/noclasse', methods=['GET'])
@student_required
def NoClasse():
    return render_template("noclasse.html", messaggio="Nessuna classe selezionata.")

# Route per la pagina manutenzione
@classedocente.route('/manutenzione', methods=['GET'])
def Manutenzione():
    return render_template("error404.html", messaggio="Manutenzione in corso.")

@classedocente.route('/rimuovi-studente', methods=['POST'])
@teacher_required
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


@classedocente.route('/aggiungi-studente', methods=['POST'])
@teacher_required
def aggiungi_studente():
    try:
        # Ottieni i dati dallo studente dalla richiesta
        data = request.get_json()  # Dati inviati come JSON
        studente_id = data.get('studente_id')
        classe_id = int(data.get('classe_id'))  # Conversione esplicita a intero

        if not studente_id or not classe_id:
            return jsonify({'error': 'ID dello studente o della classe non forniti'}), 400

        # Aggiungi lo studente alla classe
        result = classe_virtuale_control.aggiungi_studente(studente_id, classe_id)

        # Se l'inserimento è avvenuto con successo
        if result:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Errore durante l\'aggiunta dello studente'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500