def calculate_health_score(
    framework,
    entry_point,
    dependencies,
    architecture,
    security_issues=None,
    tests=None,
    code_smells=None,
    documentation=None,
    maintainability=None,
    circular_dependencies=None,
    ci_cd=None,
    community=None,
    license=None,
    configuration=None,
    secret_exposure=None,
    repository_metrics=None
):
    """
    Calculate repository health score.

    Health Score 2.0
    Final score: 0 - 100

    Score Breakdown:

    Security           = 20
    Testing            = 15
    Code Quality       = 15
    Documentation     = 10
    Maintainability    = 10
    Architecture       = 10
    CI/CD              = 5
    Community          = 5
    License            = 3
    Configuration      = 4
    Secret Exposure    = 3
    Repository Metrics = 0

    Total = 100
    """

    # =========================================================
    # DEFAULT VALUES
    # =========================================================

    security_issues = security_issues or []
    tests = tests or {}
    code_smells = code_smells or []
    documentation = documentation or {}
    maintainability = maintainability or {}
    circular_dependencies = circular_dependencies or {}
    ci_cd = ci_cd or {}
    community = community or {}
    license = license or {}
    configuration = configuration or {}
    secret_exposure = secret_exposure or {}
    repository_metrics = repository_metrics or {}

    # =========================================================
    # 1. SECURITY SCORE - 20 POINTS
    # =========================================================

    security_score = 20

    for issue in security_issues:

        severity = str(
            issue.get("severity", "")
        ).lower()

        if severity == "critical":
            security_score -= 8

        elif severity == "high":
            security_score -= 6

        elif severity == "medium":
            security_score -= 3

        elif severity == "low":
            security_score -= 1

    security_score = max(
        0,
        min(20, security_score)
    )

    # =========================================================
    # 2. TESTING SCORE - 15 POINTS
    # =========================================================

    test_quality = tests.get(
        "test_quality",
        {}
    )

    test_quality_score = test_quality.get(
        "score"
    )

    if test_quality_score is not None:

        testing_score = round(
            (test_quality_score / 100) * 15
        )

    else:

        test_files = tests.get(
            "test_file_count",
            0
        )

        test_functions = tests.get(
            "test_function_count",
            0
        )

        if test_files > 0 and test_functions > 0:

            testing_score = 15

        elif test_files > 0:

            testing_score = 8

        else:

            testing_score = 0

    testing_score = max(
        0,
        min(15, testing_score)
    )

    # =========================================================
    # 3. CODE QUALITY SCORE - 15 POINTS
    # =========================================================

    code_quality_score = 15

    for smell in code_smells:

        severity = str(
            smell.get("severity", "")
        ).lower()

        if severity == "critical":
            code_quality_score -= 6

        elif severity == "high":
            code_quality_score -= 5

        elif severity == "medium":
            code_quality_score -= 3

        elif severity == "low":
            code_quality_score -= 1

    code_quality_score = max(
        0,
        min(15, code_quality_score)
    )

    # =========================================================
    # 4. DOCUMENTATION SCORE - 10 POINTS
    # =========================================================

    documentation_quality = documentation.get(
        "documentation_quality",
        {}
    )

    documentation_raw_score = documentation_quality.get(
        "score",
        0
    )

    documentation_score = round(
        (documentation_raw_score / 100) * 10
    )

    documentation_score = max(
        0,
        min(10, documentation_score)
    )

    # =========================================================
    # 5. MAINTAINABILITY SCORE - 10 POINTS
    # =========================================================

    excellent = maintainability.get(
        "excellent",
        0
    )

    good = maintainability.get(
        "good",
        0
    )

    poor = maintainability.get(
        "poor",
        0
    )

    total_files = (
        excellent
        + good
        + poor
    )

    if total_files > 0:

        maintainability_percentage = (
            excellent
            + (good * 0.7)
            + (poor * 0.3)
        ) / total_files

        maintainability_score = round(
            maintainability_percentage * 10
        )

    else:

        maintainability_score = 0

    maintainability_score = max(
        0,
        min(10, maintainability_score)
    )

    # =========================================================
    # 6. ARCHITECTURE SCORE - 10 POINTS
    # =========================================================

    architecture_score = 10

    if not framework:
        architecture_score -= 2

    if not entry_point:
        architecture_score -= 2

    if not dependencies:
        architecture_score -= 2

    if not architecture:
        architecture_score -= 2

    if circular_dependencies.get(
        "found",
        False
    ):
        architecture_score -= 4

    architecture_score = max(
        0,
        min(10, architecture_score)
    )

    # =========================================================
    # 7. CI/CD SCORE - 5 POINTS
    # =========================================================

    if ci_cd.get(
        "github_actions",
        False
    ):

        ci_cd_score = 5

    else:

        ci_cd_score = 0

    # =========================================================
    # 8. COMMUNITY SCORE - 5 POINTS
    # =========================================================

    community_score = 0

    if community.get(
        "contributing",
        False
    ):
        community_score += 1

    if community.get(
        "code_of_conduct",
        False
    ):
        community_score += 1

    if community.get(
        "issue_templates"
    ):
        community_score += 1

    if community.get(
        "pull_request_template",
        False
    ):
        community_score += 1

    # Bonus point if the project has at least
    # one community feature.

    if community_score > 0:
        community_score += 1

    community_score = min(
        5,
        community_score
    )

    # =========================================================
    # 9. LICENSE SCORE - 3 POINTS
    # =========================================================

    license_found = license.get(
        "license_found",
        False
    )

    # Support analyzer output where license_found
    # may not exist but license_files does.

    if not license_found:

        license_file_count = license.get(
            "license_file_count",
            0
        )

        license_files = license.get(
            "license_files",
            []
        )

        if (
            license_file_count > 0
            or len(license_files) > 0
        ):
            license_found = True

    if license_found:

        license_score = 3

    else:

        license_score = 0

    # =========================================================
    # 10. CONFIGURATION SCORE - 4 POINTS
    # =========================================================

    configuration_score = 0

    config_files = configuration.get(
        "config_file_count",
        0
    )

    environment_files = configuration.get(
        "environment_file_count",
        0
    )

    env_example_found = configuration.get(
        "env_example_found",
        False
    )

    if config_files > 0:
        configuration_score += 2

    if environment_files > 0:
        configuration_score += 1

    if env_example_found:
        configuration_score += 1

    configuration_score = min(
        4,
        configuration_score
    )

    # =========================================================
    # 11. SECRET EXPOSURE SCORE - 3 POINTS
    # =========================================================

    secret_exposure_score = 3

    sensitive_file_count = secret_exposure.get(
        "sensitive_file_count",
        0
    )

    gitignore_found = secret_exposure.get(
        "gitignore_found",
        False
    )

    # Sensitive files are a serious security problem.

    if sensitive_file_count > 0:

        secret_exposure_score -= 3

    # Missing .gitignore is also a security risk.

    if not gitignore_found:

        secret_exposure_score -= 1

    secret_exposure_score = max(
        0,
        min(3, secret_exposure_score)
    )

    # =========================================================
    # 12. REPOSITORY METRICS SCORE - 0 POINTS
    # =========================================================

    # Repository metrics are displayed for analysis,
    # but currently do not affect the health score.
    #
    # This prevents large repositories from being
    # unfairly penalized.
    #
    # Therefore this remains 0.

    repository_metrics_score = 0

    # =========================================================
    # FINAL HEALTH SCORE
    # =========================================================

    total_score = (
        security_score
        + testing_score
        + code_quality_score
        + documentation_score
        + maintainability_score
        + architecture_score
        + ci_cd_score
        + community_score
        + license_score
        + configuration_score
        + secret_exposure_score
    )

    # =========================================================
    # LIMIT SCORE TO 100
    # =========================================================

    total_score = max(
        0,
        min(100, total_score)
    )

    # =========================================================
    # HEALTH LEVEL
    # =========================================================

    if total_score >= 90:

        level = "Excellent"

    elif total_score >= 75:

        level = "Good"

    elif total_score >= 50:

        level = "Fair"

    else:

        level = "Poor"

    # =========================================================
    # RETURN RESULT
    # =========================================================

    return {

        "score": total_score,

        "level": level,

        "breakdown": {

            "security": security_score,

            "testing": testing_score,

            "code_quality": code_quality_score,

            "documentation": documentation_score,

            "maintainability": maintainability_score,

            "architecture": architecture_score,

            "ci_cd": ci_cd_score,

            "community": community_score,

            "license": license_score,

            "configuration": configuration_score,

            "secret_exposure": secret_exposure_score,

            "repository_metrics": repository_metrics_score
        }
    }