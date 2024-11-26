from flask import Flask, render_template
from app.views import views  # Importa il blueprint dal modulo 'views'

# Crea l'applicazione Flask
app = Flask(__name__, template_folder='app/templates', static_folder='public')
app.register_blueprint(views, url_prefix='/')  # Il prefisso '/' è opzionale, puoi scegliere uno diverso


# Definisci una route per la homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('creazioneCV.html')


# Avvio del server
if __name__ == "__main__":
    app.run(debug=True)
