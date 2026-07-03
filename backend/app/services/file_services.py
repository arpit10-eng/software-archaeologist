import os
from app.utils.file_utils import get_file_extension

def scan_repository(repo_path):

    all_files = []

    python_files = 0
    markdown_files = 0
    json_files = 0
    text_files = 0
    other_files = 0

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in [".git", "__pycache__", "venv"]
        ]

        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)

            extension = get_file_extension(file_path)

            if extension == ".py":
                python_files += 1
            elif extension == ".md":
                markdown_files += 1
            elif extension == ".json":
                json_files += 1
            elif extension == ".txt":
                text_files += 1
            else:
                other_files += 1

    return {
        "total_files": len(all_files),
        "python_files": python_files,
        "markdown_files": markdown_files,
        "json_files": json_files,
        "text_files": text_files,
        "other_files": other_files,
        "files": all_files
    }