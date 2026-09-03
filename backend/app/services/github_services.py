import json
import os
import tempfile
from urllib.parse import urlparse

import requests
from fastapi import HTTPException

from app.database.database import SessionLocal
from app.database.models import RepositoryAnalysis

from app.services.git_services import clone_repository
from app.services.file_services import scan_repository

from app.utils.validators import is_valid_github_url
from app.utils.framework_detector import detect_framework
from app.utils.entry_point_detector import detect_entry_point
from app.utils.dependency_detector import detect_dependencies
from app.utils.language_detector import detect_language
from app.utils.architecture_detector import detect_architecture
from app.utils.summary_generator import generate_summary

from app.services.health.health_score_service import calculate_health_score

from app.utils.api_detector import detect_api_endpoints
from app.utils.code_structure_detector import detect_code_structure
from app.utils.dependency_graph import detect_dependency_graph
from app.utils.complexity_analyzer import analyze_complexity
from app.utils.circular_dependency import detect_circular_dependencies
from app.utils.quality_report import generate_quality_report
from app.utils.security_analyzer import analyze_security
from app.utils.security_summary import generate_security_summary
from app.utils.repository_metrics import generate_repository_metrics
from app.utils.code_smell_detector import detect_code_smells
from app.utils.dead_code_detector import detect_dead_code
from app.utils.maintainability_analyzer import generate_maintainability
from app.utils.ai_recommendation import generate_ai_recommendations
from app.utils.documentation_analyzer import analyze_documentation
from app.utils.size_analyzer import analyze_repository_size
from app.utils.test_analyzer import analyze_tests
from app.utils.license_analyzer import analyze_license
from app.utils.ci_cd_analyzer import analyze_ci_cd
from app.utils.community_analyzer import analyze_community
from app.utils.config_analyzer import analyze_configuration
from app.utils.secret_exposure_analyzer import analyze_secret_exposure


# =============================================================
# Helper Functions
# =============================================================

def _get_repository_url(repo):
    """
    Accept either:

    1. A plain GitHub URL string
    2. An object containing github_url
    """

    if isinstance(repo, str):
        return repo

    github_url = getattr(
        repo,
        "github_url",
        None,
    )

    if github_url:
        return github_url

    raise HTTPException(
        status_code=400,
        detail="GitHub repository URL is required.",
    )


def _get_branch(repo):
    """
    Get repository branch.

    If no branch is supplied, main is used.
    """

    if isinstance(repo, str):
        return "main"

    branch = getattr(
        repo,
        "branch",
        None,
    )

    return branch or "main"


def _clamp(value, minimum, maximum):
    """
    Keep a value inside a defined range.
    """

    try:
        value = float(value)
    except (
        TypeError,
        ValueError,
    ):
        return minimum

    return max(
        minimum,
        min(
            value,
            maximum,
        ),
    )


def _percentage_to_weighted_score(
    percentage,
    maximum,
):
    """
    Convert a 0-100 quality percentage into
    the weighted score for a health category.

    Example:

        80% with maximum 10
        -> 8 points
    """

    percentage = _clamp(
        percentage,
        0,
        100,
    )

    return round(
        (percentage / 100) * maximum,
        2,
    )


# =============================================================
# Health Category Scoring
# =============================================================

def _calculate_security_score(
    security_summary,
    maximum=15,
):
    """
    Convert security severity counts into a weighted score.

    No issues = full score.

    Critical issues receive the largest penalty,
    followed by high, medium and low issues.
    """

    if not isinstance(
        security_summary,
        dict,
    ):
        return 0

    critical = int(
        security_summary.get(
            "critical",
            0,
        )
        or 0
    )

    high = int(
        security_summary.get(
            "high",
            0,
        )
        or 0
    )

    medium = int(
        security_summary.get(
            "medium",
            0,
        )
        or 0
    )

    low = int(
        security_summary.get(
            "low",
            0,
        )
        or 0
    )

    penalty = (
        critical * 5
        + high * 3
        + medium * 1
        + low * 0.5
    )

    score = maximum - penalty

    return round(
        _clamp(
            score,
            0,
            maximum,
        ),
        2,
    )


