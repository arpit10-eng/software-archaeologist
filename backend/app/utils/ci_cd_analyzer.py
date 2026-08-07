import os


def analyze_ci_cd(repo_path, files):

    workflow_files = []

    for file in files:

        normalized = file.replace("\\", "/")

        if normalized.startswith(".github/workflows/") and normalized.endswith(".yml"):
            workflow_files.append(file)

        elif normalized.startswith(".github/workflows/") and normalized.endswith(".yaml"):
            workflow_files.append(file)

    return {
        "github_actions": len(workflow_files) > 0,
        "workflow_files": workflow_files,
        "workflow_count": len(workflow_files)
    }