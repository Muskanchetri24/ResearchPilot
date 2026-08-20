from app.ingestion.semantic_scholar import SemanticScholarClient


def test_semantic_scholar_client_init():
    client = SemanticScholarClient()
    assert client.BASE_URL == "https://api.semanticscholar.org/graph/v1"
    assert "paperId" in client.DEFAULT_PAPER_FIELDS


def test_search_papers_empty_query():
    client = SemanticScholarClient()
    results = client.search_papers("")
    assert results == []
