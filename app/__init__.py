from flask import Flask

app = Flask(__name__)


# Definisci le tue rotte qui
@app.route('/')
def home():
    return "Benvenuto nella tua app Flask!"

# Importa le tue altre componenti qui, se necessario
# from . import altre_componenti