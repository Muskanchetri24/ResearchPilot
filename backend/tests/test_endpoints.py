def test_graph_endpoint(client):
    response = client.get("/api/v1/research/graph")
    assert response.status_code == 200
    data = response.json()
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) > 0


def test_trends_endpoint(client):
    response = client.get("/api/v1/research/trends")
    assert response.status_code == 200
    data = response.json()
    assert "publication_velocity" in data
    assert "method_popularity" in data
    assert data["total_papers_analyzed"] > 0


def test_gaps_endpoint(client):
    response = client.get("/api/v1/research/gaps")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "opportunity_score" in data[0]


def test_generate_review_endpoint(client):
    response = client.post("/api/v1/research/generate-review?topic=AI-based+migraine+detection")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "executive_summary" in data
    assert len(data["identified_gaps"]) > 0
