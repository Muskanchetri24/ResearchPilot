from app.ingestion.semantic_scholar import search_papers, BASE_URL


def test_semantic_scholar_base_url():
    assert "semanticscholar.org" in BASE_URL
    assert callable(search_papers)
