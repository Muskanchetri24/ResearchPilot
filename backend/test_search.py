import requests
from app.ingestion.semantic_scholar import search_papers


def main():
    query = "retrieval augmented generation"
    print(f"🔍 Searching Semantic Scholar for: '{query}'...\n")

    try:
        papers = search_papers(query=query, limit=5)
        print(f"✅ Found {len(papers)} papers:\n")

        for idx, paper in enumerate(papers, 1):
            authors = ", ".join([a.get("name", "") for a in paper.get("authors", []) if a.get("name")])
            print(f"[{idx}] {paper.get('title')}")
            print(f"    Year: {paper.get('year')} | Venue: {paper.get('venue') or 'N/A'} | Citations: {paper.get('citationCount')}")
            print(f"    Authors: {authors or 'N/A'}")
            print(f"    URL: {paper.get('url')}")
            abstract = paper.get('abstract')
            if abstract:
                snippet = abstract[:150] + "..." if len(abstract) > 150 else abstract
                print(f"    Abstract: {snippet}")
            print("-" * 80)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("⚠️ Semantic Scholar API rate limit hit (HTTP 429).")
            print("💡 Tip: Semantic Scholar limits unauthenticated requests. You can add SEMANTIC_SCHOLAR_API_KEY to .env or wait a minute before retrying.")
        else:
            print(f"❌ HTTP Error: {e}")
    except Exception as e:
        print(f"❌ Error executing search: {e}")


if __name__ == "__main__":
    main()
