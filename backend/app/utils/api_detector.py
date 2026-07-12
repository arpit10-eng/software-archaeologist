import os


def detect_api_endpoints(repo_path, files):

    endpoints = []

    methods = [
        "get",
        "post",
        "put",
        "delete",
        "patch"
    ]

    for file in files:

        if not file.endswith(".py"):
            continue

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:

            stripped = line.strip()

            for method in methods:

                pattern = f'@app.{method}("'

                if pattern in stripped:

                    start = stripped.find('("') + 2
                    end = stripped.find('")')

                    endpoint = stripped[start:end]

                    endpoints.append({
                        "method": method.upper(),
                        "path": endpoint
                    })

    return endpoints