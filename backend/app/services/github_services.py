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

    # --------------------------------------------------
    # 1. Validate GitHub URL
    # --------------------------------------------------

    if not is_valid_github_url(repo.github_url):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL."
        )

    # --------------------------------------------------
    # 2. Clone and analyze repository
    # --------------------------------------------------

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

        # --------------------------------------------------
        # 3. Scan repository
        # --------------------------------------------------

        files = scan_repository(cloned_path)

        # --------------------------------------------------
        # 4. Basic repository analysis
        # --------------------------------------------------

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

        health_score = calculate_health_score(
            framework,
            entry_point,
            dependencies,
            architecture
        )

        # --------------------------------------------------
        # 5. API and code structure
        # --------------------------------------------------

        api_endpoints = detect_api_endpoints(
            cloned_path,
            files["files"]
        )

        code_structure = detect_code_structure(
            cloned_path,
            files["files"]
        )

        dependency_graph = detect_dependency_graph(
            cloned_path,
            files["files"]
        )

        # --------------------------------------------------
        # 6. Code quality analysis
        # --------------------------------------------------

        complexity = analyze_complexity(
            cloned_path,
            files["files"]
        )

        circular_dependencies = detect_circular_dependencies(
            dependency_graph
        )

        quality_report = generate_quality_report(
            framework,
            architecture,
            dependencies,
            files["files"]
        )

        code_smells = detect_code_smells(
            cloned_path,
            files["files"]
        )

        dead_code = detect_dead_code(
            cloned_path,
            files
        )

        maintainability = generate_maintainability(
            cloned_path,
            files["files"]
        )

        # --------------------------------------------------
        # 7. Security analysis
        # --------------------------------------------------

        security_issues = analyze_security(
            cloned_path,
            files["files"]
        )

        security_summary = generate_security_summary(
            security_issues
        )

        # --------------------------------------------------
        # 8. Repository metrics
        # --------------------------------------------------

        repository_metrics = generate_repository_metrics(
            cloned_path,
            files["files"]
        )

        documentation = analyze_documentation(
            cloned_path,
            files["files"]
        )

        repository_size = analyze_repository_size(
            cloned_path,
            files["files"]
        )

        # --------------------------------------------------
        # 9. Tests analysis
        # --------------------------------------------------

        tests = analyze_tests(
            cloned_path,
            files["files"]
        )

        # --------------------------------------------------
        # 10. License analysis
        # --------------------------------------------------

        license = analyze_license(
            cloned_path,
            files["files"]
        )

        # --------------------------------------------------
        # 11. CI/CD analysis
        # --------------------------------------------------

        ci_cd = analyze_ci_cd(
            cloned_path,
            files["files"]
        )

        # --------------------------------------------------
        # 12. Community analysis
        # --------------------------------------------------

        community = analyze_community(
            cloned_path,
            files["files"]
        )

        # --------------------------------------------------
        # 13. Configuration analysis
        # --------------------------------------------------

        configuration = analyze_configuration(
            cloned_path,
            files["files"]
        )

        # --------------------------------------------------
        # 14. Secret exposure analysis
        # --------------------------------------------------

        secret_exposure = analyze_secret_exposure(
            cloned_path,
            files["files"]
        )

        # --------------------------------------------------
        # 15. AI Recommendations
        # IMPORTANT:
        # All analyzers must run BEFORE this function.
        # --------------------------------------------------

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

        # --------------------------------------------------
        # 16. Verify GitHub repository
        # --------------------------------------------------

        api_url = repo.github_url.replace(
            "https://github.com/",
            "https://api.github.com/repos/"
        )

        response = requests.get(api_url)

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="GitHub repository not found"
            )

        # --------------------------------------------------
        # 17. Final API response
        # --------------------------------------------------

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

            "analyzer_version": "1.1.0",

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