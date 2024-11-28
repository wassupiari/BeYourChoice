from flask import Flask, render_template

# Crea l'applicazione Flask
app = Flask(__name__, template_folder='app/templates', static_folder="public")  # Imposta il percorso dei template
app.register_blueprint(classedocente, url_prefix='/')  # Usa '/' o un altro prefisso a tua scelta
app.register_blueprint(inserimentostudente, url_prefix='/inserimentostudente')  # Il prefisso '/' è opzionale, puoi scegliere uno diverso
app.register_blueprint(views, url_prefix='/')  # Il prefisso '/' è opzionale, puoi scegliere uno diverso



# Definisci una route per la homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('classeDocente.html')


# Avvio del server
if __name__ == "__main__":
    app.run(debug=True)
