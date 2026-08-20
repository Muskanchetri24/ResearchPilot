import os
import time
import logging
from typing import List, Dict, Any, Optional, Union
import requests
from dotenv import load_dotenv

# Ensure environment variables are loaded
load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_PAPER_FIELDS = [
    "paperId",
    "title",
    "abstract",
    "year",
    "authors",
    "venue",
    "citationCount",
    "referenceCount",
    "openAccessPdf",
    "publicationTypes",
    "publicationDate",
    "fieldsOfStudy",
    "url",
]

DEFAULT_AUTHOR_FIELDS = [
    "authorId",
    "name",
    "url",
    "affiliations",
    "paperCount",
    "citationCount",
    "hIndex",
]


class SemanticScholarClient:
    """
    Comprehensive client for the Semantic Scholar Academic Graph API (v1).
    Implements all paper, author, search, bulk, autocomplete, and batch endpoints
    with automatic exponential backoff retries on HTTP 429 rate limits.
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
    ):
        self.api_key = (
            api_key
            or os.getenv("SEMANTIC_SCHOLAR_API_KEY")
            or os.getenv("S2_API_KEY")
            or ""
        )
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = requests.Session()

        headers = {
            "Accept": "application/json",
            "User-Agent": "ResearchPilot/1.0 (Academic Intelligence Assistant)",
        }
        if self.api_key:
            headers["x-api-key"] = self.api_key
        self.session.headers.update(headers)

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = f"{self.BASE_URL}{endpoint}" if not endpoint.startswith("http") else endpoint

        for attempt in range(self.max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_body,
                    timeout=self.timeout,
                )

                if response.status_code == 429 and attempt < self.max_retries - 1:
                    retry_after = response.headers.get("Retry-After")
                    sleep_time = float(retry_after) if retry_after else (self.backoff_factor ** (attempt + 1))
                    logger.warning(f"Rate limited (429) on {endpoint}. Waiting {sleep_time:.1f}s before retry {attempt + 1}/{self.max_retries}...")
                    time.sleep(sleep_time)
                    continue

                response.raise_for_status()
                return response.json()

            except requests.exceptions.HTTPError as e:
                if attempt == self.max_retries - 1 or response.status_code != 429:
                    logger.error(f"Semantic Scholar API HTTP error [{e.response.status_code}] on {endpoint}: {e}")
                    raise
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    logger.error(f"Semantic Scholar API connection error on {endpoint}: {e}")
                    raise
                time.sleep(self.backoff_factor ** (attempt + 1))

        return None

    # --- Paper Endpoints ---

    def search_papers(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
        year: Optional[str] = None,
        venue: Optional[str] = None,
        fields_of_study: Optional[Union[str, List[str]]] = None,
        open_access_pdf: bool = False,
        min_citation_count: Optional[int] = None,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Relevance search for papers matching query string.
        Endpoint: GET /paper/search
        """
        if not query.strip():
            return []

        selected_fields = fields or DEFAULT_PAPER_FIELDS
        params: Dict[str, Any] = {
            "query": query,
            "limit": min(limit, 100),
            "offset": offset,
            "fields": ",".join(selected_fields),
        }
        if year:
            params["year"] = year
        if venue:
            params["venue"] = venue
        if fields_of_study:
            params["fieldsOfStudy"] = fields_of_study if isinstance(fields_of_study, str) else ",".join(fields_of_study)
        if open_access_pdf:
            params["openAccessPdf"] = ""
        if min_citation_count is not None:
            params["minCitationCount"] = str(min_citation_count)

        res = self._request("GET", "/paper/search", params=params)
        return res.get("data", []) if isinstance(res, dict) else []

    def bulk_search_papers(
        self,
        query: str,
        token: Optional[str] = None,
        sort: Optional[str] = None,
        year: Optional[str] = None,
        fields: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Bulk retrieval of basic paper data.
        Endpoint: GET /paper/search/bulk
        """
        selected_fields = fields or ["paperId", "title", "abstract", "year", "venue", "citationCount"]
        params: Dict[str, Any] = {
            "query": query,
            "fields": ",".join(selected_fields),
        }
        if token:
            params["token"] = token
        if sort:
            params["sort"] = sort
        if year:
            params["year"] = year

        res = self._request("GET", "/paper/search/bulk", params=params)
        return res if isinstance(res, dict) else {}

    def match_paper(
        self,
        query: str,
        fields: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Find closest single paper matching a title query.
        Endpoint: GET /paper/search/match
        """
        selected_fields = fields or DEFAULT_PAPER_FIELDS
        params = {
            "query": query,
            "fields": ",".join(selected_fields),
        }
        try:
            return self._request("GET", "/paper/search/match", params=params)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return None
            raise

    def autocomplete_papers(self, query: str) -> List[Dict[str, Any]]:
        """
        Suggest paper query completions.
        Endpoint: GET /paper/autocomplete
        """
        params = {"query": query}
        res = self._request("GET", "/paper/autocomplete", params=params)
        return res.get("matches", []) if isinstance(res, dict) else []

    def get_paper(
        self,
        paper_id: str,
        fields: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch details for a paper by ID (DOI, arXiv, CorpusId, S2 ID).
        Endpoint: GET /paper/{paper_id}
        """
        selected_fields = fields or DEFAULT_PAPER_FIELDS
        params = {"fields": ",".join(selected_fields)}
        try:
            return self._request("GET", f"/paper/{paper_id}", params=params)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return None
            raise

    def get_papers_batch(
        self,
        paper_ids: List[str],
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch details for multiple papers at once (up to 500 IDs).
        Endpoint: POST /paper/batch
        """
        if not paper_ids:
            return []

        selected_fields = fields or DEFAULT_PAPER_FIELDS
        params = {"fields": ",".join(selected_fields)}
        body = {"ids": paper_ids[:500]}

        res = self._request("POST", "/paper/batch", params=params, json_body=body)
        return res if isinstance(res, list) else []

    # --- Author Endpoints ---

    def search_authors(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for authors by name.
        Endpoint: GET /author/search
        """
        selected_fields = fields or DEFAULT_AUTHOR_FIELDS
        params = {
            "query": query,
            "limit": min(limit, 1000),
            "offset": offset,
            "fields": ",".join(selected_fields),
        }
        res = self._request("GET", "/author/search", params=params)
        return res.get("data", []) if isinstance(res, dict) else []

    def get_author(
        self,
        author_id: str,
        fields: Optional[List[str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Get details about an author.
        Endpoint: GET /author/{author_id}
        """
        selected_fields = fields or DEFAULT_AUTHOR_FIELDS
        params = {"fields": ",".join(selected_fields)}
        try:
            return self._request("GET", f"/author/{author_id}", params=params)
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return None
            raise

    def get_authors_batch(
        self,
        author_ids: List[str],
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get details for multiple authors at once (up to 1,000 IDs).
        Endpoint: POST /author/batch
        """
        if not author_ids:
            return []

        selected_fields = fields or DEFAULT_AUTHOR_FIELDS
        params = {"fields": ",".join(selected_fields)}
        body = {"ids": author_ids[:1000]}

        res = self._request("POST", "/author/batch", params=params, json_body=body)
        return res if isinstance(res, list) else []

    def get_author_papers(
        self,
        author_id: str,
        limit: int = 100,
        offset: int = 0,
        fields: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch the papers written by an author.
        Endpoint: GET /author/{author_id}/papers
        """
        selected_fields = fields or ["paperId", "title", "year", "venue", "citationCount", "url"]
        params = {
            "limit": min(limit, 1000),
            "offset": offset,
            "fields": ",".join(selected_fields),
        }
        res = self._request("GET", f"/author/{author_id}/papers", params=params)
        return res.get("data", []) if isinstance(res, dict) else []


# Default client instance
default_client = SemanticScholarClient()


def search_papers(query: str, limit: int = 20, api_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Convenience function matching signature for quick searches.
    """
    client = default_client if not api_key else SemanticScholarClient(api_key=api_key)
    return client.search_papers(query=query, limit=limit)