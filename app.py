from flask import Flask, render_template, request, redirect, url_for, flash
from app.controllers.MaterialeControl import MaterialeControl
from databaseManager import DatabaseManager

# Inizializza l'applicazione Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Sostituisci con una chiave segreta più sicura

# Inizializza DatabaseManager e MaterialeControl
db_manager = DatabaseManager()
materiale_control = MaterialeControl(db_manager)

@app.route('/materiale')
def visualizza_materiale():
    """Visualizza tutti i materiali."""
    materiali = materiale_control.view_all_materials()
    return render_template('materiale.html', materiali=materiali)

@app.route('/carica', methods=['GET', 'POST'])
def carica_materiale():
    """Carica un nuovo materiale."""
    if request.method == 'POST':
        titolo = request.form['titolo']
        descrizione = request.form['descrizione']
        tipo = request.form['tipo']
        file = request.files['file']

        # Salva il file sul server
        filepath = f'static/uploads/{file.filename}'
        file.save(filepath)

        # Salva i dettagli nel database
        materiale_control.upload_material(titolo, descrizione, filepath, tipo)
        flash("Materiale caricato con successo!", "success")
        return redirect(url_for('visualizza_materiale'))

    return render_template('caricamento_materiale.html')

@app.route('/modifica/<materiale_id>', methods=['GET', 'POST'])
def modifica_materiale(materiale_id):
    """Modifica un materiale esistente."""
    if request.method == 'POST':
        updated_data = {
            "Titolo": request.form['titolo'],
            "Descrizione": request.form['descrizione'],
            "Tipo": request.form['tipo'],
        }
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            filepath = f'static/uploads/{file.filename}'
            file.save(filepath)
            updated_data['File_Path'] = filepath

        materiale_control.edit_material(materiale_id, updated_data)
        flash("Materiale modificato con successo!", "success")
        return redirect(url_for('visualizza_materiale'))

    materiale = materiale_control.view_material({"_id": materiale_id})
    return render_template('modifica_materiale.html', materiale=materiale)

@app.route('/rimuovi/<materiale_id>')
def rimuovi_materiale(materiale_id):
    """Rimuove un materiale esistente."""
    materiale_control.delete_material(materiale_id)
    flash("Materiale rimosso con successo!", "success")
    return redirect(url_for('visualizza_materiale'))

if __name__ == '__main__':
    app.run(debug=True)  # Avvia l'app in modalità debug