from flask import Flask, render_template, session, redirect, url_for

from app.controllers.loginControl import login_bp
from app.controllers.registrazioneControl import registrazione_bp
from flask import Flask, render_template, session
import os
from app.controllers.loginControl import login_bp, logout
from app.controllers.registrazioneControl import registrazione_bp
from app.views.dasboardDocente import dashboardDocente_bp
from app.views.dasboardStudente import dashboard_bp
from app.views.inserimentostudente import inserimentostudente
from app.views.classedocente import classedocente
from app.views.views import views
from app.models.studenteModel import StudenteModel
from app.models.docenteModel import DocenteModel
from app.models.Attivita import Attivita
import os

# Crea l'applicazione Flask
app = Flask(__name__, template_folder='app/templates', static_folder="public")  # Imposta il percorso dei template
app.register_blueprint(classedocente, url_prefix='/')  # Usa '/' o un altro prefisso a tua scelta
app.register_blueprint(inserimentostudente, url_prefix='/inserimentostudente')  # Il prefisso '/' è opzionale, puoi scegliere uno diverso
app.register_blueprint(views, url_prefix='/')  # Il prefisso '/' è opzionale, puoi scegliere uno diverso

# Imposta la secret key (generata in modo sicuro)
app.secret_key=os.urandom(32).hex()

app.register_blueprint(dashboard_bp)
app.register_blueprint(dashboardDocente_bp)
# Definisci una route per la homepage
@app.route('/')
@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))

    else:
        logged_in = 'email' in session
        email = session.get('email')
        if email is None or email == '':
            # Se l'email non è presente nella sessione, reindirizza al login
            return redirect(url_for('login'))

        studenteModel = StudenteModel()
        docenteModel = DocenteModel()
        stud=studenteModel.trova_studente(email)
        doc=docenteModel.trova_docente(email)
        model = Attivita()

        if stud is not None: return render_template('dashboardStudente.html', logged_in=logged_in, storico=model.get_storico(studenteModel.trova_cf_per_email(email)))
        if doc is not None: return render_template('dashboardDocente.html', logged_in=logged_in)

@app.route('/login')
def login():
    return render_template('registrazioneLogin.html')

@app.route('/register')
def register():
    return render_template('registrazioneLogin.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

app.register_blueprint(login_bp)
app.register_blueprint(registrazione_bp)


# Avvio del server
if __name__ == "__main__":
    app.run(debug=True)
