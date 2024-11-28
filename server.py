from flask import Flask, render_template

from app.views.dasboardDocente import dashboardDocente_bp
from app.views.dasboardStudente import dashboard_bp
from app.views.inserimentostudente import inserimentostudente
from app.views.classedocente import classedocente
from app.views.views import views
# Crea l'applicazione Flask
app = Flask(__name__, template_folder='app/templates', static_folder="public")  # Imposta il percorso dei template
app.register_blueprint(classedocente, url_prefix='/')  # Usa '/' o un altro prefisso a tua scelta
app.register_blueprint(inserimentostudente, url_prefix='/inserimentostudente')  # Il prefisso '/' è opzionale, puoi scegliere uno diverso
app.register_blueprint(views, url_prefix='/')  # Il prefisso '/' è opzionale, puoi scegliere uno diverso
app.register_blueprint(dashboard_bp)
app.register_blueprint(dashboardDocente_bp)
# Definisci una route per la homepage




# Avvio del server
if __name__ == "__main__":
    app.run(debug=True)