def _calculate_tests_score(
    tests,
    maximum=10,
):
    """
    Convert the test analyzer's 0-100 quality score
    into the weighted health score.
    """

    if not isinstance(
        tests,
        dict,
    ):
        return 0

    quality = tests.get(
        "test_quality",
        {},
    )

    if not isinstance(
        quality,
        dict,
    ):
        return 0

    percentage = quality.get(
        "score",
        0,
    )

    return _percentage_to_weighted_score(
        percentage,
        maximum,
    )


def _calculate_documentation_score(
    documentation,
    maximum=10,
):
    """
    Convert documentation quality into
    the weighted health score.
    """

    if not isinstance(
        documentation,
        dict,
    ):
        return 0

    quality = documentation.get(
        "documentation_quality",
        {},
    )

    if not isinstance(
        quality,
        dict,
    ):
        return 0

    percentage = quality.get(
        "score",
        0,
    )

    return _percentage_to_weighted_score(
        percentage,
        maximum,
    )


def _calculate_maintainability_score(
    maintainability,
    maximum=10,
):
    """
    Calculate maintainability from the number
    of excellent, good and poor Python files.
    """

    if not isinstance(
        maintainability,
        dict,
    ):
        return 0

    excellent = int(
        maintainability.get(
            "excellent",
            0,
        )
        or 0
    )

    good = int(
        maintainability.get(
            "good",
            0,
        )
        or 0
    )

    poor = int(
        maintainability.get(
            "poor",
            0,
        )
        or 0
    )

    total = (
        excellent
        + good
        + poor
    )

    if total == 0:
        return 0

    percentage = (
        (
            excellent * 100
            + good * 75
            + poor * 30
        )
        / total
    )

    return _percentage_to_weighted_score(
        percentage,
        maximum,
    )


def _calculate_architecture_score(
    architecture,
    maximum=10,
):
    """
    Score architecture based on the number of
    recognized architectural components.

    Recognized categories include:

        models
        services
        routers
        controllers
        database
        middleware
        config
        tests
        utils
    """

    if not isinstance(
        architecture,
        dict,
    ):
        return 0

    component_count = len(
        architecture
    )

    if component_count == 0:
        return 0

    # Five or more meaningful architectural
    # categories receives full score.
    percentage = min(
        component_count / 5,
        1,
    ) * 100

    return _percentage_to_weighted_score(
        percentage,
        maximum,
    )


def _calculate_ci_cd_score(
    ci_cd,
    maximum=10,
):
    """
    Score CI/CD based on GitHub Actions workflow presence.
    """

    if not isinstance(
        ci_cd,
        dict,
    ):
        return 0

    workflow_count = int(
        ci_cd.get(
            "workflow_count",
            0,
        )
        or 0
    )

    if workflow_count == 0:
        return 0

    # Having at least one workflow means
    # the repository has CI/CD infrastructure.
    return maximum


def _calculate_community_score(
    community,
    maximum=5,
):
    """
    Score community readiness based on:

        CONTRIBUTING.md
        CODE_OF_CONDUCT.md
        issue templates
        pull request template
    """

    if not isinstance(
        community,
        dict,
    ):
        return 0

    checks = 0

    if community.get(
        "contributing",
        False,
    ):
        checks += 1

    if community.get(
        "code_of_conduct",
        False,
    ):
        checks += 1

    if int(
        community.get(
            "issue_template_count",
            0,
        )
        or 0
    ) > 0:
        checks += 1

    if community.get(
        "pull_request_template",
        False,
    ):
        checks += 1

    percentage = (
        checks / 4
    ) * 100

    return _percentage_to_weighted_score(
        percentage,
        maximum,
    )


def _calculate_license_score(
    license_info,
    maximum=10,
):
    """
    Score license quality.

    Recognized license = full score.
    License file with unknown type = partial score.
    Missing license = zero.
    """

    if not isinstance(
        license_info,
        dict,
    ):
        return 0

    status = str(
        license_info.get(
            "status",
            "",
        )
    ).lower()

    detected_license = str(
        license_info.get(
            "license",
            "Unknown",
        )
    ).lower()

    if status == "present" and detected_license != "unknown":
        return maximum

    if status == "unknown":
        return maximum * 0.5

    return 0


