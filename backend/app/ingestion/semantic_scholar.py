import os
import requests

BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"


def search_papers(query: str, limit: int = 20, api_key: str = None):
    params = {
        "query": query,
        "limit": limit,
        "fields": (
            "paperId,"
            "title,"
            "abstract,"
            "year,"
            "authors,"
            "venue,"
            "citationCount,"
            "url"
        )
    }

    headers = {
        "User-Agent": "ResearchPilot/1.0 (contact: admin@researchpilot.dev)",
        "Accept": "application/json"
    }

    key = api_key or os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    if key:
        headers["x-api-key"] = key

    response = requests.get(BASE_URL, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    return data.get("data", [])