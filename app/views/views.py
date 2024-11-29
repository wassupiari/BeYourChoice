from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.ClasseVirtualeControl import ClasseVirtualeControl

views = Blueprint('views', __name__)

# Inizializza il controller della classe virtuale
classe_control = ClasseVirtualeControl()


@views.route('creazione-classe', methods=['GET', 'POST'])
def creazione_classe():
    if request.method == 'POST':
        nome_classe = request.form['nome-classe']
        descrizione = request.form['descrizione']
        try:
            classe_control.creazioneClasseVirtuale(nome_classe, descrizione)
            return redirect(url_for('home'))  # Torna alla stessa pagina
        except Exception as e:
            return render_template('creazioneCV.html', error=str(e))
    return render_template('creazioneCV.html')

