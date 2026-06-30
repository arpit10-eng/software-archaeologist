import requests

from fastapi import HTTPException
from app.utils.validators import is_valid_github_url


def analyze_repository(repo):

    if not is_valid_github_url(repo.github_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )

    api_url = repo.github_url.replace(
        "https://github.com/",
        "https://api.github.com/repos/"
    )

    response = requests.get(api_url)

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="GitHub repository not found"
        )

    return {
        "status": "success",
        "repository": repo.github_url,
        "branch": repo.branch,
        "message": "Repository exists on GitHub!"
    }