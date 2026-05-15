from services.llm_service import generate
from rag.retriever import format_context

def answer_with_rag(question, vector_store, citation_source):
    chunks = vector_store.query(question)
    context = format_context(chunks)

    prompt = f"""
Answer STRICTLY using the context below.
Quote sentences.
Add citation [{citation_source}].

Context:
{context}

Question:
{question}
"""

    return generate(prompt)
