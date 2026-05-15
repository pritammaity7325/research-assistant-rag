import arxiv
import time


def fetch_paper(paper_title: str):

    try:
        # Exact title search
        exact_query = f'ti:"{paper_title}"'

        search = arxiv.Search(
            query=exact_query,
            max_results=1,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = list(search.results())

        # Fallback search
        if not results:

            time.sleep(1)

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

    except Exception as e:
        print(f"Error fetching paper: {e}")
        return None


def fetch_related_papers(topic: str, max_results=2):

    papers = []

    try:
        time.sleep(1)

        search = arxiv.Search(
            query=topic,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        for r in search.results():

            papers.append({
                "title": r.title,
                "summary": r.summary,
                "pdf_url": r.pdf_url
            })

    except Exception as e:
        print(f"Error fetching related papers: {e}")

    return papers