def calculate_security_score(security_summary):
    """
    Maximum score: 15
    """

    if not isinstance(security_summary, dict):
        return 0

    total = security_summary.get("total_issues", 0)
    critical = security_summary.get("critical", 0)
    high = security_summary.get("high", 0)
    medium = security_summary.get("medium", 0)
    low = security_summary.get("low", 0)

    penalty = (
        critical * 5
        + high * 3
        + medium * 1
        + low * 0.5
    )

    score = max(0, 15 - penalty)

    return round(score)


# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

def calculate_testing_score(tests):
    """
    Maximum score: 10
    """

    if not isinstance(tests, dict):
        return 0

    quality = tests.get("test_quality", {})

    if not isinstance(quality, dict):
        return 0

    score = quality.get("score", 0)

    try:
        score = float(score)
    except (TypeError, ValueError):
        return 0

    return round(max(0, min(score, 100)) / 100 * 10)


# ---------------------------------------------------------
# Documentation
# ---------------------------------------------------------

def calculate_documentation_score(documentation):
    """
    Maximum score: 10
    """

    if not isinstance(documentation, dict):
        return 0

    quality = documentation.get(
        "documentation_quality",
        {}
    )

    if not isinstance(quality, dict):
        return 0

    score = quality.get("score", 0)

    try:
        score = float(score)
    except (TypeError, ValueError):
        return 0

    return round(max(0, min(score, 100)) / 100 * 10)


# ---------------------------------------------------------
# Maintainability
# ---------------------------------------------------------

def calculate_maintainability_score(maintainability):
    """
    Maximum score: 10
    """

    if not isinstance(maintainability, dict):
        return 0

    excellent = maintainability.get("excellent", 0)
    good = maintainability.get("good", 0)
    poor = maintainability.get("poor", 0)
    worst = maintainability.get("worst", 0)

    total = excellent + good + poor + worst

    if total == 0:
        return 0

    score = (
        excellent * 1
        + good * 0.75
        + poor * 0.4
        + worst * 0.1
    )

    percentage = score / total

    return round(percentage * 10)


# ---------------------------------------------------------
# Architecture
# ---------------------------------------------------------

def calculate_architecture_score(architecture):
    """
    Maximum score: 10
    """

    if not isinstance(architecture, dict):
        return 0

    score = 0

    if architecture.get("models"):
        score += 2

    if architecture.get("services"):
        score += 2

    if architecture.get("database"):
        score += 2

    if architecture.get("tests"):
        score += 2

    if architecture.get("utils"):
        score += 2

    return min(score, 10)


# ---------------------------------------------------------
# CI/CD
# ---------------------------------------------------------

def calculate_ci_cd_score(ci_cd):
    """
    Maximum score: 10
    """

    if not isinstance(ci_cd, dict):
        return 0

    if ci_cd.get("github_actions"):
        return 10

    return 0


# ---------------------------------------------------------
# Community
# ---------------------------------------------------------

def calculate_community_score(community):
    """
    Maximum score: 5
    """

    if not isinstance(community, dict):
        return 0

    score = 0

    if community.get("contributing"):
        score += 1

    if community.get("code_of_conduct"):
        score += 1

    if community.get("issue_templates"):
        score += 1

    if community.get("pull_request_template"):
        score += 1

    if (
        community.get("contributing")
        and community.get("code_of_conduct")
    ):
        score += 1

    return min(score, 5)


# ---------------------------------------------------------
# License
# ---------------------------------------------------------

def calculate_license_score(license_data):
    """
    Maximum score: 10

    GitHub license data normally looks similar to:

    {
        "key": "mit",
        "name": "MIT License",
        "spdx_id": "MIT"
    }
    """

    if not isinstance(license_data, dict):
        return 0

    if not license_data:
        return 0

    spdx_id = license_data.get("spdx_id")

    if spdx_id and spdx_id != "NOASSERTION":
        return 10

    license_key = license_data.get("key")

    if license_key:
        return 8

    license_name = license_data.get("name")

    if license_name:
        return 8

    return 0


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

def calculate_configuration_score(configuration):
    """
    Maximum score: 5
    """

    if not isinstance(configuration, dict):
        return 0

    score = 0

    if configuration.get("environment_files"):
        score += 2

    if configuration.get("config_files"):
        score += 2

    if configuration.get("env_example_found"):
        score += 1

    return min(score, 5)


# ---------------------------------------------------------
# Secret Exposure
# ---------------------------------------------------------

def calculate_secret_exposure_score(secret_exposure):
    """
    Maximum score: 5

    More exposed sensitive files means a lower score.
    """

    if not isinstance(secret_exposure, dict):
        return 0

    score = 5

    sensitive_count = secret_exposure.get(
        "sensitive_file_count",
        0
    )

    try:
        sensitive_count = int(sensitive_count)
    except (TypeError, ValueError):
        sensitive_count = 0

    if sensitive_count > 0:
        score -= min(sensitive_count, 5)

    return max(score, 0)


# ---------------------------------------------------------
# Repository Metrics
# ---------------------------------------------------------

def calculate_repository_metrics_score(repository_metrics):
    """
    Maximum score: 5
    """

    if not isinstance(repository_metrics, dict):
        return 0

    score = 0

    python_files = repository_metrics.get(
        "python_files",
        0
    )

    directories = repository_metrics.get(
        "directories",
        0
    )

    average_file_size = repository_metrics.get(
        "average_file_size",
        0
    )

    if python_files > 0:
        score += 2

    if directories > 1:
        score += 1

    if average_file_size < 10000:
        score += 2

    return min(score, 5)


# ---------------------------------------------------------
# Code Quality
# ---------------------------------------------------------

def calculate_code_quality_score(
    code_smells,
    complexity
):
    """
    Maximum score: 10
    """

    score = 10

    # ---------------------------------------------
    # Code smells
    # ---------------------------------------------

    if isinstance(code_smells, list):

        for smell in code_smells:

            if not isinstance(smell, dict):
                continue

            severity = str(
                smell.get("severity", "")
            ).lower()

            if severity == "high":
                score -= 2

            elif severity == "medium":
                score -= 1

            elif severity == "low":
                score -= 0.5

    # ---------------------------------------------
    # Complexity
    # ---------------------------------------------

    if isinstance(complexity, dict):

        level = str(
            complexity.get(
                "complexity_level",
                ""
            )
        ).lower()

        if level == "high":
            score -= 3

        elif level == "medium":
            score -= 1

    return max(0, round(score))


# ---------------------------------------------------------
# Health Level
# ---------------------------------------------------------

def calculate_health_level(score):

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Good"

    if score >= 60:
        return "Fair"

    if score >= 40:
        return "Needs Improvement"

    return "Poor"