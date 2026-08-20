import os
import logging
from typing import List, Dict, Any, Optional
import requests
from app.core.config import settings

logger = logging.getLogger(__name__)


class SemanticScholarClient:
    """
    Client for interacting with the Semantic Scholar Academic Graph API.
    Provides methods for querying academic literature, retrieving paper metadata,
    authors, citations, references, and open-access PDF links.
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    DEFAULT_PAPER_FIELDS = [
        "paperId",
        "title",
        "abstract",
        "year",
        "citationCount",
        "referenceCount",
        "authors",
        "venue",
        "publicationTypes",
        "openAccessPdf",
        "externalIds",
        "url",
    ]

    def __init__(self, api_key: Optional[str] = None, timeout: int = 10):
        self.api_key = api_key or getattr(settings, "SEMANTIC_SCHOLAR_API_KEY", "") or os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
        self.timeout = timeout
        self.session = requests.Session()
        
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        self.session.headers.update(headers)

    def search_papers(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for academic papers matching a text query keyword or topic.

        :param query: Free text search query (e.g. 'retrieval augmented generation')
        :param limit: Maximum number of results to return (default 10, max 100)
        :param offset: Pagination offset
        :param fields: List of paper fields to request from S2 API
        :return: List of paper metadata dictionaries
        """
        if not query.strip():
            return []

        selected_fields = fields or self.DEFAULT_PAPER_FIELDS
        url = f"{self.BASE_URL}/paper/search"
        params = {
            "query": query,
            "limit": min(limit, 100),
            "offset": offset,
            "fields": ",".join(selected_fields),
        }

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Semantic Scholar search_papers API error for query '{query}': {str(e)}")
            return []

    def get_paper_details(
        self,
        paper_id: str,
        fields: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve detailed metadata for a specific paper.

        :param paper_id: Paper identifier (S2 Paper ID, DOI:10.xxx/xxx, arXiv:2005.11401, or CorpusId:xxxx)
        :param fields: List of paper fields to request
        :return: Paper metadata dictionary or None if not found
        """
        selected_fields = fields or self.DEFAULT_PAPER_FIELDS
        url = f"{self.BASE_URL}/paper/{paper_id}"
        params = {"fields": ",".join(selected_fields)}

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Semantic Scholar get_paper_details error for ID '{paper_id}': {str(e)}")
            return None

    def get_paper_citations(
        self,
        paper_id: str,
        limit: int = 10,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get papers that cite the specified paper.
        """
        selected_fields = fields or ["paperId", "title", "year", "authors", "citationCount"]
        url = f"{self.BASE_URL}/paper/{paper_id}/citations"
        params = {
            "limit": min(limit, 100),
            "fields": ",".join([f"citingPaper.{f}" for f in selected_fields]),
        }

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return [item.get("citingPaper") for item in data.get("data", []) if item.get("citingPaper")]
        except requests.exceptions.RequestException as e:
            logger.error(f"Semantic Scholar get_paper_citations error for ID '{paper_id}': {str(e)}")
            return []


# Convenient default instance
semantic_scholar_client = SemanticScholarClient()
