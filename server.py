from flask import Flask
from app.views.docente import initialize_materiale_docente_blueprint
from app.views.studente import initialize_materiale_studente_blueprint

app = Flask(__name__, template_folder='app/templates', static_folder='public')
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'public/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variabile per decidere quale blueprint registrare
USE_DOCENTE = True  # Cambia questo valore in False per usare Studente invece

# Inizializzazione del blueprint condizionale
if USE_DOCENTE:
    initialize_materiale_docente_blueprint(app)
else:
    initialize_materiale_studente_blueprint(app)

if __name__ == '__main__':
    app.run(debug=True)
