from flask import Blueprint, render_template, request, redirect, url_for, session
from app.controllers.classeVirtualeControl import ClasseVirtualeControl
from app.controllers.loginControl import teacher_required
from app.models.studenteModel import StudenteModel
from app.models.docenteModel import DocenteModel

creazioneclasse = Blueprint('creazioneclasse', __name__)

# Inizializza il controller della classe virtuale
classe_control = ClasseVirtualeControl()


@creazioneclasse.route('creazione-classe', methods=['GET', 'POST'])
def creazione_classe():
    if request.method == 'POST':
        codice_univoco_docent = session.get("CU")

        nome_classe = request.form['nome-classe']
        descrizione = request.form['descrizione']

        try:
            # Crea la classe virtuale
            classe_control.creazione_classe_virtuale(nome_classe, descrizione, codice_univoco_docent)

            # Dopo la creazione, controlla se l'utente è uno studente o un docente
            # Controlla se l'utente è uno studente
            studente_model = StudenteModel()
            docente_model = DocenteModel()
            stud = studente_model.trova_studente(session.get('email'))
            doc = docente_model.trova_docente(session.get('email'))

            if doc is not None:
                # Se è un docente, reindirizzalo alla dashboard docente
                return redirect(url_for('dashboard.dashboard_docente'))
            else:
                # Se non è né studente né docente, reindirizza alla home o login
                return redirect(url_for('home'))
        except Exception as e:
            return render_template('creazioneCV.html', error=str(e))

    return render_template('creazioneCV.html')

