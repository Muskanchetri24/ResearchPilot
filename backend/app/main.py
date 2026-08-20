from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.models.schemas import HealthCheck

app = FastAPI(
    title="ResearchPilot API",
    description="AI-powered research intelligence platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router registration
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():

    return {
        "project": "ResearchPilot",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health", response_model=HealthCheck, tags=["System"])
def health():
    return HealthCheck(
        status="ok",
        version="0.1.0",
        environment=settings.ENVIRONMENT,
    )



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True,
    )