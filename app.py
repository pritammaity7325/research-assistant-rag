import streamlit as st
from pipelines.paper_pipeline import process_paper
from pipelines.query_pipeline import answer_with_rag
from services.arxiv_service import fetch_related_papers

st.set_page_config(
    page_title="Research Paper Assistant",
    layout="wide"
)

st.title("📚 Research Paper Assistant (RAG + Gemini)")

# Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "main_store" not in st.session_state:
    st.session_state.main_store = None

if "paper_loaded" not in st.session_state:
    st.session_state.paper_loaded = False

# Input
paper_title = st.text_input(
    "Enter paper title",
    placeholder="Attention Is All You Need"
)

# Fetch Paper Button
if st.button("Fetch Paper"):

    if not paper_title.strip():
        st.warning("Please enter a paper title.")

    else:
        try:
            with st.spinner("Fetching and processing paper..."):

                result = process_paper(paper_title)

                if result is None:
                    st.error("Could not fetch paper from arXiv.")

                else:
                    paper, store = result

                    st.session_state.main_store = store
                    st.session_state.paper_loaded = True

                    st.subheader("🔹 Paper Information")

                    st.write(
                        "**1. Authors:**",
                        ", ".join(paper["authors"])
                    )

                    st.write(
                        "**2. Topic:**",
                        paper["title"]
                    )

                    st.write(
                        "**3. One-liner:**",
                        paper["summary"][:200]
                    )

                    st.write(
                        "**4. Summary:**",
                        paper["summary"]
                    )

                    # Related Papers
                    st.subheader("📄 Related Papers")

                    try:
                        related = fetch_related_papers(
                            paper["title"]
                        )

                        if related:

                            for idx, r in enumerate(related, start=1):

                                st.markdown(
                                    f"**{idx}. {r['title']}**"
                                )

                                st.write(
                                    r["summary"][:250] + "..."
                                )

                                st.markdown(
                                    f"[Open PDF]({r['pdf_url']})"
                                )

                                st.divider()

                        else:
                            st.warning(
                                "No related papers found."
                            )

                    except Exception as arxiv_error:
                        st.error(
                            "Failed to fetch related papers from arXiv."
                        )
                        print(arxiv_error)

        except Exception as e:
            st.error("Error processing paper.")
            print(e)

# Question Input
question = st.text_input(
    "Ask a follow-up question",
    placeholder="What is the main contribution of this paper?"
)

# Ask Button
if st.button("Ask"):

    if not question.strip():
        st.warning("Please enter a question.")

    elif not st.session_state.paper_loaded:
        st.warning("Please fetch a paper first.")

    else:
        st.session_state.chat_history.append(
            ("User", question)
        )

        try:
            answer = answer_with_rag(
                question,
                st.session_state.main_store,
                "Main Paper"
            )

        except Exception as e:
            answer = "Error generating answer."
            print(e)

        st.session_state.chat_history.append(
            ("Assistant", answer)
        )

# Chat Display
if st.session_state.chat_history:

    st.subheader("💬 Chat History")

    for role, msg in st.session_state.chat_history:

        if role == "User":
            st.markdown(f"🧑 **User:** {msg}")

        else:
            st.markdown(f"🤖 **Assistant:** {msg}")