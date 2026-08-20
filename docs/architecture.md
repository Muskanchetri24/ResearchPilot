# System Architecture Document 📐

## Overview
ResearchPilot follows a modular, decouplable microservice-ready architecture separating document ingestion, hybrid vector retrieval, RAG generation pipelines, and automated evaluation metrics.

```mermaid
graph TD
    User([User / Browser]) <--> Frontend[Frontend React + Vite UI]
    Frontend <--> API[FastAPI Gateway /api/v1]
    
    subgraph Backend Services
        API --> Ingest[Ingestion Pipeline - pdf_parser.py]
        API --> Search[Retrieval Service - vector_store.py]
        API --> RAG[RAG Chain Pipeline - chain.py]
        API --> Eval[Evaluator - evaluator.py]
    end
    
    Ingest --> VectorDB[(Vector Store / Embeddings)]
    Search --> VectorDB
    VectorDB --> RAG
    RAG --> Eval
```

## Core Components
1. **`app/ingestion/`**: Parses PDF/raw text files into semantic chunks and generates embeddings.
2. **`app/retrieval/`**: Interacts with the vector database to retrieve top-K relevant paper contexts.
3. **`app/rag/`**: Synthesizes structured research answers using LLM generation chains.
4. **`app/evaluation/`**: Evaluates outputs across faithfulness and relevance metrics.
