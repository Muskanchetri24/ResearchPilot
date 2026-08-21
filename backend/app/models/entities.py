from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class MethodEntity(BaseModel):
    name: str = Field(..., description="Method or model name (e.g., Vision Transformer, ResNet50, U-Net)")
    category: str = Field(default="Model", description="Architecture category (e.g., Transformer, CNN, Hybrid)")


class DatasetEntity(BaseModel):
    name: str = Field(..., description="Dataset name (e.g., ISIC, BraTS, ChestX-ray8, MIMIC-III)")
    modality: Optional[str] = Field(default=None, description="Data modality (e.g., MRI, CT, Dermoscopy, EEG)")


class TaskEntity(BaseModel):
    name: str = Field(..., description="Research task or problem (e.g., Brain Tumor Segmentation, Melanoma Classification)")
    domain: str = Field(default="Healthcare AI", description="Research domain")


class PaperMetadata(BaseModel):
    paper_id: str
    title: str
    abstract: str
    year: int
    authors: List[str] = []
    venue: Optional[str] = None
    citation_count: int = 0
    reference_count: int = 0
    open_access_pdf: Optional[str] = None
    url: Optional[str] = None
    methods: List[MethodEntity] = []
    datasets: List[DatasetEntity] = []
    tasks: List[TaskEntity] = []
    limitations: List[str] = []


class ResearchGapOpportunity(BaseModel):
    opportunity_id: str
    method: str
    dataset: str
    task: str
    paper_count: int
    recent_growth: str = Field(..., description="Growth velocity: High, Medium, Low")
    evidence_strength: str = Field(..., description="Evidence level: Strong, Moderate, Emerging")
    opportunity_score: float = Field(..., ge=0.0, le=100.0, description="Calculated 0-100 gap score")
    description: str
    supporting_paper_ids: List[str] = []
    supporting_paper_titles: List[str] = []


class LiteratureReviewReport(BaseModel):
    title: str
    topic: str
    time_period: str
    total_papers_analyzed: int
    executive_summary: str
    methodology_breakdown: Dict[str, int]
    key_findings: List[str]
    identified_gaps: List[ResearchGapOpportunity]
    sections: List[Dict[str, str]]
    references: List[Dict[str, Any]]
