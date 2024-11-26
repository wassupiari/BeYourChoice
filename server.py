from flask import Flask, render_template
from app.views.dasboardStudente import dashboard_bp
# Crea l'applicazione Flask
app = Flask(__name__, template_folder='app/templates', static_folder='public')


# Definisci una route per la homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('dashboardDocente.html')

#app.register_blueprint(dashboard_bp)
# Avvio del server
if __name__ == "__main__":
    app.run(debug=True)
