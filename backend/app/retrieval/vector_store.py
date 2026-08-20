from typing import List
from app.models.schemas import DocumentSource


class VectorStoreService:
    """
    Interface for vector store interaction (Chroma / Pinecone / Qdrant).
    """

    def __init__(self, store_path: str = "./data/processed/vector_db"):
        self.store_path = store_path

    async def search(self, query: str, top_k: int = 5) -> List[DocumentSource]:
        # Placeholder mock search returning structured document sources
        sample_results = [
            DocumentSource(
                id="doc-1",
                title="Attention Is All You Need",
                content="The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
                score=0.94,
                metadata={"authors": "Vaswani et al.", "year": 2017}
            ),
            DocumentSource(
                id="doc-2",
                title="Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
                content="Large language models can store factual knowledge in parameter weights, but their ability to access external memory improves accuracy...",
                score=0.89,
                metadata={"authors": "Lewis et al.", "year": 2020}
            )
        ]
        return sample_results[:top_k]
