def generate_ai_recommendations(
    security_issues,
    code_smells,
    dead_code,
    complexity,
    circular_dependencies,
    tests,
    license
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
                "circular dependencies."
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

    return recommendations

