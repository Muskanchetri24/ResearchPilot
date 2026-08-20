import uuid
from typing import List, Dict, Any


class PDFIngestionPipeline:
    """
    Ingestion pipeline responsible for parsing raw PDF files,
    cleaning extracted text, and creating chunk embeddings.
    """

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = " ".join(words[i:i + self.chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks if chunks else [text]

    def process_document(self, title: str, raw_text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        doc_id = str(uuid.uuid4())
        chunks = self.chunk_text(raw_text)
        return {
            "document_id": doc_id,
            "title": title,
            "chunks_created": len(chunks),
            "status": "processed",
            "metadata": metadata or {},
        }
