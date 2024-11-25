from flask import Flask, render_template

# Crea l'applicazione Flask
app = Flask(__name__, template_folder='app/templates', static_folder='app/public')


# Definisci una route per la homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('header.html')

# Avvio del server
if __name__ == "__main__":
    app.run(debug=True)
