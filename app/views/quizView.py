from flask import jsonify, render_template


class QuizView:
    @staticmethod
    def mostra_crea_quiz(id_classe):
        """
        Mostra la pagina di creazione quiz.
        """
        return render_template("creaQuiz.html", id_classe=id_classe)

    @staticmethod
    def mostra_domande_generate(domande):
        """
        Mostra le domande generate in formato JSON.
        """
        return jsonify(domande)

    @staticmethod
    def mostra_messaggio(messaggio):
        """
        Mostra un messaggio di successo o errore in formato JSON.
        """
        return jsonify({"message": messaggio})

    @staticmethod
    def mostra_errore(errore, status=500):
        """
        Mostra un messaggio di errore in formato JSON con un codice HTTP personalizzato.
        """
        return jsonify({"error": errore}), status

    @staticmethod
    def mostra_quiz(quiz, domande, tempo_rimanente):
        """
        Mostra un quiz e le sue domande.
        """
        return render_template("quiz.html", quiz=quiz, questions=domande, tempo_rimanente=tempo_rimanente)

    @staticmethod
    def mostra_quiz_precedenti(quiz_list, id_classe):
        """
        Mostra la lista dei quiz precedenti.
        """
        return render_template("quizPrecedenti.html", quiz_list=quiz_list, id_classe=id_classe)

    @staticmethod
    def mostra_domande_quiz(quiz, domande):
        """
        Mostra le domande di un quiz selezionato.
        """
        return render_template("domandeQuizPrecedenti.html", quiz=quiz, domande=domande)

    @staticmethod
    def mostra_risultati_quiz(risultati, quiz_id):
        """
        Mostra i risultati degli studenti per un quiz specifico.
        """
        return render_template("risultatiQuizPrecedenti.html", risultati=risultati, quiz_id=quiz_id)

    @staticmethod
    def mostra_ultimo_quiz(quiz):
        """
        Mostra l'ultimo quiz disponibile per una classe.
        """
        return render_template("quizDisponibile.html", quiz=quiz)

    @staticmethod
    def mostra_errore(messaggio, codice_http=403):
        """
        Mostra un messaggio di errore con un codice HTTP.
        """
        return render_template("errore.html", messaggio=messaggio), codice_http
