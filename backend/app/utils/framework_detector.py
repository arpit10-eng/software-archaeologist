import os

def detect_framework(repo_path, files):

    for file in files:

        if os.path.splitext(file)[1] != ".py":
            continue

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        if "fastapi" in content:
            return "FastAPI"

        if "flask" in content:
            return "Flask"

        if "django" in content:
            return "Django"

    return "Unknown"