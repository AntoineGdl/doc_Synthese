import os

from dotenv import load_dotenv
load_dotenv()


# Configuration de l'API et de l'application
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4"
MAX_TOKENS = 10000000000  # Limite de tokens pour la réponse

# Configuration Flask
SECRET_KEY = "your_secret_key"
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}