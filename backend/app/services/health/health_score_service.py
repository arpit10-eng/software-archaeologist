from app.services.health.score_calculators import (
    calculate_security_score,
    calculate_testing_score,
    calculate_documentation_score,
    calculate_maintainability_score,
    calculate_architecture_score,
    calculate_ci_cd_score,
    calculate_community_score,
    calculate_license_score,
    calculate_configuration_score,
    calculate_secret_exposure_score,
    calculate_repository_metrics_score,
    calculate_code_quality_score,
)


def calculate_health_score(
    security_summary=None,
    tests=None,
    code_smells=None,
    complexity=None,
    documentation=None,
    maintainability=None,
    architecture=None,
    ci_cd=None,
    community=None,
    license_data=None,
    configuration=None,
    secret_exposure=None,
    repository_metrics=None,
):
    """
    Calculate the overall health score of a repository.

    Each category produces a score between 0 and its maximum.
    The final score is normalized to 100.
    """

    security_summary = security_summary or {}
    tests = tests or {}
    code_smells = code_smells or []
    complexity = complexity or {}
    documentation = documentation or {}
    maintainability = maintainability or {}
    architecture = architecture or {}
    ci_cd = ci_cd or {}
    community = community or {}
    license_data = license_data or {}
    configuration = configuration or {}
    secret_exposure = secret_exposure or {}
    repository_metrics = repository_metrics or {}

    breakdown = {}

    # ---------------------------------------------------------
    # Individual category scores
    # ---------------------------------------------------------

    breakdown["security"] = calculate_security_score(
        security_summary
    )

    breakdown["tests"] = calculate_testing_score(
        tests
    )

    breakdown["documentation"] = calculate_documentation_score(
        documentation
    )

    breakdown["maintainability"] = calculate_maintainability_score(
        maintainability
    )

    breakdown["architecture"] = calculate_architecture_score(
        architecture
    )

    breakdown["ci_cd"] = calculate_ci_cd_score(
        ci_cd
    )

    breakdown["community"] = calculate_community_score(
        community
    )

    breakdown["license"] = calculate_license_score(
        license_data
    )

    breakdown["configuration"] = calculate_configuration_score(
        configuration
    )

    breakdown["secret_exposure"] = calculate_secret_exposure_score(
        secret_exposure
    )

    breakdown["repository_metrics"] = calculate_repository_metrics_score(
        repository_metrics
    )

    breakdown["code_quality"] = calculate_code_quality_score(
        code_smells,
        complexity
    )

    # ---------------------------------------------------------
    # Maximum possible score
    # ---------------------------------------------------------

    max_scores = {
        "security": 15,
        "tests": 10,
        "documentation": 10,
        "maintainability": 10,
        "architecture": 10,
        "ci_cd": 10,
        "community": 5,
        "license": 10,
        "configuration": 5,
        "secret_exposure": 5,
        "repository_metrics": 5,
        "code_quality": 10,
    }

    total_score = sum(breakdown.values())
    maximum_score = sum(max_scores.values())

    # Normalize to 100
    overall_score = (
        round((total_score / maximum_score) * 100, 2)
        if maximum_score > 0
        else 0
    )

    return {
        "overall_score": overall_score,
        "health_level": calculate_health_level(overall_score),
        "breakdown": breakdown,
    }


def calculate_health_level(score):
    """
    Convert numerical health score into a readable health level.
    """

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Good"

    if score >= 60:
        return "Fair"

    if score >= 40:
        return "Needs Improvement"

    return "Poor"