from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class RepositoryRequest(BaseModel):
    github_url: str
    branch: str="main"


@app.get("/")
def root():
    return {"message": "Welcome to Software Archaeologist"}


@app.post("/repository/analyze")
def analyze_repository(repo: RepositoryRequest):
    return {
        "status": "success",
        "received_url": repo.github_url,
        "branch": repo.branch
    }