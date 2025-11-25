from docx import Document
from PyPDF2 import PdfReader

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PdfReader(file)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif file.name.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""
