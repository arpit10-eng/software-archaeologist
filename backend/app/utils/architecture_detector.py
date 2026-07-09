def detect_architecture(files):

    architecture = {
        "models": [],
        "services": [],
        "routers": [],
        "controllers": [],
        "database": [],
        "middleware": [],
        "config": [],
        "tests": [],
        "utils": []
    }

    for file in files:

        if "/models/" in file:
            architecture["models"].append(file.split("/")[-1])

        elif "/services/" in file:
            architecture["services"].append(file.split("/")[-1])

        elif "/routers/" in file:
            architecture["routers"].append(file.split("/")[-1])

        elif "/controllers/" in file:
            architecture["controllers"].append(file.split("/")[-1])

        elif "/database/" in file:
            architecture["database"].append(file.split("/")[-1])

        elif "/middleware/" in file:
            architecture["middleware"].append(file.split("/")[-1])

        elif "/config/" in file:
            architecture["config"].append(file.split("/")[-1])

        elif "/tests/" in file:
            architecture["tests"].append(file.split("/")[-1])

        elif "/utils/" in file:
            architecture["utils"].append(file.split("/")[-1])

    architecture = {
        key: value
        for key, value in architecture.items()
        if value
    }

    return architecture