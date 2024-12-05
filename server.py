from flask import Flask, render_template, session, redirect, url_for
import os
from app.controllers.LoginControl import login_bp
from app.controllers.QuizControl import quiz_blueprint
from app.controllers.RegistrazioneControl import registrazione_bp
from app.controllers.DashboardControl import dashboard_blueprint
from app.views.inserimentoStudente import inserimentostudente
from app.views.classeDocente import classedocente
from app.views.scenarioView import scenario_bp
from app.views.views import views
from app.models.studenteModel import StudenteModel
from app.models.docenteModel import DocenteModel
from app.models.attivitaModel import Attivita
from app.views.materialeDocente import initialize_materiale_docente_blueprint
from app.views.materialeStudente import initialize_materiale_studente_blueprint
from app.views.profilo import initialize_profilo_blueprint
from databaseManager import DatabaseManager

# Crea l'applicazione Flask
app = Flask(__name__, template_folder='app/templates', static_folder="public")
# Imposta il percorso dei template








# Definisci una route per la homepage
@app.route('/')
@app.route('/dashboard')
def home():
    if 'email' not in session:
        return redirect(url_for('login.login'))
    else:
        logged_in = 'email' in session
        email = session.get('email')
        if email is None or email == '':
            # Se l'email non è presente nella sessione, reindirizza al login
            return redirect(url_for('login.login'))

        studenteModel = StudenteModel()
        docenteModel = DocenteModel()
        stud = studenteModel.trova_studente(email)
        doc = docenteModel.trova_docente(email)
        model = Attivita()
        if stud is not None: return render_template('dashboardStudente.html', logged_in=logged_in,
                                                    storico=model.get_storico(studenteModel.trova_cf_per_email(email)))
        if doc is not None: return render_template('dashboardDocente.html', logged_in=logged_in,
                                                   id_docente=docenteModel.get_codice_univoco_by_email(email))

app.register_blueprint(classedocente, url_prefix='/classedocente')  # Usa '/' o un altro prefisso a tua scelta
app.register_blueprint(inserimentostudente,
                       url_prefix='/inserimentostudente')  # Il prefisso '/' è opzionale, puoi scegliere uno diverso
app.register_blueprint(views, url_prefix='/')  # Il prefisso '/' è opzionale, puoi scegliere uno diverso

# Imposta la secret key (generata in modo sicuro)
app.secret_key = os.urandom(32).hex()
app.register_blueprint(dashboard_blueprint)

app.register_blueprint(scenario_bp)

app.register_blueprint(login_bp)
app.register_blueprint(registrazione_bp)
app.register_blueprint(quiz_blueprint)

UPLOAD_FOLDER = 'public/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Variabile per decidere quale blueprint registrare


# Inizializzazione del blueprint condizionale

initialize_materiale_docente_blueprint(app)

initialize_materiale_studente_blueprint(app)

initialize_profilo_blueprint(app)


# Avvio del server
if __name__ == "__main__":
    app.run(debug=True)
