import requests
import tempfile
import os

from fastapi import HTTPException

from app.services.git_services import clone_repository
from app.services.file_services import scan_repository
from app.utils.validators import is_valid_github_url
from app.utils.framework_detector import detect_framework

def analyze_repository(repo):

    if not is_valid_github_url(repo.github_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL"
        )
    
    with tempfile.TemporaryDirectory() as temp_dir:

        repo_name = repo.github_url.rstrip("/").split("/")[-1]

        destination = os.path.join(temp_dir, repo_name)

        cloned_path = clone_repository(
            repo.github_url,
            destination
        )

        files = scan_repository(cloned_path)
        framework = detect_framework(cloned_path, files["files"])

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
        "framework": framework,
        **files
    }