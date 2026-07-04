import subprocess

def clone_repository(repo_url, destination):
    subprocess.run(
        ["git", "clone", repo_url, destination],
        check=True
    )

    return destination