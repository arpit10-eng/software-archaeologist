def generate_ai_recommendations(
    security_issues,
    code_smells,
    dead_code,
    complexity,
    circular_dependencies,
    tests,
    license,
    ci_cd,
    community,
    configuration,
    secret_exposure
):

    recommendations = []

    # --------------------------------------------------
    # Security recommendations
    # --------------------------------------------------

    for issue in security_issues:

        recommendations.append({
            "priority": issue["severity"],
            "category": "Security",
            "recommendation": issue["recommendation"]
        })

    # --------------------------------------------------
    # Code smell recommendations
    # --------------------------------------------------

    for smell in code_smells:

        recommendations.append({
            "priority": smell["severity"],
            "category": "Code Quality",
            "recommendation": smell["recommendation"]
        })

    # --------------------------------------------------
    # Dead code recommendations
    # --------------------------------------------------

    for item in dead_code:

        recommendations.append({
            "priority": "Low",
            "category": "Code Quality",
            "recommendation": (
                f"Review or remove unused function "
                f"'{item['function']}' in {item['file']}."
            )
        })

    # --------------------------------------------------
    # Complexity recommendation
    # --------------------------------------------------

    longest_function = complexity.get("longest_function")

    if longest_function:

        recommendations.append({
            "priority": "Medium",
            "category": "Complexity",
            "recommendation": (
                f"Consider breaking the function "
                f"'{longest_function['name']}' in "
                f"{longest_function['file']} into smaller functions."
            )
        })

    # --------------------------------------------------
    # Circular dependency recommendation
    # --------------------------------------------------

    if circular_dependencies.get("found"):

        recommendations.append({
            "priority": "High",
            "category": "Architecture",
            "recommendation": (
                "Refactor the affected modules to remove "
                "circular dependencies."
            )
        })

    # --------------------------------------------------
    # Test recommendations
    # --------------------------------------------------

    test_file_count = tests.get("test_file_count", 0)
    test_function_count = tests.get("test_function_count", 0)

    if test_file_count == 0:

        recommendations.append({
            "priority": "Medium",
            "category": "Testing",
            "recommendation": (
                "No test files were found. Add automated tests "
                "to improve repository reliability."
            )
        })

    elif test_function_count == 0:

        recommendations.append({
            "priority": "Medium",
            "category": "Testing",
            "recommendation": (
                "Test files were detected, but no test functions "
                "were found. Add meaningful test functions."
            )
        })

    # --------------------------------------------------
    # License recommendations
    # --------------------------------------------------

    license_status = license.get("status", "Unknown")

    if license_status == "Missing":

        recommendations.append({
            "priority": "Low",
            "category": "Repository",
            "recommendation": (
                "Add a LICENSE file to clearly define "
                "the project's usage permissions."
            )
        })

    elif license_status == "Unknown":

        recommendations.append({
            "priority": "Low",
            "category": "Repository",
            "recommendation": (
                "Review the license file because the "
                "license type could not be identified."
            )
        })

    # --------------------------------------------------
    # CI/CD recommendations
    # --------------------------------------------------

    if not ci_cd.get("github_actions", False):

        recommendations.append({
            "priority": "Low",
            "category": "DevOps",
            "recommendation": (
                "Consider adding a GitHub Actions workflow "
                "for automated testing and continuous integration."
            )
        })

    # --------------------------------------------------
    # Community recommendations
    # --------------------------------------------------

    if not community.get("contributing", False):

        recommendations.append({
            "priority": "Low",
            "category": "Community",
            "recommendation": (
                "Add a CONTRIBUTING.md file to provide "
                "guidelines for contributors."
            )
        })

    if not community.get("code_of_conduct", False):

        recommendations.append({
            "priority": "Low",
            "category": "Community",
            "recommendation": (
                "Add a CODE_OF_CONDUCT.md file to define "
                "community standards."
            )
        })

    if not community.get("issue_templates", False):

        recommendations.append({
            "priority": "Low",
            "category": "Community",
            "recommendation": (
                "Add GitHub issue templates to standardize "
                "bug reports and feature requests."
            )
        })

    if not community.get("pull_request_template", False):

        recommendations.append({
            "priority": "Low",
            "category": "Community",
            "recommendation": (
                "Add a pull request template to improve "
                "the consistency of contributions."
            )
        })

    # --------------------------------------------------
    # Configuration recommendations
    # --------------------------------------------------

    environment_files = configuration.get(
        "environment_files",
        []
    )

    environment_file_names = [
        os.path.basename(
            file.replace("\\", "/")
        )
        for file in environment_files
    ]

    has_env = ".env" in environment_file_names

    if has_env and not configuration.get(
        "env_example_found",
        False
    ):

        recommendations.append({
            "priority": "Medium",
            "category": "Configuration",
            "recommendation": (
                "Add a .env.example file to document required "
                "environment variables without exposing secrets."
            )
        })

    # --------------------------------------------------
    # Secret exposure recommendations
    # --------------------------------------------------

    if secret_exposure.get(
        "sensitive_file_count",
        0
    ) > 0:

        recommendations.append({
            "priority": "High",
            "category": "Security",
            "recommendation": (
                "Sensitive files were detected in the repository. "
                "Remove them from version control and add appropriate "
                "patterns to .gitignore."
            )
        })

    if not secret_exposure.get(
        "gitignore_found",
        False
    ):

        recommendations.append({
            "priority": "Medium",
            "category": "Security",
            "recommendation": (
                "Add a .gitignore file to prevent sensitive and "
                "unnecessary files from being committed."
            )
        })

    # --------------------------------------------------
    # Return recommendations
    # --------------------------------------------------

    return recommendations