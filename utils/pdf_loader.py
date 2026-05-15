import requests
from pypdf import PdfReader
from io import BytesIO

def load_pdf_text(pdf_url: str) -> str:
    response = requests.get(pdf_url)
    reader = PdfReader(BytesIO(response.content))

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
