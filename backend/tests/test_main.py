def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


def test_research_query(client):
    payload = {
        "query": "transformer architectures",
        "top_k": 2
    }
    response = client.post("/api/v1/research/query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0


def test_document_ingest(client):
    payload = {
        "title": "Test Paper",
        "content": "This is a test paper content for testing ingestion pipeline."
    }
    response = client.post("/api/v1/research/ingest", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "document_id" in data
    assert data["status"] == "processed"
