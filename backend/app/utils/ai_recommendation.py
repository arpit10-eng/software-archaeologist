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
    configuration
):

    recommendations = []

    # Security recommendations
    for issue in security_issues:

        recommendations.append({
            "priority": issue["severity"],
            "category": "Security",
            "recommendation": issue["recommendation"]
        })

    # Code smell recommendations
    for smell in code_smells:

        recommendations.append({
            "priority": smell["severity"],
            "category": "Code Quality",
            "recommendation": smell["recommendation"]
        })

    # Dead code recommendations
    for item in dead_code:

        recommendations.append({
            "priority": "Low",
            "category": "Code Quality",
            "recommendation": (
                f"Review or remove unused function "
                f"'{item['function']}' in {item['file']}."
            )
        })

    # Complexity recommendation
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

    # Circular dependency recommendation
    if circular_dependencies.get("found"):

        recommendations.append({
            "priority": "High",
            "category": "Architecture",
            "recommendation": (
                "Refactor the affected modules to remove "
                "circular dependencies..."
            )
        })

    # Test recommendations
    if (
        tests["test_file_count"] == 0
        and tests["test_function_count"] == 0
    ):

        recommendations.append({
            "priority": "Medium",
            "category": "Testing",
            "recommendation": (
                "Add automated tests to improve "
                "project reliability."
            )
        })
        # License recommendation
    if not license["license_found"]:

        recommendations.append({
            "priority": "Low",
            "category": "Repository",
            "recommendation": (
                "Add a LICENSE file to clearly define "
                "the project's usage permissions."
            )
        })
    if not ci_cd["github_actions"]:

        recommendations.append({
            "priority": "Low",
            "category": "DevOps",
            "recommendation": (
            "Consider adding a GitHub Actions workflow "
            "for automated testing and continuous integration."
            )
        })
        # Community recommendations

    if not community["contributing"]:
        recommendations.append({
            "priority": "Low",
            "category": "Community",
            "recommendation": (
                "Add a CONTRIBUTING.md file to provide "
                "guidelines for contributors."
            )
        })

    if not community["code_of_conduct"]:
        recommendations.append({
            "priority": "Low",
            "category": "Community",
            "recommendation": (
                "Add a CODE_OF_CONDUCT.md file to define "
                "community standards."
            )
        })

    if not community["issue_templates"]:
        recommendations.append({
            "priority": "Low",
            "category": "Community",
            "recommendation": (
                "Add GitHub issue templates to standardize "
                "bug reports and feature requests."
            )
        })

    if not community["pull_request_template"]:
        recommendations.append({
            "priority": "Low",
            "category": "Community",
            "recommendation": (
                "Add a pull request template to improve "
                "the consistency of contributions.."
            )
        })
        # Configuration recommendation

    environment_files = configuration["environment_files"]

    has_env = ".env" in [
        file.split("/")[-1].replace("\\", "")
        for file in environment_files
    ]

    if has_env and not configuration["env_example_found"]:

        recommendations.append({
            "priority": "Medium",
            "category": "Configuration",
            "recommendation": (
                "Add a .env.example file to document required "
                "environment variables without exposing secrets."
            )
        })

    return recommendations

