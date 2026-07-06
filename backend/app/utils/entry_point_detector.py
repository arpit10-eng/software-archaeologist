def detect_entry_point(framework, files):

    if framework == "FastAPI":
        target = "main.py"

    elif framework == "Flask":
        target = "app.py"

    elif framework == "Django":
        target = "manage.py"

    else:
        return "Unknown"

    for file in files:
        if file.endswith(target):
            return file

    return "Unknown"