def _calculate_configuration_score(
    configuration,
    maximum=5,
):
    """
    Score repository configuration.

    A repository gets credit for:
        - configuration files
        - .env.example / sample environment files
    """

    if not isinstance(
        configuration,
        dict,
    ):
        return 0

    config_count = int(
        configuration.get(
            "config_file_count",
            0,
        )
        or 0
    )

    environment_count = int(
        configuration.get(
            "environment_file_count",
            0,
        )
        or 0
    )

    env_example = bool(
        configuration.get(
            "env_example_found",
            False,
        )
    )

    score = 0

    if config_count > 0:
        score += 60

    if environment_count > 0:
        score += 20

    if env_example:
        score += 20

    return _percentage_to_weighted_score(
        score,
        maximum,
    )


def _calculate_secret_exposure_score(
    secret_exposure,
    maximum=5,
):
    """
    Score secret exposure.

    No sensitive files = full score.

    Sensitive files reduce the score.
    A .gitignore also provides some protection.
    """

    if not isinstance(
        secret_exposure,
        dict,
    ):
        return 0

    sensitive_count = int(
        secret_exposure.get(
            "sensitive_file_count",
            0,
        )
        or 0
    )

    gitignore_found = bool(
        secret_exposure.get(
            "gitignore_found",
            False,
        )
    )

    # Start with a perfect score.
    score = float(maximum)

    # Strong penalty for exposed sensitive files.
    score -= sensitive_count * 2

    # A .gitignore provides a small positive
    # signal for repository hygiene.
    if gitignore_found and sensitive_count == 0:
        score = maximum

    return round(
        _clamp(
            score,
            0,
            maximum,
        ),
        2,
    )


def _calculate_repository_metrics_score(
    repository_metrics,
    files,
    maximum=5,
):
    """
    Score repository structure based on useful
    repository metrics.

    This is deliberately conservative because
    repository metrics are descriptive rather
    than direct quality measurements.
    """

    if not isinstance(
        repository_metrics,
        dict,
    ):
        return 0

    score = 0

    directory_count = int(
        repository_metrics.get(
            "directories",
            0,
        )
        or 0
    )

    python_files = int(
        repository_metrics.get(
            "python_files",
            0,
        )
        or 0
    )

    average_file_size = float(
        repository_metrics.get(
            "average_file_size",
            0,
        )
        or 0
    )

    # Basic repository structure.
    if directory_count > 0:
        score += 40

    # Source files exist.
    if python_files > 0:
        score += 30

    # Reasonable average file size.
    if average_file_size > 0:
        if average_file_size < 50000:
            score += 30
        elif average_file_size < 100000:
            score += 15

    return _percentage_to_weighted_score(
        score,
        maximum,
    )


def _calculate_code_quality_score(
    code_smells,
    maximum=10,
):
    """
    Convert code smell findings into a quality score.

    Fewer smells = higher quality.
    """

    if not isinstance(
        code_smells,
        list,
    ):
        return 0

    smell_count = len(
        code_smells
    )

    if smell_count == 0:
        percentage = 100

    elif smell_count <= 2:
        percentage = 85

    elif smell_count <= 5:
        percentage = 70

    elif smell_count <= 10:
        percentage = 50

    else:
        percentage = 25

    return _percentage_to_weighted_score(
        percentage,
        maximum,
    )


def _calculate_health_categories(
    security_summary,
    tests,
    documentation,
    maintainability,
    architecture,
    ci_cd,
    community,
    license_info,
    configuration,
    secret_exposure,
    repository_metrics,
    files,
    code_smells,
):
    """
    Convert the raw analyzer outputs into the exact
    weighted category scores expected by the
    health-score service.
    """

    return {
        "security": _calculate_security_score(
            security_summary
        ),

        "tests": _calculate_tests_score(
            tests
        ),

        "documentation": _calculate_documentation_score(
            documentation
        ),

        "maintainability": _calculate_maintainability_score(
            maintainability
        ),

        "architecture": _calculate_architecture_score(
            architecture
        ),

        "ci_cd": _calculate_ci_cd_score(
            ci_cd
        ),

        "community": _calculate_community_score(
            community
        ),

        "license": _calculate_license_score(
            license_info
        ),

        "configuration": _calculate_configuration_score(
            configuration
        ),

        "secret_exposure": _calculate_secret_exposure_score(
            secret_exposure
        ),

        "repository_metrics": _calculate_repository_metrics_score(
            repository_metrics,
            files,
        ),

        "code_quality": _calculate_code_quality_score(
            code_smells
        ),
    }


