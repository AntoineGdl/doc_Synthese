from document_reader import DocumentReader
from api_client import ChatGPTClient


class DocumentAssistant:
    def __init__(self):
        self.reader = DocumentReader()
        self.api_client = ChatGPTClient()

    def process_document(self, file_path):
        """Lit un document et renvoie son contenu"""
        try:
            # Lecture du document
            document_text = self.reader.read_document(file_path)
            return document_text
        except Exception as e:
            raise Exception(f"Erreur lors de la lecture du document: {str(e)}")

    def answer_question(self, document_text, question):
        """Génère une réponse à une question basée sur le contenu du document"""
        try:
            # Génération de la réponse via l'API
            answer = self.api_client.generate_answer(document_text, question)
            return answer
        except Exception as e:
            return f"Erreur lors de la génération de la réponse: {str(e)}"