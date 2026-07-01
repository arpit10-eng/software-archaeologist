import requests
from app.services.git_services import clone_repository
from fastapi import HTTPException
from app.utils.validators import is_valid_github_url


def analyze_repository(repo):

    if not is_valid_github_url(repo.github_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )
    cloned_path = clone_repository(repo.github_url)

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
    "cloned_to": cloned_path,
    "message": "Repository cloned successfully!"
}