from flask import Blueprint, request, render_template
from app.controllers.ClasseVirtualeControl import ClasseVirtualeControl

# Crea il blueprint
classDocente = Blueprint('ClasseDocente', __name__, template_folder='../templates')

@classDocente.route('/ClasseDocente')
def ClasseDocente():
    """
    Visualizza gli studenti di una classe specifica.
    """
    # Ottieni i parametri dalla query string
    ID_Classe = int(request.args.get("ID_Classe", 101))

    # Passa i dati al template
    return ClasseVirtualeControl.mostra_classe(ID_Classe)
