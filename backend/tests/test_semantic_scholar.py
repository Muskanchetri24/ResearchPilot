from unittest.mock import MagicMock, patch
from app.ingestion.semantic_scholar import SemanticScholarClient, search_papers



def test_client_initialization():
    client = SemanticScholarClient(api_key="test_key")
    assert client.api_key == "test_key"
    assert client.session.headers.get("x-api-key") == "test_key"


def test_search_papers_empty_query():
    client = SemanticScholarClient()
    results = client.search_papers("  ")
    assert results == []


@patch.object(SemanticScholarClient, "_request")
def test_mock_search_papers(mock_request):
    mock_request.return_value = {
        "data": [
            {"paperId": "p1", "title": "Test Paper 1", "year": 2023},
            {"paperId": "p2", "title": "Test Paper 2", "year": 2024},
        ]
    }
    client = SemanticScholarClient()
    papers = client.search_papers("transformer", limit=2)
    assert len(papers) == 2
    assert papers[0]["paperId"] == "p1"


@patch.object(SemanticScholarClient, "_request")
def test_mock_get_author(mock_request):
    mock_request.return_value = {
        "authorId": "a1",
        "name": "Oren Etzioni",
        "hIndex": 86,
    }
    client = SemanticScholarClient()
    author = client.get_author("a1")
    assert author["name"] == "Oren Etzioni"
    assert author["hIndex"] == 86
