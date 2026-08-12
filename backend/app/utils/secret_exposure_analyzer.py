import os


def analyze_secret_exposure(repo_path, files):

    sensitive_names = [
        ".env",
        ".env.local",
        ".env.production",
        "credentials.json",
        "secrets.json",
        "id_rsa",
        "id_rsa.pub"
    ]

    sensitive_files = []

    gitignore_found = False

    for file in files:

        normalized = file.replace("\\", "/")
        filename = os.path.basename(normalized)

        if filename == ".gitignore":
            gitignore_found = True

        if filename in sensitive_names:
            sensitive_files.append(file)

    return {
        "gitignore_found": gitignore_found,
        "sensitive_files": sensitive_files,
        "sensitive_file_count": len(sensitive_files)
    }