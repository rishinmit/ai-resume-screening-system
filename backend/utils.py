import pdfplumber
from docx import Document
import re


def extract_text_from_pdf(file_path):

    text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text

    return text


def extract_text_from_docx(file_path):

    doc = Document(file_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def extract_text(file_path):

    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        raise ValueError("Unsupported file type")


# -------- Candidate Info Extraction --------

def extract_email(text):

    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

    return match.group(0) if match else "Not found"


def extract_phone(text):

    match = re.search(r"\+?\d[\d\s-]{8,}\d", text)

    return match.group(0) if match else "Not found"


def extract_name(text):

    lines = text.split("\n")

    for line in lines[:5]:

        if len(line.split()) <= 4 and line.strip():
            return line.strip()

    return "Unknown"