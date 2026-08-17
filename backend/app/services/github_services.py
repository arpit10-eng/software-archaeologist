import requests
import tempfile
import os

from fastapi import HTTPException

from app.services.git_services import clone_repository
from app.services.file_services import scan_repository

from app.utils.validators import is_valid_github_url
from app.utils.framework_detector import detect_framework
from app.utils.entry_point_detector import detect_entry_point
from app.utils.dependency_detector import detect_dependencies
from app.utils.language_detector import detect_language
from app.utils.architecture_detector import detect_architecture
from app.utils.summary_generator import generate_summary
from app.utils.health_score import calculate_health_score
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


def analyze_repository(repo):

    # =========================================================
    # 1. Validate GitHub URL
    # =========================================================

    if not is_valid_github_url(repo.github_url):

        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL."
        )

    # =========================================================
    # 2. Clone Repository
    # =========================================================

    with tempfile.TemporaryDirectory() as temp_dir:

        repo_name = repo.github_url.rstrip("/").split("/")[-1]

        destination = os.path.join(
            temp_dir,
            repo_name
        )

        cloned_path = clone_repository(
            repo.github_url,
            destination
        )

        # =====================================================
        # 3. Scan Repository
        # =====================================================

        files = scan_repository(cloned_path)

        # =====================================================
        # 4. Basic Repository Analysis
        # =====================================================

        framework = detect_framework(
            cloned_path,
            files["files"]
        )

        entry_point = detect_entry_point(
            framework,
            files["files"]
        )

        dependencies = detect_dependencies(
            cloned_path,
            files["files"]
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
            dependencies
        )

        # =====================================================
        # 5. API Analysis
        # =====================================================

        api_endpoints = detect_api_endpoints(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 6. Code Structure
        # =====================================================

        code_structure = detect_code_structure(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 7. Dependency Graph
        # =====================================================

        dependency_graph = detect_dependency_graph(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 8. Complexity Analysis
        # =====================================================

        complexity = analyze_complexity(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 9. Circular Dependency Analysis
        # =====================================================

        circular_dependencies = detect_circular_dependencies(
            dependency_graph
        )

        # =====================================================
        # 10. Quality Report
        # =====================================================

        quality_report = generate_quality_report(
            framework,
            architecture,
            dependencies,
            files["files"]
        )

        # =====================================================
        # 11. Security Analysis
        # =====================================================

        security_issues = analyze_security(
            cloned_path,
            files["files"]
        )

        security_summary = generate_security_summary(
            security_issues
        )

        # =====================================================
        # 12. Repository Metrics
        # =====================================================

        repository_metrics = generate_repository_metrics(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 13. Code Smell Analysis
        # =====================================================

        code_smells = detect_code_smells(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 14. Dead Code Analysis
        # =====================================================

        dead_code = detect_dead_code(
            cloned_path,
            files
        )

        # =====================================================
        # 15. Maintainability Analysis
        # =====================================================

        maintainability = generate_maintainability(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 16. Documentation Analysis
        # =====================================================

        documentation = analyze_documentation(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 17. Repository Size Analysis
        # =====================================================

        repository_size = analyze_repository_size(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 18. Test Analysis
        # =====================================================

        tests = analyze_tests(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 19. License Analysis
        # =====================================================

        license = analyze_license(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 20. CI/CD Analysis
        # =====================================================

        ci_cd = analyze_ci_cd(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 21. Community Analysis
        # =====================================================

        community = analyze_community(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 22. Configuration Analysis
        # =====================================================

        configuration = analyze_configuration(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 23. Secret Exposure Analysis
        # =====================================================

        secret_exposure = analyze_secret_exposure(
            cloned_path,
            files["files"]
        )

        # =====================================================
        # 24. HEALTH SCORE 2.0
        # =====================================================
        #
        # Health Score 2.0 considers:
        #
        # Security
        # Testing
        # Code Quality
        # Documentation
        # Maintainability
        # Architecture
        # CI/CD
        # Community
        # License
        # Configuration
        # Secret Exposure
        # Repository Metrics
        #
        # =====================================================

        health_score = calculate_health_score(
            framework,
            entry_point,
            dependencies,
            architecture,
            security_issues,
            tests,
            code_smells,
            documentation,
            maintainability,
            circular_dependencies,
            ci_cd,
            community,
            license,
            configuration,
            secret_exposure,
            repository_metrics
        )

        # =====================================================
        # 25. AI Recommendations
        # =====================================================

        ai_recommendations = generate_ai_recommendations(
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
        )

    # =========================================================
    # 26. Verify GitHub Repository
    # =========================================================

    api_url = repo.github_url.replace(
        "https://github.com/",
        "https://api.github.com/repos/"
    )

    response = requests.get(
        api_url,
        timeout=10
    )

    if response.status_code == 404:

        raise HTTPException(
            status_code=404,
            detail="GitHub repository not found"
        )

    if response.status_code != 200:

        raise HTTPException(
            status_code=502,
            detail="Unable to verify GitHub repository."
        )

    # =========================================================
    # 27. Final API Response
    # =========================================================

    return {
        "status": "success",

        "repository": repo.github_url,

        "branch": repo.branch,

        "primary_language": language["primary_language"],

        "languages": language["languages"],

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

        "analyzer_version": "2.0.0",

        "maintainability": maintainability,

        "ai_recommendations": ai_recommendations,

        "documentation": documentation,

        "repository_size": repository_size,

        "tests": tests,

        "license": license,

        "ci_cd": ci_cd,

        "community": community,

        "configuration": configuration,

        "secret_exposure": secret_exposure,

        **files
    }