from flask import Flask, render_template

from app.views.dasboardDocente import dashboardDocente_bp
from app.views.dasboardStudente import dashboard_bp
# Crea l'applicazione Flask
app = Flask(__name__, template_folder='app/templates', static_folder='public')


# Definisci una route per la homepage


app.register_blueprint(dashboardDocente_bp)
app.register_blueprint(dashboard_bp)

# Avvio del server
if __name__ == "__main__":
    app.run(debug=True)