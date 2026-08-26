import os
import re


SECURITY_RULES = [
    {
        "pattern": r"password\s*=\s*['\"].+['\"]",
        "issue": "Hardcoded Password",
        "severity": "High",
        "recommendation": "Store passwords in environment variables."
    },
    {
        "pattern": r"(api[_-]?key)\s*=\s*['\"].+['\"]",
        "issue": "Hardcoded API Key",
        "severity": "High",
        "recommendation": "Store API keys in environment variables."
    },
    {
        "pattern": r"(token|access_token)\s*=\s*['\"].+['\"]",
        "issue": "Hardcoded Token",
        "severity": "High",
        "recommendation": "Store tokens securely."
    },
    {
        "pattern": r"(secret|secret_key|jwt_secret)\s*=\s*['\"].+['\"]",
        "issue": "Hardcoded Secret",
        "severity": "High",
        "recommendation": "Store secrets in environment variables."
    },
    {
        "pattern": r"(aws_access_key|aws_secret_access_key)\s*=\s*['\"].+['\"]",
        "issue": "AWS Credentials",
        "severity": "Critical",
        "recommendation": "Never commit AWS credentials."
    },
    {
        "pattern": r"-----BEGIN (RSA )?PRIVATE KEY-----",
        "issue": "Private Key Found",
        "severity": "Critical",
        "recommendation": "Never commit private keys."
    },
    {
        "pattern": r"subprocess\.(run|call)\(",
        "issue": "Use of subprocess detected",
        "severity": "Medium",
        "recommendation": "Validate user input before executing subprocess commands."
    },
    {
        "pattern": r"os\.system\(",
        "issue": "Use of os.system() detected",
        "severity": "Medium",
        "recommendation": "Use subprocess.run() with validated arguments instead."
    },
    {
        "pattern": r"\beval\(",
        "issue": "Use of eval() detected",
        "severity": "High",
        "recommendation": "Avoid eval(); use safer alternatives."
    },
    {
        "pattern": r"\bexec\(",
        "issue": "Use of exec() detected",
        "severity": "High",
        "recommendation": "Avoid exec() unless absolutely necessary."
    }
]


# =========================================================
# Database credential detection
# =========================================================

def detect_database_credentials(line):
    """
    Detect real database credentials inside database connection
    strings while ignoring harmless local SQLite URLs.
    """

    database_pattern = re.compile(
        r"(database_url|db_url|database_uri|db_uri)\s*="
        r"\s*['\"]([^'\"]+)['\"]",
        re.IGNORECASE
    )

    match = database_pattern.search(line)

    if not match:
        return None

    database_url = match.group(2)

    # Local SQLite databases do not normally contain credentials.
    if database_url.lower().startswith("sqlite://"):
        return None

    # Look for credentials inside a database URL.
    credential_pattern = re.compile(
        r"://[^/\s:@]+:[^/\s@]+@",
        re.IGNORECASE
    )

    if credential_pattern.search(database_url):

        return {
            "issue": "Database Credentials",
            "severity": "High",
            "recommendation":
                "Store database credentials securely."
        }

    return None


# =========================================================
# Security Analyzer
# =========================================================

def analyze_security(repo_path, files):

    security_issues = []

    for file in files:

        # -----------------------------------------------------
        # Analyze only Python files
        # -----------------------------------------------------

        if not file.endswith(".py"):
            continue

        # -----------------------------------------------------
        # Skip the analyzer itself
        # -----------------------------------------------------

        if os.path.basename(file) == "security_analyzer.py":
            continue

        absolute_path = os.path.join(repo_path, file)

        try:

            with open(
                absolute_path,
                "r",
                encoding="utf-8"
            ) as f:

                lines = f.readlines()

        except Exception:

            continue

        in_docstring = False

        # =====================================================
        # Analyze every line
        # =====================================================

        for line_number, line in enumerate(
            lines,
            start=1
        ):

            stripped = line.strip()

            # -------------------------------------------------
            # Ignore blank lines
            # -------------------------------------------------

            if not stripped:
                continue

            # -------------------------------------------------
            # Ignore comments
            # -------------------------------------------------

            if stripped.startswith("#"):
                continue

            # -------------------------------------------------
            # Handle triple-quoted strings
            # -------------------------------------------------

            if (
                stripped.startswith('"""')
                or stripped.startswith("'''")
            ):

                in_docstring = not in_docstring
                continue

            if in_docstring:
                continue

            # =================================================
            # Database credential detection
            # =================================================

            database_issue = detect_database_credentials(
                stripped
            )

            if database_issue:

                security_issues.append({
                    "file": file,
                    "line": line_number,
                    "code": stripped,
                    "issue": database_issue["issue"],
                    "severity": database_issue["severity"],
                    "recommendation":
                        database_issue["recommendation"]
                })

                continue

            # =================================================
            # Standard security rules
            # =================================================

            for rule in SECURITY_RULES:

                if re.search(
                    rule["pattern"],
                    line,
                    re.IGNORECASE
                ):

                    security_issues.append({
                        "file": file,
                        "line": line_number,
                        "code": stripped,
                        "issue": rule["issue"],
                        "severity": rule["severity"],
                        "recommendation":
                            rule["recommendation"]
                    })

                    # Prevent duplicate reports
                    # for the same line.
                    break

    return security_issues