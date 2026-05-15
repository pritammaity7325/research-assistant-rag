
from utils.pdf_loader import load_pdf_text
from services.arxiv_service import fetch_paper

paper = fetch_paper('Attention Is All You Need')
text = load_pdf_text(paper['pdf_url'])

print(len(text))
print(text[:1000])

