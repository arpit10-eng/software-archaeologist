from fastapi import FastAPI
from app.models.repository import RepositoryRequest
from app.services.github_services import analyze_repository
from app.database.database import Base, engine
from app.database.models import RepositoryAnalysis

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Software Archaeologist"}


@app.post("/repository/analyze")
def analyze(repo: RepositoryRequest):
    return analyze_repository(repo)