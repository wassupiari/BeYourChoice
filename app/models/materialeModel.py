import os
import re
from bson import ObjectId
from flask import flash, redirect, url_for, send_file, abort, session
from app.controllers.materialeControl import MaterialeControl
import uuid

MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'jpeg', 'png', 'txt', 'jpg', 'mp4'}


class MaterialeModel:
    def __init__(self, db_manager):
        self.control = MaterialeControl(db_manager)
        self.cartella_uploads = None

    def set_cartella_uploads(self, path_cartella):
        self.cartella_uploads = path_cartella

    def titolo_valido(self, titolo):
        return bool(re.match(r'^[A-Za-z0-9 ]{2,20}$', titolo))

    def descrizione_valida(self, descrizione):
        return bool(re.match(r'^[^§]{2,255}$', descrizione))

    def tipo_file_valido(self, nomefile):
        return '.' in nomefile and nomefile.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def grandezza_file_valido(self, file):
        return file.content_length <= MAX_FILE_SIZE_MB * 1024 * 1024

    def carica_materiale(self, request):
        """Gestisce il caricamento del materiale didattico."""
        titolo = request.form['titolo']
        descrizione = request.form['descrizione']
        tipo = request.form['tipo']
        file = request.files['file']
        ID_Classe = session.get('ID_Classe')

        if not self.titolo_valido(titolo):
            flash("Il titolo non è valido. Deve essere tra 2 e 20 caratteri e contenere solo lettere e numeri.",
                  "error")
            return redirect(request.url)

        if not self.descrizione_valida(descrizione):
            flash("La descrizione deve avere una lunghezza tra i 2 e i 255 caratteri.", "error")
            return redirect(request.url)

        if not self.tipo_file_valido(file.filename):
            flash("Il tipo di file non è valido. Ammessi: docx, pdf, jpeg, png, txt, jpg, mp4.", "error")
            return redirect(request.url)

        file_extension = file.filename.rsplit('.', 1)[1].lower()
        if tipo != file_extension:
            flash("Il tipo di file selezionato non corrisponde all'estensione del file. Seleziona il tipo corretto.",
                  "error")
            return redirect(request.url)

        if not self.grandezza_file_valido(file):
            flash(f"La dimensione del file non deve superare i {MAX_FILE_SIZE_MB} MB.", "error")
            return redirect(request.url)

        # Ottieni il percorso completo e crea la directory se non esiste
        if not os.path.exists(self.cartella_uploads):
            os.makedirs(self.cartella_uploads)

        filepath = file.filename
        file.save(os.path.join(self.cartella_uploads, filepath))

        id_MaterialeDidattico = uuid.uuid4().hex

        nuovo_materiale = {
            "ID_Materiale": id_MaterialeDidattico,
            "Titolo": titolo,
            "Descrizione": descrizione,
            "File_Path": filepath,
            "Tipo": tipo,
            "ID_Classe": ID_Classe
        }
        self.control.carica_materiali(nuovo_materiale)
        flash("Materiale caricato con successo!", "materiale_success")
        return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    def modifica_materiale(self, materiale_id, request):
        try:
            materiale_id_obj = ObjectId(materiale_id)
        except Exception:
            flash("ID del materiale non valido.", "error")
            print("Debug: ID del materiale non valido.")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        materiale = self.control.get_materiale_tramite_id(materiale_id_obj)
        if materiale is None:
            flash("Errore: Materiale non trovato.", "error")
            print(f"Debug: Nessun materiale trovato con ID: {materiale_id_obj}")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        if request.method == 'POST':
            titolo = request.form.get('titolo', '')
            descrizione = request.form.get('descrizione', '')

            if not self.titolo_valido(titolo):
                flash("Il titolo non è valido. Deve essere tra 2 e 20 caratteri e contenere solo lettere e numeri.",
                      "error")
                return redirect(request.url)

            if not self.descrizione_valida(descrizione):
                flash("La descrizione deve avere una lunghezza tra i 2 e i 255 caratteri.", "error")
                return redirect(request.url)

            file = request.files.get('file', None)
            if file:
                if not self.tipo_file_valido(file.filename):
                    flash("Il tipo di file non è valido. Ammessi: docx, pdf, jpeg, png, txt, jpg, mp4.", "error")
                    return redirect(request.url)

                if not self.grandezza_file_valido(file):
                    flash(f"La dimensione del file non deve superare i {MAX_FILE_SIZE_MB} MB.", "error")
                    return redirect(request.url)

                filepath = file.filename
                file.save(os.path.join(self.cartella_uploads, filepath))
                materiale['File_Path'] = filepath

            dati_caricati = {
                "Titolo": titolo,
                "Descrizione": descrizione,
                "File_Path": materiale.get('File_Path')
            }

            print(f"Debug: Modifica del materiale con ID: {materiale_id_obj} con i dati aggiornati: {dati_caricati}")
            self.control.modifica_materiale(materiale_id_obj, dati_caricati)
            flash("Materiale modificato con successo!", "materiale_success")
            print("Debug: Materiale modificato con successo.")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    def rimuovi_materiale(self, materiale_id):
        """Gestisce la rimozione di un materiale didattico."""
        try:
            materiale_id_obj = ObjectId(materiale_id)
        except Exception as e:
            flash("ID del materiale non valido: " + str(e), "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        materiale = self.control.visualizza_materiale({"_id": materiale_id_obj})

        if materiale is None:
            flash("Materiale non trovato.", "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        # Prova ad eliminare il materiale
        successo_rimozione = self.control.elimina_materiale(materiale_id_obj)

        if not successo_rimozione:
            flash("Errore durante la rimozione del materiale dal database.", "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        file_path = materiale.get('File_Path')
        if file_path:
            full_file_path = os.path.join(self.cartella_uploads, file_path)
            if os.path.exists(full_file_path):
                try:
                    os.remove(full_file_path)
                    flash("Materiale rimosso con successo!", "materiale_success")
                except OSError as e:
                    flash(f"Errore durante l'eliminazione del file: {e}", "error")
            else:
                flash("File non trovato, ma materiale rimosso dal database.", "warning")

        return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    def visualizza_materiali(self, id_classe):
        """Recupera e visualizza i materiali per una specifica classe."""
        materiali = self.control.get_materiali_tramite_id_classe(id_classe)
        return materiali

    def servi_file(self, nomefile):
        """Serve un file dal filesystem."""
        filepath = os.path.join(self.cartella_uploads, nomefile)
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            abort(404)