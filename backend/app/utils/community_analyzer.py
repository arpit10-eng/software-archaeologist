import os

def analyze_community(repo_path, files):

    contributing = False
    code_of_conduct = False
    issue_templates = []
    pull_request_template = False

    for file in files:

        normalized = file.replace("\\", "/")
        filename = os.path.basename(normalized).lower()

        if filename == "contributing.md":
            contributing = True

        elif filename == "code_of_conduct.md":
            code_of_conduct = True

        elif normalized.startswith(".github/issue_template/"):
            issue_templates.append(file)

        elif normalized.startswith(".github/issue_template"):
            issue_templates.append(file)

        elif normalized == ".github/pull_request_template.md":
            pull_request_template = True

    return {
        "contributing": contributing,
        "code_of_conduct": code_of_conduct,
        "issue_templates": issue_templates,
        "issue_template_count": len(issue_templates),
        "pull_request_template": pull_request_template
    }