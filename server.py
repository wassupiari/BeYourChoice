from flask import Flask

# Crea l'applicazione Flask
app = Flask(__name__)

# Definisci una route per la homepage
@app.route('/')
def home():
    return "Benvenuto nel server Flask!"

# Avvio del server
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)