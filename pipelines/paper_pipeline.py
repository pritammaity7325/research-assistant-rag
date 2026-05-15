from services.arxiv_service import fetch_paper
from utils.pdf_loader import load_pdf_text
from utils.text_splitter import split_text
from rag.vector_store import VectorStore

def process_paper(paper_title):
    paper = fetch_paper(paper_title)
    if not paper:
        return None

    full_text = load_pdf_text(paper["pdf_url"])
    chunks = split_text(full_text)

    vector_store = VectorStore()
    vector_store.build(chunks)

    return paper, vector_store
