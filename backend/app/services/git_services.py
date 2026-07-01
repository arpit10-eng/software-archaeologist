import os
import subprocess

def clone_repository(repo_url):

    repo_name = repo_url.split("/")[-1]

    destination = os.path.join("temp", repo_name)

    subprocess.run([
        "git",
        "clone",
        repo_url,
        destination
    ])

    return destination