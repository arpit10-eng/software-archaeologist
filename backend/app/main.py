import json
from base64 import b64decode
from urllib.parse import quote, urlparse

import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.database import Base, SessionLocal, engine, ensure_schema
from app.database.models import RepositoryAnalysis
from app.services.github_services import analyze_repository


# =========================================================
# Database Initialization
# =========================================================

Base.metadata.create_all(bind=engine)
ensure_schema()


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="Software Archaeologist",
    version="2.1.0",
)


# =========================================================
# CORS Configuration
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
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
        "status": "success",
        "message": "Software Archaeologist API is running.",
        "version": "2.1.0",
    }


# =========================================================
# Analyze Repository
# =========================================================

@app.post("/repository/analyze")
def analyze_repository_endpoint(
    repository_url: str = Query(
        ...,
        description="Public GitHub repository URL",
    )
):
    result = analyze_repository(
        repository_url
    )

    return result


# =========================================================
# Analysis History
# =========================================================

@app.get("/repository/history")
def get_repository_history(
    repository: str | None = None,
    branch: str | None = None,
    limit: int = Query(
        20,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        0,
        ge=0,
    ),
):
    db: Session = SessionLocal()

    try:
        query = db.query(
            RepositoryAnalysis
        )

        if repository:
            query = query.filter(
                RepositoryAnalysis.repository == repository
            )

        if branch:
            query = query.filter(
                RepositoryAnalysis.branch == branch
            )

        total = query.count()

        records = (
            query
            .order_by(
                RepositoryAnalysis.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        results = []

        for record in records:
            results.append(
                {
                    "analysis_id": record.id,
                    "repository": record.repository,
                    "branch": record.branch,
                    "primary_language": record.primary_language,
                    "created_at": (
                        record.created_at.isoformat()
                        if record.created_at
                        else None
                    ),
                }
            )

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "results": results,
        }

    finally:
        db.close()


# =========================================================
# Get Specific Analysis
# =========================================================

@app.get("/repository/history/{analysis_id}")
def get_repository_analysis(
    analysis_id: int,
):
    db: Session = SessionLocal()

    try:
        record = (
            db.query(
                RepositoryAnalysis
            )
            .filter(
                RepositoryAnalysis.id == analysis_id
            )
            .first()
        )

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found.",
            )

        try:
            analysis = json.loads(
                record.analysis_json
            )

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=500,
                detail="Stored analysis data is invalid.",
            )

        analysis["analysis_id"] = record.id

        if record.created_at:
            analysis["created_at"] = (
                record.created_at.isoformat()
            )

        return analysis

    finally:
        db.close()


# =========================================================
# Get Repository File
# =========================================================

@app.get("/repository/file")
def get_repository_file(
    repository: str = Query(
        ...,
        description="GitHub repository URL",
    ),
    branch: str = Query(
        "main",
        description="Git branch",
    ),
    path: str = Query(
        ...,
        description="Repository file path",
    ),
):
    parsed_url = urlparse(
        repository
    )

    if parsed_url.netloc.lower() != "github.com":
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL.",
        )

    parts = [
        part
        for part in parsed_url.path.split("/")
        if part
    ]

    if len(parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL.",
        )

    owner = parts[0]
    repo_name = parts[1]

    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    encoded_path = quote(
        path.lstrip("/"),
        safe="/",
    )

    api_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo_name}/contents/"
        f"{encoded_path}"
    )

    response = requests.get(
        api_url,
        params={
            "ref": branch,
        },
        timeout=10,
    )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="File not found in repository.",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve repository file.",
        )

    data = response.json()

    if data.get("type") != "file":
        raise HTTPException(
            status_code=400,
            detail="Requested path is not a file.",
        )

    encoded_content = data.get(
        "content",
        "",
    )

    try:
        content = b64decode(
            encoded_content
        ).decode(
            "utf-8",
            errors="replace",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to decode repository file.",
        )

    return {
        "repository": repository,
        "branch": branch,
        "path": path,
        "content": content,
        "size": data.get("size"),
        "sha": data.get("sha"),
    }