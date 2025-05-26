import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from summarizer import DocumentAssistant
from config import SECRET_KEY, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from document_storage import DocumentStorage


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

document_storage = DocumentStorage()
# Créer le dossier uploads s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('Aucun fichier sélectionné')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Extraire le contenu du document
        assistant = DocumentAssistant()
        try:
            document_text = assistant.process_document(filepath)
            doc_id = document_storage.save_document_text(document_text)
            session['document_id'] = doc_id
            session['filename'] = filename
            return redirect(url_for('question_form'))
        except Exception as e:
            flash(f"Erreur lors de l'analyse: {str(e)}")
            return redirect(url_for('index'))
    else:
        flash('Format de fichier non supporté')
        return redirect(request.url)


@app.route('/question')
def question_form():
    if 'document_id' not in session or 'filename' not in session:
        flash('Aucun document chargé')
        return redirect(url_for('index'))

    return render_template('question.html', filename=session['filename'])


@app.route('/answer', methods=['POST'])
def answer():
    if 'document_id' not in session:
        flash('Aucun document chargé')
        return redirect(url_for('index'))

    question = request.form.get('question', '')
    if not question:
        flash('Veuillez saisir une question')
        return redirect(url_for('question_form'))

    # Récupérer le texte du document depuis le stockage
    try:
        document_text = document_storage.get_document_text(session['document_id'])
        assistant = DocumentAssistant()
        answer = assistant.answer_question(document_text, question)

        return render_template('answer.html',
                               question=question,
                               answer=answer,
                               filename=session['filename'])
    except Exception as e:
        flash(f"Erreur: {str(e)}")
        return redirect(url_for('index'))


@app.template_filter('nl2br')
def nl2br_filter(text):
    if not text:
        return ""
    return text.replace('\n', '<br>')


if __name__ == '__main__':
    app.run(debug=True, port=5001)