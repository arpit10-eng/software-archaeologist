from fastapi import FastAPI
import json

from app.models.repository import RepositoryRequest

from app.services.github_services import analyze_repository

from app.database.database import Base, engine, SessionLocal
from app.database.models import RepositoryAnalysis


# =========================================================
# Create Database Tables
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# Create FastAPI Application
# =========================================================

app = FastAPI(
    title="Software Archaeologist",
    description="AI-powered GitHub repository analysis system",
    version="2.0.0"
)


# =========================================================
# Root Endpoint
# =========================================================

@app.get("/")
def root():

    return {
        "message": "Welcome to Software Archaeologist"
    }


# =========================================================
# Analyze Repository
# =========================================================

@app.post("/repository/analyze")
def analyze(repo: RepositoryRequest):

    return analyze_repository(repo)


# =========================================================
# Get Repository Analysis History
# =========================================================

@app.get("/repository/history/{analysis_id}")
def get_repository_analysis(analysis_id: int):

    db = SessionLocal()

    try:

        record = (
            db.query(RepositoryAnalysis)
            .filter(
                RepositoryAnalysis.id == analysis_id
            )
            .first()
        )

        if record is None:

            return {
                "status": "error",
                "message": "Analysis not found"
            }

        return json.loads(
            record.analysis_json
        )

    finally:

        db.close()