import os


def analyze_documentation(repo_path, files):

    documentation_files = []
    comments = 0
    docstrings = 0

    for file in files:

        normalized = file.replace("\\", "/")
        filename = os.path.basename(normalized)

        # ---------------------------------------------
        # Detect documentation files
        # ---------------------------------------------

        if filename.lower() in [
            "readme",
            "readme.md",
            "readme.txt",
            "documentation.md",
            "docs.md"
        ]:
            documentation_files.append(file)

        # ---------------------------------------------
        # Analyze Python documentation
        # ---------------------------------------------

        if filename.endswith(".py"):

            absolute_path = os.path.join(
                repo_path,
                normalized.replace("/", os.sep)
            )

            if not os.path.isfile(absolute_path):
                continue

            try:

                with open(
                    absolute_path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    lines = f.readlines()

                for line in lines:

                    stripped = line.strip()

                    # Count comments
                    if stripped.startswith("#"):
                        comments += 1

                    # Count simple docstrings
                    if (
                        stripped.startswith('"""')
                        or stripped.startswith("'''")
                    ):
                        docstrings += 1

            except (UnicodeDecodeError, OSError):
                continue

    # ---------------------------------------------
    # Documentation quality
    # ---------------------------------------------

    documentation_file_count = len(documentation_files)

    if (
        documentation_file_count == 0
        and comments == 0
        and docstrings == 0
    ):

        score = 0
        level = "Poor"
        reason = "No documentation or code documentation was detected."

    elif (
        documentation_file_count == 0
        and comments + docstrings < 5
    ):

        score = 30
        level = "Poor"
        reason = "Very little documentation was detected."

    elif documentation_file_count > 0 and comments + docstrings < 5:

        score = 60
        level = "Fair"
        reason = (
            "Documentation files exist, but the source code "
            "contains limited documentation."
        )

    elif documentation_file_count > 0 and docstrings >= 5:

        score = 100
        level = "Excellent"
        reason = (
            "The repository contains documentation files "
            "and a strong number of code docstrings."
        )

    else:

        score = 80
        level = "Good"
        reason = (
            "The repository contains documentation "
            "and code comments."
        )

    return {
        "documentation_files": documentation_files,
        "documentation_file_count": documentation_file_count,
        "comments": comments,
        "docstrings": docstrings,
        "documentation_quality": {
            "score": score,
            "level": level,
            "reason": reason
        }
    }