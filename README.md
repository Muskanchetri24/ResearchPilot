# ResearchPilot 🚀

**ResearchPilot** is an intelligent AI-powered research assistant platform designed to automate literature search, paper ingestion, hybrid retrieval (RAG), synthesize domain insights, and evaluate response quality.

---

## 📁 Repository Structure

```
researchpilot/
│
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers & endpoint definitions
│   │   ├── core/         # Core config, logging, security settings
│   │   ├── models/       # Pydantic schemas & domain data models
│   │   ├── services/     # Orchestration & business logic
│   │   ├── ingestion/    # Document parsing, chunking, & text extraction
│   │   ├── retrieval/    # Vector index, hybrid search & reranking
│   │   ├── rag/          # Generation chains & prompt templates
│   │   ├── evaluation/   # Faithfulness, context precision & quality metrics
│   │   └── main.py       # FastAPI application entrypoint
│   │
│   ├── tests/            # Automated pytest suite
│   └── requirements.txt  # Python backend dependencies
│
├── frontend/             # Modern React + Vite frontend application
│   ├── src/
│   │   ├── components/   # Modular UI components
│   │   ├── App.tsx       # Main dashboard layout
│   │   └── index.css     # Glassmorphic dark design system
│   └── package.json
│
├── data/                 # Data directory hierarchy
│   ├── raw/              # Unprocessed PDF papers / documents
│   ├── processed/        # Extracted text, embeddings & vector store
│   └── sample/           # Sample benchmarks & demo datasets
│
├── notebooks/            # Jupyter notebooks for EDA & prototyping
├── experiments/          # Model evaluations & retrieval experiments
├── docs/                 # System architecture & integration docs
│
├── .env                  # Local environment configuration
├── .env.example          # Environment template
├── .gitignore            # Git exclusion rules
├── docker-compose.yml    # Container orchestration configuration
└── README.md
```

---

## ⚙️ Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and `npm`
- Docker (optional)

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI development server
uvicorn app.main:app --reload --port 8000
```
API Documentation will be accessible at: `http://localhost:8000/docs`

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Frontend web application will be accessible at: `http://localhost:5173`

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

---

## 📜 License
MIT License. Created for AI-driven academic & industrial research workflows.
