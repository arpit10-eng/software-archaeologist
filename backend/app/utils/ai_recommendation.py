
def _recommendation(title, description, priority="Medium", category="General", evidence=None, action=None):
    return {"title": title, "description": description, "priority": priority,
            "category": category, "evidence": evidence or [], "action": action or "Review the finding and apply the recommended remediation."}


def _score(analysis, key, default=100):
    value = analysis.get(key, default)
    try: return float(value)
    except (TypeError, ValueError): return float(default)


def generate_ai_recommendations(analysis):
    recommendations = []
    findings = analysis.get("findings", []) or []

    # Promote the most important concrete findings first.
    for finding in findings[:12]:
        severity = finding.get("severity", "Medium")
        priority = "High" if severity in {"Critical", "High"} else severity
        recommendations.append(_recommendation(
            finding.get("title", "Review repository finding"),
            finding.get("description", "A repository issue was detected."),
            priority, finding.get("category", "General"),
            finding.get("evidence", []), finding.get("recommendation"),
        ))

    rules = [
        ("security_score", "Improve repository security", "Security", "The security score indicates unresolved security findings.", "High", "Review every security finding and remove unsafe patterns."),
        ("secret_exposure_score", "Remove potential secrets", "Security", "Potential secrets or sensitive files were detected.", "High", "Remove secrets, rotate real credentials, and use a secret manager."),
        ("tests_score", "Expand automated tests", "Testing", "The repository has limited automated testing.", "High", "Add unit and integration tests around APIs, business logic, and failure paths."),
        ("documentation_score", "Improve project documentation", "Documentation", "Documentation coverage can be improved.", "Medium", "Document setup, architecture, usage, and examples in the README."),
        ("maintainability_score", "Improve maintainability", "Maintainability", "Maintainability indicators show room for refactoring.", "Medium", "Split large functions/modules and reduce duplicated or overly complex logic."),
        ("architecture_score", "Improve project architecture", "Architecture", "The detected module structure is incomplete.", "Medium", "Keep API, business logic, data access, and utilities separated."),
        ("code_quality_score", "Address code-quality issues", "Code Quality", "Static code-quality findings were detected.", "Medium", "Fix the highest-severity smells first and keep functions focused."),
        ("ci_cd_score", "Add CI/CD automation", "CI/CD", "No sufficient CI/CD automation was detected.", "Medium", "Run tests, linting, and builds automatically on pull requests."),
        ("license_score", "Add a project license", "License", "A suitable license was not detected.", "Medium", "Choose an appropriate license and add a LICENSE file."),
        ("community_score", "Improve contribution readiness", "Community", "Community contribution files are incomplete.", "Low", "Add contribution and community guidance."),
        ("configuration_score", "Improve configuration hygiene", "Configuration", "Configuration management can be improved.", "Medium", "Keep environment-specific secrets outside source code and provide safe examples."),
    ]
    for key,title,category,description,priority,action in rules:
        score=_score(analysis,key)
        if score < 70:
            recommendations.append(_recommendation(title,description,priority,category,[f"{category} score: {score:.1f}/100"],action))

    complexity=analysis.get("complexity",{}) or {}
    if complexity.get("complexity_level") in {"High","Very High"}:
        recommendations.append(_recommendation("Reduce cyclomatic complexity","Several functions contain high branching complexity.","High","Maintainability",
            [f"Complexity level: {complexity.get('complexity_level')}",f"Average complexity: {complexity.get('average_cyclomatic_complexity',0)}"],
            "Extract decision-heavy logic and simplify nested conditionals."))
    largest=analysis.get("largest_file_lines",0) or 0
    if largest>300:
        recommendations.append(_recommendation("Split large source files","A source file is large enough to make maintenance harder.","Medium","Maintainability",
            [f"Largest file: {analysis.get('largest_file','unknown')}",f"Lines: {largest}"],"Split the file by responsibility into smaller modules."))

    unique={}
    order={"High":0,"Medium":1,"Low":2}
    for item in recommendations:
        unique[(item["category"],item["title"].lower())]=item
    return sorted(unique.values(),key=lambda x:(order.get(x["priority"],9),x["category"],x["title"]))


def generate_recommendations(analysis):
    normalized=dict(analysis or {})
    for key in ("security","secret_exposure","tests","documentation","maintainability","architecture","code_quality","ci_cd","license","community","configuration","repository_metrics"):
        if key in normalized and f"{key}_score" not in normalized:
            normalized[f"{key}_score"]=normalized[key]
    return generate_ai_recommendations(normalized)
