from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class HealthCheck(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    environment: str = "development"


class ResearchQuery(BaseModel):
    query: str = Field(..., description="The user query or research topic")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of retrieved documents")
    model: Optional[str] = Field(default=None, description="Optional override model name")


class DocumentSource(BaseModel):
    id: str
    title: str
    content: str
    score: float
    metadata: Dict[str, Any] = {}


class ResearchResponse(BaseModel):
    query: str
    answer: str
    sources: List[DocumentSource] = []
    evaluation: Optional[Dict[str, float]] = None


class DocumentIngestRequest(BaseModel):
    title: str
    content: str
    metadata: Dict[str, Any] = {}


class DocumentIngestResponse(BaseModel):
    document_id: str
    status: str
    chunks_created: int


class EvaluationMetric(BaseModel):
    faithfulness: float
    context_relevance: float
    answer_relevance: float
