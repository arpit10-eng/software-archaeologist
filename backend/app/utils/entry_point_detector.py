def detect_entry_point(framework, files):

    if framework == "FastAPI":
        target = "main.py"

    elif framework == "Flask":
        target = "app.py"

    elif framework == "Django":
        target = "manage.py"

    else:
        return "Unknown"

    ignored_folders = [
        "tests",
        "test",
        "examples",
        "docs"
    ]

    for file in files:

        if not file.endswith(target):
            continue

        if any(folder in file.split("/") for folder in ignored_folders):
            continue

        return file

    return "Unknown"