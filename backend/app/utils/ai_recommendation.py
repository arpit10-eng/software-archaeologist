import os


def _recommendation(
    title,
    description,
    priority="Medium",
    category="General",
    evidence=None,
):
    return {
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "evidence": evidence or [],
    }


def generate_ai_recommendations(analysis):
    recommendations = []

    # ---------------------------------------------------------
    # SECURITY
    # ---------------------------------------------------------

    security_score = analysis.get("security_score", 100)

    if security_score < 70:
        recommendations.append(
            _recommendation(
                title="Improve repository security",
                description=(
                    "The repository has security weaknesses. "
                    "Review sensitive configuration, subprocess usage, "
                    "input validation, and exposed credentials."
                ),
                priority="High",
                category="Security",
                evidence=[
                    f"Security score: {security_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # SECRET EXPOSURE
    # ---------------------------------------------------------

    secret_exposure_score = analysis.get(
        "secret_exposure_score",
        0,
    )

    if secret_exposure_score > 0:
        recommendations.append(
            _recommendation(
                title="Review possible secret exposure",
                description=(
                    "Potential credentials or sensitive configuration "
                    "may be present in repository files. Move secrets "
                    "to environment variables or a secure secret manager."
                ),
                priority="High",
                category="Security",
                evidence=[
                    f"Secret exposure score: {secret_exposure_score}"
                ],
            )
        )

    # ---------------------------------------------------------
    # TESTING
    # ---------------------------------------------------------

    tests_score = analysis.get("tests_score", 100)

    if tests_score < 70:
        recommendations.append(
            _recommendation(
                title="Add automated tests",
                description=(
                    "The repository has limited test coverage or testing "
                    "infrastructure. Add unit and integration tests for "
                    "important application components."
                ),
                priority="High",
                category="Testing",
                evidence=[
                    f"Testing score: {tests_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # DOCUMENTATION
    # ---------------------------------------------------------

    documentation_score = analysis.get(
        "documentation_score",
        100,
    )

    if documentation_score < 70:
        recommendations.append(
            _recommendation(
                title="Improve project documentation",
                description=(
                    "Improve the README and project documentation with "
                    "setup instructions, architecture information, "
                    "usage examples, and contribution guidelines."
                ),
                priority="Medium",
                category="Documentation",
                evidence=[
                    f"Documentation score: {documentation_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # MAINTAINABILITY
    # ---------------------------------------------------------

    maintainability_score = analysis.get(
        "maintainability_score",
        100,
    )

    if maintainability_score < 70:
        recommendations.append(
            _recommendation(
                title="Improve code maintainability",
                description=(
                    "The repository contains maintainability concerns. "
                    "Consider breaking large modules into smaller components, "
                    "reducing duplicated logic, and improving separation "
                    "of responsibilities."
                ),
                priority="Medium",
                category="Maintainability",
                evidence=[
                    f"Maintainability score: {maintainability_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # ARCHITECTURE
    # ---------------------------------------------------------

    architecture_score = analysis.get(
        "architecture_score",
        100,
    )

    if architecture_score < 70:
        recommendations.append(
            _recommendation(
                title="Improve project architecture",
                description=(
                    "The repository has architectural weaknesses. "
                    "Review module responsibilities and maintain clear "
                    "separation between API, business logic, utilities, "
                    "database, and external services."
                ),
                priority="Medium",
                category="Architecture",
                evidence=[
                    f"Architecture score: {architecture_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # CODE QUALITY
    # ---------------------------------------------------------

    code_quality_score = analysis.get(
        "code_quality_score",
        100,
    )

    if code_quality_score < 70:
        recommendations.append(
            _recommendation(
                title="Improve code quality",
                description=(
                    "Code-quality issues were detected. Refactor complex "
                    "functions, improve naming, remove unnecessary code, "
                    "and introduce consistent coding practices."
                ),
                priority="Medium",
                category="Code Quality",
                evidence=[
                    f"Code quality score: {code_quality_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # CI/CD
    # ---------------------------------------------------------

    ci_cd_score = analysis.get(
        "ci_cd_score",
        100,
    )

    if ci_cd_score < 70:
        recommendations.append(
            _recommendation(
                title="Add CI/CD automation",
                description=(
                    "The repository does not have sufficient CI/CD "
                    "automation. Add automated testing, linting, and "
                    "build checks using a CI pipeline."
                ),
                priority="Medium",
                category="CI/CD",
                evidence=[
                    f"CI/CD score: {ci_cd_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # LICENSE
    # ---------------------------------------------------------

    license_score = analysis.get(
        "license_score",
        100,
    )

    if license_score < 70:
        recommendations.append(
            _recommendation(
                title="Add an open-source license",
                description=(
                    "No suitable license was detected. Add an appropriate "
                    "LICENSE file to clearly define how others can use "
                    "and distribute the project."
                ),
                priority="Medium",
                category="Community",
                evidence=[
                    f"License score: {license_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # COMMUNITY
    # ---------------------------------------------------------

    community_score = analysis.get(
        "community_score",
        100,
    )

    if community_score < 70:
        recommendations.append(
            _recommendation(
                title="Improve community documentation",
                description=(
                    "Add contribution guidelines and community files "
                    "such as CONTRIBUTING.md and CODE_OF_CONDUCT.md "
                    "to make the repository easier to contribute to."
                ),
                priority="Low",
                category="Community",
                evidence=[
                    f"Community score: {community_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # CONFIGURATION
    # ---------------------------------------------------------

    configuration_score = analysis.get(
        "configuration_score",
        100,
    )

    if configuration_score < 70:
        recommendations.append(
            _recommendation(
                title="Improve project configuration",
                description=(
                    "Review project configuration files and keep "
                    "environment-specific settings outside the source code."
                ),
                priority="Medium",
                category="Configuration",
                evidence=[
                    f"Configuration score: {configuration_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # REPOSITORY METRICS
    # ---------------------------------------------------------

    repository_metrics_score = analysis.get(
        "repository_metrics_score",
        100,
    )

    if repository_metrics_score < 70:
        recommendations.append(
            _recommendation(
                title="Improve repository organization",
                description=(
                    "The repository structure or repository-level metrics "
                    "indicate areas that could be improved. Review unused "
                    "files, generated files, project organization, and "
                    "repository hygiene."
                ),
                priority="Low",
                category="Repository",
                evidence=[
                    f"Repository metrics score: "
                    f"{repository_metrics_score}/100"
                ],
            )
        )

    # ---------------------------------------------------------
    # COMPLEXITY
    # ---------------------------------------------------------

    complexity = analysis.get("complexity", {})

    if isinstance(complexity, dict):
        complexity_level = complexity.get(
            "complexity_level",
            "",
        )

        total_complexity = complexity.get(
            "total_cyclomatic_complexity",
            0,
        )

        if complexity_level in {
            "High",
            "Very High",
        }:
            recommendations.append(
                _recommendation(
                    title="Reduce code complexity",
                    description=(
                        "The repository contains highly complex code. "
                        "Break large functions into smaller units and "
                        "simplify deeply nested conditional logic."
                    ),
                    priority="High",
                    category="Maintainability",
                    evidence=[
                        f"Complexity level: {complexity_level}",
                        f"Total cyclomatic complexity: {total_complexity}",
                    ],
                )
            )

    # ---------------------------------------------------------
    # LARGE FILES
    # ---------------------------------------------------------

    largest_file = analysis.get("largest_file")

    largest_file_lines = analysis.get(
        "largest_file_lines",
        0,
    )

    if largest_file and largest_file_lines > 300:
        recommendations.append(
            _recommendation(
                title="Split large source files",
                description=(
                    f"{os.path.basename(largest_file)} is relatively large. "
                    "Consider splitting it into smaller modules with "
                    "focused responsibilities."
                ),
                priority="Medium",
                category="Maintainability",
                evidence=[
                    f"File: {largest_file}",
                    f"Lines: {largest_file_lines}",
                ],
            )
        )

    # ---------------------------------------------------------
    # DEPENDENCIES
    # ---------------------------------------------------------

    dependencies = analysis.get(
        "dependencies",
        [],
    )

    if isinstance(dependencies, list) and len(dependencies) > 30:
        recommendations.append(
            _recommendation(
                title="Review project dependencies",
                description=(
                    "The project has a large dependency set. Remove "
                    "unused dependencies and periodically review "
                    "dependency versions for security and maintenance."
                ),
                priority="Low",
                category="Dependencies",
                evidence=[
                    f"Detected dependencies: {len(dependencies)}"
                ],
            )
        )

    # ---------------------------------------------------------
    # DEDUPLICATE
    # ---------------------------------------------------------

    unique_recommendations = {}

    for recommendation in recommendations:
        key = (
            recommendation["category"],
            recommendation["title"].lower(),
        )

        if key not in unique_recommendations:
            unique_recommendations[key] = recommendation

    recommendations = list(
        unique_recommendations.values()
    )

    # ---------------------------------------------------------
    # PRIORITY ORDER
    # ---------------------------------------------------------

    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2,
    }

    recommendations.sort(
        key=lambda recommendation: (
            priority_order.get(
                recommendation["priority"],
                99,
            ),
            recommendation["category"],
            recommendation["title"],
        )
    )

    return recommendations


def generate_recommendations(analysis):
    """
    Compatibility wrapper for the test suite.

    The analyzer normally uses generate_ai_recommendations().
    The tests use the shorter category names such as:

        security
        tests
        documentation

    Convert those keys into the internal *_score representation.
    """

    score_keys = [
        "security",
        "secret_exposure",
        "tests",
        "documentation",
        "maintainability",
        "architecture",
        "code_quality",
        "ci_cd",
        "license",
        "community",
        "configuration",
        "repository_metrics",
    ]

    normalized_analysis = dict(analysis)

    for key in score_keys:
        if key in analysis:
            normalized_analysis[f"{key}_score"] = analysis[key]

    return generate_ai_recommendations(
        normalized_analysis
    )