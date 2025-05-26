# document_storage.py
import os
import uuid
from config import UPLOAD_FOLDER

class DocumentStorage:
    def __init__(self):
        self.storage_dir = os.path.join(UPLOAD_FOLDER, 'processed')
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_document_text(self, text):
        """Sauvegarde le texte du document et retourne un identifiant unique"""
        doc_id = str(uuid.uuid4())
        file_path = os.path.join(self.storage_dir, f"{doc_id}.txt")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)

        return doc_id

    def get_document_text(self, doc_id):
        """Récupère le texte du document à partir de son identifiant"""
        file_path = os.path.join(self.storage_dir, f"{doc_id}.txt")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document introuvable pour l'ID: {doc_id}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def delete_document(self, doc_id):
        """Supprime le document stocké"""
        file_path = os.path.join(self.storage_dir, f"{doc_id}.txt")

        if os.path.exists(file_path):
            os.remove(file_path)