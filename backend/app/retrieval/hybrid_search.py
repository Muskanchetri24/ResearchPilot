import math
from typing import List, Dict, Any
from app.models.schemas import DocumentSource
from app.retrieval.vector_store import VectorStoreService


class TriSignalHybridRetriever:
    """
    Tri-Signal Hybrid Search combining:
    1. Dense Vector Similarity (Semantic context)
    2. BM25 Lexical Matching (Keywords, model names, acronyms)
    3. Citation & Recency Weighting (Literature impact & freshness)
    """

    def __init__(self):
        self.vector_store = VectorStoreService()

    def calculate_bm25_score(self, query: str, document_text: str) -> float:
        query_terms = set(query.lower().split())
        doc_terms = document_text.lower().split()
        if not doc_terms:
            return 0.0

        matches = sum(1 for term in query_terms if term in doc_terms)
        tf = matches / len(doc_terms)
        return min(tf * 10.0, 1.0)

    def calculate_citation_recency_score(self, citation_count: int, year: int) -> float:
        citation_factor = math.log10(max(citation_count, 1) + 1) / 4.0  # Normalized ~0..1
        recency_factor = max(0.0, (year - 2015) / 11.0)  # Normalized ~0..1 for 2015-2026
        return 0.6 * citation_factor + 0.4 * recency_factor

    async def search(
        self, query: str, top_k: int = 5, dense_weight: float = 0.5, bm25_weight: float = 0.3, citation_weight: float = 0.2
    ) -> List[DocumentSource]:
        # 1. Retrieve candidates from dense vector store
        candidates = await self.vector_store.search(query, top_k=top_k * 2)

        results = []
        for candidate in candidates:
            # Dense score
            dense_score = candidate.score

            # BM25 score
            bm25_score = self.calculate_bm25_score(query, candidate.content)

            # Citation & Recency score
            citation_count = candidate.metadata.get("citation_count", candidate.metadata.get("citations", 10))
            year = candidate.metadata.get("year", 2023)
            citation_score = self.calculate_citation_recency_score(citation_count, year)

            # Tri-signal weighted hybrid score
            final_score = (dense_weight * dense_score) + (bm25_weight * bm25_score) + (citation_weight * citation_score)

            results.append(
                DocumentSource(
                    id=candidate.id,
                    title=candidate.title,
                    content=candidate.content,
                    score=round(final_score, 4),
                    metadata={
                        **candidate.metadata,
                        "dense_score": round(dense_score, 4),
                        "bm25_score": round(bm25_score, 4),
                        "citation_score": round(citation_score, 4),
                    },
                )
            )

        # Sort descending by final combined score
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]


hybrid_retriever = TriSignalHybridRetriever()
