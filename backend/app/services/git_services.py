import os
import shutil
import subprocess

def clone_repository(repo_url):
    # Extract repository name
    repo_name = repo_url.rstrip("/").split("/")[-1]

    # Create temp directory if it doesn't exist
    os.makedirs("temp", exist_ok=True)

    # Destination path
    destination = os.path.join("temp", repo_name)

    # If repository already exists, delete it
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # Clone repository
    subprocess.run(
        ["git", "clone", repo_url, destination],
        check=True
    )

    return destination