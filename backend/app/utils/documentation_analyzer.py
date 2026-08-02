import os


def analyze_documentation(repo_path, files):

    documentation_files = []
    comment_count = 0
    docstring_count = 0

    for file in files:

        if file.endswith((".md", ".rst", ".txt")):
            documentation_files.append(file)

        if not file.endswith(".py"):
            continue

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("#"):
                comment_count += 1

            if '"""' in stripped or "'''" in stripped:
                docstring_count += 1

    return {
        "documentation_files": documentation_files,
        "documentation_file_count": len(documentation_files),
        "comments": comment_count,
        "docstrings": docstring_count
    }