# =============================================================
# Main Repository Analyzer
# =============================================================

def analyze_repository(repo):

    # =========================================================
    # 1. Extract Repository Information
    # =========================================================

    repository_url = _get_repository_url(
        repo
    )

    branch = _get_branch(
        repo
    )

    # =========================================================
    # 2. Validate GitHub URL
    # =========================================================

    if not is_valid_github_url(
        repository_url
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL.",
        )

    # =========================================================
    # 3. Clone Repository
    # =========================================================

    with tempfile.TemporaryDirectory() as temp_dir:

        repo_name = (
            repository_url
            .rstrip("/")
            .split("/")[-1]
        )

        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        destination = os.path.join(
            temp_dir,
            repo_name,
        )

        cloned_path = clone_repository(
            repository_url,
            destination,
        )

        # =====================================================
        # 4. Scan Repository
        # =====================================================

        files = scan_repository(
            cloned_path
        )

        # =====================================================
        # 5. Basic Repository Analysis
        # =====================================================

        framework = detect_framework(
            cloned_path,
            files["files"],
        )

        entry_point = detect_entry_point(
            framework,
            files["files"],
        )

        dependencies = detect_dependencies(
            cloned_path,
            files["files"],
        )

        language = detect_language(
            files["files"]
        )

        architecture = detect_architecture(
            files["files"]
        )

        summary = generate_summary(
            language["primary_language"],
            framework,
            architecture,
            dependencies,
        )

        # =====================================================
        # 6. API Analysis
        # =====================================================

        api_endpoints = detect_api_endpoints(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 7. Code Structure
        # =====================================================

        code_structure = detect_code_structure(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 8. Dependency Graph
        # =====================================================

        dependency_graph = detect_dependency_graph(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 9. Complexity Analysis
        # =====================================================

        complexity = analyze_complexity(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 10. Circular Dependency Analysis
        # =====================================================

        circular_dependencies = detect_circular_dependencies(
            dependency_graph
        )

        # =====================================================
        # 11. Quality Report
        # =====================================================

        quality_report = generate_quality_report(
            framework,
            architecture,
            dependencies,
            files["files"],
        )

        # =====================================================
        # 12. Security Analysis
        # =====================================================

        security_issues = analyze_security(
            cloned_path,
            files["files"],
        )

        security_summary = generate_security_summary(
            security_issues
        )

        # =====================================================
        # 13. Repository Metrics
        # =====================================================

        repository_metrics = generate_repository_metrics(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 14. Code Smell Analysis
        # =====================================================

        code_smells = detect_code_smells(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 15. Dead Code Analysis
        # =====================================================

        dead_code = detect_dead_code(
            cloned_path,
            files,
        )

        # =====================================================
        # 16. Maintainability Analysis
        # =====================================================

        maintainability = generate_maintainability(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 17. Documentation Analysis
        # =====================================================

        documentation = analyze_documentation(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 18. Repository Size Analysis
        # =====================================================

        repository_size = analyze_repository_size(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 19. Test Analysis
        # =====================================================

        tests = analyze_tests(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 20. License Analysis
        # =====================================================

        license_info = analyze_license(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 21. CI/CD Analysis
        # =====================================================

        ci_cd = analyze_ci_cd(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 22. Community Analysis
        # =====================================================

        community = analyze_community(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 23. Configuration Analysis
        # =====================================================

        configuration = analyze_configuration(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 24. Secret Exposure Analysis
        # =====================================================

        secret_exposure = analyze_secret_exposure(
            cloned_path,
            files["files"],
        )

        # =====================================================
        # 25. Health Score
        # =====================================================

        health_analysis = _calculate_health_categories(
            security_summary=security_summary,
            tests=tests,
            documentation=documentation,
            maintainability=maintainability,
            architecture=architecture,
            ci_cd=ci_cd,
            community=community,
            license_info=license_info,
            configuration=configuration,
            secret_exposure=secret_exposure,
            repository_metrics=repository_metrics,
            files=files,
            code_smells=code_smells,
        )

        health_score = calculate_health_score(
            health_analysis
        )

        # =====================================================
        # 26. AI Recommendations
        # =====================================================

        recommendation_analysis = {
            **health_analysis,

            "security_score": health_analysis[
                "security"
            ],

            "secret_exposure_score": health_analysis[
                "secret_exposure"
            ],

            "tests_score": health_analysis[
                "tests"
            ],

            "documentation_score": health_analysis[
                "documentation"
            ],

            "maintainability_score": health_analysis[
                "maintainability"
            ],

            "architecture_score": health_analysis[
                "architecture"
            ],

            "code_quality_score": health_analysis[
                "code_quality"
            ],

            "ci_cd_score": health_analysis[
                "ci_cd"
            ],

            "community_score": health_analysis[
                "community"
            ],

            "license_score": health_analysis[
                "license"
            ],

            "configuration_score": health_analysis[
                "configuration"
            ],

            "repository_metrics_score": health_analysis[
                "repository_metrics"
            ],

            "complexity": complexity,

            "largest_file": files.get(
                "largest_file"
            ),

            "largest_file_lines": files.get(
                "largest_file_lines",
                0,
            ),

            "dependencies": dependencies,

            "security_issues": security_issues,

            "code_smells": code_smells,

            "dead_code": dead_code,

            "circular_dependencies": circular_dependencies,

            "documentation": documentation,

            "tests": tests,

            "ci_cd": ci_cd,

            "community": community,

            "license": license_info,

            "configuration": configuration,

            "secret_exposure": secret_exposure,
        }

        ai_recommendations = generate_ai_recommendations(
            recommendation_analysis
        )

    # =========================================================
    # 27. Verify GitHub Repository
    # =========================================================

    parsed_url = urlparse(
        repository_url
    )

    path_parts = [
        part
        for part in parsed_url.path.split("/")
        if part
    ]

    if len(path_parts) < 2:
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL.",
        )

    owner = path_parts[0]
    repository = path_parts[1]

    if repository.endswith(".git"):
        repository = repository[:-4]

    api_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repository}"
    )

    try:
        response = requests.get(
            api_url,
            timeout=10,
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=502,
            detail="Unable to connect to GitHub.",
        )

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="GitHub repository not found.",
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Unable to verify GitHub repository.",
        )

    # =========================================================
    # 28. Create Final Analysis Result
    # =========================================================

    result = {
        "status": "success",

        "repository": repository_url,

        "branch": branch,

        "primary_language": language[
            "primary_language"
        ],

        "languages": language[
            "languages"
        ],

        "framework": framework,

        "entry_point": entry_point,

        "dependencies": dependencies,

        "architecture": architecture,

        "summary": summary,

        "health_score": health_score,

        "api_endpoints": api_endpoints,

        "code_structure": code_structure,

        "dependency_graph": dependency_graph,

        "complexity": complexity,

        "circular_dependencies": circular_dependencies,

        "quality_report": quality_report,

        "security_issues": security_issues,

        "security_summary": security_summary,

        "repository_metrics": repository_metrics,

        "code_smells": code_smells,

        "dead_code": dead_code,

        "analyzer_version": "2.2.0",

        "maintainability": maintainability,

        "ai_recommendations": ai_recommendations,

        "documentation": documentation,

        "repository_size": repository_size,

        "tests": tests,

        "license": license_info,

        "ci_cd": ci_cd,

        "community": community,

        "configuration": configuration,

        "secret_exposure": secret_exposure,

        **files,
    }

    # =========================================================
    # 29. Save Analysis To Database
    # =========================================================

    db = SessionLocal()

    try:

        analysis_record = RepositoryAnalysis(
            repository=repository_url,
            branch=branch,
            primary_language=language[
                "primary_language"
            ],
            analysis_json=json.dumps(
                result,
                default=str,
            ),
        )

        db.add(
            analysis_record
        )

        db.commit()

        db.refresh(
            analysis_record
        )

        # Add database information to response.
        result[
            "analysis_id"
        ] = analysis_record.id

        if analysis_record.created_at:
            result[
                "created_at"
            ] = analysis_record.created_at.isoformat()

        # Update stored JSON so history contains
        # analysis ID and creation timestamp.
        analysis_record.analysis_json = json.dumps(
            result,
            default=str,
        )

        db.commit()

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()

    # =========================================================
    # 30. Return Final Result
    # =========================================================

    return result