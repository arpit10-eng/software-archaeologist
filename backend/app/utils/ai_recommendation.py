def generate_ai_recommendations(
    security_issues,
    code_smells,
    dead_code,
    complexity,
    circular_dependencies
):

    recommendations = []

    for issue in security_issues:

        recommendations.append({
            "priority": issue["severity"],
            "category": "Security",
            "recommendation": issue["recommendation"]
        })

    return recommendations  