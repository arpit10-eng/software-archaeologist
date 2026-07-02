import os

def scan_repository(repo_path):

    all_files = []

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in [".git", "__pycache__", "venv"]
        ]

        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

    return all_files