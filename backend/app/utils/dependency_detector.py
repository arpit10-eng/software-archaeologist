import os


def detect_dependencies(repo_path, files):

    requirements_path = None

    for file in files:

        if file.endswith("requirements.txt"):
            requirements_path = os.path.join(repo_path, file)
            break

    if requirements_path is None:
        return []

    dependencies = []

    with open(requirements_path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            dependencies.append(line)

    return dependencies