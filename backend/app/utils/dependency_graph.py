import os


def detect_dependency_graph(repo_path, files):

    graph = {}

    # Get only Python filenames
    python_files = [
        os.path.basename(file)
        for file in files
        if file.endswith(".py")
    ]

    for file in files:

        if not file.endswith(".py"):
            continue

        graph[file] = []

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("from app."):

                parts = stripped.split()

                module = parts[1].split(".")[-1] + ".py"

                if module in python_files:
                    graph[file].append(module)

    return graph