import os


def analyze_configuration(repo_path, files):

    environment_files = []
    config_files = []

    environment_names = [
        ".env",
        ".env.example",
        ".env.sample",
        ".env.template"
    ]

    config_names = [
        "config.py",
        "settings.py",
        "config.yaml",
        "config.yml",
        "config.json"
    ]

    for file in files:

        normalized = file.replace("\\", "/")
        filename = os.path.basename(normalized)

        if filename in environment_names:
            environment_files.append(file)

        elif filename in config_names:
            config_files.append(file)

    return {
        "environment_files": environment_files,
        "environment_file_count": len(environment_files),
        "config_files": config_files,
        "config_file_count": len(config_files),
        "env_example_found": (
            ".env.example" in
            [os.path.basename(file) for file in environment_files]
        )
    }