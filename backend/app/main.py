from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.repository import RepositoryRequest
from app.services.github_services import analyze_repository

from app.database.database import Base, engine
from app.database import models


Base.metadata.create_all(bind=engine)


app = FastAPI()


# =========================================================
# CORS Configuration
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
# Repository Analysis
# =========================================================

@app.post("/repository/analyze")
def analyze(repo: RepositoryRequest):

    return analyze_repository(repo)


# =========================================================
# Repository History
# =========================================================

@app.get("/repository/history/{analysis_id}")
def get_repository_analysis(analysis_id: int):

    from app.database.database import SessionLocal
    from app.database.models import RepositoryAnalysis
    import json

    db = SessionLocal()

    try:

        record = (
            db.query(RepositoryAnalysis)
            .filter(RepositoryAnalysis.id == analysis_id)
            .first()
        )

        if record is None:

            return {
                "status": "error",
                "message": "Analysis not found"
            }

        return json.loads(record.analysis_json)

    finally:

        db.close()