SEVERITY_ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}

def _finding(category, title, severity, description, evidence=None, recommendation=None):
    return {
        "category": category,
        "title": title,
        "severity": severity,
        "description": description,
        "evidence": evidence or [],
        "recommendation": recommendation or "Review the finding and apply the suggested remediation.",
    }

def generate_findings(analysis):
    findings = []
    security = analysis.get("security_issues", []) or []
    for issue in security:
        findings.append(_finding(
            "Security", issue.get("issue", "Security issue"), issue.get("severity", "Medium"),
            "A security-sensitive pattern was detected during static analysis.",
            [f"{issue.get('file', 'unknown file')}:{issue.get('line', '?')}", issue.get("code", "")],
            issue.get("recommendation"),
        ))

    secrets = analysis.get("secret_exposure", {}) or {}
    for item in secrets.get("findings", []) or []:
        findings.append(_finding(
            "Secret Exposure", item.get("type", "Potential secret"), item.get("severity", "High"),
            item.get("message", "Potential secret exposure was detected."),
            [f"{item.get('file', 'unknown file')}:{item.get('line', '?')}", item.get("code", "")],
            "Remove the secret from source control, rotate it if it was real, and use environment variables or a secret manager.",
        ))

    complexity = analysis.get("complexity", {}) or {}
    for item in (complexity.get("complexity_warnings", []) or [])[:20]:
        findings.append(_finding(
            "Maintainability", f"Complex function: {item.get('function', 'unknown')}", item.get("severity", "Medium"),
            "A function exceeds the configured complexity or size threshold.",
            [f"{item.get('file', 'unknown file')}:{item.get('lines', '?')} lines", f"Cyclomatic complexity: {item.get('complexity', '?')}"],
            item.get("recommendation"),
        ))

    for item in (analysis.get("code_smells", []) or [])[:30]:
        findings.append(_finding(
            "Code Quality", item.get("issue", "Code smell"), item.get("severity", "Medium"),
            "A maintainability or code-quality pattern was detected.",
            [f"{item.get('file', 'unknown file')}:{item.get('line', '?')}"], item.get("recommendation"),
        ))

    tests = analysis.get("tests", {}) or {}
    if tests.get("test_file_count", 0) == 0:
        findings.append(_finding("Testing", "No automated test files", "High", "No recognizable test files were found.", [], "Add unit and integration tests for the most important application paths."))
    elif tests.get("test_function_count", 0) < 5:
        findings.append(_finding("Testing", "Small test suite", "Medium", "Only a small number of test cases were detected.", [f"Detected test cases: {tests.get('test_function_count', 0)}"], "Expand tests around business logic, APIs, error paths, and repository analysis."))

    documentation = analysis.get("documentation", {}) or {}
    if documentation.get("documentation_file_count", 0) == 0:
        findings.append(_finding("Documentation", "No dedicated documentation file", "Medium", "No README or recognized documentation file was detected.", [], "Add a README covering setup, architecture, usage, and examples."))

    ci_cd = analysis.get("ci_cd", {}) or {}
    if not ci_cd.get("github_actions"):
        findings.append(_finding("CI/CD", "No CI workflow", "Medium", "No GitHub Actions workflow was detected.", [], "Add automated test, lint, and build checks for pushes and pull requests."))

    license_info = analysis.get("license", {}) or {}
    if license_info.get("status") == "Missing":
        findings.append(_finding("License", "Missing license", "Medium", "No license file was detected.", [], "Choose an appropriate open-source license and add a LICENSE file."))

    community = analysis.get("community", {}) or {}
    if not community.get("contributing"):
        findings.append(_finding("Community", "Missing contribution guidelines", "Low", "CONTRIBUTING.md was not detected.", [], "Add contribution, development, and pull-request guidance."))

    configuration = analysis.get("configuration", {}) or {}
    if configuration.get("environment_file_count", 0) and not configuration.get("env_example_found"):
        findings.append(_finding("Configuration", "Environment file without example", "Medium", "An environment file was detected without a corresponding example file.", [], "Keep secrets out of source control and provide a sanitized .env.example."))

    findings.sort(key=lambda x: (SEVERITY_ORDER.get(x["severity"], 99), x["category"], x["title"]))
    return findings
