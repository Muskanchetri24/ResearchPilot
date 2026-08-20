from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    ResearchQuery,
    ResearchResponse,
    DocumentIngestRequest,
    DocumentIngestResponse,
)
from app.services.research_service import ResearchService
from app.ingestion.pdf_parser import PDFIngestionPipeline

router = APIRouter()
research_service = ResearchService()
ingestion_pipeline = PDFIngestionPipeline()


@router.post("/query", response_model=ResearchResponse, status_code=status.HTTP_200_OK)
async def query_research(request: ResearchQuery):
    """
    Execute a literature search and RAG synthesis on stored paper embeddings.
    """
    try:
        response = await research_service.process_query(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error executing research query: {str(e)}",
        )


@router.post("/ingest", response_model=DocumentIngestResponse, status_code=status.HTTP_201_CREATED)
async def ingest_document(request: DocumentIngestRequest):
    """
    Ingest and chunk raw text / research paper content.
    """
    try:
        result = ingestion_pipeline.process_document(
            title=request.title,
            raw_text=request.content,
            metadata=request.metadata,
        )
        return DocumentIngestResponse(
            document_id=result["document_id"],
            status=result["status"],
            chunks_created=result["chunks_created"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error ingesting document: {str(e)}",
        )
