import json
import logging
from base64 import b64decode
from urllib.parse import quote, urlparse

import requests
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.database.database import (
    Base,
    SessionLocal,
    engine,
    ensure_schema,
)
from app.database.models import RepositoryAnalysis
from app.services.github_services import analyze_repository


# =========================================================
# Logging Configuration
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("software_archaeologist")


# =========================================================
# Database Initialization
# =========================================================

Base.metadata.create_all(
    bind=engine
)

ensure_schema()


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)


# =========================================================
# CORS Configuration
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Exception Handlers
# =========================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    """
    Handle FastAPI request validation errors.

    Returns a consistent API error response instead
    of exposing FastAPI's default validation structure.
    """

    logger.warning(
        "Request validation failed: %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "error": "validation_error",
            "message": "Request validation failed.",
            "details": exc.errors(),
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    """
    Handle HTTP exceptions consistently.
    """

    logger.warning(
        "HTTP error %s: %s %s",
        exc.status_code,
        request.method,
        request.url.path,
    )

    detail = exc.detail

    if isinstance(detail, dict):
        message = detail.get(
            "message",
            "Request failed.",
        )
    else:
        message = str(detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error": "http_error",
            "message": message,
        },
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected server errors.

    Internal exception details are deliberately not returned
    to the client.
    """

    logger.exception(
        "Unexpected server error: %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error": "internal_server_error",
            "message": "An unexpected server error occurred.",
        },
    )


# =========================================================
# Root Endpoint
# =========================================================

@app.get("/")
def root():
    logger.info(
        "Root endpoint requested."
    )

    return {
        "status": "success",
        "message": "Software Archaeologist API is running.",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# =========================================================
# Analyze Repository
# =========================================================

@app.post("/repository/analyze")
def analyze_repository_endpoint(
    repository_url: str = Query(
        ...,
        min_length=1,
        max_length=500,
        description="Public GitHub repository URL",
    )
):
    """
    Analyze a GitHub repository.

    The repository analysis service may raise HTTPException
    for invalid repositories or GitHub failures. Those errors
    are handled centrally by the exception handlers above.
    """

    logger.info(
        "Repository analysis requested: %s",
        repository_url,
    )

    result = analyze_repository(
        repository_url
    )

    logger.info(
        "Repository analysis completed: %s",
        repository_url,
    )

    return result


# =========================================================
# Analysis History
# =========================================================

@app.get("/repository/history")
def get_repository_history(
    repository: str | None = Query(
        default=None,
        max_length=500,
    ),
    branch: str | None = Query(
        default=None,
        max_length=250,
    ),
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
    """
    Retrieve repository analysis history.

    Pagination is limited to prevent unnecessarily large
    database queries.
    """

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

    except Exception:
        logger.exception(
            "Failed to retrieve repository history."
        )
        raise

    finally:
        db.close()


# =========================================================
# Get Specific Analysis
# =========================================================

@app.get("/repository/history/{analysis_id}")
def get_repository_analysis(
    analysis_id: int,
):
    """
    Retrieve a previously stored repository analysis.
    """

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
            logger.error(
                "Invalid stored analysis JSON for ID %s.",
                analysis_id,
            )

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

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Failed to retrieve analysis ID %s.",
            analysis_id,
        )
        raise

    finally:
        db.close()


# =========================================================
# Get Repository File
# =========================================================

@app.get("/repository/file")
def get_repository_file(
    repository: str = Query(
        ...,
        min_length=1,
        max_length=500,
        description="GitHub repository URL",
    ),
    branch: str = Query(
        "main",
        min_length=1,
        max_length=250,
        description="Git branch",
    ),
    path: str = Query(
        ...,
        min_length=1,
        max_length=1000,
        description="Repository file path",
    ),
):
    """
    Retrieve the contents of a file from a public GitHub repository.
    """

    parsed_url = urlparse(
        repository
    )

    if (
        parsed_url.scheme != "https"
        or parsed_url.netloc.lower() != "github.com"
    ):
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

    if not owner or not repo_name:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL.",
        )

    encoded_path = quote(
        path.lstrip("/"),
        safe="/",
    )

    api_url = (
        "https://api.github.com/repos/"
        f"{owner}/{repo_name}/contents/"
        f"{encoded_path}"
    )

    logger.info(
        "Fetching repository file: %s/%s/%s",
        owner,
        repo_name,
        path,
    )

    try:
        response = requests.get(
            api_url,
            params={
                "ref": branch,
            },
            timeout=settings.GITHUB_API_TIMEOUT,
        )

    except requests.Timeout:
        logger.warning(
            "GitHub API request timed out."
        )

        raise HTTPException(
            status_code=504,
            detail="GitHub API request timed out.",
        )

    except requests.RequestException:
        logger.exception(
            "GitHub API request failed."
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to connect to GitHub.",
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="File not found in repository.",
        )

    if response.status_code == 403:
        raise HTTPException(
            status_code=502,
            detail="GitHub API access was denied or rate limited.",
        )

    if response.status_code != 200:
        logger.warning(
            "GitHub API returned status %s.",
            response.status_code,
        )

        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve repository file.",
        )

    try:
        data = response.json()

    except ValueError:
        logger.error(
            "GitHub returned invalid JSON."
        )

        raise HTTPException(
            status_code=502,
            detail="GitHub returned an invalid response.",
        )

    if data.get("type") != "file":
        raise HTTPException(
            status_code=400,
            detail="Requested path is not a file.",
        )

    encoded_content = data.get(
        "content",
        "",
    )

    if not encoded_content:
        raise HTTPException(
            status_code=500,
            detail="Repository file has no readable content.",
        )

    try:
        content = b64decode(
            encoded_content
        ).decode(
            "utf-8",
            errors="replace",
        )

    except Exception:
        logger.exception(
            "Unable to decode repository file."
        )

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