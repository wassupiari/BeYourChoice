from flask import Blueprint, render_template, request, redirect, url_for, session
from app.controllers.ClasseVirtualeControl import ClasseVirtualeControl
from app.controllers.loginControl import teacher_required
views = Blueprint('views', __name__)

# Inizializza il controller della classe virtuale
classe_control = ClasseVirtualeControl()


@views.route('creazione-classe', methods=['GET', 'POST'])
def creazione_classe():
    if request.method == 'POST':
        codice_univoco_docent = session.get("CU")
        print(codice_univoco_docent)

        nome_classe = request.form['nome-classe']
        descrizione = request.form['descrizione']

        try:
            classe_control.creazioneClasseVirtuale(nome_classe, descrizione,codice_univoco_docent )
            return redirect(url_for('home'))  # Torna alla stessa pagina
        except Exception as e:
            return render_template('creazioneCV.html', error=str(e))
    return render_template('creazioneCV.html')

