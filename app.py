import streamlit as st
from pipelines.paper_pipeline import process_paper
from pipelines.query_pipeline import answer_with_rag
from services.arxiv_service import fetch_related_papers
from rag.vector_store import VectorStore
from utils.pdf_loader import load_pdf_text
from utils.text_splitter import split_text

st.set_page_config(page_title="Research Paper Assistant", layout="wide")

st.title("📚 Research Paper Assistant (RAG + Gemini)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "main_store" not in st.session_state:
    st.session_state.main_store = None

paper_title = st.text_input("Enter paper title")

if st.button("Fetch Paper"):
    paper, store = process_paper(paper_title)
    st.session_state.main_store = store

    st.subheader("🔹 Fixed Outputs")

    st.write("**1. Authors:**", ", ".join(paper["authors"]))
    st.write("**2. Topic:**", paper["title"])
    st.write("**3. One-liner:**", paper["summary"][:200])
    st.write("**4. Summary:**", paper["summary"])
    st.write("**5. Related Papers:**")

    related = fetch_related_papers(paper["title"])
    st.session_state.related_stores = {}

    for r in related:
        st.write("-", r["title"])
        text = load_pdf_text(r["pdf_url"])
        chunks = split_text(text)
        vs = VectorStore()
        vs.build(chunks)
        st.session_state.related_stores[r["title"]] = vs

question = st.text_input("Ask a follow-up question")

if st.button("Ask"):
    st.session_state.chat_history.append(("User", question))

    if st.session_state.main_store:
        answer = answer_with_rag(question, st.session_state.main_store, "Main Paper")
    else:
        answer = "Please load a paper first."

    st.session_state.chat_history.append(("Assistant", answer))

for role, msg in st.session_state.chat_history:
    st.write(f"**{role}:** {msg}")
