import os
import PyPDF2
import docx
import fitz  # PyMuPDF

class DocumentReader:
    def __init__(self):
        self.supported_formats = {
            '.pdf': self.read_pdf,
            '.docx': self.read_docx,
            '.txt': self.read_txt
        }

    def read_document(self, file_path):
        """Lit un document selon son extension"""
        _, extension = os.path.splitext(file_path)

        if extension.lower() not in self.supported_formats:
            raise ValueError(f"Format non supporté: {extension}")

        return self.supported_formats[extension.lower()](file_path)

    def read_pdf(self, file_path):
        """Extrait le texte d'un fichier PDF en utilisant PyPDF2"""
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text() + "\n"
        return text

    def read_docx(self, file_path):
        """Extrait le texte d'un fichier Word"""
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def read_txt(self, file_path):
        """Lit un fichier texte"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()