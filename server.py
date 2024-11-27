from flask import Flask, render_template, session
import os
from app.controllers.loginControl import login_bp, logout
from app.controllers.registrazioneControl import registrazione_bp


# Crea l'applicazione Flask
app = Flask(__name__, template_folder='app/templates', static_folder='public')

# Imposta la secret key (generata in modo sicuro)
app.secret_key=os.urandom(32).hex()

# Definisci una route per la homepage
@app.route('/')
@app.route('/home')
def home():
    logged_in = 'email' in session
    return render_template('testHome.html', logged_in=logged_in)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('registrazione.html')

@app.route('/logout')
def logout():
    return render_template('logoutprova.html')

app.register_blueprint(login_bp)
app.register_blueprint(registrazione_bp)


# Avvio del server
if __name__ == "__main__":
    app.run(debug=True)
