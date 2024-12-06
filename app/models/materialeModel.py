import os
import re
from bson import ObjectId
from flask import flash, redirect, url_for, send_file, abort, session
from app.controllers.MaterialeControl import MaterialeControl
import uuid

MAX_FILE_SIZE_MB = 2
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'jpeg', 'png', 'txt', 'jpg', 'mp4'}


class MaterialeModel:
    def __init__(self, db_manager):
        self.control = MaterialeControl(db_manager)
        self.upload_folder = None

    def set_upload_folder(self, folder_path):
        self.upload_folder = folder_path

    def is_title_valid(self, title):
        return bool(re.match(r'^[A-Za-z0-9 ]{2,20}$', title))

    def is_description_valid(self, description):
        return 2 <= len(description) <= 255

    def is_file_type_valid(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def is_file_size_valid(self, file):
        return file.content_length <= MAX_FILE_SIZE_MB * 1024 * 1024

    def carica_materiale(self, request):
        """Gestisce il caricamento del materiale didattico."""
        titolo = request.form['titolo']
        descrizione = request.form['descrizione']
        tipo = request.form['tipo']
        file = request.files['file']
        ID_Classe = session.get('ID_Classe')

        if not self.is_title_valid(titolo):
            flash("Il titolo non è valido. Deve essere tra 2 e 20 caratteri e contenere solo lettere e numeri.",
                  "error")
            return redirect(request.url)

        if not self.is_description_valid(descrizione):
            flash("La descrizione deve avere una lunghezza tra i 2 e i 255 caratteri.", "error")
            return redirect(request.url)

        if not self.is_file_type_valid(file.filename):
            flash("Il tipo di file non è valido. Ammessi: docx, pdf, jpeg, png, txt, jpg, mp4.", "error")
            return redirect(request.url)

        file_extension = file.filename.rsplit('.', 1)[1].lower()
        if tipo != file_extension:
            flash("Il tipo di file selezionato non corrisponde all'estensione del file. Seleziona il tipo corretto.",
                  "error")
            return redirect(request.url)

        if not self.is_file_size_valid(file):
            flash(f"La dimensione del file non deve superare i {MAX_FILE_SIZE_MB} MB.", "error")
            return redirect(request.url)

        # Ottieni il percorso completo e crea la directory se non esiste
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

        filepath = file.filename
        file.save(os.path.join(self.upload_folder, filepath))

        id_MaterialeDidattico = uuid.uuid4().hex

        nuovo_materiale = {
            "ID_Materiale": id_MaterialeDidattico,
            "Titolo": titolo,
            "Descrizione": descrizione,
            "File_Path": filepath,
            "Tipo": tipo,
            "ID_Classe": ID_Classe
        }
        self.control.upload_material(nuovo_materiale)
        flash("Materiale caricato con successo!", "materiale_success")
        return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    def modifica_materiale(self, materiale_id, request):
        try:
            material_id_obj = ObjectId(materiale_id)
        except Exception:
            flash("ID del materiale non valido.", "error")
            print("Debug: ID del materiale non valido.")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        materiale = self.control.get_material_by_id(material_id_obj)
        if materiale is None:
            flash("Errore: Materiale non trovato.", "error")
            print(f"Debug: Nessun materiale trovato con ID: {material_id_obj}")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        if request.method == 'POST':
            titolo = request.form.get('titolo', '')
            descrizione = request.form.get('descrizione', '')

            if not self.is_title_valid(titolo):
                flash("Il titolo non è valido. Deve essere tra 2 e 20 caratteri e contenere solo lettere e numeri.",
                      "error")
                return redirect(request.url)

            if not self.is_description_valid(descrizione):
                flash("La descrizione deve avere una lunghezza tra i 2 e i 255 caratteri.", "error")
                return redirect(request.url)

            file = request.files.get('file', None)
            if file:
                if not self.is_file_type_valid(file.filename):
                    flash("Il tipo di file non è valido. Ammessi: docx, pdf, jpeg, png, txt, jpg, mp4.", "error")
                    return redirect(request.url)

                if not self.is_file_size_valid(file):
                    flash(f"La dimensione del file non deve superare i {MAX_FILE_SIZE_MB} MB.", "error")
                    return redirect(request.url)

                filepath = file.filename
                file.save(os.path.join(self.upload_folder, filepath))
                materiale['File_Path'] = filepath

            updated_data = {
                "Titolo": titolo,
                "Descrizione": descrizione,
                "File_Path": materiale.get('File_Path')
            }

            print(f"Debug: Modifica del materiale con ID: {material_id_obj} con i dati aggiornati: {updated_data}")
            self.control.edit_material(material_id_obj, updated_data)
            flash("Materiale modificato con successo!", "materiale_success")
            print("Debug: Materiale modificato con successo.")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    def rimuovi_materiale(self, materiale_id):
        """Gestisce la rimozione di un materiale didattico."""
        try:
            material_id_obj = ObjectId(materiale_id)
        except Exception as e:
            flash("ID del materiale non valido: " + str(e), "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        materiale = self.control.view_material({"_id": material_id_obj})

        if materiale is None:
            flash("Materiale non trovato.", "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        # Prova ad eliminare il materiale
        delete_success = self.control.delete_material(material_id_obj)

        if not delete_success:
            flash("Errore durante la rimozione del materiale dal database.", "error")
            return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

        file_path = materiale.get('File_Path')
        if file_path:
            full_file_path = os.path.join(self.upload_folder, file_path)
            if os.path.exists(full_file_path):
                try:
                    os.remove(full_file_path)
                    flash("Materiale rimosso con successo!", "success")
                except OSError as e:
                    flash(f"Errore durante l'eliminazione del file: {e}", "error")
            else:
                flash("File non trovato, ma materiale rimosso dal database.", "warning")

        return redirect(url_for('MaterialeDocente.visualizza_materiale_docente'))

    def visualizza_materiali(self, id_classe):
        """Recupera e visualizza i materiali per una specifica classe."""
        materiali = self.control.get_materials_by_id(id_classe)
        return materiali

    def serve_file(self, filename):
        """Serve un file dal filesystem."""
        filepath = os.path.join(self.upload_folder, filename)
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            abort(404)