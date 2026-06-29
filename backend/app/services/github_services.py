from fastapi import HTTPException
from app.utils.validators import is_valid_github_url

def analyze_repository(repo):

    if not is_valid_github_url(repo.github_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )

    return {
        "status": "success",
        "repository": repo.github_url,
        "branch": repo.branch,
        "message": "Repository received successfully!"
    }