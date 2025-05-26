import openai
from config import OPENAI_API_KEY

import tiktoken


class ChatGPTClient:
    def __init__(self, api_key=OPENAI_API_KEY):
        self.api_key = api_key
        openai.api_key = api_key
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def num_tokens(self, text):
        """Estime le nombre de tokens dans un texte"""
        return len(self.encoding.encode(text))

    def call_api(self, prompt, max_tokens=500):
        """
        Appelle l'API OpenAI pour obtenir une réponse à partir d'un prompt
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Vous êtes un assistant utile qui répond à des questions sur des documents."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erreur lors de l'appel à l'API: {str(e)}")
            return f"Je n'ai pas pu traiter cette requête en raison d'une erreur: {str(e)}"

    def generate_answer(self, text, question):
        """
        Génère une réponse à une question basée sur le texte fourni
        """
        return self.answer_question(text, question)

    def summarize_text(self, text):
        """
        Génère une synthèse du texte fourni en gérant les documents longs
        """
        # Calcul des tokens disponibles
        system_prompt_tokens = self.num_tokens(
            "Vous êtes un assistant utile qui répond à des questions sur des documents.") + 100
        summarize_instruction_tokens = self.num_tokens(
            "Voici un texte, merci de le synthétiser en conservant les informations importantes:")

        # Tokens disponibles pour le texte
        max_text_tokens = 16385 - system_prompt_tokens - summarize_instruction_tokens - 1000  # 1000 pour la réponse

        if self.num_tokens(text) <= max_text_tokens:
            # Si le texte est court, on utilise l'approche standard
            prompt = f"Voici un texte, merci de le synthétiser en conservant les informations importantes:\n\n{text}"
            return self.call_api(prompt, max_tokens=1000)
        else:
            # Si le texte est trop long, on prend seulement une partie du texte
            sections = self.split_text(text, max_text_tokens // 4)  # Diviser en sections plus petites

            # Ne traiter que la première section pour éviter les dépassements
            first_section = sections[0]
            prompt = f"Voici le début d'un document très long, merci de le synthétiser en précisant qu'il s'agit seulement du début:\n\n{first_section}"

            # Réduire max_tokens pour éviter les dépassements
            return self.call_api(prompt, max_tokens=700)

    def answer_question(self, text, question):
        """
        Répond à une question sur le texte fourni en découpant si nécessaire
        """
        # Ajout du système + question aux tokens déjà utilisés
        system_question_tokens = self.num_tokens(
            "Vous êtes un assistant utile qui répond à des questions sur des documents.") + self.num_tokens(
            question) + 100  # marge

        # Tokens disponibles pour le texte
        max_text_tokens = 16385 - system_question_tokens - 800  # 800 pour la réponse

        if self.num_tokens(text) <= max_text_tokens:
            # Si le texte est court, on utilise l'approche standard
            prompt = f"Texte: {text}\n\nQuestion: {question}\n\nRéponse:"
            return self.call_api(prompt, max_tokens=800)
        else:
            # Si le texte est trop long, on prend seulement une partie du texte
            sections = self.split_text(text, max_text_tokens // 4)  # Diviser en sections plus petites

            # Ne traiter que la première section pour éviter les dépassements
            first_section = sections[0]
            prompt = f"Voici un extrait du document (le début seulement): {first_section}\n\nQuestion: {question}\n\nRéponse en précisant que vous n'avez accès qu'à une partie du document:"
            return self.call_api(prompt, max_tokens=700)

    def answer_question(self, text, question):
        """
        Répond à une question sur le texte fourni en découpant si nécessaire
        """
        # Ajout du système + question aux tokens déjà utilisés
        system_question_tokens = self.num_tokens(
            "Vous êtes un assistant utile qui répond à des questions sur des documents.") + self.num_tokens(
            question) + 100

        max_text_tokens = 16385 - system_question_tokens - 700  # 700 pour la réponse

        if self.num_tokens(text) <= max_text_tokens:
            prompt = f"Texte: {text}\n\nQuestion: {question}\n\nRéponse:"
            return self.call_api(prompt, max_tokens=700)
        else:
            reduced_max_tokens = max_text_tokens // 2
            truncated_text = text[:10000]

            while self.num_tokens(truncated_text) > reduced_max_tokens and len(truncated_text) > 1000:
                truncated_text = truncated_text[:len(truncated_text) // 2]

            prompt = f"Voici le début d'un document très long (le texte est tronqué): \n\n{truncated_text}\n\nQuestion: {question}\n\nRéponse en précisant clairement que vous n'avez accès qu'au début du document:"
            return self.call_api(prompt, max_tokens=600)

    def split_text(self, text, max_tokens_per_section):
        """Divise le texte en sections plus petites"""
        paragraphs = text.split("\n\n")
        sections = []
        current_section = ""

        for para in paragraphs:
            if self.num_tokens(current_section + para) > max_tokens_per_section:
                if current_section:
                    sections.append(current_section)
                current_section = para
            else:
                current_section += "\n\n" + para if current_section else para

        if current_section:
            sections.append(current_section)

        return sections