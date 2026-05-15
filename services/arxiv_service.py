import arxiv


def fetch_paper(paper_title: str):
    # 1️⃣ Exact title search (highest priority)
    exact_query = f'ti:"{paper_title}"'
    search = arxiv.Search(
        query=exact_query,
        max_results=1,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = list(search.results())

    # 2️⃣ Fallback to normal search if exact not found
    if not results:
        search = arxiv.Search(
            query=paper_title,
            max_results=1,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = list(search.results())

    if not results:
        raise ValueError("No paper found on arXiv")

    paper = results[0]

    return {
        "title": paper.title,
        "authors": [a.name for a in paper.authors],
        "summary": paper.summary,
        "pdf_url": paper.pdf_url
    }



def fetch_related_papers(topic: str, max_results=3):
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = []
    for r in search.results():
        papers.append({
            "title": r.title,
            "summary": r.summary,
            "pdf_url": r.pdf_url
        })
    return papers
