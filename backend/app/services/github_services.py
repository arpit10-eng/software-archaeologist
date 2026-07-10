import requests
import tempfile
import os

from fastapi import HTTPException
from app.services.git_services import clone_repository
from app.services.file_services import scan_repository
from app.utils.validators import is_valid_github_url
from app.utils.framework_detector import detect_framework
from app.utils.entry_point_detector import detect_entry_point
from app.utils.dependency_detector import detect_dependencies
from app.utils.language_detector import detect_language
from app.utils.architecture_detector import detect_architecture
from app.utils.summary_generator import generate_summary

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
        entry_point = detect_entry_point(framework,files["files"])
        dependencies = detect_dependencies(cloned_path,files["files"])
        language = detect_language(files["files"])
        architecture = detect_architecture(files["files"])
        summary = generate_summary(language["primary_language"],framework,architecture,dependencies)

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
    "primary_language": language["primary_language"],
    "languages": language["languages"],
    "framework": framework,
    "entry_point": entry_point,
    "dependencies": dependencies,
    "architecture": architecture,
    "summary": summary,
    **files
}
