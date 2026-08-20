import sys
import requests
from app.ingestion.semantic_scholar import SemanticScholarClient, search_papers


def main():
    client = SemanticScholarClient()
    query = "retrieval augmented generation"
    print(f"🔍 Searching Semantic Scholar for: '{query}'...\n")

    try:
        papers = client.search_papers(query=query, limit=5)
        print(f"✅ Successfully retrieved {len(papers)} papers:\n")

        for idx, paper in enumerate(papers, 1):
            authors = ", ".join([a.get("name", "") for a in paper.get("authors", []) if a.get("name")])
            print(f"[{idx}] {paper.get('title')}")
            print(f"    Year: {paper.get('year')} | Venue: {paper.get('venue') or 'N/A'} | Citations: {paper.get('citationCount')}")
            print(f"    Authors: {authors or 'N/A'}")
            print(f"    Paper ID: {paper.get('paperId')}")
            print(f"    URL: {paper.get('url')}")
            abstract = paper.get('abstract')
            if abstract:
                snippet = abstract[:150] + "..." if len(abstract) > 150 else abstract
                print(f"    Abstract: {snippet}")
            print("-" * 80)

    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            print("\n⚠️ Semantic Scholar API unauthenticated rate limit hit (HTTP 429).")
            print("💡 Tip: Semantic Scholar limits free unauthenticated IP requests to ~10 req/min.")
            print("🔑 You can add your SEMANTIC_SCHOLAR_API_KEY to backend/.env for higher rate limits (up to 100 req/sec).")
        else:
            print(f"\n❌ HTTP Error: {e}")
    except Exception as e:
        print(f"\n❌ Error executing search: {e}")


if __name__ == "__main__":
    main()
